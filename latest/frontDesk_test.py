__author__ = 'Sarbartha SJB Rana'
import unittest
import sys, os, datetime
sys.path.append('../')
import time
from numpy import *
import csv
from sys import exit
from frontDesk import *


class test_checkin(unittest.TestCase):
    def setUp(self):
        print
        print 'Start test:'
        print '================================================'

    def test_check_in(self):
        print 'Creating customer'
        checkin = '555','2015,12,01,10,30','2015,12,14,10,30'
        print 'customer created successfully.'
        print

    def test_check_in_attribute_value(self):
        print 'checking value'
        checkin = '555','2015,12,01,10,30','2015,12,14,10,30'
        self.assertEqual('555', '555')
        self.assertEqual('2015,12,01,10,30', '2015,12,01,10,30', msg='test successful')
        self.assertEqual('2015,12,14,10,30', '2015,12,14,10,30', msg='test successful')

# suite = (unittest.TestCase()
# .loadTestsFromTestCase(test_checkin)
# unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == '__main__':
    unittest.main()
