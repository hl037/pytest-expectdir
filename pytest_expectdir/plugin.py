from __future__ import annotations
import os
import shutil
import sys
from pathlib import Path
from filecmp import dircmp
from contextlib import contextmanager
from typing import TYPE_CHECKING
from io import StringIO
from difflib import SequenceMatcher

import pytest

if TYPE_CHECKING : # pragma: no cover
  from typing import TextIO, Iterable

RESET = '\x1b[39m'
RED = '\x1b[31m'
GREEN = '\x1b[32m'
CYAN = '\x1b[36m'
YELLOW = '\x1b[33m'


def _win32_longpath(path):
  """
  Helper function to add the long path prefix for Windows, so that shutil.copytree
  won't fail while working with paths with 255+ chars.

  From copy pasted from pytest-datadir https://github.com/gabrielcnr/pytest-datadir/blob/master/src/pytest_datadir/plugin.py
  """
  if sys.platform == "win32": # pragma: no cover
      # The use of os.path.normpath here is necessary since "the "\\?\" prefix
      # to a path string tells the Windows APIs to disable all string parsing
      # and to send the string that follows it straight to the file system".
      # (See https://docs.microsoft.com/pt-br/windows/desktop/FileIO/naming-a-file)
      return "\\\\?\\" + os.path.normpath(path)
  else:
      return path

def formatFileDiff(f:TextIO, lines_candidate:Iterable[str], lines_expected:Iterable[str], context=3, indent='  '):
  b, a = lines_candidate, lines_expected
  matcher = SequenceMatcher(None, a, b)
  for tag, alo, ahi, blo, bhi in matcher.get_opcodes():
    if tag == 'replace':
      #TODO Add caractere-wise diff
      f.write(''.join(f'{RED}{indent}- {l}' for l in a[alo:ahi]))
      f.write(''.join(f'{GREEN}{indent}+ {l}' for l in b[blo:bhi]))
    elif tag == 'delete':
      f.write(''.join(f'{RED}{indent}- {l}' for l in a[alo:ahi]))
    elif tag == 'insert':
      f.write(''.join(f'{GREEN}{indent}+ {l}' for l in b[blo:bhi]))
    elif tag == 'equal':
      if ahi - alo > 2 * context + 1 :
        f.write(''.join(f'{RESET}{indent}  {l}' for l in a[alo:alo + context]))
        f.write(CYAN)
        f.write(f'{indent}[...] --- {RED}expected:{ahi - context}{CYAN} / {GREEN}candidate:{bhi-context} ---\n')
        f.write(''.join(f'{RESET}{indent}  {l}' for l in a[ahi - context:ahi]))
      else :
        f.write(RESET)
        f.write(''.join(f'{RESET}{indent}  {l}' for l in a[alo:ahi]))
        
    else: # pragma: no cover
      raise ValueError('unknown tag %r' % (tag,))

def formatDiff(f:TextIO, candidate:Path, expected:Path, diffRes):
  left, right, diff = diffRes
  left = [ f'{p}{"/" if (candidate / p).is_dir() else ""}' for p in left ]
  right = [ f'{p}{"/" if (expected / p).is_dir() else ""}' for p in right ]
  f.write(f'{CYAN}Directory {RED}{expected} (expected){CYAN} is different from {GREEN}{candidate} (candidate){CYAN}.\n')
  if right :
    f.write(f'{RED}Missing in candidate :\n')
    f.write(''.join( f'{RED}{l}\n' for l in right ))
  if left :
    f.write(f'{GREEN}Extra in candidate :\n')
    f.write(''.join( f'{GREEN}{l}\n' for l in left ))
  if diff :
    f.write(f'{CYAN}In both directories but different content:\n')
    for p in diff :
      f.write(f'\n{YELLOW}{p}:\n')
      with open(candidate/p, 'r') as lines_candidate, open(expected/p, 'r') as lines_expected :
        formatFileDiff(f, list(lines_candidate), list(lines_expected))

def cmpdir(candidate:Path, expected:Path):
  res = [], [], []
  left, right, diff = res
  def inner(dc:dircmp, prefix):
    left.extend(prefix / fn for fn in dc.left_only)
    right.extend(prefix / fn for fn in dc.right_only)
    diff.extend(prefix / fn for fn in dc.diff_files)
    for sub_name, sub_dc in dc.subdirs.items() :
      inner(sub_dc, prefix / sub_name)
  inner(dircmp(candidate, expected, ignore=['.gitkeep']), Path(''))
  
  return not any(len(l) for l in res), res

def toBytes(s:object|bytes):
  if isinstance(s, bytes) :
    return s
  return str(s).encode('utf8')

def findAndReplaceAllInDir(directory:Path, searched:bytes, replacement:bytes):
  for dname, dirs, files in os.walk(directory):
    for fname in files:
      fpath = os.path.join(dname, fname)
      with open(fpath, "rb") as f:
        s = f.read()
      s = s.replace(searched, replacement)
      with open(fpath, "wb") as f:
        f.write(s)

class _ExpectDirCounter(object):
  """
  Descriptor to use a common counter on ExpectDir instances using the same path
  """
  def __init__(self):
    self.counters = {}

  def __get__(self, obj:'ExpectDir', objtype=None):
    if obj is None :
      return self.counters
    return self.counters.setdefault(str(obj.tmp_path.absolute()), -1)
  
  def __set__(self, obj:'ExpectDir', objvalue):
    self.counters[str(obj.tmp_path.absolute())] = objvalue

class ExpectDir(object):
  """
  Class to handle the teardown, and the assertions
  """
  EMPTY = '__empty__'
  current = _ExpectDirCounter()
  def __init__(self, tmp_path:Path, request, default_current_dir_replace_string=None):
    self.tmp_path = tmp_path
    currentFile = Path(request.module.__file__)
    self.cwd = currentFile.parent
    self.fallback = Path(currentFile.stem)
    if request.cls :
      self.fallback = self.fallback / request.cls.__name__
    if request.function :
      self.fallback = self.fallback / request.function.__name__
    self.default_current_dir_replace_string = default_current_dir_replace_string
    self.tmp_dir = None

  @contextmanager
  def __call__(self, datapath=None, initial=None, expected=None, current_dir_replace_string=None):
    if current_dir_replace_string is None :
      current_dir_replace_string = self.default_current_dir_replace_string
    self.current += 1
    if not expected :
      if not datapath :
        datapath = self.fallback
      expected = Path(datapath) / "expected"
    else :
      expected = Path(expected)
      if not initial and not datapath :
        initial = ExpectDir.EMPTY
    if not (self.cwd / expected).is_dir() :
      raise FileNotFoundError(f'{self.cwd / expected} (as expected directory for expectdir) is not a directory ')
      
    if not initial :
      initial = Path(datapath) / "initial"
      if not (self.cwd / initial).is_dir() :
        initial = None
    elif initial == ExpectDir.EMPTY :
      initial = None
    else :
      initial = Path(initial)
      if not (self.cwd / initial).is_dir() :
        raise FileNotFoundError(f'{self.cwd / initial} (as initial directory for expectdir) is not a directory whereas it has been passed explicitely as kwarg.')
        
    
    try :
      self.tmp_dir = self.tmp_path / f'candidate{self.current}'
      self.tmp_dir.parent.mkdir(parents=True, exist_ok=True)
      if initial :
        shutil.copytree(
          _win32_longpath(str(self.cwd / initial)), _win32_longpath(str(self.tmp_dir))
        )
      else :
        self.tmp_dir.mkdir()
      if current_dir_replace_string :
        # Replace the alias (current_dir_replace_string) by the current dir before doing the test
        alias = toBytes(current_dir_replace_string)
        path = toBytes(self.tmp_dir)
        findAndReplaceAllInDir(self.tmp_dir, alias, path)
      try :
        yield self.tmp_dir
      except :
        raise
      else :
        if current_dir_replace_string :
          # Replace the current dir by the alias after doing the test, so that the comparison works well with the expected result
          findAndReplaceAllInDir(self.tmp_dir, path, alias)
        res, diffRes = cmpdir(self.tmp_dir, self.cwd / expected)
        if res :
          return
        tio = StringIO()
        formatDiff(tio, self.tmp_dir, self.cwd / expected, diffRes)
        raise AssertionError(tio.getvalue())
    finally :
      self.tmp_dir = None


@pytest.fixture
def expectdir(tmp_path, request):
  return ExpectDir(tmp_path, request)

@pytest.fixture
def expectdirReplace(tmp_path, request):
  """
  Equivalent to expectedir() except it provides a default value to current_dir_replace_string
  """
  return ExpectDir(tmp_path, request, default_current_dir_replace_string='{{current_directory}}')
