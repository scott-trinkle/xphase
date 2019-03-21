import numpy as np
from .material import Material

# Get nominal n for water for E = 20 keV
H2O_n20 = Material('H2O').interp('n', E=20)

# Get nominal delta and beta for osmium
Os = Material('Os')
Os_d20 = Os.interp('delta', 20)
Os_b20 = Os.interp('beta', 20)


def default_sphere(shape=(256, 256, 256)):
    nx, ny, nz = shape
    x0, y0, z0 = np.array(shape) // 2
    r = 0.5 * np.mean((nx, ny, nz)) // 2

    x, y, z = np.meshgrid(np.arange(nx),
                          np.arange(ny),
                          np.arange(nz))

    mask = ((x - x0)**2 + (y - y0)**2 + (z - z0) ** 2 <= r**2)

    # background is air, n = 1 + 0j
    data = np.ones(shape, dtype=np.complex128)

    # sphere object is imbedded in cube of water
    data[ny // 10: 9 * ny // 10, nx // 10: 9 * nx // 10] = H2O_n20

    # sphere object is
    data.real[mask] = 1 - \
        np.random.normal(Os_d20, 0.05 * Os_d20, size=mask.sum())
    data.imag[mask] = np.random.normal(Os_b20, 0.05 * Os_b20, size=mask.sum())

    return data
