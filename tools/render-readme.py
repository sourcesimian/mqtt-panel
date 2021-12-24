#!/usr/bin/env python

import glob
import os
import re
import tempfile

INCLUDE_BEGIN = '<!-- include:begin %s -->'
INCLUDE_END = '<!-- include:end -->'

# print(INCLUDE_BEGIN % '(?P<path>.*)' + '(?P<content>.*?)' + INCLUDE_END)
re_include = re.compile(INCLUDE_BEGIN % '(?P<path>.*?)' + '(?P<content>.*?)' + INCLUDE_END, re.MULTILINE | re.DOTALL)

def repl(match):
  path = match.group('path')
  
  parts = [INCLUDE_BEGIN % path + '\n']
  for file in glob.iglob(path):
    with open(file, 'rt', encoding="utf8") as fh:
      content = fh.read()
      parts.append(content)
      if content[-1] != '\n':
        parts.append('\n')
  parts.append(INCLUDE_END)

  return ''.join(parts)

def update_md_includes(filename):
  with open(filename, 'rt', encoding="utf8") as fh:
    content = fh.read()

  new_content = re_include.sub(repl, content)

  with tempfile.NamedTemporaryFile('wt', prefix=filename, delete=False) as fh:
    fh.write(new_content)
    tmp = fh.name
  os.rename(tmp, filename)


update_md_includes('README.md')