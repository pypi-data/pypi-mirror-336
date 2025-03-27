import unittest
import math
import sys
import limit


class Tests(unittest.TestCase):
	def test_sommation(self):
		identity = lambda x:x
		self.assertEqual(limit.sum(identity,-100,100),0)
		self.assertEqual(limit.sum(identity,0,100),5050)
		self.assertEqual(limit.sum(abs,-100,100),5050*2)
		self.assertEqual(limit.sum(abs,0,100),5050)
	def test_integral(self):
		self.assertGreater(limit.integral(math.sin,-1,1),-0.01) 
		self.assertGreater(0.01,limit.integral(math.sin,-1,1)) 
	def test_fourier_transform(self):
		sinw = lambda x:math.sin(2*math.pi*x)
		self.assertGreater(abs(limit.fourier_transform(sinw)(1)),1000)


if __name__ == '__main__':
    unittest.main()
