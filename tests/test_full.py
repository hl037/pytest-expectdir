from pathlib import Path
import pytest

class CustomError(RuntimeError):
  pass

def test_imports():
  """Because coverage start after imports, lets write a dummy test to mark them as covered"""
  import sys
  del sys.modules['pytest_expectdir']
  del sys.modules['pytest_expectdir.plugin']
  import pytest_expectdir
  import pytest_expectdir.plugin

def test_no_error(expectdir, expectdirReplace):
  with expectdir('data/test1') as tmp_dir :
    inst_tmp_dir = expectdir.tmp_dir
  assert inst_tmp_dir == tmp_dir
  
  with expectdirReplace('data/test1', current_dir_replace_string=None) as tmp_dir :
    inst_tmp_dir = expectdirReplace.tmp_dir
  assert inst_tmp_dir == tmp_dir
  
  with expectdirReplace('data/test1', current_dir_replace_string='{{current_directory}}') as tmp_dir :
    inst_tmp_dir = expectdirReplace.tmp_dir
  assert inst_tmp_dir == tmp_dir
  assert isinstance(expectdir.__class__.current, dict)
  
def test_forward_errors(expectdir, expectdirReplace):
  with pytest.raises(CustomError) as excinfo :
    with expectdir('data/test2') as tmp_dir :
      raise CustomError('This error should be raised instead of a directory comparison')
  with pytest.raises(CustomError) as excinfo :
    with expectdirReplace('data/test2', current_dir_replace_string=None) as tmp_dir :
      raise CustomError('This error should be raised instead of a directory comparison')
  with pytest.raises(CustomError) as excinfo :
    with expectdirReplace('data/test2', current_dir_replace_string='{{current_directory}}') as tmp_dir :
      raise CustomError('This error should be raised instead of a directory comparison')
  
def test_no_initial_data_path(expectdir, expectdirReplace):
  with expectdir('data/test2') as tmp_dir :
    inst_tmp_dir = expectdir.tmp_dir
    with open(tmp_dir / 'f1', 'w') as f :
      f.write('Hello1\n')
  assert inst_tmp_dir == tmp_dir
  
  with expectdirReplace('data/test2', current_dir_replace_string=None) as tmp_dir :
    inst_tmp_dir = expectdirReplace.tmp_dir
    with open(tmp_dir / 'f1', 'w') as f :
      f.write('Hello1\n')
  assert inst_tmp_dir == tmp_dir
  
  with expectdirReplace('data/test2', current_dir_replace_string='{{current_directory}}') as tmp_dir :
    inst_tmp_dir = expectdirReplace.tmp_dir
    with open(tmp_dir / 'f1', 'w') as f :
      f.write('Hello1\n')
  assert inst_tmp_dir == tmp_dir
  assert expectdir.current is expectdirReplace.current
      
def test_no_initial_expected(expectdir, expectdirReplace):
  with expectdir(expected='data/test2/expected') as tmp_dir :
    inst_tmp_dir = expectdir.tmp_dir
    with open(tmp_dir / 'f1', 'w') as f :
      f.write('Hello1\n')
  assert inst_tmp_dir == tmp_dir
  
  with expectdirReplace(expected='data/test2/expected', current_dir_replace_string=None) as tmp_dir :
    inst_tmp_dir = expectdirReplace.tmp_dir
    with open(tmp_dir / 'f1', 'w') as f :
      f.write('Hello1\n')
  assert inst_tmp_dir == tmp_dir
  
  with expectdirReplace(expected='data/test2/expected', current_dir_replace_string='{{current_directory}}') as tmp_dir :
    inst_tmp_dir = expectdirReplace.tmp_dir
    with open(tmp_dir / 'f1', 'w') as f :
      f.write('Hello1\n')
  assert inst_tmp_dir == tmp_dir
  assert expectdir.current is expectdirReplace.current

def test_full_data_path(expectdir, request, expectdirReplace):
  tmp_path = None
  with pytest.raises(AssertionError) as excinfo :
    with expectdir('data/test3') :
      tmp_path = expectdir.tmp_path
  assert tmp_path is not None, "The with part was not executed before the assertion"
  expected = Path(request.module.__file__).parent / 'data/test3/expected'
  candidate = tmp_path / f'candidate{expectdir.current}'
  
  EXPECTED_MSG = f'\x1b[36mDirectory \x1b[31m{expected} (expected)\x1b[36m is different from \x1b[32m{candidate} (candidate)\x1b[36m.\n\x1b[31mMissing in candidate :\n\x1b[31mdir3/\n\x1b[31mf1\n\x1b[32mExtra in candidate :\n\x1b[32mdir2/\n\x1b[32mf4\n\x1b[36mIn both directories but different content:\n\n\x1b[33mf3:\n\x1b[31m  - This line is removed\n\x1b[31m  - And this one too\n\x1b[39m\x1b[39m    This is a complex test\n\x1b[31m  - Hello 3\n\x1b[32m  + Hello 3 And replaced ones\n\x1b[39m\x1b[39m    With some lines\n\x1b[32m  + And added lines\n\x1b[39m    And otherlines\n\x1b[39m    common 1\n\x1b[39m    common 2\n\x1b[36m  [...] --- \x1b[31mexpected:11\x1b[36m / \x1b[32mcandidate:10 ---\n\x1b[39m    common 6\n\x1b[39m    common 7\n\x1b[39m    common 8\n\x1b[31m  - and diff 1\n\x1b[32m  + diff\n\n\x1b[33mdir4/f3:\n\x1b[31m  - This line is removed\n\x1b[31m  - And this one too\n\x1b[39m\x1b[39m    This is a complex test\n\x1b[31m  - Hello 3\n\x1b[32m  + Hello 3 And replaced ones\n\x1b[39m\x1b[39m    With some lines\n\x1b[32m  + And added lines\n\x1b[39m    And otherlines\n\x1b[39m    common 1\n\x1b[39m    common 2\n\x1b[36m  [...] --- \x1b[31mexpected:11\x1b[36m / \x1b[32mcandidate:10 ---\n\x1b[39m    common 6\n\x1b[39m    common 7\n\x1b[39m    common 8\n\x1b[31m  - and diff 1\n\x1b[32m  + diff\n'
  assert str(excinfo.value) == EXPECTED_MSG
  
  
  tmp_path = None
  with pytest.raises(AssertionError) as excinfo :
    with expectdirReplace('data/test3', current_dir_replace_string=None) :
      tmp_path = expectdirReplace.tmp_path
  assert tmp_path is not None, "The with part was not executed before the assertion"
  expected = Path(request.module.__file__).parent / 'data/test3/expected'
  candidate = tmp_path / f'candidate{expectdirReplace.current}'
  
  EXPECTED_MSG = f'\x1b[36mDirectory \x1b[31m{expected} (expected)\x1b[36m is different from \x1b[32m{candidate} (candidate)\x1b[36m.\n\x1b[31mMissing in candidate :\n\x1b[31mdir3/\n\x1b[31mf1\n\x1b[32mExtra in candidate :\n\x1b[32mdir2/\n\x1b[32mf4\n\x1b[36mIn both directories but different content:\n\n\x1b[33mf3:\n\x1b[31m  - This line is removed\n\x1b[31m  - And this one too\n\x1b[39m\x1b[39m    This is a complex test\n\x1b[31m  - Hello 3\n\x1b[32m  + Hello 3 And replaced ones\n\x1b[39m\x1b[39m    With some lines\n\x1b[32m  + And added lines\n\x1b[39m    And otherlines\n\x1b[39m    common 1\n\x1b[39m    common 2\n\x1b[36m  [...] --- \x1b[31mexpected:11\x1b[36m / \x1b[32mcandidate:10 ---\n\x1b[39m    common 6\n\x1b[39m    common 7\n\x1b[39m    common 8\n\x1b[31m  - and diff 1\n\x1b[32m  + diff\n\n\x1b[33mdir4/f3:\n\x1b[31m  - This line is removed\n\x1b[31m  - And this one too\n\x1b[39m\x1b[39m    This is a complex test\n\x1b[31m  - Hello 3\n\x1b[32m  + Hello 3 And replaced ones\n\x1b[39m\x1b[39m    With some lines\n\x1b[32m  + And added lines\n\x1b[39m    And otherlines\n\x1b[39m    common 1\n\x1b[39m    common 2\n\x1b[36m  [...] --- \x1b[31mexpected:11\x1b[36m / \x1b[32mcandidate:10 ---\n\x1b[39m    common 6\n\x1b[39m    common 7\n\x1b[39m    common 8\n\x1b[31m  - and diff 1\n\x1b[32m  + diff\n'
  assert str(excinfo.value) == EXPECTED_MSG
  
  
  tmp_path = None
  with pytest.raises(AssertionError) as excinfo :
    with expectdirReplace('data/test3', current_dir_replace_string='{{current_directory}}') :
      tmp_path = expectdirReplace.tmp_path
  assert tmp_path is not None, "The with part was not executed before the assertion"
  expected = Path(request.module.__file__).parent / 'data/test3/expected'
  candidate = tmp_path / f'candidate{expectdirReplace.current}'
  
  EXPECTED_MSG = f'\x1b[36mDirectory \x1b[31m{expected} (expected)\x1b[36m is different from \x1b[32m{candidate} (candidate)\x1b[36m.\n\x1b[31mMissing in candidate :\n\x1b[31mdir3/\n\x1b[31mf1\n\x1b[32mExtra in candidate :\n\x1b[32mdir2/\n\x1b[32mf4\n\x1b[36mIn both directories but different content:\n\n\x1b[33mf3:\n\x1b[31m  - This line is removed\n\x1b[31m  - And this one too\n\x1b[39m\x1b[39m    This is a complex test\n\x1b[31m  - Hello 3\n\x1b[32m  + Hello 3 And replaced ones\n\x1b[39m\x1b[39m    With some lines\n\x1b[32m  + And added lines\n\x1b[39m    And otherlines\n\x1b[39m    common 1\n\x1b[39m    common 2\n\x1b[36m  [...] --- \x1b[31mexpected:11\x1b[36m / \x1b[32mcandidate:10 ---\n\x1b[39m    common 6\n\x1b[39m    common 7\n\x1b[39m    common 8\n\x1b[31m  - and diff 1\n\x1b[32m  + diff\n\n\x1b[33mdir4/f3:\n\x1b[31m  - This line is removed\n\x1b[31m  - And this one too\n\x1b[39m\x1b[39m    This is a complex test\n\x1b[31m  - Hello 3\n\x1b[32m  + Hello 3 And replaced ones\n\x1b[39m\x1b[39m    With some lines\n\x1b[32m  + And added lines\n\x1b[39m    And otherlines\n\x1b[39m    common 1\n\x1b[39m    common 2\n\x1b[36m  [...] --- \x1b[31mexpected:11\x1b[36m / \x1b[32mcandidate:10 ---\n\x1b[39m    common 6\n\x1b[39m    common 7\n\x1b[39m    common 8\n\x1b[31m  - and diff 1\n\x1b[32m  + diff\n'
  assert str(excinfo.value) == EXPECTED_MSG


def test_full_initial_expected(expectdir, request, expectdirReplace):
  tmp_path = None
  with pytest.raises(AssertionError) as excinfo :
    with expectdir(initial='data/test3/initial', expected='data/test3/expected') :
      tmp_path = expectdir.tmp_path
  assert tmp_path is not None, "The with part was not executed before the assertion"
  expected = Path(request.module.__file__).parent / 'data/test3/expected'
  candidate = tmp_path / f'candidate{expectdir.current}'
  
  EXPECTED_MSG = f'\x1b[36mDirectory \x1b[31m{expected} (expected)\x1b[36m is different from \x1b[32m{candidate} (candidate)\x1b[36m.\n\x1b[31mMissing in candidate :\n\x1b[31mdir3/\n\x1b[31mf1\n\x1b[32mExtra in candidate :\n\x1b[32mdir2/\n\x1b[32mf4\n\x1b[36mIn both directories but different content:\n\n\x1b[33mf3:\n\x1b[31m  - This line is removed\n\x1b[31m  - And this one too\n\x1b[39m\x1b[39m    This is a complex test\n\x1b[31m  - Hello 3\n\x1b[32m  + Hello 3 And replaced ones\n\x1b[39m\x1b[39m    With some lines\n\x1b[32m  + And added lines\n\x1b[39m    And otherlines\n\x1b[39m    common 1\n\x1b[39m    common 2\n\x1b[36m  [...] --- \x1b[31mexpected:11\x1b[36m / \x1b[32mcandidate:10 ---\n\x1b[39m    common 6\n\x1b[39m    common 7\n\x1b[39m    common 8\n\x1b[31m  - and diff 1\n\x1b[32m  + diff\n\n\x1b[33mdir4/f3:\n\x1b[31m  - This line is removed\n\x1b[31m  - And this one too\n\x1b[39m\x1b[39m    This is a complex test\n\x1b[31m  - Hello 3\n\x1b[32m  + Hello 3 And replaced ones\n\x1b[39m\x1b[39m    With some lines\n\x1b[32m  + And added lines\n\x1b[39m    And otherlines\n\x1b[39m    common 1\n\x1b[39m    common 2\n\x1b[36m  [...] --- \x1b[31mexpected:11\x1b[36m / \x1b[32mcandidate:10 ---\n\x1b[39m    common 6\n\x1b[39m    common 7\n\x1b[39m    common 8\n\x1b[31m  - and diff 1\n\x1b[32m  + diff\n'
  assert str(excinfo.value) == EXPECTED_MSG
  tmp_path = None
  with pytest.raises(AssertionError) as excinfo :
    with expectdirReplace(initial='data/test3/initial', expected='data/test3/expected', current_dir_replace_string=None) :
      tmp_path = expectdirReplace.tmp_path
  assert tmp_path is not None, "The with part was not executed before the assertion"
  expected = Path(request.module.__file__).parent / 'data/test3/expected'
  candidate = tmp_path / f'candidate{expectdirReplace.current}'
  
  EXPECTED_MSG = f'\x1b[36mDirectory \x1b[31m{expected} (expected)\x1b[36m is different from \x1b[32m{candidate} (candidate)\x1b[36m.\n\x1b[31mMissing in candidate :\n\x1b[31mdir3/\n\x1b[31mf1\n\x1b[32mExtra in candidate :\n\x1b[32mdir2/\n\x1b[32mf4\n\x1b[36mIn both directories but different content:\n\n\x1b[33mf3:\n\x1b[31m  - This line is removed\n\x1b[31m  - And this one too\n\x1b[39m\x1b[39m    This is a complex test\n\x1b[31m  - Hello 3\n\x1b[32m  + Hello 3 And replaced ones\n\x1b[39m\x1b[39m    With some lines\n\x1b[32m  + And added lines\n\x1b[39m    And otherlines\n\x1b[39m    common 1\n\x1b[39m    common 2\n\x1b[36m  [...] --- \x1b[31mexpected:11\x1b[36m / \x1b[32mcandidate:10 ---\n\x1b[39m    common 6\n\x1b[39m    common 7\n\x1b[39m    common 8\n\x1b[31m  - and diff 1\n\x1b[32m  + diff\n\n\x1b[33mdir4/f3:\n\x1b[31m  - This line is removed\n\x1b[31m  - And this one too\n\x1b[39m\x1b[39m    This is a complex test\n\x1b[31m  - Hello 3\n\x1b[32m  + Hello 3 And replaced ones\n\x1b[39m\x1b[39m    With some lines\n\x1b[32m  + And added lines\n\x1b[39m    And otherlines\n\x1b[39m    common 1\n\x1b[39m    common 2\n\x1b[36m  [...] --- \x1b[31mexpected:11\x1b[36m / \x1b[32mcandidate:10 ---\n\x1b[39m    common 6\n\x1b[39m    common 7\n\x1b[39m    common 8\n\x1b[31m  - and diff 1\n\x1b[32m  + diff\n'
  assert str(excinfo.value) == EXPECTED_MSG
  tmp_path = None
  with pytest.raises(AssertionError) as excinfo :
    with expectdirReplace(initial='data/test3/initial', expected='data/test3/expected', current_dir_replace_string='{{current_directory}}') :
      tmp_path = expectdirReplace.tmp_path
  assert tmp_path is not None, "The with part was not executed before the assertion"
  expected = Path(request.module.__file__).parent / 'data/test3/expected'
  candidate = tmp_path / f'candidate{expectdirReplace.current}'
  
  EXPECTED_MSG = f'\x1b[36mDirectory \x1b[31m{expected} (expected)\x1b[36m is different from \x1b[32m{candidate} (candidate)\x1b[36m.\n\x1b[31mMissing in candidate :\n\x1b[31mdir3/\n\x1b[31mf1\n\x1b[32mExtra in candidate :\n\x1b[32mdir2/\n\x1b[32mf4\n\x1b[36mIn both directories but different content:\n\n\x1b[33mf3:\n\x1b[31m  - This line is removed\n\x1b[31m  - And this one too\n\x1b[39m\x1b[39m    This is a complex test\n\x1b[31m  - Hello 3\n\x1b[32m  + Hello 3 And replaced ones\n\x1b[39m\x1b[39m    With some lines\n\x1b[32m  + And added lines\n\x1b[39m    And otherlines\n\x1b[39m    common 1\n\x1b[39m    common 2\n\x1b[36m  [...] --- \x1b[31mexpected:11\x1b[36m / \x1b[32mcandidate:10 ---\n\x1b[39m    common 6\n\x1b[39m    common 7\n\x1b[39m    common 8\n\x1b[31m  - and diff 1\n\x1b[32m  + diff\n\n\x1b[33mdir4/f3:\n\x1b[31m  - This line is removed\n\x1b[31m  - And this one too\n\x1b[39m\x1b[39m    This is a complex test\n\x1b[31m  - Hello 3\n\x1b[32m  + Hello 3 And replaced ones\n\x1b[39m\x1b[39m    With some lines\n\x1b[32m  + And added lines\n\x1b[39m    And otherlines\n\x1b[39m    common 1\n\x1b[39m    common 2\n\x1b[36m  [...] --- \x1b[31mexpected:11\x1b[36m / \x1b[32mcandidate:10 ---\n\x1b[39m    common 6\n\x1b[39m    common 7\n\x1b[39m    common 8\n\x1b[31m  - and diff 1\n\x1b[32m  + diff\n'
  assert str(excinfo.value) == EXPECTED_MSG

def test_function(expectdir, request, expectdirReplace):
  tmp_path = None
  with pytest.raises(AssertionError) as excinfo :
    with expectdir() :
      tmp_path = expectdir.tmp_path
  assert tmp_path is not None, "The with part was not executed before the assertion"
  expected = Path(request.module.__file__).parent / 'test_full/test_function/expected'
  candidate = tmp_path / f'candidate{expectdir.current}'
  
  EXPECTED_MSG = f'\x1b[36mDirectory \x1b[31m{expected} (expected)\x1b[36m is different from \x1b[32m{candidate} (candidate)\x1b[36m.\n\x1b[31mMissing in candidate :\n\x1b[31mdir3/\n\x1b[31mf1\n\x1b[32mExtra in candidate :\n\x1b[32mdir2/\n\x1b[32mf4\n\x1b[36mIn both directories but different content:\n\n\x1b[33mf3:\n\x1b[31m  - This line is removed\n\x1b[31m  - And this one too\n\x1b[39m\x1b[39m    This is a complex test\n\x1b[31m  - Hello 3\n\x1b[32m  + Hello 3 And replaced ones\n\x1b[39m\x1b[39m    With some lines\n\x1b[32m  + And added lines\n\x1b[39m    And otherlines\n\x1b[39m    common 1\n\x1b[39m    common 2\n\x1b[36m  [...] --- \x1b[31mexpected:11\x1b[36m / \x1b[32mcandidate:10 ---\n\x1b[39m    common 6\n\x1b[39m    common 7\n\x1b[39m    common 8\n\x1b[31m  - and diff 1\n\x1b[32m  + diff\n\n\x1b[33mdir4/f3:\n\x1b[31m  - This line is removed\n\x1b[31m  - And this one too\n\x1b[39m\x1b[39m    This is a complex test\n\x1b[31m  - Hello 3\n\x1b[32m  + Hello 3 And replaced ones\n\x1b[39m\x1b[39m    With some lines\n\x1b[32m  + And added lines\n\x1b[39m    And otherlines\n\x1b[39m    common 1\n\x1b[39m    common 2\n\x1b[36m  [...] --- \x1b[31mexpected:11\x1b[36m / \x1b[32mcandidate:10 ---\n\x1b[39m    common 6\n\x1b[39m    common 7\n\x1b[39m    common 8\n\x1b[31m  - and diff 1\n\x1b[32m  + diff\n'
  assert str(excinfo.value) == EXPECTED_MSG
  tmp_path = None
  with pytest.raises(AssertionError) as excinfo :
    with expectdirReplace(current_dir_replace_string=None) :
      tmp_path = expectdirReplace.tmp_path
  assert tmp_path is not None, "The with part was not executed before the assertion"
  expected = Path(request.module.__file__).parent / 'test_full/test_function/expected'
  candidate = tmp_path / f'candidate{expectdirReplace.current}'
  
  EXPECTED_MSG = f'\x1b[36mDirectory \x1b[31m{expected} (expected)\x1b[36m is different from \x1b[32m{candidate} (candidate)\x1b[36m.\n\x1b[31mMissing in candidate :\n\x1b[31mdir3/\n\x1b[31mf1\n\x1b[32mExtra in candidate :\n\x1b[32mdir2/\n\x1b[32mf4\n\x1b[36mIn both directories but different content:\n\n\x1b[33mf3:\n\x1b[31m  - This line is removed\n\x1b[31m  - And this one too\n\x1b[39m\x1b[39m    This is a complex test\n\x1b[31m  - Hello 3\n\x1b[32m  + Hello 3 And replaced ones\n\x1b[39m\x1b[39m    With some lines\n\x1b[32m  + And added lines\n\x1b[39m    And otherlines\n\x1b[39m    common 1\n\x1b[39m    common 2\n\x1b[36m  [...] --- \x1b[31mexpected:11\x1b[36m / \x1b[32mcandidate:10 ---\n\x1b[39m    common 6\n\x1b[39m    common 7\n\x1b[39m    common 8\n\x1b[31m  - and diff 1\n\x1b[32m  + diff\n\n\x1b[33mdir4/f3:\n\x1b[31m  - This line is removed\n\x1b[31m  - And this one too\n\x1b[39m\x1b[39m    This is a complex test\n\x1b[31m  - Hello 3\n\x1b[32m  + Hello 3 And replaced ones\n\x1b[39m\x1b[39m    With some lines\n\x1b[32m  + And added lines\n\x1b[39m    And otherlines\n\x1b[39m    common 1\n\x1b[39m    common 2\n\x1b[36m  [...] --- \x1b[31mexpected:11\x1b[36m / \x1b[32mcandidate:10 ---\n\x1b[39m    common 6\n\x1b[39m    common 7\n\x1b[39m    common 8\n\x1b[31m  - and diff 1\n\x1b[32m  + diff\n'
  assert str(excinfo.value) == EXPECTED_MSG
  tmp_path = None
  with pytest.raises(AssertionError) as excinfo :
    with expectdirReplace(current_dir_replace_string='{{current_directory}}') :
      tmp_path = expectdirReplace.tmp_path
  assert tmp_path is not None, "The with part was not executed before the assertion"
  expected = Path(request.module.__file__).parent / 'test_full/test_function/expected'
  candidate = tmp_path / f'candidate{expectdirReplace.current}'
  
  EXPECTED_MSG = f'\x1b[36mDirectory \x1b[31m{expected} (expected)\x1b[36m is different from \x1b[32m{candidate} (candidate)\x1b[36m.\n\x1b[31mMissing in candidate :\n\x1b[31mdir3/\n\x1b[31mf1\n\x1b[32mExtra in candidate :\n\x1b[32mdir2/\n\x1b[32mf4\n\x1b[36mIn both directories but different content:\n\n\x1b[33mf3:\n\x1b[31m  - This line is removed\n\x1b[31m  - And this one too\n\x1b[39m\x1b[39m    This is a complex test\n\x1b[31m  - Hello 3\n\x1b[32m  + Hello 3 And replaced ones\n\x1b[39m\x1b[39m    With some lines\n\x1b[32m  + And added lines\n\x1b[39m    And otherlines\n\x1b[39m    common 1\n\x1b[39m    common 2\n\x1b[36m  [...] --- \x1b[31mexpected:11\x1b[36m / \x1b[32mcandidate:10 ---\n\x1b[39m    common 6\n\x1b[39m    common 7\n\x1b[39m    common 8\n\x1b[31m  - and diff 1\n\x1b[32m  + diff\n\n\x1b[33mdir4/f3:\n\x1b[31m  - This line is removed\n\x1b[31m  - And this one too\n\x1b[39m\x1b[39m    This is a complex test\n\x1b[31m  - Hello 3\n\x1b[32m  + Hello 3 And replaced ones\n\x1b[39m\x1b[39m    With some lines\n\x1b[32m  + And added lines\n\x1b[39m    And otherlines\n\x1b[39m    common 1\n\x1b[39m    common 2\n\x1b[36m  [...] --- \x1b[31mexpected:11\x1b[36m / \x1b[32mcandidate:10 ---\n\x1b[39m    common 6\n\x1b[39m    common 7\n\x1b[39m    common 8\n\x1b[31m  - and diff 1\n\x1b[32m  + diff\n'
  assert str(excinfo.value) == EXPECTED_MSG

def test_empty(expectdir, expectdirReplace):
  with expectdir(initial='__empty__') :
    pass

  with expectdir('test_full/test_empty', initial='__empty__') :
    pass
  
  with expectdir(expected='test_full/test_empty/expected') :
    pass
  
  
  with expectdirReplace(initial='__empty__', current_dir_replace_string=None) :
    pass

  with expectdirReplace('test_full/test_empty', initial='__empty__', current_dir_replace_string=None) :
    pass
  
  with expectdirReplace(expected='test_full/test_empty/expected', current_dir_replace_string=None) :
    pass
  
  
  with expectdirReplace(initial='__empty__', current_dir_replace_string='{{current_directory}}') :
    pass

  with expectdirReplace('test_full/test_empty', initial='__empty__', current_dir_replace_string='{{current_directory}}') :
    pass
  
  with expectdirReplace(expected='test_full/test_empty/expected', current_dir_replace_string='{{current_directory}}') :
    pass

def test_filenotfound(expectdir, expectdirReplace):
  with pytest.raises(FileNotFoundError, match='test_full/test_filenotfound/expected') :
    with expectdir(initial='test_full/test_empty/initial') :
      pass
    
  with pytest.raises(FileNotFoundError, match='test_full/test_filenotfound/expected') :
    with expectdir(initial='test_full/test_empty/initial', expected='test_full/test_filenotfound/expected') :
      pass
    
  with pytest.raises(FileNotFoundError, match='test_full/test_filenotfound/expected') :
    with expectdir('test_full/test_filenotfound', initial='test_full/test_empty/initial') :
      pass
    
  with pytest.raises(FileNotFoundError, match='test_full/test_filenotfound/initial') :
    with expectdir(initial='test_full/test_filenotfound/initial', expected='test_full/test_empty/expected') :
      pass
    

  with pytest.raises(FileNotFoundError, match='test_full/test_filenotfound/expected') :
    with expectdirReplace(initial='test_full/test_empty/initial', current_dir_replace_string=None) :
      pass
    
  with pytest.raises(FileNotFoundError, match='test_full/test_filenotfound/expected') :
    with expectdirReplace(initial='test_full/test_empty/initial', expected='test_full/test_filenotfound/expected', current_dir_replace_string=None) :
      pass
    
  with pytest.raises(FileNotFoundError, match='test_full/test_filenotfound/expected') :
    with expectdirReplace('test_full/test_filenotfound', initial='test_full/test_empty/initial', current_dir_replace_string=None) :
      pass
    
  with pytest.raises(FileNotFoundError, match='test_full/test_filenotfound/initial') :
    with expectdirReplace(initial='test_full/test_filenotfound/initial', expected='test_full/test_empty/expected', current_dir_replace_string=None) :
      pass
    

  with pytest.raises(FileNotFoundError, match='test_full/test_filenotfound/expected') :
    with expectdirReplace(initial='test_full/test_empty/initial', current_dir_replace_string='{{current_directory}}') :
      pass
    
  with pytest.raises(FileNotFoundError, match='test_full/test_filenotfound/expected') :
    with expectdirReplace(initial='test_full/test_empty/initial', expected='test_full/test_filenotfound/expected', current_dir_replace_string='{{current_directory}}') :
      pass
    
  with pytest.raises(FileNotFoundError, match='test_full/test_filenotfound/expected') :
    with expectdirReplace('test_full/test_filenotfound', initial='test_full/test_empty/initial', current_dir_replace_string='{{current_directory}}') :
      pass
    
  with pytest.raises(FileNotFoundError, match='test_full/test_filenotfound/initial') :
    with expectdirReplace(initial='test_full/test_filenotfound/initial', expected='test_full/test_empty/expected', current_dir_replace_string='{{current_directory}}') :
      pass


class TestClass():
  def test_method(self, expectdir, expectdirReplace):
    with expectdir() :
      pass
    with expectdirReplace(current_dir_replace_string=None) :
      pass
    with expectdirReplace(current_dir_replace_string='{{current_directory}}') :
      pass


def test_replacement(expectdir, expectdirReplace):
  with expectdir(current_dir_replace_string='{{current_directory}}') as tmp_dir :
    with open(tmp_dir/'test_file', 'r') as f :
      content = f.read()
    assert content == f'{tmp_dir}\n'
    
  with expectdirReplace() as tmp_dir :
    with open(tmp_dir/'test_file', 'r') as f :
      content = f.read()
    assert content == f'{tmp_dir}\n'
    
  with expectdirReplace(current_dir_replace_string='{{current_directory}}') as tmp_dir :
    with open(tmp_dir/'test_file', 'r') as f :
      content = f.read()
    assert content == f'{tmp_dir}\n'

def test_replacement_bytes(expectdir, expectdirReplace):
  with expectdir(current_dir_replace_string=b'{{current_directory}}') as tmp_dir :
    with open(tmp_dir/'test_file', 'r') as f :
      content = f.read()
    assert content == f'{tmp_dir}\n'
    
  with expectdirReplace(current_dir_replace_string=b'{{current_directory}}') as tmp_dir :
    with open(tmp_dir/'test_file', 'r') as f :
      content = f.read()
    assert content == f'{tmp_dir}\n'

