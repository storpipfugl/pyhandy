import unittest

from pyhandy import handy


EPSILON = 1e-6

class TestSocietyEvolution(unittest.TestCase):

    def test_equal_soft(self):
        """Basic test to confirm model runs
        """

        society = handy.create_society('egalitarian', 'soft')
        (time, commoner_population, elite_population, 
         nature, wealth, carrying_capacity) = society.evolve(1000)

        res = time[-1]
        exp_res = 1000
        self.assertEqual(res, exp_res,
            msg='Expected time to be {0} got: {1}'.format(exp_res, res))

        res = commoner_population[-1]
        exp_res = 74999.9812687
        delta = exp_res * EPSILON
        self.assertAlmostEqual(res, exp_res, delta=delta,
            msg='Expected commoner_population to be {0} got: {1}'.format(exp_res, res))

        res = elite_population[-1]
        exp_res = 0
        delta = exp_res * EPSILON
        self.assertAlmostEqual(res, exp_res, delta=delta,
            msg='Expected elite_population to be {0} got: {1}'.format(exp_res, res))
        
        res = nature[-1]
        exp_res = 49.9750124938
        delta = exp_res * EPSILON
        self.assertAlmostEqual(res, exp_res, delta=delta,
            msg='Expected nature to be {0} got: {1}'.format(exp_res, res))

        res = wealth[-1]
        exp_res = 249.999937562
        delta = exp_res * EPSILON
        self.assertAlmostEqual(res, exp_res, delta=delta,
            msg='Expected wealth to be {0} got: {1}'.format(exp_res, res))

        res = carrying_capacity[-1]
        exp_res = 75000.0
        delta = exp_res * EPSILON
        self.assertAlmostEqual(res, exp_res, delta=delta,
            msg='Expected carrying_capacity to be {0} got: {1}'.format(exp_res, res))
