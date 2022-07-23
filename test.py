#!/usr/bin/env python3
import cstags as cst

if __name__ != "__main__": raise SystemExit

class_tests = [
  ("class a { }", "a"),
  ("public class a { }", "a"),
  ("[attr1] [attr2] class a { }", "a"),
  ("class a : b { }", "a"),
  ("class a<b> where b : c { }", "a"),
]

for test_case, expectation  in class_tests:
  actual = cst.parse_class(test_case)
  assert expectation == actual, f"{expectation} != {actual}"

print("'class' parsing works")
