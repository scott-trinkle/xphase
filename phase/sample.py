from .phantoms import default_sphere
from .vis import show_refindex_slice


class Sample(object):
    '''
    This class holds sample objects on L_2(C^3), described by
    the complex, 3D index of refraction
    '''

    def __init__(self, n=None, pix_size=1.2e-4):

        if n is not None:
            self.n = n
        else:
            self.n = default_sphere()

        self.shape = self.n.shape
        self.pix_size = pix_size
        self.zo = self.shape[-1] * self.pix_size

    def plot(self, z=None, log=False, show=True, save=False, fn=None):
        show_refindex_slice(self.n, z, log, show, save, fn)
