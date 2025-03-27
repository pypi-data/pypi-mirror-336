import unittest
import num

class Tests(unittest.TestCase):
    def test_pgcd(self):
        self.assertEqual(num.pgcd(60,40),20)
        self.assertEqual(num.pgcd(50,15),5)

if __name__ == '__main__':
    unittest.main()
