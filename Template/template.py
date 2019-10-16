#insert your imports here
import random
"""
Please Read ALL the comments in this document before you write your own classs.

Naming Conventions for Classes: Class names should not be wordy but descriptive and brief.
                                Multiple words should be one line and in CamelCase ie:BasicArithmeticOperations
Naming Conventions for Functions: Function names should be descriptive.
                                Multiple words should be separated by an '_' as seen below.
                                Format should be (verb_noun) ie: find_sum()

TIP: Make sure you place comments below each function declaration. Try to write your code
        as elegant as possible.

"""
class ArithmeticOperations:
    """
    ***This is the where you should write a brief description of your class***

    The ArithmeticOperations Class choses sets x and y to two random variables. It finds the sum,
    the product, and the remainder of these two numbers. This python class will be used in conjunction
    with the python DAG, template, located in the template_dag.py file.

    """
    def __init__(self):
        """
        We initialize the class by declaring two different variables, x and y, and set them to random numbers.
        """
        self.x, self.y  = random.randint(1,20), random.randint(1,50)
        print("This is the value of x: {} and y: {}".format(self.x, self.y))

    def find_sum(self):
        """
        This function returns the sum of x and y.
        """
        return self.x + self.y

    def print_sum(self):
        """
        This function calls on function find_sum() to print the sum of x and y.
        """
        print("{} + {} = {}".format(self.x, self.y, self.find_sum()))

    def find_product(self):
        """
        This function finds the product of x and y.
        """
        return self.x * self.y

    def print_product(self):
        """
        This function calls on the function find_product() to print the product of
        x and y.
        """
        print("{} * {} = {}".format(self.x, self.y, self.find_product()))

    def find_remainder(self):
        """
        This function checks to see which of the two variables is larger, then calculates the modulus
        in the format remainder = a mod n where a >= n. It then returns three values, the remainder,
        a, and n.
        """
        return (self.x % self.y, self.x, self.y) if self.x > self.y else (self.y % self.x, self.y, self.x)

    def print_remainder(self):
        """
        This function calls on the function find_remainder() to print in this format: a mod n = remainder,
        where a >= n.
        """
        remainder, a, n = self.find_remainder()
        print("{} mod {} = {}".format(a, n, remainder))

