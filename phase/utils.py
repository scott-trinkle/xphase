import numpy as np
from scipy.interpolate import interp1d
from .constants import h, c


def E_to_lambda(E):
    '''
    Converts energy in keV to wavelength in cm

    Parameters
    _________
    E : int or float
        Energy in keV

    Returns
    _______
    lam : float
        Wavelength in cm
    '''
    lam = h * c / E
    return lam


def lambda_to_E(lam):
    E = h * c / lam
    return E


def log_interp(x, y, x_new, kind='linear'):
    '''
    Import model input, model output, new input, returns log-interpolated
    output
    '''

    with np.errstate(divide='ignore'):
        logx = np.log10(x)
        logy = np.log10(y)
    lin_interp = interp1d(logx, logy, kind=kind)

    def log_interp(z): return np.power(10.0, lin_interp(np.log10(z)))
    return log_interp(x_new)
