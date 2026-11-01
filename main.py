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
    f = uwg_file if hasattr(uwg_file, "readline") else open(uwg_file)

    vertices = []
    number_of_vertices = int(f.readline())
    for i in range(1,int(number_of_vertices)+1):
        vertices.append(i)

    adjancancy_matrix = [[None for _ in range(number_of_vertices)] for _ in range(number_of_vertices)]
   

    number_of_edges = int(f.readline())

    if number_of_edges > ((number_of_vertices * (number_of_vertices-1))/2):
        raise NotValidInputError("Not valid input: The number of edges cannot exceed (n(n-1))/2")

    big_M = f.readline()
    big_M = int(big_M)

    rest_of_file = f.read()
    lines = rest_of_file.splitlines()
    if len(lines) != number_of_edges:
        raise NotValidInputError(
            "Not valid input: The number of edge lines must equal the number of edges specified"
        )

    counter = 0

    for line in lines:
        counter += 1

        elements = line.split()
        if len(elements) != 3:
            raise NotValidInputError(
                "Not valid input: Each edge line must contain exactly three values"
            )

        try:
            first_endpoint = int(elements[0])
            second_endpoint = int(elements[1])
            edge_weight = int(elements[2])
        except ValueError:
            raise NotValidInputError(
                "Not valid input: Edge endpoints and weight must be integers"
            )

        if not (1 <= first_endpoint <= number_of_vertices) or not (
            1 <= second_endpoint <= number_of_vertices):
            raise NotValidInputError(
                "Not valid input: Edge endpoints must be between 1 and the number of vertices"
            )

        if first_endpoint == second_endpoint:
            raise NotValidInputError(
                "Not valid input: An edge cannot connect a vertex to itself"
            )

        if edge_weight > int(big_M):
            raise NotValidInputError("Not valid input: An edge cannot have higher weight than M")
        
        elif edge_weight < 0:
                    raise NotValidInputError("Not valid input: An edge cannot be negative")

        first_vertex = first_endpoint - 1
        second_vertex = second_endpoint - 1

        if adjancancy_matrix[first_vertex][second_vertex] is not None:
            raise NotValidInputError(
                "Not valid input: An edge between these vertices is already present"
            )

        edge = (counter, edge_weight)
        adjancancy_matrix[first_vertex][second_vertex] = edge
        adjancancy_matrix[second_vertex][first_vertex] = edge

    return adjancancy_matrix, vertices, big_M

def make_tree(adjancancy_matrix, vertices, big_M):
    nodes = [Node(vertex) for vertex in vertices]

    for i in range(len(adjancancy_matrix)):
        for j in range(len(adjancancy_matrix)):
            if i == j:
                continue

            edge = adjancancy_matrix[i][j]
            if edge is not None:
                edge_index, edge_weight = edge
                nodes[i].children.append((nodes[j], edge_index, edge_weight))

        nodes[i].children.sort(key=lambda edge: abs(edge[2] - big_M // 2))

    return nodes[0]

def run_modified_DFS(root, adjancancy_matrix, vertices, current_path, big_M, B_min, path,
                     current_weight_sum, current_weight_complementary_sum, visited=None):

    if visited is None:
        visited = set()
    visited.add(root.number)

    if root.number == len(vertices):
        if max(current_weight_sum, current_weight_complementary_sum) < B_min:
            B_min = max(current_weight_sum, current_weight_complementary_sum)
            path = current_path.copy()
        return path, B_min


    for child, edge_index, edge_weight in root.children:
        if child.number in visited:
            continue

        new_weight_sum = current_weight_sum + edge_weight
        new_weight_complementary_sum = (big_M - edge_weight) + current_weight_complementary_sum
        new_b = max(new_weight_sum, new_weight_complementary_sum)

        if new_b < B_min:
            current_path.append(edge_index)
            visited.add(child.number)
            path, B_min = run_modified_DFS(child, adjancancy_matrix, vertices, current_path, big_M, B_min, path, new_weight_sum, new_weight_complementary_sum,visited)
            visited.remove(child.number)
            current_path.pop()

    return path, B_min

def print_path(path, b_min):
    if not path and b_min == float('inf'):
        print("NO")
        return
    
    for edge_id in path:
        print(edge_id)
    print(b_min)

def main():
    try:
        adjancancy_matrix, vertices, big_M = parse_input(sys.stdin)
    except NotValidInputError as e:
        print(e.message)
        sys.exit(1)

    root = make_tree(adjancancy_matrix, vertices, big_M)
    path, b_min = run_modified_DFS(
        root, adjancancy_matrix, vertices, [], big_M, float('inf'), [], 0, 0
    )
    print_path(path, b_min)

if __name__ == "__main__":
    main()

        

        
