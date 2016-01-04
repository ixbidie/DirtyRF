import numpy as np
import cmath as cm
import math as m



# a simulation which is artificially degrading the quality of a signal via several real world RF impairments
class DirtyRF:
  # PHASE NOISE
  # sending time of a symbol in uS
  Ts            = 0
  
  # NON-LINEARITIES
  # the Input Intercept Points (IIP) measured for a certain oscillator. The number stands for the nth order of the IIP
  IIP3          = 0
  IIP5          = 0
  b2            = -0.15
  b3            = 0.05
  
  # IQ IMBALANCE
  # amplitude gain and phase error of one branch
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
  
  # non-linearities with polynominal representation
  # x - symbol to be distorted
  def nl(self, x):
    i = x.real
    q = x.imag
    xp = abs(x)
    phi = cm.phase(x) #cm.atan(q / i)
    
    xp2 = xp*xp
    xp3 = xp2*xp
    
    r_nl = xp + self.b2*xp2 + self.b3*xp3
    
    # e to cartesian
    i = r_nl * cm.cos(phi)
    q = r_nl * cm.sin(phi)
    
    #return i + q*1j
    return cm.rect(xp + self.b2*xp2 + self.b3*xp3, cm.phase(x))

  
  # phase noise
  # x - input symbol
  def pn(self, x):
    self._teta += np.random.normal(scale=self._derivationPn)
    return cm.rect(abs(x), cm.phase(x)+self._teta) #  * cm.exp(1j * self._teta)


  # iq imbalance
  # x - input symbol, must be complex!
  def iq(self, x):
    if not isinstance(x, complex):
      raise ValueError('input is not a complex number and therefore invalid.')
    amp_dist = self.alpha * x.imag
    i = x.real - amp_dist * np.sin(self.phi)
    q = amp_dist * np.cos(self.phi)
    return i + q * 1j
  

  # all in one imolementation
  def impairments(self, x):
    # iq 
    amp_dist = self.alpha * x.imag
    i = x.real - amp_dist * m.sin(self.phi)
    q = amp_dist * m.cos(self.phi)
    
    # conversion e notation
    r = m.sqrt(i*i + q*q)
    phi = m.atan2(q, i)
    
    # nl
    xp = r
    xp2 = xp*xp
    xp3 = xp2*xp
    
    # nl and pn
    self._teta += np.random.normal(scale=self._derivationPn)
    phi_pn = phi + self._teta
    r_nl = xp + self.b2*xp2 + self.b3*xp3
    
    # e to cartesian
    i = r_nl * m.cos(phi_pn)
    q = r_nl * m.sin(phi_pn)
    
    return i + q*1j