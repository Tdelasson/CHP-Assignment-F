import sys

class NotValidInputError(Exception):
    """Exception raised for non-valid uwg files."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class Node:
    def __init__(self, number):
        self.number = number
        self.children = []
        self.balanced_weight = 0

def parse_input(uwg_file):
    f = open(uwg_file)

    vertices = []
    number_of_vertices = int(f.readline())
    for i in range(1,int(number_of_vertices)+1):
        vertices.append(i)

     # We just use the upper right triangle of the matrix. [rows][cols]
    adjancancy_matrix = [[float('inf') for _ in range(number_of_vertices)] for _ in range(number_of_vertices)] 
   

    number_of_edges = int(f.readline())

    if number_of_edges > ((number_of_vertices * (number_of_vertices-1))/2):
        raise NotValidInputError("Not valid input: The number of edges cannot exceed (n(n-1))/2")

    big_M = f.readline()
    big_M = int(big_M)

    rest_of_file = f.read()
    lines = rest_of_file.splitlines()
    counter = 0

    # While end of file is not reached loop through the edges
    for line in lines:
        counter += 1

        if counter > number_of_edges:
            raise NotValidInputError("Not valid input: The number of edges in the file is less than the number of edges specified")

        elements = line.split() # split based on blank space

        if int(elements[0]) > number_of_vertices or int(elements[1]) > number_of_vertices:
            raise NotValidInputError("Not valid input: Edges cannot be connected to a higher vertex number than there are verteces")

        if int(elements[2]) > int(big_M):
            raise NotValidInputError("Not valid input: An edge cannot have higher weight than M")

        adjancancy_matrix[int(elements[0])-1][int(elements[1])-1] = int(elements[2])

    # print("Number of vertices: ", number_of_vertices)
    # print("Number of edges: ", number_of_edges)
    # print("Big M: ", big_M)
    # print("Vertices: ", vertices)
    # print("Adjacancy matrix: ", adjancancy_matrix)
    return adjancancy_matrix, vertices, big_M

def make_tree(adjancancy_matrix, vertices):
    nodes = [Node(vertex) for vertex in vertices]

    for i in range(len(adjancancy_matrix)):
        for j in range(len(adjancancy_matrix)):
            if i == j:
                continue

            if adjancancy_matrix[i][j] != float('inf'):
                nodes[i].children.append(nodes[j])

    return nodes[0]

def print_tree(root):
    if root is None:
        return
    #print(root.number)
    for child in root.children:
        print_tree(child)

def run_modified_DFS(root, adjancancy_matrix, vertices, current_path, big_M, B_min, path,
                     current_weight_sum, current_weight_complementary_sum, visited=None):
    #print("Visiting node: ", root.number)

    if visited is None:
        visited = set()
    visited.add(root.number)

    if root.number == len(vertices):
        if max(current_weight_sum, current_weight_complementary_sum) < B_min:
            B_min = max(current_weight_sum, current_weight_complementary_sum)
            path = current_path.copy()
            #print("New best path found: ", path)
            #print("New best B: ", B_min)
        return path, B_min


    for child in root.children:
        if child.number in visited:
            continue

        edge_weight = adjancancy_matrix[root.number - 1][child.number - 1]
        if edge_weight == float('inf'):
            edge_weight = adjancancy_matrix[child.number - 1][root.number - 1]
        edge_weight_balanced = abs(edge_weight - round(big_M/2))
        child.balanced_weight = edge_weight_balanced

    root.children.sort(key=lambda x: x.balanced_weight)
    #print("Children sorted by balanced edge weights: ", [child.number for child in root.children])
    
    for child in root.children:
        if child.number in visited:
            continue

        edge_weight = adjancancy_matrix[root.number - 1][child.number - 1]
        if edge_weight == float('inf'):
            edge_weight = adjancancy_matrix[child.number - 1][root.number - 1]
        new_weight_sum = current_weight_sum + edge_weight
        new_weight_complementary_sum = (big_M - edge_weight) + current_weight_complementary_sum
        new_b = max(new_weight_sum, new_weight_complementary_sum)

        if new_b < B_min:
            current_path.append(child.number)
            #print("Current path: ", current_path)
            #print("Current B: ", new_b)
            visited.add(child.number)
            path, B_min = run_modified_DFS(child, adjancancy_matrix, vertices, current_path, big_M, B_min, path, new_weight_sum, new_weight_complementary_sum)
            visited.remove(child.number)
            current_path.pop()

    return path, B_min

def print_path(path, b_min):
    if not path:
        print("NO")
        return
    
    for edge_weight in path:
        print(edge_weight)
    print(b_min)

def main():
    uwg_files = ["test01.uwg", "test02.uwg", "test03.uwg", "test04.uwg", "test05.uwg",
                 "test06.uwg", "test07.uwg", "test08.uwg", "test09.uwg", "test10.uwg",
                 "test11.uwg", "test12.uwg", "test13.uwg", "test14.uwg"
                 ]
    for uwg_file in uwg_files:
        uwg_file = uwg_file
        try:
            adjancancy_matrix, vertices, big_M = parse_input(uwg_file)
        except NotValidInputError as e:
            print(e.message)
            sys.exit(1)

        #print("Parsing completed successfully.")

        root = make_tree(adjancancy_matrix, vertices)
        #print("Printing tree:")
        #print_tree(root)

        path, b_min = run_modified_DFS(root, adjancancy_matrix, vertices, [], round(big_M), float('inf'), [], 0, 0)

        print_path(path, b_min)
        print("--------------------------------------------------")

if __name__ == "__main__":
    main()

        

        
