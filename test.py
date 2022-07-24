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

method_tests = [
  ("void M() { }", "M"),
  ("ref b M() { }", "M"),
  ("ref readonly b M() { }", "M"),
  ("b<c> M() { }", "M"),
  ("b<c> M(A a) { }", "M"),
  ("b<c> M(A a, B b) { }", "M"),
  ("b M<c>() where b : d { }", "M"),
  ("void M() => { }", "M"),
  ("[attr1] [attr2] void M() => { }", "M"),
  ("var m = M()", None),
]

interface_tests = [
  ("interface a { }", "a"),
  ("public interface a { }", "a"),
  ("interface a : b { }", "a"),
  ("interface a<b> where b : c { }", "a"),
]

for test_case, expectation  in class_tests:
  actual = cst.parse_class(test_case)
  assert expectation == actual, f"{test_case} -> {expectation} != {actual}"

print("'class' parsing works")

for test_case, expectation  in method_tests:
  actual = cst.parse_method(test_case)
  assert expectation == actual, f"{test_case} -> {expectation} != {actual}"

print("'method' parsing works")

for test_case, expectation  in interface_tests:
  actual = cst.parse_interface(test_case)
  assert expectation == actual, f"{test_case} -> {expectation} != {actual}"

print("'interface' parsing works")
