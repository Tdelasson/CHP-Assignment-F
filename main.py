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
    for i in range(1,int(number_of_vertices)+1):
        vertices.append("v" + str(i))

     # We just use the upper right triangle of the matrix. [rows][cols]
    adjancancy_matrix = [[0 for _ in range(number_of_vertices)] for _ in range(number_of_vertices)] 
   

    number_of_edges = int(f.readline())

    if number_of_edges > ((number_of_vertices * (number_of_vertices-1))/2):
        raise NotValidInputError("Not valid input: The number of edges cannot exceed (n(n-1))/2")

    big_M = f.readline()

    rest_of_file = f.read()
    lines = rest_of_file.splitlines()

    # While end of file is not reached loop through the edges
    for line in lines:
        elements = line.split() # split based on blank space

        if int(elements[0]) > number_of_vertices or int(elements[1]) > number_of_vertices:
            raise NotValidInputError("Not valid input: Edges cannot be connected to a higher vertex number than there are verteces")

        if int(elements[2]) > int(big_M):
            raise NotValidInputError("Not valid input: An edge cannot have higher weight than M")

        adjancancy_matrix[int(elements[0])-1][int(elements[1])-1] = int(elements[2])

    print("Number of vertices: ", number_of_vertices)
    print("Number of edges: ", number_of_edges)
    print("Big M: ", big_M)
    print("Vertices: ", vertices)
    print("Adjacancy matrix: ", adjancancy_matrix)
    return adjancancy_matrix, vertices, big_M

def make_tree(adjancancy_matrix, vertices):
    root = Node(vertices[0])
    for i in range(len(adjancancy_matrix)):
        for j in range(i+1, len(adjancancy_matrix)):
            if adjancancy_matrix[i][j] != 0:
                child_node = Node(vertices[j])
                root.children.append(child_node)
    return root

def print_tree(root):
    if root is None:
        return
    print(root.data)
    for child in root.children:
        print_tree(child)

def main():
    uwg_file = "test01.uwg"
    try:
        adjancancy_matrix, vertices, big_M = parse_input(uwg_file)
    except NotValidInputError as e:
        print(e.message)
        sys.exit(1)

    print("Parsing completed successfully.")

    root = make_tree(adjancancy_matrix, vertices)
    print("Printing tree:")
    print_tree(root)

if __name__ == "__main__":
    main()

        

        



