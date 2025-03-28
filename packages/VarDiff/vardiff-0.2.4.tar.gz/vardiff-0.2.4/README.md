# VarDiff - Kohan Mathers

VarDiff is a Python package for comparing variables and files. 
It provides a simple interface for identifying differences between two variables (strings, numbers, lists, and dictionaries) or two text files (line-by-line comparison).

## Installation

To install VarDiff, use:

```bash
pip install VarDiff
```

## Example Usage
Compare 2 variables:

```py
import vardiff

comp = VarDiff()

foo = 123
bar = 321

comp.compare(foo, bar)
```

Compare 2 files:
```py
import vardiff

comp = FileDiff()

foo = 'path/to/your/file1.txt'
bar = 'path/to/your/file2.txt'

comp.compare(foo, bar)
```