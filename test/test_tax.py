import sys
sys.path.append('../module/')

import unittest
from dir.cart import Product


class TestProductTaxMethod(unittest.TestCase):
    """
    Test unit to check whether the calculation of taxes is made 
    with the appropriate rounding.
    """
    def test_right_tax(self):
        # product in cart 1 
        p1 = Product(label='p1', group='books', count=1, price=12.49, imported=False)
        p2 = Product(label='p2', group='default', count=1, price=14.99, imported=False)
        p3 = Product(label='p3', group='food', count=1, price=0.85, imported=False)

        # product in cart 2 
        p4 = Product(label='p4', group='food', count=1, price=10.00, imported=True)
        p5 = Product(label='p5', group='default', count=1, price=47.50, imported=True)

        # product in cart 3 
        p6 = Product(label='p6', group='default', count=1, price=27.99, imported=True)
        p7 = Product(label='p7', group='default', count=1, price=18.99, imported=False)
        p8 = Product(label='p8', group='medical', count=1, price=9.75, imported=False)
        p9 = Product(label='p9', group='food', count=1, price=11.25, imported=True)

        self.assertEqual(p1.get_tax(), 0)
        self.assertEqual(p2.get_tax(), 1.50)
        self.assertEqual(p3.get_tax(), 0)
        self.assertEqual(p4.get_tax(), 0.5)
        
        # Round 7.125 led me to correct the calculation.
        self.assertEqual(p5.get_tax(), 7.15)
        self.assertNotEqual(p5.get_tax(), 7.12)

        self.assertEqual(p6.get_tax(), 4.20)
        self.assertEqual(p7.get_tax(), 1.9)
        self.assertEqual(p8.get_tax(), 0)
        self.assertEqual(p9.get_tax(), 0.60)

if __name__ == '__main__':
    unittest.main()