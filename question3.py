import matplotlib.pyplot as plt
import random

class Vertex:
    def __init__(self, n):
        self.name = n
        self.label = 0
        self.id = (self.name, self.label)
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
    for vertex in graph.vertices:
        total += len(graph.vertices[vertex].neighbours)
    print(total / 2)

    return graph


def make_random_graph(n, p):
    random_graph = Graph()
    for i in range(n):
        vertex = Vertex(i)
        random_graph.add_vertex(vertex)
    for vertex_key in random_graph.vertices:
        for i in range(n):
            prob = random.uniform(0, 1)
            if i != vertex_key and prob < p:
                vertex_1 = random_graph.vertices[vertex_key]
                vertex_2 = random_graph.vertices[i]
                vertex_1.add_neighbour(i)
                vertex_2.add_neighbour(vertex_key)
    return random_graph



def random_search(graph, start, target):
    found = False
    search_time = 0
    vertex =  graph.vertices[start]
    if vertex == target:
        found = True
    while not found:
        search_time += 1
        vertex_key = random.choice(vertex.neighbours)
        if vertex_key == target:
            found = True
        vertex = graph.vertices[vertex_key]
    return search_time


def naive_search(graph, start, target):
    found = False
    search_time = 0
    vertex =  graph.vertices[start]
    if vertex == target:
        found = True
    while not found:
        for vertex_key in vertex.neighbours:
            if vertex_key == target:
                found = True
            search_time += 1
        vertex_key = random.choice(vertex.neighbours)
        vertex = graph.vertices[vertex_key]
    return search_time


def hybrid_search(graph, start, target):
    found = False
    search_time = 0
    vertex =  graph.vertices[start]
    if vertex == target:
        found = True
    while not found:
        if (len(vertex.neighbours)/len(graph.vertices) > 0.5) or (len(vertex.neighbours)/len(graph.vertices) > 0.01):
            for vertex_key in vertex.neighbours:
                if vertex_key == target:
                    found = True
                search_time += 1
            vertex_key = random.choice(vertex.neighbours)
        else:
            search_time += 1
            vertex_key = random.choice(vertex.neighbours)
        vertex = graph.vertices[vertex_key]
        if vertex_key == target:
            found = True
    return search_time


def plot_st_v_n():
    points1 = {}
    points2 = {}
    points3 = {}
    for n in range(250, 400, 5):
        graph = make_random_graph(n, 0.1)
        start = random.choice(list(graph.vertices.keys()))
        target = random.choice(list(graph.vertices.keys()))
        if start != target:
            search_time = hybrid_search(graph, start, target)
        points1[n] = search_time
        if start != target:
            search_time = random_search(graph, start, target)
        points2[n] = search_time
        if start != target:
            search_time = naive_search(graph, start, target)
        points3[n] = search_time

    for point in points1:
        points1[point] = points1[point]
    points1 = sorted(points1.items())
    for point in points2:
        points2[point] = points2[point]
    points2 = sorted(points2.items())
    for point in points3:
        points3[point] = points3[point]
    points3 = sorted(points3.items())
    plt.clf()
    plt.title('Comparison of search time for number of nodes for different search methods.')
    plt.xlabel('Number of Nodes')
    plt.ylabel('Search Time')
    x, y = zip(*points1)
    plt.scatter(x, y, color='red', s=10, label = 'Hybrid Search')
    x, y = zip(*points2)
    plt.scatter(x, y, color='blue', s=10, label = 'Random Search')
    x, y = zip(*points3)
    plt.scatter(x, y, color='green', s=10, label = 'Naive Search')
    plt.legend(loc = 'upper right')
    plt.show()


def plot_frequency_v_st_random():
    points1 = {}
    points2 = {}
    points3 = {}

    for i in range(500):
        graph = make_random_graph(500, 0.1)
        start = random.choice(list(graph.vertices.keys()))
        target = random.choice(list(graph.vertices.keys()))
        if start != target:
            search_time = hybrid_search(graph, start, target)

        rounded_search_time = int(50 * round(float(search_time) / 50))
        if rounded_search_time  in points1:
            points1[rounded_search_time] += 1
        else:
            points1[rounded_search_time] = 1

        if start != target:
            search_time = random_search(graph, start, target)
        rounded_search_time = int(50 * round(float(search_time) / 50))
        if rounded_search_time in points2:
            points2[rounded_search_time] += 1
        else:
            points2[rounded_search_time] = 1

        if start != target:
            search_time = naive_search(graph, start, target)
        rounded_search_time = int(50 * round(float(search_time) / 50))
        if rounded_search_time in points3:
            points3[rounded_search_time] += 1
        else:
            points3[rounded_search_time] = 1
    points1 = sorted(points1.items())
    points2 = sorted(points2.items())
    points3 = sorted(points3.items())

    plt.clf()
    plt.title('Comparison of search time frequency for different search methods.')
    plt.xlabel('Search Time')
    plt.ylabel('Frequency of search time')
    x, y = zip(*points1)
    plt.scatter(x, y, color='red', s=10, label='Hybrid Search')
    x, y = zip(*points2)
    plt.scatter(x, y, color='blue', s=10, label='Random Search')
    x, y = zip(*points3)
    plt.scatter(x, y, color='green', s=10, label='Naive Search')
    plt.legend(loc='upper right')
    plt.show()

def distance(node1, node2):
    opt1 = (node1.label - node2.label)%25
    opt2 = (node2.label - node1.label)%25
    return min(opt1, opt2)



def search_ring_group_graph(graph, start, target):
    search_time = 0
    found = False
    vertex = graph.vertices[start]
    if vertex.name == target:
        found = True
    while not found:
        if distance(vertex, graph.vertices[target]) <= 1:
            for vertex_key in vertex.neighbours:
                search_time += 1
                if vertex_key == target:
                    found = True
            vertex = graph.vertices[random.choice(vertex.neighbours)]
        else:
            query_vertex = graph.vertices[random.choice(vertex.neighbours)]
            search_time += 1
            if distance(vertex, query_vertex) <= distance(vertex, graph.vertices[target]):
                vertex = query_vertex
            elif distance(vertex, query_vertex) <= distance(vertex, graph.vertices[target]) + round(len(graph.vertices)/10):
                prob = random.random()
                if prob < 0.2:
                    vertex = query_vertex
            else:
                prob = random.random()
                if prob < 0.05:
                    vertex = query_vertex

    return search_time


def plot_frequency_v_st_rgg():
    points1 = {}
    points2 = {}
    p = 0.3
    q = 0.05
    for i in range(500):
        graph = make_ring_group_graph(25, 20, p, q)
        start = random.choice(list(graph.vertices.keys()))
        target = random.choice(list(graph.vertices.keys()))
        search_time = search_ring_group_graph(graph, start, target)
        rounded_search_time = int(50 * round(float(search_time) / 50))
        if rounded_search_time  in points1:
            points1[rounded_search_time] += 1
        else:
            points1[rounded_search_time] = 1
        search_time = naive_search(graph, start, target)
        rounded_search_time = int(50 * round(float(search_time) / 50))
        if rounded_search_time in points2:
            points2[rounded_search_time] += 1
        else:
            points2[rounded_search_time] = 1
    points1 = sorted(points1.items())
    points2 = sorted(points2.items())
    plt.clf()
    plt.title('Comparison of search times of Hybrid and Naive search methods.')
    plt.xlabel('Search Time')
    plt.ylabel('Frequency of search time')
    x, y = zip(*points1)
    plt.scatter(x, y, color='red', s=10, label='RGG Search')
    x, y = zip(*points2)
    plt.scatter(x, y, color='blue', s=10, label='Naive Search')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    plot_st_v_n()
    plot_frequency_v_st_random()
    plot_frequency_v_st_rgg()
