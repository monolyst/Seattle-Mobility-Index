import unittest


class BasketCalcTest(unittest.Testcase):

    def setUp(self):
        self.basket_calc = Basket

    def test_calculate_distance_API():
        def reader():
            # return a JSON string


    def test_basket_rank():
        # Check columns
        # Check ranks are integers
        # Check size of input and output match
        pass


    def test_create_basket():
        # Check that each blockgroup has a basket of 25 
        # Check that the count for each category matches basket
        # Check that every pair is unique
        pass

if __name__ == "__main__":
    unittest.main()

