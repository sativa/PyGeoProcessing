# Program that computes the real roots of a quadratic equation.
# Illustrates use of the numpy library for numerical calculations.
# Python Data Analysis
# Author: Baburao Kamble


import numpy  # Makes the numpy library available.

def myfunction():
    print("This program finds the real solutions to a quadratic")
    #a, b, c = eval(input("Please enter the coefficients (a, b, c): "))
    a=3
    b=4
    c=-1
    discRoot = numpy.sqrt(b * b - 4 * a * c)
    root1 = (-b + discRoot) / (2 * a)
    root2 = (-b - discRoot) / (2 * a)
    print("The solutions are:", root1, root2 )
myfunction()
