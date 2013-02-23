from __future__ import division

from cPickle import dump

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import sparse
from scipy.io import loadmat, savemat
from datetime import datetime
import os
try:
    import gmail
except ImportError:
    pass


# Change path to local version.
s = pd.HDFStore('/Volumes/HDD/Users/tom/DataStorage/Patents/patents.h5')


def get_tech_patents(store=pd.HDFStore(
        '/Volumes/HDD/Users/tom/DataStorage/Patents/patents.h5')):
    """
    Just tech industries (see classifications.py)
    store is an HDFStore with the utility file.
    returns a DataFrame with patent numbers.
    """
    df = store['utility']
    cat = df['subcat']
    t = df[(cat == 22.0) | (cat == 24.0) | (cat == 25.0)]

    return t[['patent']]


def filter(full, tech, filter_='citing', store=pd.HDFStore(
        '/Volumes/HDD/Users/tom/DataStorage/Patents/patents.h5')):
    """
    full is all the pairs.  Tech is from get_tech_patents.
    Probably will filter via CITING, not CITED.
    """
    sub = np.intersect1d(tech['patent'].unique(),
        full[filter_].unique())  # with len 261445
    return full[full[filter_].isin(sub)]  # Pretty expensive


def save_(file_, matrix, conflict=0, name='A'):
    """
    """
    if os.path.exists(file_):
        parts = file_.split('.')
        file_ = ''.join(parts[:-1]) + str(conflict) + '.' + ''.join(parts[-1])
        conflict += 1
        return save_(file_, matrix, conflict=conflict)
    else:
        try:
            savemat(file_, {name: matrix})
            print('Saved the matrix to %s' % file_)
        except IOError:
            print('Failed to save the matrix')


def gen_dicts(name_1, name_2, just_tech=True,
        store=pd.HDFStore('/Volumes/HDD/Users/tom/DataStorage/Patents/patents.h5')):
    """
    For use when looking up later.
    name_1 and name_2 are filenames for the pickles. One for # -> Z, second
    for inverse.
    """
    net = store['cites']
    if just_tech:
        tech = filter(net, get_tech_patents(store))  # Comes close to paging out.
        idx = pd.Series(np.union1d(tech['citing'].unique(),
            tech['cited'].unique()))
    else:
        raise NotImplemented
    d = idx.to_dict()                         # d : Z -> Patents
    inv_d = {v: k for k, v in d.iteritems()}  # inv_d : Patents -> Z
    with open(name_1, 'w') as f:
        dump(d, f, 2)
    with open(name_2, 'w') as f:
        dump(inv_d, f, 2)

def gen_sparse_matrix(save=True, mail=True,
        store=pd.HDFStore('/Volumes/HDD/Users/tom/DataStorage/Patents/patents.h5')):
    """
    Testing
    """
    start = datetime.now()
    net = store['cites']
    tech = filter(net, get_tech_patents(store))  # Comes close to paging out.

    idx = pd.Series(np.union1d(tech['citing'].unique(),
            tech['cited'].unique()))
    d = idx.to_dict()                        # d : Z -> Patents
    inv_d = {v: k for k, v in d.iteritems()}  # inv_d : Patents -> Z

    rows = []
    cols = []
    final = tech.index[-1]
    print(len(tech.index))
    for k in tech.index:
        i = inv_d[tech.ix[k]['citing']]
        j = inv_d[tech.ix[k]['cited']]
        rows.append(i)
        cols.append(j)
        if k % 10000 == 0:
            print(k / final)

    rows = np.array(rows)
    cols = np.array(cols)
    data = np.ones(len(tech))
    N = np.max([cols.max(), rows.max()])
    sp = sparse.coo_matrix((data, (rows, cols)), shape=(N + 1, N + 1))
    if save:
        try:
            save_(save, sp)
        except IOError:
            save_('/Users/tom/tom/DataStorage/Patents/sparse_out.mat',
                sp)
    if mail:
        try:
            time = str(datetime.now() - start)
            gmail.mail('thomas-augspurger@uiowa.edu', 'Results',
                time)
        except:
            print(str(datetime.now() - start))
    return sp
