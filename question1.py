import random
import matplotlib.pyplot as plt
import queue
import numpy as np

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


def ring_group_graph(m, k, p, q):
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
    return graph


def get_degree_distribution(graph):
    degree_distribution = {}
    for vertex_key in graph.vertices:
        vertex = graph.vertices[vertex_key]
        if len(vertex.neighbours) not in degree_distribution:
            degree_distribution[len(vertex.neighbours)] = 1
        else:
            degree_distribution[len(vertex.neighbours)] += 1
    return degree_distribution



def plot_degree_distribution():
    m = int(input('Input a value for m: '))
    k = int(input('Input a value for k: '))
    p = 0.5
    q = 0.05
    cumulative_distribution = {}
    for i in range(200):
        graph = ring_group_graph(m, k, p, q)
        degree_distribution = get_degree_distribution(graph)
        for degree in degree_distribution:
            if degree in cumulative_distribution:
                cumulative_distribution[degree] += degree_distribution[degree]
            else:
                cumulative_distribution[degree] = degree_distribution[degree]
    normalised_distribution = {}
    for degree in cumulative_distribution:
        normalised_distribution[degree] = cumulative_distribution[degree]/(200*m*k)
    points = sorted(normalised_distribution.items())


    x, y = zip(*points)
    plt.title('Degree Distribution of Ring Group Graph')
    plt.xlabel('Degree')
    plt.ylabel('Normalised Rate')
    plt.scatter(x, y, color='black', s=10,
                label='m = ' + str(m) + '\nk = ' + str(k) + '\np = ' + str(p) + '\nq = ' + str(q))
    plt.legend(loc='upper right')
    plt.show()



def max_dist(graph, source):
    """finds the distance (the length of the shortest path) from the source to
    every other vertex in the same component using breadth-first search, and
    returns the value of the largest distance found"""
    q = queue.Queue()
    found = {}
    distance = {}
    for vertex in graph.vertices:                                        #set up arrays
        found[vertex] = 0                                       #to record whether a vertex has been discovered
        distance[vertex] = -1                                   #and its distance from the source
    max_distance = 0
    found[source] = 1                                           #initialize arrays with values for the source
    distance[source] = 0
    q.put(source)                                               #put the source in the queue
    while q.empty() == False:
        current = q.get()                                       #process the vertex at the front of the queue
        for neighbour in graph.vertices[current].neighbours:                        #look at its neighbours
            if found[neighbour] == 0:                           #if undiscovered, update arrays and add to the queue
                found[neighbour] = 1
                distance[neighbour] = distance[current] + 1
                max_distance = distance[neighbour]
                q.put(neighbour)
    return max_distance


def plot_diameter():
    m = int(input('Input a value for m: '))
    k = int(input('Input a value for k: '))

    q1= 0.002
    q2 = 0.0085
    q3 = 0.05
    points1 = {}
    points2 = {}
    points3 = {}
    for j in range(0, 25,1):
        print(j)
        p = round(j/100, 2)
        graph =ring_group_graph(m, k, p, q1)
        distances1 = []
        for vertex in graph.vertices:
            distances1 += [max_dist(graph, vertex)]
        points1[p] = max(distances1)
        graph = ring_group_graph(m, k, p, q2)
        distances2 = []
        for vertex in graph.vertices:
            distances2 += [max_dist(graph, vertex)]
        points2[p] = max(distances2)
        graph = ring_group_graph(m, k, p, q3)
        distances3 = []
        for vertex in graph.vertices:
            distances3 += [max_dist(graph, vertex)]
        points3[p] = max(distances3)

    points1 = sorted(points1.items())
    x, y = zip(*points1)
    plt.clf()
    plt.title('Relationship of p and Diameter in a Ring Group Graph')
    plt.xlabel('p')
    plt.ylabel('Diameter')
    plt.yticks(np.arange(0, max(y) +1, 1.0))
    plt.scatter(x, y, color='red', s=10, label = 'm = ' + str(m) + '\n k = ' + str(k) + '\nq = ' + str(q1))
    points2 = sorted(points2.items())
    x, y = zip(*points2)
    plt.scatter(x, y, color='green', s=10, label='m = ' + str(m) + '\n k = ' + str(k) + '\nq = ' + str(q2))
    points3 = sorted(points3.items())
    x, y = zip(*points3)
    plt.scatter(x, y, color='blue', s=10, label='m = ' + str(m) + '\n k = ' + str(k) + '\nq = ' + str(q3))
    plt.legend(loc='upper right')
    plt.show()

if __name__ == '__main__':
    plot_degree_distribution()
    plot_diameter()