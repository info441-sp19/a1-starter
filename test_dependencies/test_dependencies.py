import subprocess
import sys
import os

# https://stackoverflow.com/questions/7445658/how-to-detect-if-the-console-does-support-ansi-escape-codes-in-python
def supports_color():
    """
    Returns True if the running system's terminal supports color, and False
    otherwise.
    """
    plat = sys.platform
    supported_platform = plat != 'Pocket PC' and (plat != 'win32' or
                                                  'ANSICON' in os.environ)
    # isatty is not always implemented, #6223.
    is_a_tty = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
    if not supported_platform or not is_a_tty:
        return False
    return True

# def colors for nice formatting in cmd line
# from https://stackoverflow.com/questions/287871/print-in-terminal-with-colors
class col:
    SUPPORTS_COLOR = supports_color()
    END      = '\33[0m' if SUPPORTS_COLOR else ""
    BOLD     = '\33[1m' if SUPPORTS_COLOR else ""
    ITALIC   = '\33[3m' if SUPPORTS_COLOR else ""
    URL      = '\33[4m' if SUPPORTS_COLOR else ""
    BLINK    = '\33[5m' if SUPPORTS_COLOR else ""
    BLINK2   = '\33[6m' if SUPPORTS_COLOR else ""
    SELECTED = '\33[7m' if SUPPORTS_COLOR else ""

    BLACK  = '\33[30m' if SUPPORTS_COLOR else ""
    RED    = '\33[31m' if SUPPORTS_COLOR else ""
    GREEN  = '\33[32m' if SUPPORTS_COLOR else ""
    YELLOW = '\33[33m' if SUPPORTS_COLOR else ""
    BLUE   = '\33[34m' if SUPPORTS_COLOR else ""
    VIOLET = '\33[35m' if SUPPORTS_COLOR else ""
    BEIGE  = '\33[36m' if SUPPORTS_COLOR else ""
    WHITE  = '\33[37m' if SUPPORTS_COLOR else ""

    BLACKBG  = '\33[40m' if SUPPORTS_COLOR else ""
    REDBG    = '\33[41m' if SUPPORTS_COLOR else ""
    GREENBG  = '\33[42m' if SUPPORTS_COLOR else ""
    YELLOWBG = '\33[43m' if SUPPORTS_COLOR else ""
    BLUEBG   = '\33[44m' if SUPPORTS_COLOR else ""
    VIOLETBG = '\33[45m' if SUPPORTS_COLOR else ""
    BEIGEBG  = '\33[46m' if SUPPORTS_COLOR else ""
    WHITEBG  = '\33[47m' if SUPPORTS_COLOR else ""

    GREY    = '\33[90m' if SUPPORTS_COLOR else ""
    RED2    = '\33[91m' if SUPPORTS_COLOR else ""
    GREEN2  = '\33[92m' if SUPPORTS_COLOR else ""
    YELLOW2 = '\33[93m' if SUPPORTS_COLOR else ""
    BLUE2   = '\33[94m' if SUPPORTS_COLOR else ""
    VIOLET2 = '\33[95m' if SUPPORTS_COLOR else ""
    BEIGE2  = '\33[96m' if SUPPORTS_COLOR else ""
    WHITE2  = '\33[97m' if SUPPORTS_COLOR else ""

    GREYBG    = '\33[100m' if SUPPORTS_COLOR else ""
    REDBG2    = '\33[101m' if SUPPORTS_COLOR else ""
    GREENBG2  = '\33[102m' if SUPPORTS_COLOR else ""
    YELLOWBG2 = '\33[103m' if SUPPORTS_COLOR else ""
    BLUEBG2   = '\33[104m' if SUPPORTS_COLOR else ""
    VIOLETBG2 = '\33[105m' if SUPPORTS_COLOR else ""
    BEIGEBG2  = '\33[106m' if SUPPORTS_COLOR else ""
    WHITEBG2  = '\33[107m' if SUPPORTS_COLOR else ""

class tester:
    fail_count = 0
    case_count = 0
    p = "python"
    script = ""

    def __init__(self, p, script="script1.py"):
        self.p = p
        self.script = script

    def describe(self, val):
        print("\t{}".format(val))

    def it(self, val, func):
        output = ""
        self.case_count += 1
        try:
            output = func()
        except Exception as e:
            print("\t\t{}{} FAIL {} {}".format(col.REDBG, col.WHITE, col.END, val))
            print("\t\t{rbg}{rc} {cend}\n\t\t{rbg}{rc} {cend} Error received: {err} \n\t\t{rbg}{rc} {cend}".format(rbg=col.REDBG, rc=col.RED, cend=col.END, err=e))
            self.fail_count += 1
            return

        if output is True:
            print("\t\t{}{} PASS {} {}".format(col.GREENBG, col.BLACK, col.END, val))
        else:
            print("\t\t{}{} FAIL {} {}".format(col.REDBG, col.WHITE, col.END, val))
            print("\t\t{rbg}{rc} {cend}\n\t\t{rbg}{rc} {cend} {output} \n\t\t{rbg}{rc} {cend}".format(rbg=col.REDBG, rc=col.RED, cend=col.END, output=output))
            self.fail_count += 1
        return

    def get_success(self):
        bg = col.GREENBG if self.fail_count == 0 else col.YELLOWBG
        return "{}{} {} out of {} cases passed {}".format(bg, col.BLACK, self.case_count - self.fail_count, self.case_count, col.END)

    def expect_output(self, student_output, expected_val):
        if student_output == expected_val:
            return (True, True)
        expected, got = ("","")
        split_student_output = student_output.strip().split("\n")
        split_expected_val = expected_val.strip().split("\n")
        for idx, line in enumerate(split_expected_val):
            if split_student_output[idx] != line:
                expected = line
                got = split_student_output[idx]
                return (expected, got)
        return (True, True)

    def try_except_output(self, expect_in, cmd_args):
        def return_func():
            expect = expect_in
            try:
                output = subprocess.check_output([self.p, self.script, *cmd_args], universal_newlines=True, stderr=subprocess.STDOUT)
                expected, got = self.expect_output(output, expect)
                if expected == True and got == True:
                    return True
                return "Expected [{exp}] but got [{got}]".format(exp=expected, got=got)
            except subprocess.CalledProcessError as exc:
                return exc.output
        return return_func
    
    def try_expect_failure(self, expect_in, cmd_args):
        def return_func():
            expect = expect_in
            try:
                output = subprocess.check_output([self.p, self.script, *cmd_args], universal_newlines=True, stderr=subprocess.STDOUT)
                return "Expected error '{exp}' but did not receive it".format(exp=expect)
            except subprocess.CalledProcessError as output:
                expected, got = self.expect_output(output.output, expect)
                if expected == True and got == True:
                    return True
                return "Expected [{exp}] but got [{got}]".format(exp=expected, got=got)
        return return_func
    
    def assert_equals(self, expected, got):
        def return_func():
            if expected != got:
                return "Expected [{exp}] but got [{got}]".format(exp=expected, got=got)
            return True
        return return_func

# Test the tester
if __name__ == "__main__":
    def test():
        return "Expected ABC but got CDF"

    def testT():
        return True

    def retErr():
        raise ValueError("Failed holy crap")

    t = tester()

    t.describe("Overall test")
    t.it("test", test)
    t.it("test2", testT)
    t.it("test3", retErr)
    expected, got = t.expect_output("1234\ntes2t", "1234\ntest")
    print(expected, got)
    print("\n" + t.get_success())

# misc code below
"""
try:
    a = subprocess.check_output(['python', 'script1.py', '1', 'a', 'raise'], universal_newlines=True)
    # a = subprocess.check_output(["python3", "a.py"])
except subprocess.CalledProcessError as exc:
    print("status: ", exc.output)
"""
