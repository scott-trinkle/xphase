import numpy as np
import matplotlib.pyplot as plt
from .utils import E_to_lambda, log_interp
from ._ffast import lookup, load_ffast
from .constants import elemprops, N_A, re


class Material(object):
    def __init__(self, elem, rho=None, Ma=None):

        if type(elem) == int:
            name = lookup(elem)
        else:
            name = elem

        mat = load_ffast(elem)

        self.E = mat.E
        self.f2 = mat.f2
        self.Tot = mat.Tot
        self.lam = E_to_lambda(self.E)
        self.k = 2 * np.pi / self.lam

        # Water does not have f1
        try:
            self.f1 = mat.f1
        except AttributeError:
            self.f1 = 1

        # Initialize rho and Ma to nominal values for
        # water, osmium or uranium
        if (rho is None) & (name in elemprops.keys()):
            self.rho = elemprops[name][0]
        else:
            self.rho = rho
        if (Ma is None) & (name in elemprops.keys()):
            self.Ma = elemprops[name][1]
        else:
            self.Ma = Ma

        self.set_delta_beta()

        if name == 'H2O':
            # Sloppy for now, setting delta to value at 20 keV, based
            # on this paper:
            # https://journals.aps.org/pr/pdf/10.1103/PhysRev.40.156
            self.delta = np.ones_like(self.E) * 3.7e-10

        self.n = 1 - self.delta + 1j * self.beta

    def set_delta_beta(self, rho=None):
        if rho is None:
            rho = self.rho
        na = rho * N_A / self.Ma
        self.delta = na * re * (self.lam ** 2) / (2 * np.pi) * self.f1
        self.beta = na * re * (self.lam ** 2) / (2 * np.pi) * self.f2

    def plot(self, attr, title=None,
             show=True, save=False, fn=None):
        y = getattr(self, attr)

        fig, ax = plt.subplots()
        ax.loglog(self.E, y)
        ax.set_xlabel('E [keV]')
        ax.set_ylabel(attr)
        if title is None:
            title = attr
        ax.set_title(title)
        fig.tight_layout()
        if show:
            plt.show()
        if save:
            fig.savefig(fn)

    def interp(self, attr, E):
        y = getattr(self, attr)
        return log_interp(self.E, y, E)
