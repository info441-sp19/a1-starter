import subprocess
import sys
import time
from script2a import INVALID_ARGUMENTS, FILE_NOT_FOUND
from script2b import anagram
sys.path.append("../test_dependencies")
from test_dependencies import col, tester
import random
import os

# IF YOU USE "python3", REPLACE THIS LINE WITH "python3"
p = "python3"

t = tester(p=p, script="script2a.py")
tic = int(time.time()*1000)
print("\nTest for Program 2")
print("Warning: you will fail these tests if you renamed the files inside the test_files directory")
t.describe("Output correctness")
next_exp_string = "Occurrence Count: a:1, b:1, c:1, d:1\nNew letters: ['a', 'b', 'c', 'd']\n\nOccurrence Count: b:3, c:1, e:1, f:1\nNew letters: ['e', 'f']\n"
t.it("abcd, efbcbB simple", t.try_except_output(next_exp_string, ["test_files/test.txt"]))
next_exp_string = "Occurrence Count: a:1, b:1, c:1, d:1\nNew letters: ['a', 'b', 'c', 'd']\nContains anagram: TRUE\n\nOccurrence Count: b:3, c:1, e:1, f:1\nNew letters: ['e', 'f']\nContains anagram: FALSE\n"
t.it("abcd, efbcbB anagrams", t.try_except_output(next_exp_string, ["test_files/test.txt", "cab"]))
next_exp_string = "a:1 (line 0)\nb:4 (line 0)\nc:2 (line 0)\nd:1 (line 0)\ne:1 (line 1)\nf:1 (line 1)\n"
read_file = open("test_files/test_results.txt", "r")
contents = read_file.read()
t.it("File output correctness", t.assert_equals(next_exp_string, contents))
print()
t.describe("Expected errors")
t.it("Invalid arguments", t.try_expect_failure(INVALID_ARGUMENTS, []))
t.it("File not found", t.try_expect_failure(FILE_NOT_FOUND, ["abc_dont_make_this_file_please.txt"]))
t.it("Empty file", t.try_expect_failure("File empty.", ["test_files/test_empty.txt"]))
print()
t.describe("Test anagrams function")
t.it("Simple case #1", t.assert_equals(True, anagram("abcdef", "cdf")))
t.it("Simple case #2", t.assert_equals(False, anagram("cdf", "abcdef")))
t.it("Simple case #3", t.assert_equals(True, anagram("abcdef", "abcdef")))
t.it("Empty anagram", t.assert_equals(True, anagram("", "")))
t.it("Capitalizations #1", t.assert_equals(True, anagram("AbCdEfG", "abc")))
t.it("Capitalizations #2", t.assert_equals(False, anagram("AbCdEfG", "AbCa")))
t.it("Multiple of same letter #1", t.assert_equals(True, anagram("AaAaA", "AaAaA")))
t.it("Multiple of same letter #2", t.assert_equals(False, anagram("AaAa", "AaAaA")))
t.it("Multiple of same letter #3", t.assert_equals(True, anagram("AaAaA", "Aaaa")))
print()
t.describe("Style")
t.it("Anagram has docstring", t.assert_equals(True, anagram.__doc__ is not None))




toc = int(time.time()*1000)
print()
print(t.get_success() + " in {} milliseconds\n".format(toc-tic))