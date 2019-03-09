import numpy as np
import pandas as pd
from urllib.parse import urlencode
import pkg_resources
data_path = pkg_resources.resource_filename('phase', 'data/')


def lookup(Z):
    elems = ['H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne', 'Na', 'Mg',
             'Al', 'Si', 'P', 'S', 'Cl', 'Ar', 'K', 'Ca', 'Sc', 'Ti', 'V',
             'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se',
             'Br', 'Kr', 'Rb', 'Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh',
             'Pd', 'Ag', 'Cd', 'In', 'Sn', 'Sb', 'Te', 'I', 'Xe', 'Cs', 'Ba',
             'La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho',
             'Er', 'Tm', 'Yb', 'Lu', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt',
             'Au', 'Hg', 'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn', 'Fr', 'Ra', 'Ac',
             'Th', 'Pa', 'U']

    return elems[Z-1]


def get_NIST_data(mat, lower=0, upper=100):
    '''
    Scrapes mass attenuation data for an element or material
    from the NIST X-ray Form Factor, Attenuation and Scattering
    Tables (FFAST)

    https://physics.nist.gov/PhysRefData/FFast/html/form.html

    Parameters
    __________
    mat : str or int
        Atomic number (Z) if int, material name if str
    lower : float or int
        Lower bound on energy range
    upper : float or int
        Upper bound on energy range (Note, FFAST only goes to 433 keV)

    Returns
    _______
    data : pd.DataFrame
        FFAST data for 'mat'
    '''

    baseurl = 'https://physics.nist.gov/cgi-bin/ffast/ffast.pl?'

    # Parses 'mat' input and sets Z and Formula paramters accordingly
    Z, Formula = (str(mat), '') if type(mat) == int else ('', str(mat))

    params = {'Z': Z,
              'Formula': Formula,
              'gtype': '4',  # Indicates mass attenuation tables
              'range': 'S',
              'lower': str(lower),
              'upper': str(upper),
              'density': '',
              'frames': 'no',
              'htmltable': '1'}

    # Returns a list of html tables as a pandas dataframe.
    # For these pages, there is only one html table, so we return the
    # first one and save as ndarray with ".values"
    data = pd.read_html(baseurl + urlencode(params), header=0)[0]
    data.columns = fix_header(data.columns)
    data = fix_E_column(data)

    return data


def fix_header(cols):
    new_cols = []
    for col in cols:
        if col == 'E keV':
            new_cols.append('E')
        if col == 'f1\xa0e atom-1':
            new_cols.append('f1')
        if col == 'f2\xa0e atom-1':
            new_cols.append('f2')
        if col == '[]Photoelectriccm2\xa0g-1':
            new_cols.append('Ph')
        if col == '[/]  Coh+inccm2\xa0g-1':
            new_cols.append('Sc')
        if col == '[]Totalcm2\xa0g-1':
            new_cols.append('Tot')
        if col == '[]K\xa0cm2\xa0g-1':
            new_cols.append('K')
        if col == 'nm':
            new_cols.append('lam')
    return new_cols


def fix_E_column(data):
    # f1 values are mistakenly concatenated with E for some elements

    try:
        # creates a mask of faulty rows
        cond = [len(val.split()) == 2 for val in data.E]
    except AttributeError:  # returns attribute error if there is no problem
        return data

    # Creates "correct" copy of E, f1 for problem rows, zeros otherwise
    nrows, ncols = data.shape
    fixed = np.zeros((nrows, 2))
    fixed[cond] = [val.split() for val in data[cond].E]

    # Copy values over from right to left up until f1
    for i in range(1, ncols-1):
        data.iloc[:, -i] = np.where(cond,
                                    data.iloc[:, -i-1], data.iloc[:, -i])
    # Copy f1 values from fixed to f1 column
    data.iloc[:, -ncols +
              1] = np.where(cond, fixed[:, 1], data.iloc[:, -ncols+1])

    # Set E values to correct values from fixed
    data.iloc[:, -ncols] = np.where(cond,
                                    fixed[:, 0], data.iloc[:, -ncols])

    # E column has mixed dtype, fix that here
    data.iloc[:, -ncols] = data.iloc[:, -ncols].astype(np.float64)

    return data


def update_all():
    Z = range(1, 93)

    for i in Z:
        print('Updating {}, Z = {}'.format(lookup(i), i))
        get_NIST_data(
            i, lower=0, upper=500).to_pickle('data/' + lookup(i) + '.pkl')

    print('Updating H2O')
    get_NIST_data('H2O', lower=0, upper=500).to_pickle('data/H2O.pkl')


def load_ffast(elem):
    '''
    Parameters
    __________
    elem : str or int
        Z or element symbol

    Returns
    _______
    data : pd.DataFrame
        ffast data for elem

    '''
    elems = [lookup(z) for z in range(1, 93)] + ['H2O']
    if type(elem) == int:
        elem = lookup(elem)
    if elem not in elems:
        print('{} is not in the database'.format(elem))
        return
    else:
        data = pd.read_pickle(data_path + '{}.pkl'.format(elem))
        return data
