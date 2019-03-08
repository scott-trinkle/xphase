import numpy as np
import matplotlib.pyplot as plt

n = 100
deltas = np.linspace(0, 2000, n)  # mm
lam = (6e-11) * 1000  # mm
h = 1.5

Nfs = (h**2) / (lam * deltas)

# Near: Nf >> 1
# Intermediate Nf ~ 1
# Far: Nf << 1

fig, ax = plt.subplots(1, 1)

ax.plot(deltas / 10, Nfs, 'k')
ax.set_xlabel(r'$\Delta$ [cm]')
ax.set_ylabel('$N_F$')
ax.ticklabel_format(style='plain', axis='y',
                    scilimits=(0, 0), useMathText=True)
fig.tight_layout()
fig.savefig('fresnelnum.pdf')
