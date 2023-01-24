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
├ my_pkg/
│ └ ...
└ tests/
  ├ test_feature.py
  └ test_feature/
    ├ initial (optional)/
    │ └ ... your initial data
    └ expected/
      └ ... expected output tree

```

Then you write your test as follow :

`test_feature.py`
```
def test_feature(expectdir):
  with expectdir('test_feature') as output_dir:
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


If your test data follows this schema :

```
tests/
├ test_feature.py
└ test_feature/
  └ TestCaseClassName (if one)/
    └ test_method
      ├ initial (optional)/
      │ └ ...
      └ expected
        └ ...
```

(like the first example), then you can even omit the parameters :

```
def test_feature(expectdir):
  with expectdir() as output_dir:
    # ...
```

## API

### (`pytest.fixture`) `expectdir(datapath=None, *, initial=None, expected=None) -> contextmanager as outputDir:Path`

The main fixture. Its value is a function that returns a context manager. The context manager will return (when opened) a path to a temporary directory that will get compared to the Expected directory at closing. An AssertionError will then be raised if the two directory are not the same. `.gitkeep` files, conventionally used to keep empty directories are ignored.

The function choose an optional initial directory and a required expected directory as follow :

#### Expected
* If the `expected` keyword argument is provided, it's this directory that will be used.
* Else, if the `datapath` positional argument is provided, expected will be `datapath/"expected"`.
* Else, the test path will be used as fallback, i.e. `currentModuleDirectory/TestCaseClassName/test_method/expected` if inside a testCase class, else, `currentModuleDirectory/test_function/expected` if the test is a standalone function.
* If the selected path does not exist, raises a FileNotFoundError.

#### Initial
* If the `initial` keyword argument is provided and equal to `__empty__`, then the initial directory will be empty.
* If the `initial` keyword argument is provided and is a different string or a `Path` instance, it's this directory that will be used.
* Else, if the `datapath` positional argument is provided, expected will be `datapath/"initial"`.
* Else, if the `expected` keyword argument is **not** provided, the test path will be used as fallback, i.e. `currentModuleDirectory/TestCaseClassName/test_method/initial` if inside a TestCase class, else, `currentModuleDirectory/test_function/initial` if the test is a standalone function.
* Else, the initial directory will be empty.
* If the initial keyword argument is a Path, and this path does not exists, raises a FileNotFoundError.

### `cmpdir(candidate:Path, expected:Path) -> Tuple[result:bool, Tuple[candidate_only:list[Path], expected_only:list[Path], different:list[Path]]]`

Compare two directories recursively, and list files only in the first, only on the second, and in both but different.

The result is `True` if the directories are identical.

When a subdirectory is present only in one of the compared directories, only the subdirectory itself is listed (not all its content).

Files `.gitkeep` are ignored.

### `formatDiff(file_output:TextIO, candidate:Path, expected:Path, diffRes:Tuple[candidate_only:list[Path], expected_only:list[Path], different:list[Path]]) -> None`

Takes the result of `cmpdir`, and print to `file_output` the diff summary.

### `formatFileDiff(file_output:TextIO, lines_candidate:Iterable[str], lines_expected:Iterable[str], context=3, indent='  ') -> None`

Format the diff of two files, and output to `file_output`. `context` is the number of identical to show before and after insertion / deletion for context. `indent` is the line prefix, so that the output is indented.


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

