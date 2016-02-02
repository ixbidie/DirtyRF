from myhdl import *
import unittest
from unittest import TestCase


def Inc(count, enable, clk, reset, n):
  """ Incrementer with enable and reset abillities 
  
  count -- output
  enable -- control input, increment when 1
  clk -- clock, increments on posedge
  reset -- async reset input
  n -- counter max value
  """
  
  @always_seq(clk.posedge, reset=reset)
  def incLogic():
    if enable:
      count.next = (count + 1) % n
  
  return incLogic



########################################################
#                                                      #
#                      TESTS                           #
#                                                      #
########################################################

class TestIncremeter(TestCase):
  def testOverflow(self):
    """ Check that after reaching the maximum value starting at 0 again """
    
    def test(count, enable, clk, reset, width):
      count.next = 2**width-1
      enable.next = True
      for i in range(2):
        yield clk.posedge
      enable.next = False
      self.assertEqual(int(count), 0)
      raise StopSimulation
    
    @always(delay(10))
    def clkGen():
      clk.next = not clk
    
    m = 8
    clk = Signal(bool(0))
    reset = ResetSignal(0, active=1, async=True)
    count = Signal(modbv(0)[m:])
    enable = Signal(bool(0))
    
    inst_inc = Inc(count, enable, clk, reset, 2**m) #toVHDL(Inc, count, enable, clk, reset, 2**m)
    inst_test = test(count, enable, clk, reset, m)
    sim = Simulation(clkGen, inst_inc, inst_test)
    sim.run(quiet=1)
  
  
  
  def testReset(self):
    """ Resetting should reset the counter """
    
    def test(count, enable, clk, reset, width):
      count.next = 2**width/2
      reset.next = 1
      enable.next = True
      for i in range(5):
        yield clk.posedge
      self.assertEqual(int(count), 0)
      raise StopSimulation
      
    @always(delay(10))
    def clkGen():
      clk.next = not clk
    
    m = 8
    clk = Signal(bool(0))
    reset = ResetSignal(0, active=1, async=True)
    count = Signal(modbv(0)[m:])
    enable = Signal(bool(0))
    
    inst_inc = Inc(count, enable, clk, reset, 2**m)
    inst_test = test(count, enable, clk, reset, m)
    sim = Simulation(clkGen, inst_inc, inst_test)
    sim.run(quiet=1)
  
  
  def testEnable(self):
    """ If the enable bit is low, a clock change should not change the counter value """

    def test(count, enable, clk, reset):
      count.next = 0
      enable.next = True
      for i in range(2):
        yield clk.posedge
      self.assertEqual(int(count), 1)
      
      enable.next = False
      yield clk.posedge
      count.next = 0
      yield clk.posedge
      self.assertEqual(int(count), 0)
      raise StopSimulation
    

    @always(delay(10))
    def clkGen():
      clk.next = not clk

    
    m = 8
    clk = Signal(bool(0))
    reset = ResetSignal(0, active=1, async=True)
    count = Signal(modbv(0)[m:])
    enable = Signal(bool(0))
    
    inst_inc = Inc(count, enable, clk, reset, 2**m)
    inst_test = test(count, enable, clk, reset)
    sim = Simulation(clkGen, inst_inc, inst_test)
    sim.run(quiet=1)


if __name__ == "__main__":
  unittest.main()

