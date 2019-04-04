import subprocess
from script1 import multiply, raise_string, your_main_program, INVALID_NUM_ARGS_ERROR, INVALID_NUM_ERROR
import sys
import time
sys.path.append("../test_dependencies")
from test_dependencies import col, tester
import random
import os

# IF YOU USE "python3", REPLACE THIS LINE WITH "python3"
p = "python3"

t = tester(p=p, script="script1.py")
tic = int(time.time()*1000)
print("\nTest for Program 1")
t.describe("Output correctness")

t.it("5 * 10", t.try_except_output("50\n", ["5", "10"]))
t.it("5 * 959595", t.try_except_output("4797975\n", ["5", "959595"]))
t.it("5 ^ 3", t.try_except_output("5 * 5 * 5\n125\n", ["5", "3", "raise"]))
t.it("1 ^ 0", t.try_except_output("1\n", ["1", "0", "raise"]))
t.it("0 ^ 0", t.try_except_output("1\n", ["0", "0", "raise"]))
t.it("1 ^ 1", t.try_except_output("1\n1\n", ["1", "1", "raise"]))
t.it("2 ^ 0", t.try_except_output("1\n", ["2", "0", "raise"]))
print()
t.describe("Failure correctness")
t.it("Invalid number of arguments [1]",
    t.try_expect_failure(INVALID_NUM_ARGS_ERROR + "\n", ["1"]))
t.it("Invalid numbers provided [1, a]",
    t.try_expect_failure(INVALID_NUM_ERROR + "\n", ["1", "a"]))
print()
t.describe("Multiply was implemented correctly")
t.it("5 * 5", t.assert_equals(25, multiply(5,5)))
t.it("3 * 25", t.assert_equals(75, multiply(3,25)))

rand_int_1 = random.randint(1, 25)
rand_int_2 = random.randint(1, 25)
t.it("Random values", 
    t.assert_equals(rand_int_1 * rand_int_2, 
        multiply(rand_int_1, rand_int_2)))
print()
t.describe("Raise_string was implemented correctly")
sys.stdout = open(os.devnull, 'w')
fiveToThree = raise_string(5,3)
threeToFive = raise_string(3,5)
sys.stdout = sys.__stdout__
t.it("5 ^ 3", t.assert_equals(125, fiveToThree))
t.it("3 ^ 5", t.assert_equals(243, threeToFive))

print()
t.describe("Style")
t.it("Multiply has docstring", t.assert_equals(True, 
    multiply.__doc__ is not None))
t.it("Raise_string has docstring", t.assert_equals(True,
    raise_string.__doc__ is not None))


toc = int(time.time()*1000)
print()
print(t.get_success() + " in {} milliseconds\n".format(toc-tic))