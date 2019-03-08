import numpy as np
import pandas as pd
import ffastpy as ff
import matplotlib.pyplot as plt


def set_delta_beta(elem):
    Na = 6.022e23  # num/mol
    re = 2.8179403227e-15  # m

    elem.na = elem.rho * Na / elem.Ma
    elem['delta'] = elem.na * re * (elem.lam * 1e-9)**2 * elem.f1 / (2*np.pi)
    elem['beta'] = elem.na * re * (elem.lam * 1e-9)**2 * elem.f2 / (2*np.pi)


Os = ff.load_data('Os')
U = ff.load_data('U')

Os.rho = 22.59 * 100**3  # g / m3
Os.Ma = 190.23  # g / mol
U.rho = 19.1 * 100**3  # g / m3
U.Ma = 238.02891  # g / mol

set_delta_beta(Os)
set_delta_beta(U)

fig3, ax3 = plt.subplots(1, 1)

ax3.semilogy(Os.E, Os.delta, label=r'$\delta_{Os}$')
ax3.semilogy(Os.E, Os.beta, ':', label=r'$\beta_{Os}$', color='C0')

ax3.semilogy(U.E, U.delta, label=r'$\delta_U$')
ax3.semilogy(U.E, U.beta, ':', label=r'$\beta_U$', color='C1')

ax3.legend()
ax3.set_xlabel('Energy [keV]')
ax3.set_title(r'n = 1 - $\delta$ + $i\beta$')
ax3.set_xlim([0, 30])
fig3.tight_layout()

fig3.savefig('refindex.pdf')
