# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.16.6
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# # Programming in Python
# ## Exam: June 24, 2025
#
#
# You can solve the exercises below by using standard Python 3.12 libraries, NumPy, Matplotlib, Pandas, PyMC.
# You can browse the documentation: [Python](https://docs.python.org/3.12/), [NumPy](https://numpy.org/doc/1.26/index.html), [Matplotlib](https://matplotlib.org/3.10.0/users/index.html), [Pandas](https://pandas.pydata.org/pandas-docs/version/2.2/index.html), [PyMC](https://www.pymc.io/projects/docs/en/stable/api.html).
# You can also look at the [slides](https://homes.di.unimi.it/monga/lucidi2425/pyqb00.pdf) or your code on [GitHub](https://github.com).
#
#
# **The exam is "open book", but it is strictly forbidden to communicate with others or "ask questions" online (i.e., stackoverflow is ok if the answer is already there, but you cannot ask a new question or use ChatGPT and similar products). Suspicious canned answers or plagiarism among student solutions will cause the invalidation of the exam for all the people involved.**
#
# To test examples in docstrings use
#
# ```python
# import doctest
# doctest.testmod()
# ```

# **SOLVE EACH EXERCISE IN ONE OR MORE NOTEBOOK CELLS AFTER THE QUESTION.**

import numpy as np
import pandas as pd  # type: ignore
import matplotlib.pyplot as plt # type: ignore
import pymc as pm   # type: ignore
import arviz as az  # type: ignore


# ### Exercise 1 (max 3 points)
#
# The file [mice.csv](./mice.csv) (source: https://archive.ics.uci.edu/ml/datasets/Mice+Protein+Expression) contains the expression levels of 77 proteins/protein modifications that produced detectable signals in the nuclear fraction of cortex.
# The eight classes of mice are described based on features such as genotype, behavior and treatment. According to genotype, mice can be control or trisomic. According to behavior, some mice have been stimulated to learn (context-shock, C/S) and others have not (shock-context, S/C) and in order to assess the effect of the drug memantine in recovering the ability to learn in trisomic mice, some mice have been injected with the drug and others have not.
#
# Load the data using `MouseID` as the index and print the unique values for all the columns whose name does not end with "_N".

df = pd.read_csv('mice.csv', index_col='MouseID')
df.head()

for column in df[[c for c in df.columns if not c.endswith('_N')]]:
    print(f"{column}: {df[column].unique()}")

# ### Exercise 2 (max 2 points)
#
# Plot a histogram of the "NR1_N" values.
#

_ = df['NR1_N'].hist(bins='auto', density=True, legend=True)

# ### Exercise 3 (max 3 points)
#
# Make a figure with two columns of plots. In the first column plot together (contrast) the histograms of 'NR1_N' for the two genotypes. In the second column plot together (contrast) the histograms of 'NR1_N' for the two treatments. Use density histograms to make the diagrams easy to compare; add proper titles and legends.
#

fig, ax = plt.subplots(ncols=2, figsize=(10, 5))
for i, k in enumerate(['Genotype', 'Treatment']):
    for g in df[k].unique():
        ax[i].hist(df[df[k] == g]['NR1_N'], density=True, alpha=.7, bins='auto', label=g)
    ax[i].legend()
    ax[i].set_title(k)

# ### Exercise 4 (max 5 points)
#
# Make a figure with four plots (2 rows and 2 columns) with the histograms of both "NR1_N" and "NR2A_N" in the four feature combinations of "Genotype" and "Treatment". 
#

fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(10, 10), sharex=True, sharey=True)
for i, g in enumerate(df['Genotype'].unique()):
    for j, t in enumerate(df['Treatment'].unique()):
        for p in ['NR1_N', 'NR2A_N']:
            ax[i, j].hist(df[(df['Genotype'] == g) & (df['Treatment'] == t)][p], density=True, alpha=.7, bins='auto', label=f"{g} {t} {p}")
        ax[i, j].legend()


# ### Exercise 5 (max 7 points)
#
# Define a function that takes a list (a basic list, not a numpy array or pandas series) of floats and returns the median of all the values less than a given threshold. (The median is the middle element of an ordered series of numbers, when the number of elements is even the result is the mean of the two central ones). For example, if the list contains 2., 3., 1., 6., -1., 0.3, and the threshold is 5., the result is 1.; if the list contains 2., 3., 1., 6., -1., 0.4, 0. and the threshold is 5., the result is 0.7. 
#
#
# To get the full marks, you should declare correctly the type hints and add a test within a doctest string.

def median_under_threshold(numbers: list[float], threshold: float) -> float:
    """Return the median of all the numbers below the threshold.

    >>> import math
    >>> math.isclose(median_under_threshold([2., 3., 1., 6., -1., 0.3], 5.), 1.)
    True
    >>> math.isclose(median_under_threshold([2., 3., 1., 6., -1., 0.4, 0], 5.), 0.7)
    True
    >>> math.isnan(median_under_threshold([2., 3., 1., 6., -1., 0.4, 0], -2.))
    True

    """
    below = [x for x in numbers if x < threshold]
    n = len(below)
    if n == 0:
        return float('nan')
    if n % 2 != 0:
        return sorted(below)[len(below) // 2]
    low = len(below) // 2 - 1
    high = low + 1
    bb = sorted(below)
    return (bb[low] + bb[high]) / 2


import doctest
doctest.testmod()

# ### Exercise 6 (max 4 points)
#
# Apply the function defined in exercise 5 to "NR1_N" data, with a threshold of 2. Be sure to use arguments with the types required by the signature of the function. Compare the result with the one computed with pandas methods.

median_under_threshold(df['NR1_N'].to_list(), 2), df['NR1_N'][df['NR1_N'] < 2].median()

# ### Exercise 7 (max 4 points)
#
# Add a column `classification` to the data with a string that encodes the features of each observation. The genotype is encoded with c or t, the treatment with m and s: a record for a mouse with genotype Ts65Dn, behavior C/S, and treatment Saline will be encoded with the string "c-C/S-s". 

df['classification'] = df['Genotype'].str.lower().str.slice(0,1) + '-' + df['Behavior'] + '-' + df['Treatment'].str.lower().str.slice(0,1)

# ### Exercise 8 (max 5 points)
#
# Consider this statistical model: the value of "NR1_N" is normal with an unknown mean $\alpha + \beta\cdot x$, where $x$ is the value of "NR2A_N", and an unknown standard deviation $\sigma$. Your *a priori* estimation for both $\alpha$ and $\beta$ distribution is a normal distibution with mean 0 and std deviation 2; your *a priori* estimation for $\sigma$ exponential distribution with $\lambda=1$. Use PyMC to sample the posterior distributions after having seen the actual values, ignoring all the records in which either "NR1_N" or "NR2A" is not available. Plot the posterior distributions of the variables.
#
#

# +
dd = df[~df['NR1_N'].isnull() & ~df['NR2A_N'].isnull()]

with pm.Model():
    a = pm.Normal('alpha', mu=0, sigma=2)
    b = pm.Normal('beta', mu=0, sigma=2)
    s = pm.Exponential('sigma', lam=1)

    pm.Normal('NR1', mu=a+b*dd['NR2A_N'], observed=dd['NR1_N'])

    idata = pm.sample()
    
# -

_ = az.plot_posterior(idata)


