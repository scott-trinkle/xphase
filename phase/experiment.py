import numpy as np
from .utils import E_to_lambda
from .sample import Sample


class Experiment(object):
    '''
    An Experiment object holds all relevant information about
    a given x-ray imaging experiment, including the sample being
    imaged, and the complex amplitude and wavelength of the incoming
    radiation.
    '''

    def __init__(self, sample=None, lam=E_to_lambda(20), psi0=None):
        '''
        Parameters
        __________
        sample : Sample
            The sample being imaged, defined by the 3D
            complex index of refraction, n.
        lam : float
            The wavelength in cm of the incoming wave-field
        psi0 : function
            Function yielding the complex amplitude of the incoming wave-field
            at a given position z on the optic axis
        '''

        if sample is not None:
            self.sample = sample
        else:
            self.sample = Sample()

        self.beam_shape = self.sample.shape[:2]

        self.lam = lam
        self.k = 2 * np.pi / self.lam

        if psi0 is not None:
            self.psi0 = psi0
        else:
            # defaults to plane wave with intensity = 1
            self.psi0 = lambda z: np.exp(
                1j * self.k * z)*np.ones(self.beam_shape)
