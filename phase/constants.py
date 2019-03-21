'''
Physical constants

Note: I am keeping all energy units in keV, and
all length units in cm
'''

# Planck's constant
h = 4.135667662e-15  # eV, https://en.wikipedia.org/wiki/Planck_constant
h *= 1e-3  # keV

# Speed of light in vacuum
c = 299792458  # m/s, https://en.wikipedia.org/wiki/Speed_of_light
c *= 100  # cm / s

# Avogadro Constant
N_A = 6.022140857e23  # mol^-1, https://en.wikipedia.org/wiki/Avogadro_constant

# Classical electron radius
re = 2.8179403227e-15  # m, https://en.wikipedia.org/wiki/Classical_electron_radius
re *= 100  # cm

# Density (g/cc) and molar mass (g/mol) for useful elements
elemprops = {'H2O': [1.0, 18.015],
             'U': [19.1, 238.02891],
             'Os': [22.59, 190.23]}
