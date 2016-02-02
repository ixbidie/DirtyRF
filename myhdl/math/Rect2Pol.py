from myhdl import *
import unittest
from unittest import TestCase
import cmath as cm
from math import *

t_State = enum("WAITING", "CALCULATING")
CYCLECOUNT_ITERATION = 2.0

def Rect2Pol_cordic(iReal, iImag, oRadius, oPhase, cycle_constraint, iStart, oDone, clk, reset):
  """
  Cordic based complex number converter from rect to polar with pipelining support
  
  iReal - real value
  iImag - imaginary value
  oRadius - output radius, make sure it's bitwidth is at least 1 (pytagoras)
  oPhase - output Phase, ranging from -pi to pi and is upscaled to 2^(input bitwidth)
  cycle_constraint - maximum cycles this algorithm is allowed to block, doesn't change the delay of 2^(input bitwidth + 1) which is constant
  start - starts the calculation
  done - indicates wether the algorithm finished
  clk - input clock
  reset - reset signal
  """
  
  W = len(iReal)

  # nr of iterations equals nr of significant input bits
  N = W-1
  
  # scaling factor corresponds to the nr of bits after the point
  M = 2**(W-2)
  
  # tuple with elementary angles
  alpha = tuple([int(round(M*atan(2**(-i)))) for i in range(N)])

  @instance
  def processor():
    # iterative cordic processor
    limit = 2**(len(iReal)+1)
    x = intbv(0, min=-limit, max=limit)
    y = intbv(0, min=-limit, max=limit)
    z = intbv(0, min=-limit, max=limit)
    dx = intbv(0, min=iReal.min, max=iReal.max)
    dy = intbv(0, min=iReal.min, max=iReal.max)
    dz = intbv(0, min=iReal.min, max=iReal.max)
    i = intbv(0, min=0, max=N)
    state = t_State.WAITING

    while True:
      yield clk.posedge, reset.posedge

      if reset:
        state = t_State.WAITING
        oDone.next = False
        x[:] = 0
        x[:] = 0
        z[:] = 0
        i[:] = 0

      else:
        if state == t_State.WAITING:
          if iStart:
            #if iReal < 0:
              #x[:] = -iReal
              ##z[:] = int(20000*pi)
              
            #else:
            x[:] = iReal
            y[:] = iImag
            z[:] = 0
            i[:] = 0
              
            oDone.next = False
            state = t_State.CALCULATING

        elif state == t_State.CALCULATING:
          # shifting performs the 2**(-i) operation
          dx[:] = x >> i
          dy[:] = y >> i
          dz[:] = alpha[int(i)]
          if (y < 0):
            #print "dy: %d" % dy
            x[:] -= dy
            y[:] += dx
            z[:] -= dz
          else:
              x[:] += dy
              y[:] -= dx
              z[:] += dz
          if i == N-1:
            oRadius.next = x
            oPhase.next = z
            state = t_State.WAITING
            oDone.next = True
          else:
            i += 1

  return processor


########################################################
#                                                      #
#                      TESTS                           #
#                                                      #
########################################################

class TestRect2PolConverter(TestCase):
  def testQuadrants(self):
    """ Does it compute all angles right? Are the signs ok? """
    
    # maximal Error
    dmax = 5
    
    # input/output width
    m = 16
    
    limit = 2**m
    
    # signals
    real = Signal(intbv(0, min=-limit, max=limit))
    imag = Signal(intbv(0, min=-limit, max=limit))
    radius = Signal(intbv(0, min=-limit, max=int(sqrt(2)*limit)))
    phase = Signal(intbv(0, min=-limit, max=limit))
    start = Signal(bool(False))
    done = Signal(bool(False))
    clk = Signal(bool(0))
    reset = ResetSignal(0, active=1, async=True)
    
    # test values
    #potencies = (12, 14) # multiplies the values for real and imag with these potencies to test high values as well
    values = []
    rad = [2**15-1, -2**15-1]
    
    for r in rad:
      for i in range(9):
        values.append(cm.rect(r, pi/2 - i*pi/8))
    
  
    # actual test
    def test(real, imag, radius, phase, clk, start, done):
      for val in values:
        yield clk.negedge
        rt = int(round(val.real))
        it = int(round(val.imag))
        real.next = rt
        imag.next = it
        ref = cm.polar(rt + it*1j)
        start.next = True
        yield clk.negedge
        start.next = False
        yield done.posedge
        print "%d: rect(%d, %dj), r = %d, phi = %.2f, r_ref = %d, phi_ref = %.2f" % (now(), rt, it, int(radius*0.60725), (int(phase)/2.0**(m-1)/pi), int(round(ref[0])), ref[1]/pi)
        #assert abs(ref[0] - radius) < dmax
        #assert abs(ref[1] - phase) < dmax
      raise StopSimulation
      
    #def polar2pi(rectVal):
      #polar = cm.polar(rectVal[0] + rectVal[1]*1j)
      #radius = polar[0]
      #phase = polar[1]
      #if phase < 0:
        #p = 2*cm.pi + phase
      #else:
        #p = phase
      #return (radius, p)
    
    # instances
    dut = Rect2Pol_cordic(iReal=real, iImag=imag, oRadius=radius, oPhase=phase, cycle_constraint=32, clk=clk, iStart=start, oDone=done, reset=reset)
    inst_test = test(real, imag, radius, phase, clk, start, done)
    
    # clock generator
    @always(delay(1))
    def clkGen():
      clk.next = not clk
      
    sim = Simulation(clkGen, dut, inst_test)
    sim.run(quiet=1)
    
    
if __name__ == "__main__":
  unittest.main()

  