# June 24, 2025

The file [mice.csv](./mice.csv) (source:
https://archive.ics.uci.edu/ml/datasets/Mice+Protein+Expression) contains the
expression levels of 77 proteins/protein modifications that produced detectable
signals in the nuclear fraction of cortex. The eight classes of mice are
described based on features such as genotype, behavior and treatment. According
to genotype, mice can be control or trisomic. According to behavior, some mice
have been stimulated to learn (context-shock, C/S) and others have not
(shock-context, S/C) and in order to assess the effect of the drug memantine in
recovering the ability to learn in trisomic mice, some mice have been injected
with the drug and others have not.

## Setup

The `exam.py` is intended to be modified as a
[jupyter](https://jupyter.org/) notebook. The notebook format `.ipynb`, however,
is not very convenient for configuration management, testing, and giving
feedback via the usual "pull-request" mechanism provided by Github. Thus, this
repository uses
[jupytext](https://jupytext.readthedocs.io/en/latest/install.html) to **pair** a
pure Python file with a notebook with the same name. The notebook is
automatically created when you open the Python file with jupyter, and the two
files are kept in sync. Do not add `exercise.ipynb` to the files managed by git.

To start, you need the following actions:

```sh
python3.12 -m venv VIRTUAL_ENVIRONMENT
# remember to activate the virtual environment according to your operating system rules:
# source VIRTUAL_ENVIRONMENT/bin/activate # adapt to your system
pip install -r requirements.txt
jupyter notebook
```

Then you can open the `exam.py` as a notebook in the browser.


## Test

To test examples in docstrings use:

```python
import doctest
doctest.testmod()
```


You can execute tests locally on the python file:


```sh
mypy exam.py
python -m doctest exam.py
```
