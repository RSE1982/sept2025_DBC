'''
    Helper functions for Python Challenge-052
'''


def add_integers(list_integers):
    '''
        Function to add integers in a list
    '''
    total = 0
    for x in list_integers:
        total += x
    return total


def multiply_intergers(list_integers):
    '''
        Function to multiply integers in a list
    '''
    total = list_integers[0]
    for x in list_integers:
        # As it is a tuple you can use the in keyword to iterate
        total = total * x
    return total
