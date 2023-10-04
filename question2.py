import matplotlib.pyplot as plt
import random

class Vertex:
    def __init__(self, n):
        self.name = n
        self.label = 0
        self.neighbours = list()

    def add_neighbour(self, vertex):
        if vertex not in self.neighbours:
            self.neighbours.append(vertex)


class Graph:
    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex):
        if isinstance(vertex, Vertex) and vertex.name not in self.vertices:
            self.vertices[vertex.name] = vertex
            return True
        else:
            return False


def make_coauthorship_graph(filename):
    contents = []
    graph = Graph()
    with open(filename) as file:
        for line in file:
            contents.append([int(num) for num in line.split() if num.isdigit()])
    contents.remove(contents[0])
    for elem in contents:
        if len(elem) == 1:
            vertex = Vertex(elem[0])
            graph.add_vertex(vertex)
        elif len(elem) == 3:
            if elem[0] != elem[1]:
                vertex_1 = graph.vertices[elem[0]]
                vertex_2 = graph.vertices[elem[1]]
                vertex_1.add_neighbour(elem[1])
                vertex_2.add_neighbour(elem[0])
    return graph

def make_ring_group_graph(m, k, p, q):
    graph = Graph()
    for i in range(0, m * k):
        graph.add_vertex(Vertex(i))
    index = 0
    for i in range(0, m):
        for j in range(0, k):
            graph.vertices[index].label = i
            index += 1
    for i in range(0, m*k):
        vertex_1 = graph.vertices[i]
        for j in range(0, m*k):
            if i != j:
                vertex_2 = graph.vertices[j]
                prob = random.random()
                if ((vertex_1.label == vertex_2.label) or ((vertex_1.label - vertex_2.label) == 1) or ((vertex_1.label - vertex_2.label) == m-1)) and prob <= p:
                    vertex_1.add_neighbour(vertex_2.name)
                    vertex_2.add_neighbour(vertex_1.name)
                elif prob <= q:
                    if vertex_1.name not in vertex_2.neighbours:
                        vertex_1.add_neighbour(vertex_2.name)
                        vertex_2.add_neighbour(vertex_1.name)
    total = 0
    num = 0
    for vertex in graph.vertices:
        total += len(graph.vertices[vertex].neighbours)
        num += 1
    print(total / 2)
    print(num)
    sum = 0
    print(total / num)
    return graph


class PATrial:
    """
    Used when each new node is added in creation of a PA graph.
    Maintains a list of node numbers with multiple instances of each number.
    The number of instances of each node number are in proportion to the
    probability that it is linked to.
    Uses random.choice() to select a node number from this list for each trial.
    """
    def __init__(self, num_nodes):
        """
        Initialize a PATrial object corresponding to a
        complete graph with num_nodes nodes

        Note the initial list of node numbers has num_nodes copies of
        each node number
        """
        self._num_nodes = num_nodes
        self._node_numbers = [node for node in range(num_nodes) for dummy_idx in range(num_nodes)]
    def run_trial(self, num_nodes):
        """
        Conduct num_node trials using by applying random.choice()
        to the list of node numbers

        Updates the list of node numbers so that the number of instances of
        each node number is in the same ratio as the desired probabilities

        Returns:
        Set of nodes
        """
        # compute the neighbors for the newly-created node
        new_node_neighbors = set()
        for dummy_idx in range(num_nodes):
            new_node_neighbors.add(random.choice(self._node_numbers))
        # update the list of node numbers so that each node number
        # appears in the correct ratio
        self._node_numbers.append(self._num_nodes)
        self._node_numbers.extend(list(new_node_neighbors))
        # update the number of nodes
        self._num_nodes += 1
        return new_node_neighbors


def make_complete_graph(num_nodes):
    complete_graph = Graph()
    for i in range(num_nodes):
        vertex = Vertex(i)
        complete_graph.add_vertex(vertex)
        for j in range(num_nodes):
            if i != j:
                vertex.add_neighbour(j)
    return complete_graph


def preferential_attachment_graph(total_nodes, out_degree):
    pa_graph = make_complete_graph(out_degree)
    trial = PATrial(out_degree)
    for vertex in range(out_degree, total_nodes):
        new_vertex = Vertex(vertex)
        pa_graph.add_vertex(new_vertex)
        new_neighbours = trial.run_trial(out_degree)
        for new_neighbour in new_neighbours:
            new_vertex.add_neighbour(new_neighbour)
            pa_graph.vertices[new_neighbour].add_neighbour(vertex)
    total = 0
    num = 0
    for vertex in pa_graph.vertices:
        total += len(pa_graph.vertices[vertex].neighbours)
        num += 1
    print(total / 2)
    print(num)
    sum = 0
    print(total / num)
    return pa_graph


def sort_neighbours_by_degree(graph, neighbours, order):
    sorted_neighbours = {}
    for neighbour_key in neighbours:
        neighbour = graph.vertices[neighbour_key]
        sorted_neighbours[neighbour_key] = len(neighbour.neighbours)
    sorted_neighbours = sorted(sorted_neighbours.items(), key=lambda kv: kv[1], reverse=order)
    sorted_neighbours = [x[0] for x in sorted_neighbours]
    return sorted_neighbours


def approximate_brilliance(graph):
    points = {}
    for vertex_key in graph.vertices:
        vertex = graph.vertices[vertex_key]
        brilliance = []
        #random.shuffle(vertex.neighbours)
        for neighbour_key in vertex.neighbours:
            neighbour = graph.vertices[neighbour_key]
            add_to_brilliance = True
            neighbours_2 = sort_neighbours_by_degree(graph, neighbour.neighbours, False)
            for neighbours_neighbour in neighbours_2:
                if neighbours_neighbour in brilliance and add_to_brilliance:
                    add_to_brilliance = False
            if add_to_brilliance:
                brilliance.append(neighbour_key)

        brilliance = len(brilliance)
        if brilliance in points:
            points[brilliance] += 1
        else:
            points[brilliance] = 1
    sum = 0
    for brilliance in points:
        sum += points[brilliance]
    avg = sum/len(points)
    print(avg/len(graph.vertices))
    points = sorted(points.items())
    x, y = zip(*points)

    normalised_y = [y_i / len(graph.vertices) for y_i in y]
    plt.clf()
    plt.title('Brilliance distribution of the Preferential Attachment Graph')
    plt.xlabel('Brilliance')
    plt.ylabel('Normalised Rate')
    plt.scatter(x, normalised_y, color='black', s=10)
    plt.show()


if __name__ == '__main__':
    graph = make_coauthorship_graph('coauthorship.txt')
    approximate_brilliance(graph)
    graph = make_ring_group_graph(50, 31, 0.2, 0.01)
    approximate_brilliance(graph)
    graph = preferential_attachment_graph(1559, 36)
    approximate_brilliance(graph)