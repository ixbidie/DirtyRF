import numpy as np
import cmath as cm



# a simulation which is artificially degrading the quality of a signal via several real world RF impairments
class DirtyRF:
  # PHASE NOISE
  # sending time of a symbol in uS
  Ts            = 0
  
  # NON-LINEARITIES
  # the Input Intercept Points (IIP) measured for a certain oscillator. The number stands for the nth order of the IIP
  IIP3          = 0
  IIP5          = 0
  
  # IQ IMBALANCE
  # amplitude gain  and phase error of one branch
  alpha         = 0
  phi           = 0
  
  # INTERNAL variables
  _varPn        = 0
  _derivationPn = 0
  _teta         = 0
  
  # test
  def __init__(self, beta=1, IIP3=2.2, IIP5=1.4, alpha=1, phi=0, Ts=1e-6):
    self.Ts = Ts
    self.setBeta(beta)
    self.IIP3 = IIP3
    self.IIP5 = IIP5
    self.alpha = alpha
    self.phi = phi

  # sets the quality of the oscillatoer. It's the offset of f_c where the oscillator exhibits a gain of -3dB.
  def setBeta(self, beta):
    self._derivationPn = np.sqrt(4 * np.pi * beta * self.Ts)
  
  # non-linearities
  # x - symbol to be distorted
  def nl(self, x):
    b3 = -4.0 / (3.0*np.power(self.IIP3,2))
    b5 = 8.0 / (5.0*np.power(self.IIP5,4))
    return x*( 1 + b3*np.power(x,2) + b5*np.power(x,4) + 0.09*np.power(x,6))
  
  # phase noise
  # x - input symbol
  def pn(self, x):
    self._teta += np.random.normal(scale=self._derivationPn)
    return x * cm.exp(1j * self._teta)

  # iq imbalance
  # x - input symbol, must be complex!
  def iq(self, x):
    if not isinstance(x, complex):
      raise ValueError('input is not a complex number and therefore invalid.')
    tmp = self.alpha * x.imag
    i = x.real - tmp * np.sin(self.phi)
    q = tmp * np.cos(self.phi)
    return i + q * 1j




  


# ---------------------------------------
# OLD CODE (to be removed)

#def g_poly_ssa(self, A, p=1, A0=1):
    #IIP3 = np.sqrt(8/3) * A0
    #IIP5 = np.power(64/3.0 , 1/4.0) * A0
    #return g(A, IIP3, IIP5)

  #def g_poly_twta(self, A, xA=1, kA=0.25):
    #IIP3 = np.sqrt(4.0 / 3.0 / kA )
    #IIP5 = np.power(8 / 5 / np.power(kA,2) , 1.0/4)
    #return g(A, IIP3, IIP5)