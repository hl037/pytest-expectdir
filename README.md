# pytest-expectdir

![tests](https://github.com/hl037/pytest-expectdir/actions/workflows/tests.yml/badge.svg)
[![codecov](https://codecov.io/github/hl037/pytest-expectdir/branch/master/graph/badge.svg?token=IEML9TAP59)](https://codecov.io/github/hl037/pytest-expectdir)


This pytest plugin provides an easy way to test file generation and file-system transformation.

## Install

```
pip install pytest-expectdir
```

## Usage

Here is the workflow :

Create a directory containing files and directories expected to be generated, and optionally one with your initial data so that it looks like this :

```
my_pkg/
  my_pkg/
    ...
  tests/
    test_feature.py
    data_test_feature/
      initial/
        ... (optional) your initial data
      expected/
        ... expected output tree

```

Then you write your test as follow :

`test_feature.py`
```
def test_feature(expectdir):
  with expectdir('data_test_feature') as output_dir:
    # Do whatever you want inside output_dir, which is a temporary directory copied from initial/
  # At the end of the with, output_dir gets compared with expected
  # ...And you get a fancy report of the difference if there are (as an AssertionError).
```

Note that you can also pass manually the keyword arguments `initial` and `expected` to `expectdir`. If, for example, you have multiple tests ending up with the same expected result, or with the same initial one.

The following is equivalent to the previous example : 

```
def test_feature(expectdir):
  with expectdir(initial='data_test_feature/initial', expected='data_test_feature/expected') as output_dir:
    # ...
```


## How Fancy ?

Here is a sample from the tests : 

```
In [1]: import sys
   ...: from pytest_expectdir.plugin import cmpdir, formatDiff
   ...: initial = './tests/data/test3/initial/'
   ...: expected = './tests/data/test3/expected/'
   ...: formatDiff(sys.stdout, initial, expected, cmpdir(initial, expected)[1])
Directories ./tests/data/test3/expected/ (expected) is different from ./tests/data/test3/initial/ (candidate).
Missing in candidate :
dir3/
f1
Extra in candidate :
dir2/
f4
In both directories but different content:

f3:
  - This line is removed
  - And this one too
    This is a complex test
  - Hello 3
  + Hello 3 And replaced ones
    With some lines
  + And added lines
    And otherlines
    common 1
    common 2
  [...] --- expected:11 / candidate:10 ---
    common 6
    common 7
    common 8
  - and diff 1
  + diff

dir4/f3:
  - This line is removed
  - And this one too
    This is a complex test
  - Hello 3
  + Hello 3 And replaced ones
    With some lines
  + And added lines
    And otherlines
    common 1
    common 2
  [...] --- expected:11 / candidate:10 ---
    common 6
    common 7
    common 8
  - and diff 1
  + diff
```

![Preview Image](https://github.com/hl037/pytest-expectdir/blob/master/screenshot.png?raw=true)

