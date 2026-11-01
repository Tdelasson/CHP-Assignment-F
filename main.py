import sys

class NotValidInputError(Exception):
    """Exception raised for non-valid uwg files."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class Node:
    def __init__(self, data):
        self.data = data
        self.children = []

def parse_input(uwg_file):
    f = open(uwg_file)

    vertices = []
    number_of_vertices = int(f.readline())
    for i in range(1,int(number_of_vertices)):
        vertices.append("v" + str(i))

    adjancancy_matrix = [[0 for _ in range(number_of_vertices)] for _ in range(number_of_vertices)] # We just use the upper right triangle of the matrix



    number_of_edges = int(f.readline())

    vertices = {}

    if number_of_edges > ((number_of_vertices * (number_of_vertices-1))/2):
        raise NotValidInputError("Not valid input: The number of edges cannot exceed (n(n-1))/2")

    big_M = f.readline()

    rest_of_file = f.read()
    print("ROF: ", rest_of_file)
    lines = rest_of_file.splitlines()

    # While end of file is not reached loop through the edges
    for line in lines:
        elements = line.split() # split based on blank space
        print(elements)

        if int(elements[0]) > number_of_vertices or int(elements[1]) > number_of_vertices:
            raise NotValidInputError("Not valid input: Edges cannot be connected to a higher vertex number than there are verteces")

        if int(elements[2]) > int(big_M):
            raise NotValidInputError("Not valid input: An edge cannot have higher weight than M")

        adjancancy_matrix[int(elements[0])-1][int(elements[1])-1] = int(elements[2])

    print(adjancancy_matrix)

uwg_file = "test01.uwg"
parse_input(uwg_file)

        

        



