# pytest-expectdir

This pytest plugin provide an easy way to test file generation and filesystem transformation.

## Install

```
pip install pytest-expectdir
```

## Usage

Here is the workflow :

Create a directory withour expected generated files and directories, and optionaly one with your initial data so that it looks like this :

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

Note that you can also pass manually the keyword arguments `initial` and `expected` to `expectdir` if, for example, you have multiple tests ending up with the same expected result, or with the same initial one.

This is equivalent to the previous example : 

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



<body style="font-family:'MiscFixedSC613_Custom',monospace;font-size:9pt;color:#b2b2b2;background-color:#040404;"><span style="color:#008000;background-color:#040404;">In [</span><span style="font-weight:bold;color:#54ff54;background-color:#040404;">1</span><span style="color:#008000;background-color:#040404;">]: </span><span style="font-weight:bold;color:#008700;background-color:#040404;">import</span><span style="color:#b2b2b2;background-color:#040404;"> </span><span style="font-weight:bold;color:#5454ff;background-color:#040404;">sys</span><span style="color:#b2b2b2;background-color:#040404;">
</span><br><span style="color:#008000;background-color:#040404;"> &#160;&#160;...: </span><span style="font-weight:bold;color:#008700;background-color:#040404;">from</span><span style="color:#b2b2b2;background-color:#040404;"> </span><span style="font-weight:bold;color:#5454ff;background-color:#040404;">pytest_expectdir.plugin</span><span style="color:#b2b2b2;background-color:#040404;"> </span><span style="font-weight:bold;color:#008700;background-color:#040404;">import</span><span style="color:#b2b2b2;background-color:#040404;"> cmpdir, formatDiff
</span><br><span style="color:#008000;background-color:#040404;"> &#160;&#160;...: </span><span style="color:#b2b2b2;background-color:#040404;">initial = </span><span style="color:#c0c000;background-color:#040404;">'./tests/data/test3/initial/'</span><span style="color:#b2b2b2;background-color:#040404;">
</span><br><span style="color:#008000;background-color:#040404;"> &#160;&#160;...: </span><span style="color:#b2b2b2;background-color:#040404;">expected = </span><span style="color:#c0c000;background-color:#040404;">'./tests/data/test3/expected/'</span><span style="color:#b2b2b2;background-color:#040404;">
</span><br><span style="color:#008000;background-color:#040404;"> &#160;&#160;...: </span><span style="color:#b2b2b2;background-color:#040404;">formatDiff(sys.stdout, initial, expected, cmpdir(initial, expected)[</span><span style="color:#008000;background-color:#040404;">1</span><span style="color:#b2b2b2;background-color:#040404;">])
</span><br><span style="color:#18b2b2;background-color:#040404;">Directories </span><span style="color:#c00000;background-color:#040404;">./tests/data/test3/expected/ (expected)</span><span style="color:#18b2b2;background-color:#040404;"> is different from </span><span style="color:#008000;background-color:#040404;">./tests/data/test3/initial/ (candidate)</span><span style="color:#18b2b2;background-color:#040404;">.</span><span style="color:#b2b2b2;background-color:#040404;">
</span><br><span style="color:#c00000;background-color:#040404;">Missing in candidate :</span><span style="color:#b2b2b2;background-color:#040404;">
</span><br><span style="color:#c00000;background-color:#040404;">dir3/</span><span style="color:#b2b2b2;background-color:#040404;">
</span><br><span style="color:#c00000;background-color:#040404;">f1</span><span style="color:#b2b2b2;background-color:#040404;">
</span><br><span style="color:#008000;background-color:#040404;">Extra in candidate :</span><span style="color:#b2b2b2;background-color:#040404;">
</span><br><span style="color:#008000;background-color:#040404;">dir2/</span><span style="color:#b2b2b2;background-color:#040404;">
</span><br><span style="color:#008000;background-color:#040404;">f4</span><span style="color:#b2b2b2;background-color:#040404;">
</span><br><span style="color:#18b2b2;background-color:#040404;">In both directories but different content:</span><span style="color:#b2b2b2;background-color:#040404;">
</span><br>
<br><span style="color:#c0c000;background-color:#040404;">f3:</span><span style="color:#b2b2b2;background-color:#040404;">
</span><br><span style="color:#c00000;background-color:#040404;"> &#160;- This line is removed</span><span style="color:#b2b2b2;background-color:#040404;">
</span><br><span style="color:#c00000;background-color:#040404;"> &#160;- And this one too</span><span style="color:#b2b2b2;background-color:#040404;">
</span><br> &#160;&#160;&#160;This is a complex test
<br><span style="color:#c00000;background-color:#040404;"> &#160;- Hello 3</span><span style="color:#b2b2b2;background-color:#040404;">
</span><br><span style="color:#008000;background-color:#040404;"> &#160;+ Hello 3 And replaced ones</span><span style="color:#b2b2b2;background-color:#040404;">
</span><br> &#160;&#160;&#160;With some lines
<br><span style="color:#008000;background-color:#040404;"> &#160;+ And added lines</span><span style="color:#b2b2b2;background-color:#040404;">
</span><br> &#160;&#160;&#160;And otherlines
<br> &#160;&#160;&#160;common 1
<br> &#160;&#160;&#160;common 2
<br><span style="color:#18b2b2;background-color:#040404;"> &#160;[...] --- </span><span style="color:#c00000;background-color:#040404;">expected:11</span><span style="color:#18b2b2;background-color:#040404;"> / </span><span style="color:#008000;background-color:#040404;">candidate:10 ---</span><span style="color:#b2b2b2;background-color:#040404;">
</span><br> &#160;&#160;&#160;common 6
<br> &#160;&#160;&#160;common 7
<br> &#160;&#160;&#160;common 8
<br><span style="color:#c00000;background-color:#040404;"> &#160;- and diff 1</span><span style="color:#b2b2b2;background-color:#040404;">
</span><br><span style="color:#008000;background-color:#040404;"> &#160;+ diff</span><span style="color:#b2b2b2;background-color:#040404;">
</span><br>
<br><span style="color:#c0c000;background-color:#040404;">dir4/f3:</span><span style="color:#b2b2b2;background-color:#040404;">
</span><br><span style="color:#c00000;background-color:#040404;"> &#160;- This line is removed</span><span style="color:#b2b2b2;background-color:#040404;">
</span><br><span style="color:#c00000;background-color:#040404;"> &#160;- And this one too</span><span style="color:#b2b2b2;background-color:#040404;">
</span><br> &#160;&#160;&#160;This is a complex test
<br><span style="color:#c00000;background-color:#040404;"> &#160;- Hello 3</span><span style="color:#b2b2b2;background-color:#040404;">
</span><br><span style="color:#008000;background-color:#040404;"> &#160;+ Hello 3 And replaced ones</span><span style="color:#b2b2b2;background-color:#040404;">
</span><br> &#160;&#160;&#160;With some lines
<br><span style="color:#008000;background-color:#040404;"> &#160;+ And added lines</span><span style="color:#b2b2b2;background-color:#040404;">
</span><br> &#160;&#160;&#160;And otherlines
<br> &#160;&#160;&#160;common 1
<br> &#160;&#160;&#160;common 2
<br><span style="color:#18b2b2;background-color:#040404;"> &#160;[...] --- </span><span style="color:#c00000;background-color:#040404;">expected:11</span><span style="color:#18b2b2;background-color:#040404;"> / </span><span style="color:#008000;background-color:#040404;">candidate:10 ---</span><span style="color:#b2b2b2;background-color:#040404;">
</span><br> &#160;&#160;&#160;common 6
<br> &#160;&#160;&#160;common 7
<br> &#160;&#160;&#160;common 8
<br><span style="color:#c00000;background-color:#040404;"> &#160;- and diff 1</span><span style="color:#b2b2b2;background-color:#040404;">
</span><br><span style="color:#008000;background-color:#040404;"> &#160;+ diff</span><span style="color:#b2b2b2;background-color:#040404;">
</span><br>
<br></body>



