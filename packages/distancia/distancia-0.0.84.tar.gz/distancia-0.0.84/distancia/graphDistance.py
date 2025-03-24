from .mainClass import Distance
from .vectorDistance import Euclidean,L1
from .tools     import Graph
        
        
class ShortestPath(Distance):
	
    def __init__(self)-> None:
        """
        Initialise la classe avec un graphe représenté sous forme de dictionnaire.
        :param graph: Un dictionnaire représentant le graphe, où les clés sont les nœuds et les valeurs sont des dictionnaires
                      de voisins avec les poids des arêtes.
        """
        super().__init__()
        self.type='graph'


    def compute(self,graph, start_node, end_node):
        """
        Obtient la distance du plus court chemin entre deux nœuds dans le graphe.
        :param start_node: Le nœud de départ.
        :param end_node: Le nœud d'arrivée.
        :return: La distance du plus court chemin.
        """

        return graph.dijkstra(start_node, end_node)
        
    def example(self):
        # Create a weighted, undirected graph
        g = Graph(directed=False, weighted=True)
    
        # Add some edges
        g.add_edge("A", "B", 4)
        g.add_edge("B", "C", 3)
        g.add_edge("C", "D", 2)
        g.add_edge("D", "A", 5)
    
        # Perform Dijkstra
        distance, path = self.compute(g,"A", "C")
        print(f"Shortest path from A to C: {path}")
        print(f"Distance: {distance}")
        print(f"{self.__class__.__name__} distance between A and C in {g} is {distance:.2f}")



class GraphEditDistance(Distance):
    def __init__(self)-> None:
        """
        Initializes the GraphEditDistance class with two graphs.
        
        :param graph1: The first graph as a dictionary where keys are nodes and values are sets of connected nodes.
        :param graph2: The second graph as a dictionary where keys are nodes and values are sets of connected nodes.
        """
        super().__init__()
        self.type='graph'

        

    def compute(self, graph1, graph2):
        """
        Computes the Graph Edit Distance (GED) between the two graphs.

        :return: The Graph Edit Distance between the two graphs.
        """
        
        # Compute node differences
        node_diff = self.node_diff(graph1,graph2)

        # Compute edge differences
        edge_diff = self.edge_diff(graph1,graph2)

        # Total cost is the sum of node and edge differences
        return node_diff + edge_diff

    def node_diff(self,g1,g2):
        """
        Computes the difference in nodes between two graphs.
        
        :param g1: The first graph.
        :param g2: The second graph.
        :return: The node difference.
        """

        # Nodes to delete from g1 or add to g2
        node_intersection = g1.nodes & g2.nodes
        node_union = g2.nodes | g1.nodes

        # Node difference is the sum of deletions and additions
        return len(node_union) - len(node_intersection)

    def edge_diff(self, g1, g2):
        """
        Computes the difference in edges between two graphs.
        
        :param g1: The first graph.
        :param g2: The second graph.
        :return: The edge difference.
        """
        g1_edges = set(g1.get_edges())
        g2_edges = set(g2.get_edges())

        # Edges to delete from g1 or add to g2
        edge_intersection = g1_edges & g2_edges
        edge_union = g2_edges | g1_edges

        # Edge difference is the sum of deletions and additions
        return len(edge_union) + len(edge_intersection)
        
    def example(self):
        g1 = Graph(directed=False, weighted=True)
    
        # Add some edges
        g1.add_edge("A", "B", 4)
        g1.add_edge("B", "C", 3)
        g1.add_edge("C", "D", 2)
        g1.add_edge("D", "A", 5)
        
        g2 = Graph(directed=False, weighted=True)
    
        # Add some edges
        g2.add_edge("A", "B", 4)
        g2.add_edge("C", "D", 2)
        g2.add_edge("D", "A", 5)
        
        #graph=Graph(Graph.nodes_1,Graph.edges_1)
        distance=self.compute(g1,g2)
        print(f"{self.__class__.__name__} distance between {g2} in {g1} is {distance:.2f}")
        
        
#claude A I
try:
  import networkx as nx
  nx_installed=True
except ImportError:
    nx = None  # networkx n'est pas disponible
    
class c(Distance):
    """
    A class to compute the spectral distance between two graphs.

    The spectral distance is based on the difference between the eigenvalues
    of the Laplacian matrices of the graphs.

    Attributes:
        k (int): Number of eigenvalues to consider (default is None, which uses all eigenvalues)
        normalized (bool): Whether to use normalized Laplacian (default is False)
    """

    def __init__(self, k=None, normalized=False)-> None:
        """
        Initialize the SpectralDistance object.

        Args:
            k (int, optional): Number of eigenvalues to consider. If None, all eigenvalues are used.
            normalized (bool, optional): Whether to use the normalized Laplacian. Defaults to False.
        """
        super().__init__()
        if not nx_installed:
          raise ImportError("nx_installed need networkx. Install networkx 'pip install networkx'.")
        self.type='graph'

        self.k = k
        self.normalized = normalized

    def laplacian_matrix(self, G):
        """
        Compute the Laplacian matrix of the graph.

        Args:
            G (networkx.Graph): Input graph

        Returns:
            list of list: Laplacian matrix
        """
        n = G.number_of_nodes()
        L = [[0 for _ in range(n)] for _ in range(n)]
        
        for i in range(n):
            for j in range(n):
                if i == j:
                    L[i][j] = G.degree(i)
                elif G.has_edge(i, j):
                    L[i][j] = -1
        
        if self.normalized:
            for i in range(n):
                for j in range(n):
                    if G.degree(i) > 0 and G.degree(j) > 0:
                        L[i][j] /= (G.degree(i) * G.degree(j))**0.5
        
        return L

    def eigenvalues(self, matrix):
        """
        Compute eigenvalues using the power iteration method.

        Args:
            matrix (list of list): Input matrix

        Returns:
            list: Approximate eigenvalues
        """
        n = len(matrix)
        eigenvalues = []
        for _ in range(n):
            # Initialize random vector
            v = [1/(n)**0.5 for _ in range(n)]
            for _ in range(100):  # Number of iterations
                # Matrix-vector multiplication
                u = [sum(matrix[i][j] * v[j] for j in range(n)) for i in range(n)]
                # Normalize
                norm = (sum(x*x for x in u))**0.5
                if norm==0:norm=1
                v = [x/norm for x in u]
            # Compute Rayleigh quotient
            lambda_ = sum(v[i] * sum(matrix[i][j] * v[j] for j in range(n)) for i in range(n))
            eigenvalues.append(lambda_)
            # Deflate the matrix
            for i in range(n):
                for j in range(n):
                    matrix[i][j] -= lambda_ * v[i] * v[j]
        return sorted(eigenvalues)

    def compute(self, G1, G2):
        """
        Calculate the spectral distance between two graphs.

        Args:
            G1 (networkx.Graph): First graph
            G2 (networkx.Graph): Second graph

        Returns:
            float: Spectral distance between G1 and G2

        Raises:
            ValueError: If the graphs have different numbers of nodes and k is None
        """
        L1 = self.laplacian_matrix(G1)
        L2 = self.laplacian_matrix(G2)
        
        eig1 = self.eigenvalues(L1)
        eig2 = self.eigenvalues(L2)

        if self.k is None:
            if len(eig1) != len(eig2):
                raise ValueError("Graphs must have the same number of nodes when k is None")
            k = len(eig1)
        else:
            k = min(self.k, len(eig1), len(eig2))

        # Pad or truncate eigenvalues to length k
        eig1 = eig1[:k] + [0] * max(0, k - len(eig1))
        eig2 = eig2[:k] + [0] * max(0, k - len(eig2))

        # Compute Euclidean distance between eigenvalues
        #distance = (sum((e1 - e2)**2 for e1, e2 in zip(eig1, eig2)))**0.5
        distance = Euclidean().calculate(eig1, eig2)

        return distance
    def example(self):
        def create_sample_graphs():
         # Create a path graph
         P10 = nx.path_graph(10)
         # Create a cycle graph
         C10 = nx.cycle_graph(10)
         # Create a complete graph
         K10 = nx.complete_graph(10)
         # Create two random graphs
         G1 = nx.gnm_random_graph(10, 20)
         G2 = nx.gnm_random_graph(10, 20)
         return P10, C10, K10, G1, G2
        def compare_graphs(graphs, names):
         # Initialize SpectralDistance object
         sd = SpectralDistance(k=5, normalized=True)
         print("Spectral distances between graphs:")
         for i, (G1, name1) in enumerate(zip(graphs, names)):
          for j, (G2, name2) in enumerate(zip(graphs[i+1:], names[i+1:])):
            distance = sd.calculate(G1, G2)
            print(f"{name1} vs {name2}: {distance:.4f}")
        # Create sample graphs
        P10, C10, K10, G1, G2 = create_sample_graphs()
        graph_names = ["Path", "Cycle", "Complete", "Random1", "Random2"]
        # Compare the graphs
        compare_graphs([P10, C10, K10, G1, G2], graph_names)
#claude
from collections import Counter

class WeisfeilerLehmanSimilarity(Distance):
    """
    A class to compute the Weisfeiler-Lehman similarity between two graphs.

    The Weisfeiler-Lehman algorithm is used to create a multi-set of labels
    for each graph, which are then compared to compute a similarity score.

    Attributes:
        num_iterations (int): Number of iterations for the WL algorithm
        node_label_attr (str): Attribute name for initial node labels
    """

    def __init__(self, num_iterations=3, node_label_attr=None)-> None:
        """
        Initialize the WeisfeilerLehmanSimilarity object.

        Args:
            num_iterations (int): Number of iterations for the WL algorithm. Default is 3.
            node_label_attr (str, optional): Attribute name for initial node labels.
                If None, all nodes are initially labeled with the same value.
        """
        super().__init__()
        self.type='graph'

        self.num_iterations = num_iterations
        self.node_label_attr = node_label_attr

    def wl_labeling(self, G):
        """
        Perform Weisfeiler-Lehman labeling on the graph.

        Args:
            G (networkx.Graph): Input graph

        Returns:
            list: List of label multi-sets for each iteration
        """
        if self.node_label_attr:
            labels = nx.get_node_attributes(G, self.node_label_attr)
        else:
            labels = {node: '1' for node in G.nodes()}

        label_lists = [Counter(labels.values())]

        for _ in range(self.num_iterations):
            new_labels = {}
            for node in G.nodes():
                # Collect labels of neighbors
                neighbor_labels = sorted(labels[nbr] for nbr in G.neighbors(node))
                # Create a new label by combining current label and sorted neighbor labels
                new_labels[node] = f"{labels[node]}({''.join(neighbor_labels)})"
            
            # Update labels and add to label_lists
            labels = new_labels
            label_lists.append(Counter(labels.values()))

        return label_lists

    def compute(self, G1, G2):
        """
        Calculate the Weisfeiler-Lehman similarity between two graphs.

        Args:
            G1 (networkx.Graph): First graph
            G2 (networkx.Graph): Second graph

        Returns:
            float: Weisfeiler-Lehman similarity between G1 and G2
        """
        # Get label multi-sets for both graphs
        label_lists1 = self.wl_labeling(G1)
        label_lists2 = self.wl_labeling(G2)

        # Compute similarity for each iteration
        similarities = []
        for labels1, labels2 in zip(label_lists1, label_lists2):
            intersection = sum((labels1 & labels2).values())
            union = sum((labels1 | labels2).values())
            similarities.append(intersection / union if union > 0 else 0)

        # Return the average similarity across all iterations
        return sum(similarities) / len(similarities)

    def is_isomorphic(self, G1, G2, threshold=0.99):
        """
        Check if two graphs are potentially isomorphic using WL similarity.

        Args:
            G1 (networkx.Graph): First graph
            G2 (networkx.Graph): Second graph
            threshold (float): Similarity threshold for isomorphism. Default is 0.99.

        Returns:
            bool: True if the graphs are potentially isomorphic, False otherwise
        """
        if G1.number_of_nodes() != G2.number_of_nodes() or G1.number_of_edges() != G2.number_of_edges():
            return False
        
        similarity = self.calculate(G1, G2)
        return similarity > threshold
    def example(self):
     pass
'''
import numpy as np
import networkx as nx

class ComparingRandomWalkStationaryDistributions(Distance):
    """
    A class to compare stationary distributions of random walks on graphs.
    """

    def __init__(self,metric=L1())-> None:
        """
        Initialize the Distance object with two graphs.

        Parameters:
        graph1 (networkx.Graph): The first graph to compare
        graph2 (networkx.Graph): The second graph to compare
        """
        super().__init__()
        self.type='graph'

        self.metric = metric

    def compute_stationary_distribution(self, graph):
        """
        Compute the stationary distribution of a random walk on the given graph.

        Parameters:
        graph (networkx.Graph): The graph to compute the stationary distribution for

        Returns:
        numpy.ndarray: The stationary distribution vector
        """
        # Get the adjacency matrix
        adj_matrix = nx.adjacency_matrix(graph).toarray()

        # Compute the transition matrix
        degree = np.sum(adj_matrix, axis=1)
        transition_matrix = adj_matrix / degree[:, np.newaxis]

        # Compute the eigenvalues and eigenvectors
        eigenvalues, eigenvectors = np.linalg.eig(transition_matrix.T)

        # Find the eigenvector corresponding to eigenvalue 1
        stationary_index = np.argmin(np.abs(eigenvalues - 1))
        stationary_distribution = np.real(eigenvectors[:, stationary_index])

        # Normalize the distribution
        return stationary_distribution / np.sum(stationary_distribution)

    def compute(self, graph1, graph2):
        """
        Compare the stationary distributions of the two graphs.

        Parameters:
        metric (str): The distance metric to use. Options: 'l1', 'l2', 'kl'. Default is 'l1'.

        Returns:
        float: The distance between the two stationary distributions
        """
        dist1 = self.compute_stationary_distribution(graph1)
        dist2 = self.compute_stationary_distribution(graph2)

        if len(dist1) != len(dist2):
            raise ValueError("The graphs must have the same number of nodes")

        return self.metric.compute(dist1,dist2)
        
    def compare_random_walks(self, num_walks, walk_length):
        """
        Compare random walks on both graphs.

        Parameters:
        num_walks (int): The number of random walks to perform on each graph
        walk_length (int): The length of each random walk

        Returns:
        dict: A dictionary containing the average walk length and node visit frequencies for both graphs
        """
        results = {}

        for i, graph in enumerate([self.graph1, self.graph2]):
            total_length = 0
            node_visits = {node: 0 for node in graph.nodes()}

            for _ in range(num_walks):
                walk = self.random_walk(graph, walk_length)
                total_length += len(walk)
                for node in walk:
                    node_visits[node] += 1

            avg_length = total_length / num_walks
            visit_freq = {node: visits / (num_walks * walk_length) for node, visits in node_visits.items()}

            results[f'graph{i+1}'] = {
                'avg_walk_length': avg_length,
                'node_visit_frequencies': visit_freq
            }

        return results
    def example(self):
      """
      Test the distance calculation between graphs
      """
      # Test 1: Identical graphs
      g1 = Graph(weighted=True)
      g1.add_edge('A', 'B', 1.0)
      g1.add_edge('B', 'C', 2.0)
    
      # Test 3: Different structure
      print("Test : Different structure of graph")
      g4 = Graph(weighted=True)
      g4.add_edge('A', 'B', 1.0)
      g4.add_edge('B', 'C', 2.0)
      g4.add_edge('A', 'C', 1.5)  # Additional edge
    
      g1.add_node('C')  # Ensure both graphs have same nodes
      distance = self.compute(g1,g4)
      print(f"Distance between graphs with different structure: {distance}")
'''
from typing import Dict, Set
from collections import defaultdict
class ComparingRandomWalkStationaryDistributions(Distance):
  """
  A class to compare stationary distributions of random walks on graphs.
  """

  def __init__(self)-> None:
        """
        Initialize the Distance object with two graphs.

        Parameters:
        graph1 (networkx.Graph): The first graph to compare
        graph2 (networkx.Graph): The second graph to compare
        """
        super().__init__()
        self.type='graph'
        


  def power_iteration(self,matrix: Dict[str, Dict[str, float]], nodes: Set[str], 
                   num_iterations: int = 100, tolerance: float = 1e-10) -> Dict[str, float]:
    """
    Calcule le vecteur propre principal par la méthode des puissances.
    """
    # Distribution initiale uniforme
    n = len(nodes)
    vector = {node: 1.0/n for node in nodes}
    
    for _ in range(num_iterations):
        new_vector = Graph.multiply_matrix_vector(matrix, vector)
        new_vector = Graph.normalize_vector(new_vector)
        
        # Vérification de la convergence
        diff = sum(abs(new_vector[node] - vector[node]) for node in nodes)
        if diff < tolerance:
            return new_vector
            
        vector = new_vector
    
    return vector

  def compute(self,graph1, graph2):
    """
    Compare les distributions stationnaires de deux graphes.
    graph1, graph2: objets graphe avec la structure spécifiée
    Retourne: (différence L1, distribution1, distribution2)
    """
    # Calcul des matrices de transition
    trans_matrix1 = Graph.get_transition_matrix(graph1)
    trans_matrix2 = Graph.get_transition_matrix(graph2)
    
    # Calcul des distributions stationnaires
    stat_dist1 = self.power_iteration(trans_matrix1, graph1.nodes)
    stat_dist2 = self.power_iteration(trans_matrix2, graph2.nodes)
    
    # Pour assurer que nous comparons les mêmes nœuds
    all_nodes = set(graph1.nodes).union(set(graph2.nodes))
    
    # Compléter les distributions avec des zéros pour les nœuds manquants
    for node in all_nodes:
        if node not in stat_dist1:
            stat_dist1[node] = 0.0
        if node not in stat_dist2:
            stat_dist2[node] = 0.0
    
    # Calcul de la distance L1
    l1_distance = sum(abs(stat_dist1[node] - stat_dist2[node]) 
                     for node in all_nodes)
    
    return l1_distance, stat_dist1, stat_dist2
    
  def example(self):
    # Création de deux graphes d'exemple
    graph1 = Graph(directed=False, weighted=True)
    graph1.add_edge("A", "B", 1.0)
    graph1.add_edge("B", "C", 2.0)
    graph1.add_edge("C", "A", 1.5)
    
    graph2 = Graph(directed=False, weighted=True)
    graph2.add_edge("A", "B", 2.0)
    graph2.add_edge("B", "C", 1.0)
    graph2.add_edge("C", "D", 1.0)
    graph2.add_edge("D", "E", 1.0)
    
    distance, dist1, dist2 = ComparingRandomWalkStationaryDistributions().compute(graph1, graph2)
    print(f"Distance L1: {distance}")
    print(f"Distribution stationnaire graphe 1: {dist1}")
    print(f"Distribution stationnaire graphe 2: {dist2}")

    
''' fonctionne tres bien mais avec networkx
#claude
import networkx as nx
from collections import deque

class DiffusionDistance(Distance):
    """
    A class to compare diffusion processes on two graphs.
    """

    def __init__(self, steps =  5, metric='l1')-> None:
        """
        Initialize the DiffusionDistance object with two graphs.

        Parameters:
        graph1 (networkx.Graph): The first graph to compare
        graph2 (networkx.Graph): The second graph to compare
        """
        super().__init__()
        self.type='graph'

        self.steps = steps
        self.metric = metric


    def computeDiffusion(self, graph, source_node=None, steps=None):
        """
        Compute the diffusion process on the given graph starting from the source node.

        Parameters:
        graph (networkx.Graph): The graph to compute the diffusion process on
        source_node (int): The starting node for the diffusion process
        steps (int): The number of steps to run the diffusion process

        Returns:
        dict: A dictionary where the keys are the nodes and the values are the diffusion values
        """
        if source_node is None:
           source_node = np.random.choice(list(graph.nodes()))
           
        diffusion_values = {node: 0 for node in graph.nodes()}
        diffusion_values[source_node] = 1

        queue = deque([(source_node, 0)])

        while queue and queue[0][1] < steps:
            node, step = queue.popleft()
            neighbors = list(graph.neighbors(node))

            for neighbor in neighbors:
                diffusion_values[neighbor] += diffusion_values[node] / len(neighbors)

            for neighbor in neighbors:
                queue.append((neighbor, step + 1))

        return diffusion_values

    def compute(self, graph1, graph2, source_node):
        """
        Compare the diffusion processes on the two graphs.

        Parameters:
        source_node (int): The starting node for the diffusion process
        steps (int): The number of steps to run the diffusion process
        metric (str): The distance metric to use. Options: 'l1', 'l2'. Default is 'l1'.

        Returns:
        float: The distance between the two diffusion processes
        """
        diff1 = self.computeDiffusion(graph1, source_node, self.steps)
        diff2 = self.computeDiffusion(graph2, source_node, self.steps)

        if self.metric == 'l1':
            return sum(abs(diff1[node] - diff2[node]) for node in graph1.nodes())
        elif self.metric == 'l2':
            return sum((diff1[node] - diff2[node])**2 for node in graph1.nodes())**0.5
        else:
            raise ValueError("Invalid metric. Choose 'l1' or 'l2'.")
    def example(self):
      G1 = nx.erdos_renyi_graph(10, 0.3, seed=42)
      G2 = nx.erdos_renyi_graph(10, 0.35, seed=42)
      steps = 5
      diffusion_distance = DiffusionDistance(steps)
      source_node = 0
      l1_distance = diffusion_distance.compute(G1, G2,source_node)
      diffusion_distance = DiffusionDistance(steps,metric='l2')
      l2_distance = diffusion_distance.compute(G1, G2,source_node)
      print(f"L1 distance between diffusion processes: {l1_distance:.4f}")
      print(f"L2 distance between diffusion processes: {l2_distance:.4f}")
'''
from typing import Dict, Set, List, Tuple
from collections import defaultdict, deque
import random
from math import exp
class DiffusionDistance(Distance):
    """
    A class to compare diffusion processes on two graphs.
    """

    def __init__(self, steps =  5, metric='l1')-> None:
        """
        Initialize the DiffusionDistance object with two graphs.

        Parameters:
        graph1 (networkx.Graph): The first graph to compare
        graph2 (networkx.Graph): The second graph to compare
        """
        super().__init__()
        self.type='graph'

        self.steps = steps
        self.metric = metric
        
    def compute_hitting_times(self, graph) -> Dict[str, Dict[str, float]]:
        hitting_times = defaultdict(dict)
        nodes = list(graph.nodes)
        
        for target in nodes:
            distances = {node: float('inf') for node in nodes}
            distances[target] = 0
            queue = deque([(target, 0)])
            
            while queue:
                current, dist = queue.popleft()
                neighbors = (graph.adj_list[current].keys() if graph.weighted 
                           else graph.adj_list[current])
                
                for neighbor in neighbors:
                    weight = (1.0 if not graph.weighted 
                            else graph.adj_list[current][neighbor])
                    new_dist = dist + weight
                    
                    if new_dist < distances[neighbor]:
                        distances[neighbor] = new_dist
                        queue.append((neighbor, new_dist))
            
            hitting_times[target] = distances
            
        return hitting_times

    def compute_diffusion_kernel(self, graph, beta: float = 1.0,max_iterations=100,epsilon = 1e-10) -> Dict[str, Dict[str, float]]:
        transition = Graph.get_transition_matrix(graph)
        kernel = defaultdict(dict)
        
        for i in graph.nodes:
            vector = {node: 1.0 if node == i else 0.0 for node in graph.nodes}
            
            for _ in range(max_iterations):
                new_vector = Graph.multiply_matrix_vector(transition, vector)
                new_vector = {k: v * exp(-beta) for k, v in new_vector.items()}
                
                diff = sum(abs(new_vector[node] - vector[node]) for node in graph.nodes)
                if diff < epsilon:
                    kernel[i] = new_vector
                    break
                    
                vector = new_vector
            
            kernel[i] = vector
            
        return kernel

    def compare_graphs(self, graph1, graph2) -> Dict[str, float]:
        results = {}
        
        # Compare stationary distributions
        stat1 = Graph().compute_stationary_distribution(graph1)
        stat2 = Graph().compute_stationary_distribution(graph2)
        all_nodes = graph1.nodes.union(graph2.nodes)
        
        stat_distance = sum(abs(stat1.get(node, 0) - stat2.get(node, 0)) 
                          for node in all_nodes)
        results['stationary_distance'] = stat_distance
        
        # Compare hitting times
        hit1 = self.compute_hitting_times(graph1)
        hit2 = self.compute_hitting_times(graph2)
        common_nodes = graph1.nodes.intersection(graph2.nodes)
        
        if common_nodes:
            hit_distance = sum(abs(hit1[i][j] - hit2[i][j]) 
                             for i in common_nodes 
                             for j in common_nodes 
                             if hit1[i][j] != float('inf') and hit2[i][j] != float('inf'))
            results['hitting_time_distance'] = hit_distance / len(common_nodes)
        
        # Compare diffusion kernels
        kernel1 = self.compute_diffusion_kernel(graph1)
        kernel2 = self.compute_diffusion_kernel(graph2)
        
        if common_nodes:
            kernel_distance = sum(abs(kernel1[i][j] - kernel2[i][j]) 
                                for i in common_nodes 
                                for j in common_nodes)
            results['kernel_distance'] = kernel_distance / len(common_nodes)
        
        return results

    def simulate_diffusion(self, graph, start_nodes: Set[str], 
                         steps: int) -> List[Set[str]]:
        infected = set(start_nodes)
        history = [infected.copy()]
        
        for _ in range(steps):
            new_infected = infected.copy()
            
            for node in infected:
                neighbors = (graph.adj_list[node].keys() if graph.weighted 
                           else graph.adj_list[node])
                
                for neighbor in neighbors:
                    if neighbor not in infected:
                        prob = (1.0 if not graph.weighted 
                               else graph.adj_list[node][neighbor])
                        if random.random() < prob:
                            new_infected.add(neighbor)
            
            infected = new_infected
            history.append(infected.copy())
        
        return history

    def compare_diffusion_processes(self, graph1, graph2, 
                                  start_nodes: Set[str], 
                                  steps: int, 
                                  num_simulations: int = 10) -> Dict[str, float]:
        total_diff = 0
        max_diff = float('-inf')
        min_diff = float('inf')
        
        for _ in range(num_simulations):
            hist1 = self.simulate_diffusion(graph1, start_nodes, steps)
            hist2 = self.simulate_diffusion(graph2, start_nodes, steps)
            
            diff = sum(len(set1.symmetric_difference(set2)) 
                      for set1, set2 in zip(hist1, hist2)) / steps
            
            total_diff += diff
            max_diff = max(max_diff, diff)
            min_diff = min(min_diff, diff)
        
        return {
            'average_difference': total_diff / num_simulations,
            'max_difference': max_diff,
            'min_difference': min_diff
        }        
    def example(self):
      # Example usage
      graph1 = Graph(weighted=True)
      graph1.add_edge("A", "B", 1.0)
      graph1.add_edge("B", "C", 2.0)
      graph1.add_edge("C", "A", 1.5)

      graph2 = Graph(directed=False, weighted=True)
      graph2.add_edge("A", "B", 2.0)
      graph2.add_edge("B", "C", 1.0)
      graph2.add_edge("C", "D", 1.0)
      graph2.add_edge("D", "E", 1.0)

      comparator = DiffusionDistance()
    
      # Compare basic properties
      results = comparator.compare_graphs(graph1, graph2)
      print("Graph comparison results:", results)
    
      # Compare diffusion processes
      start_nodes = {"A"}
      diffusion_results = comparator.compare_diffusion_processes(
        graph1, graph2, start_nodes, steps=5, num_simulations=10
    )
      print("Diffusion comparison results:", diffusion_results)

#claude ai
from typing import Dict, Set, List, Tuple
from collections import defaultdict
import math

class GraphKernelDistance(Distance):
         
    def __init__(self, max_iterations: int = 100, tolerance: float = 1e-10)-> None:
        super().__init__()
        self.type='graph'
        self.max_iterations = max_iterations
        self.tolerance = tolerance

    def compute_heat_kernel(self, graph, t: float = 1.0) -> Dict[str, Dict[str, float]]:
        kernel = defaultdict(dict)
        laplacian = Graph.compute_laplacian(graph)
        
        for start_node in graph.nodes:
            vector = {node: 1.0 if node == start_node else 0.0 for node in graph.nodes}
            result = vector.copy()
            factorial = 1
            power = vector.copy()
            
            for k in range(1, self.max_iterations):
                factorial *= k
                power = Graph.multiply_matrix_vector(laplacian, power)
                term = {node: ((-t) ** k) * val / factorial 
                       for node, val in power.items()}
                
                max_change = 0.0
                for node in graph.nodes:
                    result[node] += term[node]
                    max_change = max(max_change, abs(term[node]))
                
                if max_change < self.tolerance:
                    break
            
            kernel[start_node] = result
        
        return kernel
    
    def compute_random_walk_kernel(self, graph, lambda_param: float = 0.1) -> Dict[str, Dict[str, float]]:
        transition = graph.get_transition_matrix()
        kernel = defaultdict(dict)
        
        for start_node in graph.nodes:
            vector = {node: 1.0 if node == start_node else 0.0 for node in graph.nodes}
            result = {node: lambda_param * val for node, val in vector.items()}
            current = vector.copy()
            current_lambda = lambda_param
            
            for _ in range(self.max_iterations):
                current_lambda *= lambda_param
                current = Graph.multiply_matrix_vector(transition, current)
                
                max_change = 0.0
                for node in graph.nodes:
                    change = current_lambda * current[node]
                    result[node] += change
                    max_change = max(max_change, abs(change))
                
                if max_change < self.tolerance:
                    break
            
            kernel[start_node] = result
        
        return kernel
    
    def compute_kernel_distance(self, graph1, graph2, kernel_type: str = 'heat', 
                              **kernel_params) -> float:
        if kernel_type == 'heat':
            t = kernel_params.get('t', 1.0)
            kernel1 = self.compute_heat_kernel(graph1, t)
            kernel2 = self.compute_heat_kernel(graph2, t)
        else:
            lambda_param = kernel_params.get('lambda_param', 0.1)
            kernel1 = self.compute_random_walk_kernel(graph1, lambda_param)
            kernel2 = self.compute_random_walk_kernel(graph2, lambda_param)
        
        common_nodes = graph1.nodes.intersection(graph2.nodes)
        if not common_nodes:
            return float('inf')
        
        distance = 0.0
        for i in common_nodes:
            for j in common_nodes:
                diff = kernel1[i][j] - kernel2[i][j]
                distance += diff * diff
        
        return math.sqrt(distance)
    
    def compute_multiple_kernel_distances(self, graph1, graph2) -> Dict[str, float]:
        return {
            'heat_kernel_t_1': self.compute_kernel_distance(
                graph1, graph2, kernel_type='heat', t=1.0
            ),
            'heat_kernel_t_0.1': self.compute_kernel_distance(
                graph1, graph2, kernel_type='heat', t=0.1
            ),
            'random_walk_lambda_0.1': self.compute_kernel_distance(
                graph1, graph2, kernel_type='random_walk', lambda_param=0.1
            ),
            'random_walk_lambda_0.01': self.compute_kernel_distance(
                graph1, graph2, kernel_type='random_walk', lambda_param=0.01
            )
        }
    def example(self):
    
      # Example usage
      graph1 = Graph(weighted=True)
      graph1.add_edge("A", "B", 1.0)
      graph1.add_edge("B", "C", 2.0)
      graph1.add_edge("C", "A", 1.5)

      graph2 = Graph(weighted=True)
      graph2.add_edge("A", "B", 2.0)
      graph2.add_edge("B", "C", 1.0)
      graph2.add_edge("C", "A", 1.0)

      kernel_distance = GraphKernelDistance()
    
      # Compute single kernel distance
      distance = kernel_distance.compute_kernel_distance(graph1, graph2, 'heat', t=1.0)
      print(f"Heat kernel distance (t=1.0): {distance}")
    
      # Compute multiple kernel distances
      distances = kernel_distance.compute_multiple_kernel_distances(graph1, graph2)
      for name, dist in distances.items():
        print(f"{name}: {dist}")
        
class FrobeniusDistance(Distance):
    def __init__(self)-> None:
        super().__init__()
        self.type='graph'
    '''
    def compute(self, graph1, graph2):
        if len(graph1.nodes) != len(graph2.nodes):
            raise ValueError("Graphs must have the same number of nodes")

        distance = 0
        matrix1 = graph1.adj_list
        matrix2 = graph2.adj_list
        
        for i in range(len(matrix1)):
            for j in range(len(matrix1[i])):
                diff = matrix1[i][j] - matrix2[i][j]
                distance += diff * diff
        
        return distance ** 0.5
    '''
    def compute(self,g1: 'Graph',g2: 'Graph') -> float:
        """
        Calculate the Frobenius distance between this graph and another graph.
        The Frobenius distance is defined as the Frobenius norm of the difference 
        between the adjacency matrices of the two graphs.
        
        Args:
            other (Graph): Another graph to compare with
            
        Returns:
            float: The Frobenius distance between the two graphs
            
        Raises:
            ValueError: If the graphs have different nodes or incompatible properties
            
        Example:
            >>> g1 = Graph()
            >>> g1.add_edge('A', 'B', 1.0)
            >>> g2 = Graph()
            >>> g2.add_edge('A', 'B', 2.0)
            >>> distance = g1.frobenius_distance(g2)
        """
        # Check if graphs have the same properties
        if g1.directed != g2.directed:
            raise ValueError("Cannot compare directed with undirected graphs")
        if g1.weighted != g2.weighted:
            raise ValueError("Cannot compare weighted with unweighted graphs")
            
        # Ensure both graphs have the same nodes
        if g1.nodes != g2.nodes:
            raise ValueError("Graphs must have the same set of nodes")
            
        # Get adjacency matrices
        matrix1 = g1.get_adjacency_matrix()
        matrix2 = g2.get_adjacency_matrix()
        
        # Calculate Frobenius norm of the difference
        sum_squares = 0.0
        for i in range(len(matrix1)):
            for j in range(len(matrix1[0])):
                diff = matrix1[i][j] - matrix2[i][j]
                sum_squares += diff * diff
                
        return sum_squares**0.5
         
    def example(self):
      """
      Test the Frobenius distance calculation between graphs
      """
      # Test 1: Identical graphs
      g1 = Graph(weighted=True)
      g1.add_edge('A', 'B', 1.0)
      g1.add_edge('B', 'C', 2.0)
    
      # Test 3: Different structure
      print("Test : Different structure of graph")
      g4 = Graph(weighted=True)
      g4.add_edge('A', 'B', 1.0)
      g4.add_edge('B', 'C', 2.0)
      g4.add_edge('A', 'C', 1.5)  # Additional edge
    
      g1.add_node('C')  # Ensure both graphs have same nodes
      distance = self.compute(g1,g4)
      print(f"Distance between graphs with different structure: {distance}")
'''ne fonctionne pas avec la structure dict
class PatternBasedDistance(Distance):
    def __init__(self,motif_size=3)-> None:
        super().__init__()
        self.type='graph'

        self.motif_size = motif_size

    def compute(self, graph1, graph2):
        motifs1 = graph1.count_motifs(self.motif_size)
        motifs2 = graph2.count_motifs(self.motif_size)
        return self._calculate_distance(motifs1, motifs2)

    def _calculate_distance(self, motifs1, motifs2):
        all_motifs = set(motifs1.keys()).union(set(motifs2.keys()))
        distance = 0
        for motif in all_motifs:
            freq1 = motifs1.get(motif, 0)
            freq2 = motifs2.get(motif, 0)
            distance += abs(freq1 - freq2)
        return distance
        
    def example(self):
       # Example usage
      graph1 = Graph(weighted=True)
      graph1.add_edge("A", "B", 1.0)
      graph1.add_edge("B", "C", 2.0)
      graph1.add_edge("C", "A", 1.5)

      graph2 = Graph(weighted=True)
      graph2.add_edge("A", "B", 2.0)
      graph2.add_edge("B", "C", 1.0)
      graph2.add_edge("C", "A", 1.0)

      #graph1 = Graph(nodes1, edges1)
      #graph2 = Graph(nodes2, edges2)

      pattern_distance = self.compute(graph1, graph2)

      print(f"La distance basée sur les motifs entre les deux graphes est: {pattern_distance}")
 '''
from typing import Dict, Set, List, Tuple, DefaultDict
from collections import defaultdict, deque

class PatternBasedDistance(Distance):

    def __init__(self, max_pattern_size: int = 4)-> None:
        super().__init__()

        self.max_pattern_size = max_pattern_size
        self.patterns_cache = {}
    
    def _get_neighbors(self, graph, node) -> Set[str]:
        if graph.weighted:
            return set(graph.adj_list[node].keys())
        return graph.adj_list[node]
    
    def _find_cycles(self, graph, node: str, size: int) -> List[Set[str]]:
        cycles = []
        visited = {node}
        path = [node]
        
        def dfs(current: str, start: str, depth: int):
            if depth == size - 1:
                neighbors = self._get_neighbors(graph, current)
                if start in neighbors:
                    cycles.append(set(path))
                return
            
            for neighbor in self._get_neighbors(graph, current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    path.append(neighbor)
                    dfs(neighbor, start, depth + 1)
                    path.pop()
                    visited.remove(neighbor)
        
        dfs(node, node, 0)
        return cycles
    
    def _find_paths(self, graph, node: str, length: int) -> List[List[str]]:
        paths = []
        path = [node]
        
        def dfs(current: str, depth: int):
            if depth == length:
                paths.append(path[:])
                return
            
            for neighbor in self._get_neighbors(graph, current):
                if neighbor not in path:
                    path.append(neighbor)
                    dfs(neighbor, depth + 1)
                    path.pop()
        
        dfs(node, 1)
        return paths
    
    def _find_stars(self, graph, node: str, size: int) -> List[Set[str]]:
        neighbors = self._get_neighbors(graph, node)
        if len(neighbors) < size - 1:
            return []
        
        stars = []
        from itertools import combinations
        for star_neighbors in combinations(neighbors, size - 1):
            stars.append({node} | set(star_neighbors))
        
        return stars
    
    def _compute_pattern_frequency(self, graph, pattern_type: str, size: int) -> DefaultDict[int, float]:
        cache_key = (id(graph), pattern_type, size)
        if cache_key in self.patterns_cache:
            return self.patterns_cache[cache_key]
        
        patterns = defaultdict(float)
        total_patterns = 0
        
        for node in graph.nodes:
            if pattern_type == 'cycle':
                found_patterns = self._find_cycles(graph, node, size)
            elif pattern_type == 'path':
                found_patterns = [set(path) for path in self._find_paths(graph, node, size)]
            else:  # star
                found_patterns = self._find_stars(graph, node, size)
            
            for pattern in found_patterns:
                pattern_hash = len(pattern)  # Simplified hash
                patterns[pattern_hash] += 1
                total_patterns += 1
        
        if total_patterns > 0:
            for key in patterns:
                patterns[key] /= total_patterns
        
        self.patterns_cache[cache_key] = patterns
        return patterns
    
    def _compute_weighted_pattern_frequency(self, graph, pattern_type: str, size: int) -> DefaultDict[int, float]:
        if not graph.weighted:
            return self._compute_pattern_frequency(graph, pattern_type, size)
        
        patterns = defaultdict(float)
        total_weight = 0
        
        for node in graph.nodes:
            if pattern_type == 'cycle':
                found_patterns = self._find_cycles(graph, node, size)
            elif pattern_type == 'path':
                found_patterns = [set(path) for path in self._find_paths(graph, node, size)]
            else:  # star
                found_patterns = self._find_stars(graph, node, size)
            
            for pattern in found_patterns:
                pattern_hash = len(pattern)  # Simplified hash
                pattern_weight = 0
                
                pattern_list = list(pattern)
                for i in range(len(pattern_list)):
                    for j in range(i + 1, len(pattern_list)):
                        u, v = pattern_list[i], pattern_list[j]
                        if v in graph.adj_list[u]:
                            pattern_weight += graph.adj_list[u][v]
                
                patterns[pattern_hash] += pattern_weight
                total_weight += pattern_weight
        
        if total_weight > 0:
            for key in patterns:
                patterns[key] /= total_weight
        
        return patterns
    
    def compute_pattern_vector(self, graph) -> Dict[str, DefaultDict[int, float]]:
        pattern_vector = {}
        
        for pattern_type in ['cycle', 'path', 'star']:
            for size in range(3, self.max_pattern_size + 1):
                key = f"{pattern_type}_{size}"
                pattern_vector[key] = self._compute_weighted_pattern_frequency(
                    graph, pattern_type, size
                )
        
        return pattern_vector
    
    def compute(self, graph1, graph2, 
                        pattern_weights: Dict[str, float] = None) -> Dict[str, float]:
        if pattern_weights is None:
            pattern_weights = {
                'cycle': 1.0,
                'path': 1.0,
                'star': 1.0
            }
        
        vector1 = self.compute_pattern_vector(graph1)
        vector2 = self.compute_pattern_vector(graph2)
        
        distances = {}
        
        # L1 distance
        l1_distance = 0
        for key in vector1:
            pattern_type = key.split('_')[0]
            weight = pattern_weights.get(pattern_type, 1.0)
            
            all_patterns = set(vector1[key].keys()) | set(vector2[key].keys())
            for pattern in all_patterns:
                diff = abs(vector1[key].get(pattern, 0) - vector2[key].get(pattern, 0))
                l1_distance += weight * diff
        distances['l1'] = l1_distance
        
        # L2 distance
        l2_distance = 0
        for key in vector1:
            pattern_type = key.split('_')[0]
            weight = pattern_weights.get(pattern_type, 1.0)
            
            all_patterns = set(vector1[key].keys()) | set(vector2[key].keys())
            for pattern in all_patterns:
                diff = vector1[key].get(pattern, 0) - vector2[key].get(pattern, 0)
                l2_distance += weight * (diff * diff)
        distances['l2'] = math.sqrt(l2_distance)
        
        return distances
    
    def compare_specific_patterns(self, graph1, graph2, 
                                pattern_type: str, 
                                size: int) -> Dict[str, float]:
        freq1 = self._compute_weighted_pattern_frequency(graph1, pattern_type, size)
        freq2 = self._compute_weighted_pattern_frequency(graph2, pattern_type, size)
        
        all_patterns = set(freq1.keys()) | set(freq2.keys())
        
        l1_distance = sum(abs(freq1.get(p, 0) - freq2.get(p, 0)) for p in all_patterns)
        l2_distance = (sum((freq1.get(p, 0) - freq2.get(p, 0)) ** 2 
                                  for p in all_patterns))**0.5
        
        return {
            'l1_distance': l1_distance,
            'l2_distance': l2_distance,
            'pattern_count_1': len(freq1),
            'pattern_count_2': len(freq2)
        }

    def example(self):
    
      # Example usage
      graph1 = Graph(weighted=True)
      graph1.add_edge("A", "B", 1.0)
      graph1.add_edge("B", "C", 2.0)
      graph1.add_edge("C", "D", 1.5)
      graph1.add_edge("D", "A", 1.0)
      graph1.add_edge("A", "C", 2.0)

      graph2 = Graph(weighted=True)
      graph2.add_edge("A", "B", 1.0)
      graph2.add_edge("B", "C", 1.0)
      graph2.add_edge("C", "D", 1.0)
      graph2.add_edge("D", "A", 1.0)

      pattern_distance = PatternBasedDistance(max_pattern_size=4)
    
      # Compare all patterns
      distances = pattern_distance.compute(
        graph1, graph2,
        pattern_weights={'cycle': 1.5, 'path': 1.0, 'star': 0.5}
    )
      print("Overall distances:", distances)
    
      # Compare specific pattern type
      cycle_comparison = pattern_distance.compare_specific_patterns(
        graph1, graph2, 'cycle', 4
    )
      print("Cycle pattern comparison:", cycle_comparison)
    
import zlib

class GraphCompressionDistance(Distance):
    def __init__(self)-> None:
        """
        Initialize the GraphCompressionDistance class with two graphs.
        Each graph is represented as an adjacency matrix, which is a list of lists.

        :param graph1: Adjacency matrix of the first graph
        :param graph2: Adjacency matrix of the second graph
        """
        super().__init__()
        self.type='graph'
        
    def compress(self, data):
        """
        Compress the data using zlib compression and return the compressed size.

        :param data: String representation of the graph
        :return: Length of the compressed data
        """
        compressed_data = zlib.compress(data.encode('utf-8'))
        return len(compressed_data)

    def combined_compression(self,graph1,graph2):
        """
        Compress the combined adjacency matrices of both graphs.

        :return: Length of the compressed combined adjacency matrix
        """
        combined_matrix = graph1.adjacency_to_string() + graph2.adjacency_to_string()
        return self.compress(combined_matrix)

    def compute(self, graph1, graph2):
        """
        Compute the Graph Compression Distance between the two graphs.

        :return: Compression distance between the two graphs
        """
        graph1_compressed_size = self.compress(graph1.adjacency_to_string())
        graph2_compressed_size = self.compress(graph2.adjacency_to_string())
        combined_compressed_size = self.combined_compression(graph1,graph2)

        distance = combined_compressed_size - min(graph1_compressed_size, graph2_compressed_size)
        return distance
        
    def example(self):
      # Example usage
      graph1 = Graph(weighted=True)
      graph1.add_edge("A", "B", 1.0)
      graph1.add_edge("B", "C", 2.0)
      graph1.add_edge("C", "D", 1.5)
      graph1.add_edge("D", "A", 1.0)
      graph1.add_edge("A", "C", 2.0)

      graph2 = Graph(weighted=True)
      graph2.add_edge("A", "B", 1.0)
      graph2.add_edge("B", "C", 1.0)
      graph2.add_edge("C", "D", 1.0)
      graph2.add_edge("D", "A", 1.0)
      
      distance_calculator = GraphCompressionDistance().compute(graph1, graph2)
      print(f"Graph Compression Distance: {distance_calculator}")
      
'''ne fonctionne pas avec la structure de graph dict      
class DegreeDistributionDistance(Distance):
    def __init__(self)-> None:
        """
        Initializes the DegreeDistributionDistance class with two graphs.

        :param graph1: First graph, represented as an adjacency list or edge list.
        :param graph2: Second graph, represented as an adjacency list or edge list.
        """
        super().__init__()
        self.type='graph'


    def compare_distributions(self, dist1, dist2):
        """
        Compares two degree distributions using a simple difference metric.

        :param dist1: Degree distribution of the first graph.
        :param dist2: Degree distribution of the second graph.
        :return: A floating-point value representing the difference between the distributions.
        """
        all_degrees = set(dist1.keys()).union(set(dist2.keys()))
        difference = 0.0
        for degree in all_degrees:
            count1 = dist1.get(degree, 0)
            count2 = dist2.get(degree, 0)
            difference += abs(count1 - count2)
        return difference

    def compute(self, graph1, graph2):
        """
        Computes the degree distribution distance between the two graphs.

        :return: A floating-point value representing the distance between the degree distributions of the two graphs.
        """
        dist1 = Graph.compute_degree_distribution(graph1)
        dist2 = Graph.compute_degree_distribution(graph2)
        return self.compare_distributions(dist1, dist2)
        

'''
from collections import defaultdict
from typing import Dict, Set

class DegreeDistributionDistance(Distance):
    def __init__(self)-> None:
      
        super().__init__()
        self.type='graph'
        self.reset()

    def reset(self):
        self.degrees1 = {}
        self.degrees2 = {}
        self.distance = 0.0

    def compute(self, graph1: Graph, graph2: Graph) -> float:
        self.reset()
        
        # Verify that both graphs are of the same type
        if graph1.weighted != graph2.weighted or graph1.directed != graph2.directed:
            raise ValueError("Graphs must be of the same type (both weighted or both unweighted, both directed or both undirected)")
        
        # Compute degree distributions
        self.degrees1 = Graph.compute_degrees(graph1)
        self.degrees2 = Graph.compute_degrees(graph2)
        
        # Get all unique degrees
        all_degrees = set(list(self.degrees1.keys()) + list(self.degrees2.keys()))
        
        # Calculate L1 distance
        self.distance = 0.0
        for degree in all_degrees:
            prob1 = self.degrees1.get(degree, 0.0)
            prob2 = self.degrees2.get(degree, 0.0)
            self.distance += abs(prob1 - prob2)
        
        return self.distance

    def get_distributions(self):
        return self.degrees1, self.degrees2

    def example(self):
      # Example usage
      graph1 = Graph(weighted=True)
      graph1.add_edge("A", "B", 1.0)
      graph1.add_edge("B", "C", 2.0)
      graph1.add_edge("C", "D", 1.5)
      graph1.add_edge("D", "A", 1.0)
      graph1.add_edge("A", "C", 2.0)

      graph2 = Graph(weighted=True)
      graph2.add_edge("A", "B", 1.0)
      graph2.add_edge("B", "C", 1.0)
      
      distance=self.compute(graph1,graph2)
      print(f"Graph DegreeDistributionDistance: {distance}")

from collections import defaultdict
from typing import Dict, Set, List, Tuple
import random

class CommunityStructureDistance(Distance):
    def __init__(self)-> None:
      
        super().__init__()
        self.type='graph'
        self.reset()

    def reset(self):
        # Reset computed values
        self.communities1 = {}
        self.communities2 = {}
        self.distance = 0.0

    def modularity(self, graph: Graph, communities: Dict[str, int]) -> float:
        # Calculate modularity Q = 1/2m * sum(Aij - kikj/2m)δ(ci,cj)
        if not graph.nodes:
            return 0.0

        total_weight = 0
        node_degrees = defaultdict(float)

        # Calculate total weight and node degrees
        for node in graph.nodes:
            for neighbor, weight in graph.adj_list[node].items():
                if graph.weighted:
                    w = weight
                else:
                    w = 1.0
                node_degrees[node] += w
                if not graph.directed:
                    total_weight += w / 2
                else:
                    total_weight += w

        if total_weight == 0:
            return 0.0

        modularity = 0.0
        for node in graph.nodes:
            for neighbor in graph.adj_list[node]:
                if communities[node] == communities[neighbor]:
                    if graph.weighted:
                        actual = graph.adj_list[node][neighbor]
                    else:
                        actual = 1.0
                    expected = node_degrees[node] * node_degrees[neighbor] / (2.0 * total_weight)
                    modularity += (actual - expected)

        modularity /= (2.0 * total_weight)
        return modularity

    def detect_communities(self, graph: Graph) -> Dict[str, int]:
        # Implementation of Louvain method for community detection
        communities = {node: idx for idx, node in enumerate(graph.nodes)}
        n_communities = len(communities)
        
        improvement = True
        while improvement:
            improvement = False
            
            # Phase 1: Modularity optimization
            for node in graph.nodes:
                current_community = communities[node]
                neighbor_communities = {}
                
                # Calculate gain for moving to each neighbor's community
                for neighbor in graph.adj_list[node]:
                    neighbor_community = communities[neighbor]
                    if neighbor_community not in neighbor_communities:
                        # Remove node from its current community
                        communities[node] = neighbor_community
                        gain = self.modularity(graph, communities)
                        communities[node] = current_community
                        neighbor_communities[neighbor_community] = gain
                
                # Find best community
                best_community = current_community
                best_gain = 0.0
                
                for community, gain in neighbor_communities.items():
                    if gain > best_gain:
                        best_gain = gain
                        best_community = community
                
                if best_community != current_community:
                    communities[node] = best_community
                    improvement = True
            
            if not improvement:
                break
            
            # Phase 2: Community aggregation
            new_communities = {}
            idx = 0
            for old_community in set(communities.values()):
                new_communities[old_community] = idx
                idx += 1
            
            for node in communities:
                communities[node] = new_communities[communities[node]]

        return communities

    def compute(self, graph1: Graph, graph2: Graph) -> float:
        # Reset previous computations
        self.reset()
        
        # Verify graphs are compatible
        if graph1.weighted != graph2.weighted or graph1.directed != graph2.directed:
            raise ValueError("Graphs must be of the same type")

        # Detect communities in both graphs
        self.communities1 = self.detect_communities(graph1)
        self.communities2 = self.detect_communities(graph2)

        # Convert to community size distributions
        dist1 = self._get_community_size_distribution(self.communities1)
        dist2 = self._get_community_size_distribution(self.communities2)

        # Calculate L1 distance between distributions
        all_sizes = set(list(dist1.keys()) + list(dist2.keys()))
        
        distance = 0.0
        for size in all_sizes:
            prob1 = dist1.get(size, 0.0)
            prob2 = dist2.get(size, 0.0)
            distance += abs(prob1 - prob2)

        return distance

    def _get_community_size_distribution(self, communities: Dict[str, int]) -> Dict[int, float]:
        # Count community sizes
        community_sizes = defaultdict(int)
        for community_id in communities.values():
            community_sizes[community_id] += 1
        
        # Convert to size distribution
        size_distribution = defaultdict(float)
        total_nodes = len(communities)
        
        for community_id, size in community_sizes.items():
            size_distribution[size] += 1
        
        # Normalize
        for size in size_distribution:
            size_distribution[size] /= total_nodes
            
        return dict(size_distribution)

    def get_communities(self):
        return self.communities1, self.communities2
        
    def example(self):
      # Example usage
      graph1 = Graph(weighted=True)
      graph1.add_edge("A", "B", 1.0)
      graph1.add_edge("B", "C", 2.0)
      graph1.add_edge("C", "D", 1.5)
      graph1.add_edge("D", "A", 1.0)
      graph1.add_edge("A", "C", 2.0)

      graph2 = Graph(weighted=True)
      graph2.add_edge("A", "B", 1.0)
      graph2.add_edge("B", "C", 1.0)
      graph2.add_edge("C", "D", 1.0)
      # Compare community structures
      csd = CommunityStructureDistance()
      distance = csd.compute(graph1, graph2)
      print(f"Community structure distance: {distance}")

      # Get detected communities if needed
      communities1, communities2 = csd.get_communities()
      print("Communities in graph 1:", communities1)
      print("Communities in graph 2:", communities2)

###########################################
#a terminer claude 	ai
from typing import Dict, List, Set, Tuple
from collections import defaultdict, deque

class GraphBetweennessDistance(Distance):
    """
    Calculates distance between two graphs using Betweenness Centrality metrics.
    
    Measures the structural difference between graphs based on how nodes function
    as bridges in their respective networks.
    """
    def __init__(self)-> None:
      
        super().__init__()
        self.type='graph'
            
    def calculate_distance(
        self,
        graph1: Dict[int, List[int]],
        graph2: Dict[int, List[int]]
    ) -> float:
        """
        Calculate distance between two graphs using betweenness centrality.
        
        Args:
            graph1 (Dict[int, List[int]]): First graph as adjacency list
            graph2 (Dict[int, List[int]]): Second graph as adjacency list
        
        Returns:
            float: Distance measure between the graphs
        """
        # Calculate betweenness centrality for both graphs
        centrality1 = self._compute_betweenness_centrality(graph1)
        centrality2 = self._compute_betweenness_centrality(graph2)
        
        # Compute distance based on centrality differences
        return self._compute_centrality_distance(centrality1, centrality2)
    
    def _compute_betweenness_centrality(
        self,
        graph: Dict[int, List[int]]
    ) -> Dict[int, float]:
        """
        Compute betweenness centrality for all nodes in the graph.
        
        Args:
            graph (Dict[int, List[int]]): Graph as adjacency list
        
        Returns:
            Dict[int, float]: Node betweenness centrality scores
        """
        centrality = defaultdict(float)
        nodes = list(graph.keys())
        n = len(nodes)
        
        for source in nodes:
            # Get shortest paths and path counts
            paths_data = self._get_shortest_paths(graph, source)
            shortest_paths, path_counts = paths_data
            
            # Calculate dependencies
            dependencies = self._compute_dependencies(
                graph, source, shortest_paths, path_counts
            )
            
            # Update centrality scores
            for node, dependency in dependencies.items():
                if node != source:
                    centrality[node] += dependency
        
        # Normalize scores
        if n > 2:
            norm_factor = 1.0 / ((n - 1) * (n - 2))
            for node in centrality:
                centrality[node] *= norm_factor
                
        return dict(centrality)
    
    def _get_shortest_paths(
        self,
        graph: Dict[int, List[int]],
        source: int
    ) -> Tuple[Dict[int, List[int]], Dict[int, int]]:
        """
        Find shortest paths from source node using BFS.
        
        Args:
            graph (Dict[int, List[int]]): Graph structure
            source (int): Starting node
            
        Returns:
            Tuple containing shortest paths and path counts
        """
        shortest_paths = defaultdict(list)
        path_counts = defaultdict(int)
        distances = {source: 0}
        path_counts[source] = 1
        queue = deque([(source, 0)])
        
        while queue:
            node, distance = queue.popleft()
            
            for neighbor in graph[node]:
                # Discover new node
                if neighbor not in distances:
                    distances[neighbor] = distance + 1
                    queue.append((neighbor, distance + 1))
                    path_counts[neighbor] = path_counts[node]
                    shortest_paths[neighbor].append(node)
                # Additional path found
                elif distances[neighbor] == distance + 1:
                    path_counts[neighbor] += path_counts[node]
                    shortest_paths[neighbor].append(node)
        
        return dict(shortest_paths), dict(path_counts)
    
    def _compute_dependencies(
        self,
        graph: Dict[int, List[int]],
        source: int,
        shortest_paths: Dict[int, List[int]],
        path_counts: Dict[int, int]
    ) -> Dict[int, float]:
        """
        Calculate node dependencies for centrality computation.
        
        Args:
            graph (Dict[int, List[int]]): Graph structure
            source (int): Source node
            shortest_paths (Dict[int, List[int]]): Shortest paths from source
            path_counts (Dict[int, int]): Number of shortest paths
            
        Returns:
            Dict[int, float]: Node dependencies
        """
        dependencies = defaultdict(float)
        nodes = sorted(
            shortest_paths.keys(),
            key=lambda x: -len(shortest_paths[x])
        )
        
        for node in nodes:
            coeff = (1.0 + dependencies[node]) / path_counts[node]
            for predecessor in shortest_paths[node]:
                dependencies[predecessor] += path_counts[predecessor] * coeff
                
        return dict(dependencies)
    
    def _compute_centrality_distance(
        self,
        centrality1: Dict[int, float],
        centrality2: Dict[int, float]
    ) -> float:
        """
        Compute distance between two centrality distributions.
        
        Args:
            centrality1 (Dict[int, float]): First graph centrality scores
            centrality2 (Dict[int, float]): Second graph centrality scores
            
        Returns:
            float: Distance measure between centrality distributions
        """
        # Get all nodes from both graphs
        all_nodes = set(centrality1.keys()) | set(centrality2.keys())
        
        # Calculate squared differences in centrality
        squared_diff_sum = sum(
            (centrality1.get(node, 0) - centrality2.get(node, 0)) ** 2
            for node in all_nodes
        )
        
        return math.sqrt(squared_diff_sum)



#####################
from typing import Dict, Set, List, Tuple
from copy import deepcopy

class KCoreDistance(Distance):
    """
    A class to calculate the K-Core distance between two weighted graphs.
    K-Core is the largest subgraph where all nodes have at least k neighbors.
    
    Attributes:
        graph1 (Dict[str, Dict[str, float]]): First weighted graph represented as adjacency dict
        graph2 (Dict[str, Dict[str, float]]): Second weighted graph represented as adjacency dict
    """
    
    def __init__(self, graph1: Dict[str, Dict[str, float]], graph2: Dict[str, Dict[str, float]]):
        """
        Initialize the KCoreDistance calculator with two weighted graphs.
        
        Args:
            graph1: First weighted graph as adjacency dictionary
            graph2: Second weighted graph as adjacency dictionary
        """
      
        super().__init__()
        self.type='graph'
        
        self.graph1 = deepcopy(graph1)
        self.graph2 = deepcopy(graph2)
    
    def compute_k_core(self, graph: Dict[str, Dict[str, float]], k: int) -> Set[str]:
        """
        Compute the k-core of a graph using the k-core decomposition algorithm.
        
        Args:
            graph: Weighted graph as adjacency dictionary
            k: Minimum number of neighbors required
            
        Returns:
            Set of nodes that belong to the k-core
        """
        # Make a copy to avoid modifying the original graph
        working_graph = deepcopy(graph)
        
        while True:
            # Find nodes with degree less than k
            to_remove = set()
            for node in working_graph:
                if len(working_graph[node]) < k:
                    to_remove.add(node)
            
            if not to_remove:
                break
                
            # Remove nodes and their edges
            for node in to_remove:
                # Remove edges to this node from all neighbors
                for neighbor in working_graph[node]:
                    if neighbor in working_graph:
                        working_graph[neighbor].pop(node, None)
                # Remove the node itself
                working_graph.pop(node)
        
        return set(working_graph.keys())
    
    def get_max_k_core(self, graph: Dict[str, Dict[str, float]]) -> int:
        """
        Find the maximum k for which a k-core exists in the graph.
        
        Args:
            graph: Weighted graph as adjacency dictionary
            
        Returns:
            Maximum k value for which a k-core exists
        """
        max_k = 0
        k = 1
        
        while True:
            core = self.compute_k_core(graph, k)
            if not core:
                break
            max_k = k
            k += 1
            
        return max_k
    
    def calculate_distance(self) -> Tuple[int, int, float]:
        """
        Calculate the K-Core distance between the two graphs.
        
        Returns:
            Tuple containing:
            - Maximum k-core number of first graph
            - Maximum k-core number of second graph
            - Normalized distance between the two k-core numbers
        """
        max_k1 = self.get_max_k_core(self.graph1)
        max_k2 = self.get_max_k_core(self.graph2)
        
        # Calculate normalized distance between 0 and 1
        max_k = max(max_k1, max_k2)
        if max_k == 0:
            distance = 0.0
        else:
            distance = abs(max_k1 - max_k2) / max_k
            
        return max_k1, max_k2, distance



###############################
from typing import Dict, List, Tuple, Set
from collections import defaultdict
from math import inf
import heapq
from copy import deepcopy

class ClosenessCentralityDistance(Distance):
    """
    A class to calculate the Closeness Centrality distance between two weighted graphs.
    Closeness Centrality measures how close a node is to all other nodes in the graph.
    
    Attributes:
        graph1 (Dict[str, Dict[str, float]]): First weighted graph represented as adjacency dict
        graph2 (Dict[str, Dict[str, float]]): Second weighted graph represented as adjacency dict
    """
    
    def __init__(self, graph1: Dict[str, Dict[str, float]], graph2: Dict[str, Dict[str, float]]):
        """
        Initialize the ClosenessCentrality calculator with two weighted graphs.
        
        Args:
            graph1: First weighted graph as adjacency dictionary
            graph2: Second weighted graph as adjacency dictionary
        """
      
        super().__init__()
        self.type='graph'
        
        self.graph1 = deepcopy(graph1)
        self.graph2 = deepcopy(graph2)
    
    def dijkstra(self, graph: Dict[str, Dict[str, float]], start: str) -> Dict[str, float]:
        """
        Compute shortest paths from start node to all other nodes using Dijkstra's algorithm.
        
        Args:
            graph: Weighted graph as adjacency dictionary
            start: Starting node
            
        Returns:
            Dictionary of shortest distances from start node to all other nodes
        """
        distances = {node: inf for node in graph}
        distances[start] = 0
        pq = [(0, start)]
        visited = set()
        
        while pq:
            current_distance, current_node = heapq.heappop(pq)
            
            if current_node in visited:
                continue
                
            visited.add(current_node)
            
            for neighbor, weight in graph[current_node].items():
                distance = current_distance + weight
                
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(pq, (distance, neighbor))
        
        return distances
    
    def compute_closeness_centrality(self, graph: Dict[str, Dict[str, float]]) -> Dict[str, float]:
        """
        Compute closeness centrality for all nodes in the graph.
        
        Args:
            graph: Weighted graph as adjacency dictionary
            
        Returns:
            Dictionary of closeness centrality values for each node
        """
        centrality = {}
        n = len(graph)
        
        for node in graph:
            # Get shortest paths from current node to all others
            shortest_paths = self.dijkstra(graph, node)
            
            # Sum of all finite distances
            total_distance = sum(d for d in shortest_paths.values() if d != inf)
            
            # Count number of reachable nodes (excluding self)
            reachable = sum(1 for d in shortest_paths.values() if d != inf) - 1
            
            if reachable > 0:
                # Compute closeness centrality
                # We use (reachable / (n-1)) term to normalize for disconnected graphs
                centrality[node] = (reachable / (n-1)) * (reachable / total_distance)
            else:
                centrality[node] = 0.0
        
        return centrality
    
    def calculate_distance(self) -> Tuple[Dict[str, float], Dict[str, float], float]:
        """
        Calculate the distance between two graphs based on their closeness centrality distributions.
        
        Returns:
            Tuple containing:
            - Closeness centrality values for first graph
            - Closeness centrality values for second graph
            - Average absolute difference in centrality values
        """
        centrality1 = self.compute_closeness_centrality(self.graph1)
        centrality2 = self.compute_closeness_centrality(self.graph2)
        
        # Calculate average absolute difference in centrality values
        all_nodes = set(centrality1.keys()) | set(centrality2.keys())
        total_diff = 0.0
        
        for node in all_nodes:
            val1 = centrality1.get(node, 0.0)
            val2 = centrality2.get(node, 0.0)
            total_diff += abs(val1 - val2)
            
        avg_distance = total_diff / len(all_nodes)
        
        return centrality1, centrality2, avg_distance
        

##############################
from typing import Dict, List, Set, Tuple
from collections import defaultdict
from copy import deepcopy
from math import inf

class BetweennessCentralityDistance(Distance):
    """
    A class to calculate the Betweenness Centrality distance between two weighted graphs.
    Betweenness Centrality quantifies how often a node acts as a bridge along the shortest
    path between two other nodes.
    
    Attributes:
        graph1 (Dict[str, Dict[str, float]]): First weighted graph represented as adjacency dict
        graph2 (Dict[str, Dict[str, float]]): Second weighted graph represented as adjacency dict
    """
    
    def __init__(self, graph1: Dict[str, Dict[str, float]], graph2: Dict[str, Dict[str, float]]):
        """
        Initialize the BetweennessCentrality calculator with two weighted graphs.
        
        Args:
            graph1: First weighted graph as adjacency dictionary
            graph2: Second weighted graph as adjacency dictionary
        """
      
        super().__init__()
        self.type='graph'
        
        self.graph1 = deepcopy(graph1)
        self.graph2 = deepcopy(graph2)
    
    def shortest_paths_dijkstra(self, graph: Dict[str, Dict[str, float]], 
                              start: str) -> Tuple[Dict[str, float], Dict[str, List[str]]]:
        """
        Compute shortest paths and predecessors from start node using Dijkstra's algorithm.
        
        Args:
            graph: Weighted graph as adjacency dictionary
            start: Starting node
            
        Returns:
            Tuple containing:
            - Dictionary of shortest distances
            - Dictionary of predecessor lists for each node
        """
        distances = {node: inf for node in graph}
        distances[start] = 0
        predecessors = {node: [] for node in graph}
        
        unvisited = set(graph.keys())
        
        while unvisited:
            # Find unvisited node with minimum distance
            current = min(unvisited, key=lambda x: distances[x])
            
            if distances[current] == inf:
                break
                
            unvisited.remove(current)
            
            for neighbor, weight in graph[current].items():
                distance = distances[current] + weight
                
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    predecessors[neighbor] = [current]
                elif distance == distances[neighbor]:
                    predecessors[neighbor].append(current)
        
        return distances, predecessors
    
    def accumulate_betweenness(self, graph: Dict[str, Dict[str, float]], 
                              start: str) -> Dict[str, float]:
        """
        Compute the contribution to betweenness centrality from paths starting at given node.
        
        Args:
            graph: Weighted graph as adjacency dictionary
            start: Starting node
            
        Returns:
            Dictionary of betweenness contributions for each node
        """
        betweenness = {node: 0.0 for node in graph}
        distances, predecessors = self.shortest_paths_dijkstra(graph, start)
        
        # Initialize dependency accumulation
        dependency = {node: 0.0 for node in graph}
        
        # Process nodes in order of decreasing distance from start
        stack = sorted([(d, n) for n, d in distances.items() if n != start], reverse=True)
        
        for _, node in stack:
            coeff = (1.0 + dependency[node]) / len(predecessors[node])
            for pred in predecessors[node]:
                dependency[pred] += coeff
                betweenness[pred] += coeff
        
        return betweenness
    
    def compute_betweenness_centrality(self, graph: Dict[str, Dict[str, float]]) -> Dict[str, float]:
        """
        Compute betweenness centrality for all nodes in the graph.
        
        Args:
            graph: Weighted graph as adjacency dictionary
            
        Returns:
            Dictionary of normalized betweenness centrality values for each node
        """
        betweenness = {node: 0.0 for node in graph}
        
        # Accumulate betweenness from all source nodes
        for start in graph:
            contributions = self.accumulate_betweenness(graph, start)
            for node in graph:
                betweenness[node] += contributions[node]
        
        # Normalize the values
        n = len(graph)
        normalization = (n - 1) * (n - 2)  # Number of possible paths excluding source
        
        if normalization > 0:
            for node in betweenness:
                betweenness[node] /= normalization
        
        return betweenness
    
    def calculate_distance(self) -> Tuple[Dict[str, float], Dict[str, float], float]:
        """
        Calculate the distance between two graphs based on their betweenness centrality distributions.
        
        Returns:
            Tuple containing:
            - Betweenness centrality values for first graph
            - Betweenness centrality values for second graph
            - Average absolute difference in centrality values
        """
        centrality1 = self.compute_betweenness_centrality(self.graph1)
        centrality2 = self.compute_betweenness_centrality(self.graph2)
        
        # Calculate average absolute difference in centrality values
        all_nodes = set(centrality1.keys()) | set(centrality2.keys())
        total_diff = 0.0
        
        for node in all_nodes:
            val1 = centrality1.get(node, 0.0)
            val2 = centrality2.get(node, 0.0)
            total_diff += abs(val1 - val2)
            
        avg_distance = total_diff / len(all_nodes)
        
        return centrality1, centrality2, avg_distance
        

##################################
from typing import Dict, List, Tuple, Set
from copy import deepcopy
from math import sqrt

class EigenvectorCentralityDistance(Distance):
    """
    A class to calculate the Eigenvector Centrality distance between two weighted graphs.
    Eigenvector Centrality measures node influence based on connections to other influential nodes.
    
    Attributes:
        graph1 (Dict[str, Dict[str, float]]): First weighted graph represented as adjacency dict
        graph2 (Dict[str, Dict[str, float]]): Second weighted graph represented as adjacency dict
        max_iterations (int): Maximum number of iterations for power iteration method
        tolerance (float): Convergence tolerance for power iteration method
    """
    
    def __init__(self, 
                 graph1: Dict[str, Dict[str, float]], 
                 graph2: Dict[str, Dict[str, float]], 
                 max_iterations: int = 100,
                 tolerance: float = 1e-6):
        """
        Initialize the EigenvectorCentrality calculator with two weighted graphs.
        
        Args:
            graph1: First weighted graph as adjacency dictionary
            graph2: Second weighted graph as adjacency dictionary
            max_iterations: Maximum number of power iterations
            tolerance: Convergence tolerance
        """      
        super().__init__()
        self.type='graph'
        
        self.graph1 = deepcopy(graph1)
        self.graph2 = deepcopy(graph2)
        self.max_iterations = max_iterations
        self.tolerance = tolerance
    
    def normalize_vector(self, vector: Dict[str, float]) -> Dict[str, float]:
        """
        Normalize a vector using L2 norm.
        
        Args:
            vector: Dictionary representing a vector
            
        Returns:
            Normalized vector
        """
        # Calculate L2 norm
        norm = sqrt(sum(x * x for x in vector.values()))
        
        if norm > 0:
            return {k: v / norm for k, v in vector.items()}
        return vector
    
    def matrix_vector_multiply(self, 
                             graph: Dict[str, Dict[str, float]], 
                             vector: Dict[str, float]) -> Dict[str, float]:
        """
        Multiply adjacency matrix by vector.
        
        Args:
            graph: Weighted graph as adjacency dictionary
            vector: Vector to multiply with
            
        Returns:
            Result vector of the multiplication
        """
        result = {node: 0.0 for node in graph}
        
        for node in graph:
            for neighbor, weight in graph[node].items():
                result[node] += weight * vector[neighbor]
                
        return result
    
    def compute_eigenvector_centrality(self, 
                                     graph: Dict[str, Dict[str, float]]) -> Dict[str, float]:
        """
        Compute eigenvector centrality for all nodes using power iteration method.
        
        Args:
            graph: Weighted graph as adjacency dictionary
            
        Returns:
            Dictionary of eigenvector centrality values for each node
        """
        # Initialize eigenvector with equal values
        n = len(graph)
        if n == 0:
            return {}
            
        centrality = {node: 1.0 / sqrt(n) for node in graph}
        
        for _ in range(self.max_iterations):
            # Store previous iteration for convergence check
            prev_centrality = centrality.copy()
            
            # Power iteration step
            centrality = self.matrix_vector_multiply(graph, centrality)
            
            # Normalize the vector
            centrality = self.normalize_vector(centrality)
            
            # Check for convergence
            diff = sum((centrality[node] - prev_centrality[node]) ** 2 
                      for node in centrality)
            if sqrt(diff) < self.tolerance:
                break
        
        # Ensure all values are positive
        min_value = min(centrality.values())
        if min_value < 0:
            centrality = {k: v - min_value for k, v in centrality.items()}
            centrality = self.normalize_vector(centrality)
            
        return centrality
    
    def calculate_distance(self) -> Tuple[Dict[str, float], Dict[str, float], float]:
        """
        Calculate the distance between two graphs based on their eigenvector centrality distributions.
        
        Returns:
            Tuple containing:
            - Eigenvector centrality values for first graph
            - Eigenvector centrality values for second graph
            - Average absolute difference in centrality values
        """
        centrality1 = self.compute_eigenvector_centrality(self.graph1)
        centrality2 = self.compute_eigenvector_centrality(self.graph2)
        
        # Calculate average absolute difference in centrality values
        all_nodes = set(centrality1.keys()) | set(centrality2.keys())
        
        if not all_nodes:
            return {}, {}, 0.0
            
        total_diff = 0.0
        for node in all_nodes:
            val1 = centrality1.get(node, 0.0)
            val2 = centrality2.get(node, 0.0)
            total_diff += abs(val1 - val2)
            
        avg_distance = total_diff / len(all_nodes)
        
        return centrality1, centrality2, avg_distance
        
##########################################

from typing import Dict, List, Tuple, Set
from copy import deepcopy
from math import sqrt

class KatzCentralityDistance(Distance):
    """
    A class to calculate the Katz Centrality distance between two weighted graphs.
    Katz Centrality measures node importance considering all possible paths, with 
    longer paths having geometrically decreasing weights.
    
    Attributes:
        graph1 (Dict[str, Dict[str, float]]): First weighted graph represented as adjacency dict
        graph2 (Dict[str, Dict[str, float]]): Second weighted graph represented as adjacency dict
        alpha (float): Damping factor (attenuation factor for path lengths)
        beta (float): Base constant for centrality
        max_iterations (int): Maximum number of iterations for convergence
        tolerance (float): Convergence tolerance
    """
    
    def __init__(self, 
                 graph1: Dict[str, Dict[str, float]], 
                 graph2: Dict[str, Dict[str, float]],
                 alpha: float = 0.1,
                 beta: float = 1.0,
                 max_iterations: int = 100,
                 tolerance: float = 1e-6):
        """
        Initialize the KatzCentrality calculator with two weighted graphs.
        
        Args:
            graph1: First weighted graph as adjacency dictionary
            graph2: Second weighted graph as adjacency dictionary
            alpha: Damping factor (should be less than reciprocal of largest eigenvalue)
            beta: Base constant added to each node's centrality
            max_iterations: Maximum number of iterations
            tolerance: Convergence tolerance
        """      
        super().__init__()
        self.type='graph'
        
        self.graph1 = deepcopy(graph1)
        self.graph2 = deepcopy(graph2)
        self.alpha = alpha
        self.beta = beta
        self.max_iterations = max_iterations
        self.tolerance = tolerance
    
    def normalize_vector(self, vector: Dict[str, float]) -> Dict[str, float]:
        """
        Normalize a vector using L2 norm.
        
        Args:
            vector: Dictionary representing a vector
            
        Returns:
            Normalized vector
        """
        norm = sqrt(sum(x * x for x in vector.values()))
        if norm > 0:
            return {k: v / norm for k, v in vector.items()}
        return vector
    
    def matrix_vector_multiply(self, 
                             graph: Dict[str, Dict[str, float]], 
                             vector: Dict[str, float]) -> Dict[str, float]:
        """
        Multiply adjacency matrix by vector.
        
        Args:
            graph: Weighted graph as adjacency dictionary
            vector: Vector to multiply with
            
        Returns:
            Result vector of the multiplication
        """
        result = {node: 0.0 for node in graph}
        
        for node in graph:
            for neighbor, weight in graph[node].items():
                result[node] += weight * vector[neighbor]
                
        return result
    
    def compute_katz_centrality(self, 
                              graph: Dict[str, Dict[str, float]]) -> Dict[str, float]:
        """
        Compute Katz centrality for all nodes using power iteration method.
        
        Args:
            graph: Weighted graph as adjacency dictionary
            
        Returns:
            Dictionary of Katz centrality values for each node
        """
        if not graph:
            return {}
            
        # Initialize centrality with beta values
        centrality = {node: self.beta for node in graph}
        
        for iteration in range(self.max_iterations):
            # Store previous iteration for convergence check
            prev_centrality = centrality.copy()
            
            # Compute new centralities
            new_centrality = self.matrix_vector_multiply(graph, centrality)
            
            # Apply damping factor and add base constant
            centrality = {
                node: self.alpha * new_centrality[node] + self.beta 
                for node in graph
            }
            
            # Check for convergence
            diff = sum((centrality[node] - prev_centrality[node]) ** 2 
                      for node in centrality)
            if sqrt(diff) < self.tolerance:
                break
        
        # Normalize final values
        return self.normalize_vector(centrality)
    
    def estimate_largest_eigenvalue(self, graph: Dict[str, Dict[str, float]]) -> float:
        """
        Estimate the largest eigenvalue of the adjacency matrix using power iteration.
        
        Args:
            graph: Weighted graph as adjacency dictionary
            
        Returns:
            Estimated largest eigenvalue
        """
        if not graph:
            return 0.0
            
        # Initialize random vector
        vector = {node: 1.0 for node in graph}
        vector = self.normalize_vector(vector)
        
        for _ in range(10):  # Few iterations for estimation
            new_vector = self.matrix_vector_multiply(graph, vector)
            new_vector = self.normalize_vector(new_vector)
            vector = new_vector
        
        # Rayleigh quotient
        Ax = self.matrix_vector_multiply(graph, vector)
        numerator = sum(vector[node] * Ax[node] for node in graph)
        denominator = sum(vector[node] * vector[node] for node in graph)
        
        return numerator / denominator if denominator > 0 else 0.0
    
    def calculate_distance(self) -> Tuple[Dict[str, float], Dict[str, float], float]:
        """
        Calculate the distance between two graphs based on their Katz centrality distributions.
        
        Returns:
            Tuple containing:
            - Katz centrality values for first graph
            - Katz centrality values for second graph
            - Average absolute difference in centrality values
        """
        # Ensure alpha is small enough for convergence
        eigenvalue1 = self.estimate_largest_eigenvalue(self.graph1)
        eigenvalue2 = self.estimate_largest_eigenvalue(self.graph2)
        max_eigenvalue = max(eigenvalue1, eigenvalue2)
        
        if max_eigenvalue > 0:
            self.alpha = min(self.alpha, 0.9 / max_eigenvalue)
        
        centrality1 = self.compute_katz_centrality(self.graph1)
        centrality2 = self.compute_katz_centrality(self.graph2)
        
        # Calculate average absolute difference in centrality values
        all_nodes = set(centrality1.keys()) | set(centrality2.keys())
        
        if not all_nodes:
            return {}, {}, 0.0
            
        total_diff = 0.0
        for node in all_nodes:
            val1 = centrality1.get(node, 0.0)
            val2 = centrality2.get(node, 0.0)
            total_diff += abs(val1 - val2)
            
        avg_distance = total_diff / len(all_nodes)
        
        return centrality1, centrality2, avg_distance
        


from typing import Dict, List, Tuple, Set
from copy import deepcopy

class PageRankDistance(Distance):
    """
    A class to calculate the PageRank distance between two weighted graphs.
    PageRank measures node importance based on the structure of incoming links
    and their weights.
    
    Attributes:
        graph1 (Dict[str, Dict[str, float]]): First weighted graph represented as adjacency dict
        graph2 (Dict[str, Dict[str, float]]): Second weighted graph represented as adjacency dict
        damping_factor (float): Random walk continuation probability
        max_iterations (int): Maximum number of iterations for convergence
        tolerance (float): Convergence tolerance
    """
    
    def __init__(self, 
                 graph1: Dict[str, Dict[str, float]], 
                 graph2: Dict[str, Dict[str, float]],
                 damping_factor: float = 0.85,
                 max_iterations: int = 100,
                 tolerance: float = 1e-6):
        """
        Initialize the PageRank calculator with two weighted graphs.
        
        Args:
            graph1: First weighted graph as adjacency dictionary
            graph2: Second weighted graph as adjacency dictionary
            damping_factor: Probability of continuing the random walk (typically 0.85)
            max_iterations: Maximum number of iterations
            tolerance: Convergence tolerance
        """      
        super().__init__()
        self.type='graph'
        
        self.graph1 = deepcopy(graph1)
        self.graph2 = deepcopy(graph2)
        self.damping_factor = damping_factor
        self.max_iterations = max_iterations
        self.tolerance = tolerance
    
    def normalize_weights(self, graph: Dict[str, Dict[str, float]]) -> Dict[str, Dict[str, float]]:
        """
        Normalize edge weights so outgoing weights from each node sum to 1.
        
        Args:
            graph: Weighted graph as adjacency dictionary
            
        Returns:
            Graph with normalized weights
        """
        normalized = deepcopy(graph)
        
        for node in normalized:
            total_weight = sum(normalized[node].values())
            if total_weight > 0:
                normalized[node] = {
                    neighbor: weight / total_weight 
                    for neighbor, weight in normalized[node].items()
                }
                
        return normalized
    
    def get_incoming_edges(self, 
                          graph: Dict[str, Dict[str, float]]) -> Dict[str, Dict[str, float]]:
        """
        Create a dictionary of incoming edges for each node.
        
        Args:
            graph: Weighted graph as adjacency dictionary
            
        Returns:
            Dictionary mapping nodes to their incoming edges and weights
        """
        incoming = {node: {} for node in graph}
        
        for source in graph:
            for target, weight in graph[source].items():
                if target not in incoming:
                    incoming[target] = {}
                incoming[target][source] = weight
                
        return incoming
    
    def compute_pagerank(self, graph: Dict[str, Dict[str, float]]) -> Dict[str, float]:
        """
        Compute PageRank values for all nodes in the graph.
        
        Args:
            graph: Weighted graph as adjacency dictionary
            
        Returns:
            Dictionary of PageRank values for each node
        """
        if not graph:
            return {}
            
        # Normalize weights
        normalized_graph = self.normalize_weights(graph)
        
        # Get incoming edges for efficient updates
        incoming = self.get_incoming_edges(normalized_graph)
        
        # Initialize PageRank values
        n = len(graph)
        pagerank = {node: 1.0 / n for node in graph}
        
        # Random jump probability distribution
        base_probability = (1 - self.damping_factor) / n
        
        for iteration in range(self.max_iterations):
            prev_pagerank = pagerank.copy()
            
            # Update PageRank for each node
            for node in graph:
                rank_sum = sum(
                    prev_pagerank[source] * weight 
                    for source, weight in incoming[node].items()
                )
                
                pagerank[node] = base_probability + self.damping_factor * rank_sum
            
            # Check for convergence
            diff = sum(abs(pagerank[node] - prev_pagerank[node]) 
                      for node in pagerank)
            if diff < self.tolerance:
                break
        
        return pagerank
    
    def handle_dangling_nodes(self, graph: Dict[str, Dict[str, float]]) -> Dict[str, Dict[str, float]]:
        """
        Handle dangling nodes (nodes with no outgoing edges) by adding uniform
        transitions to all other nodes.
        
        Args:
            graph: Weighted graph as adjacency dictionary
            
        Returns:
            Graph with handled dangling nodes
        """
        modified_graph = deepcopy(graph)
        n = len(graph)
        
        for node in graph:
            if not graph[node]:  # If node has no outgoing edges
                modified_graph[node] = {
                    other_node: 1.0 / (n - 1)
                    for other_node in graph
                    if other_node != node
                }
                
        return modified_graph
    
    def compute(self) -> Tuple[Dict[str, float], Dict[str, float], float]:
        """
        Calculate the distance between two graphs based on their PageRank distributions.
        
        Returns:
            Tuple containing:
            - PageRank values for first graph
            - PageRank values for second graph
            - Average absolute difference in PageRank values
        """
        # Handle dangling nodes
        graph1_modified = self.handle_dangling_nodes(self.graph1)
        graph2_modified = self.handle_dangling_nodes(self.graph2)
        
        # Compute PageRank for both graphs
        pagerank1 = self.compute_pagerank(graph1_modified)
        pagerank2 = self.compute_pagerank(graph2_modified)
        
        # Calculate average absolute difference in PageRank values
        all_nodes = set(pagerank1.keys()) | set(pagerank2.keys())
        
        if not all_nodes:
            return {}, {}, 0.0
            
        total_diff = 0.0
        for node in all_nodes:
            val1 = pagerank1.get(node, 0.0)
            val2 = pagerank2.get(node, 0.0)
            total_diff += abs(val1 - val2)
            
        avg_distance = total_diff / len(all_nodes)
        
        return pagerank1, pagerank2, avg_distance
        


##########################################
from typing import Dict, List, Tuple, Set, DefaultDict
from collections import defaultdict
from copy import deepcopy
from math import inf
import heapq

class EdgeBetweennessDistance(Distance):
    """
    A class to calculate the Edge Betweenness distance between two weighted graphs.
    Edge Betweenness measures the number of shortest paths passing through each edge.
    
    Attributes:
        graph1 (Dict[str, Dict[str, float]]): First weighted graph represented as adjacency dict
        graph2 (Dict[str, Dict[str, float]]): Second weighted graph represented as adjacency dict
    """
    
    def __init__(self, graph1: Dict[str, Dict[str, float]], graph2: Dict[str, Dict[str, float]]):
        """
        Initialize the EdgeBetweenness calculator with two weighted graphs.
        
        Args:
            graph1: First weighted graph as adjacency dictionary
            graph2: Second weighted graph as adjacency dictionary
        """      
        super().__init__()
        self.type='graph'
        
        self.graph1 = deepcopy(graph1)
        self.graph2 = deepcopy(graph2)
    
    def dijkstra_with_paths(self, 
                           graph: Dict[str, Dict[str, float]], 
                           start: str) -> Tuple[Dict[str, float], Dict[str, List[List[str]]]]:
        """
        Compute shortest paths from start node to all other nodes using Dijkstra's algorithm.
        
        Args:
            graph: Weighted graph as adjacency dictionary
            start: Starting node
            
        Returns:
            Tuple containing:
            - Dictionary of shortest distances
            - Dictionary mapping each node to its list of shortest paths from start
        """
        distances = {node: inf for node in graph}
        distances[start] = 0
        
        # Initialize paths
        paths: DefaultDict[str, List[List[str]]] = defaultdict(list)
        paths[start] = [[start]]
        
        # Priority queue for Dijkstra
        pq = [(0, start)]
        visited = set()
        
        while pq:
            current_distance, current = heapq.heappop(pq)
            
            if current in visited:
                continue
                
            visited.add(current)
            
            for neighbor, weight in graph[current].items():
                distance = current_distance + weight
                
                if distance < distances[neighbor]:
                    # New shortest path found
                    distances[neighbor] = distance
                    paths[neighbor] = [path + [neighbor] for path in paths[current]]
                    heapq.heappush(pq, (distance, neighbor))
                elif distance == distances[neighbor]:
                    # Additional shortest path found
                    paths[neighbor].extend(path + [neighbor] for path in paths[current])
        
        return distances, paths
    
    def compute_edge_betweenness(self, graph: Dict[str, Dict[str, float]]) -> Dict[Tuple[str, str], float]:
        """
        Compute edge betweenness centrality for all edges.
        
        Args:
            graph: Weighted graph as adjacency dictionary
            
        Returns:
            Dictionary mapping edge tuples to their betweenness values
        """
        betweenness: DefaultDict[Tuple[str, str], float] = defaultdict(float)
        n = len(graph)
        
        if n < 2:
            return dict(betweenness)
        
        # Compute shortest paths from each node
        for start in graph:
            _, paths = self.dijkstra_with_paths(graph, start)
            
            # Count paths through each edge
            for target in graph:
                if target == start:
                    continue
                    
                num_paths = len(paths[target])
                if num_paths == 0:
                    continue
                    
                # Calculate contribution of each path
                contribution = 1.0 / num_paths
                
                # Add contribution to each edge in each path
                for path in paths[target]:
                    for i in range(len(path) - 1):
                        edge = tuple(sorted([path[i], path[i + 1]]))
                        betweenness[edge] += contribution
        
        # Normalize by number of possible paths
        normalization = (n - 1) * (n - 2)
        if normalization > 0:
            betweenness = {
                edge: value / normalization 
                for edge, value in betweenness.items()
            }
        
        return dict(betweenness)
    
    def compute(self) -> Tuple[Dict[Tuple[str, str], float], 
                                        Dict[Tuple[str, str], float], 
                                        float]:
        """
        Calculate the distance between two graphs based on their edge betweenness distributions.
        
        Returns:
            Tuple containing:
            - Edge betweenness values for first graph
            - Edge betweenness values for second graph
            - Average absolute difference in edge betweenness values
        """
        betweenness1 = self.compute_edge_betweenness(self.graph1)
        betweenness2 = self.compute_edge_betweenness(self.graph2)
        
        # Get all edges from both graphs
        all_edges = set(betweenness1.keys()) | set(betweenness2.keys())
        
        if not all_edges:
            return {}, {}, 0.0
            
        # Calculate average absolute difference in betweenness values
        total_diff = 0.0
        for edge in all_edges:
            val1 = betweenness1.get(edge, 0.0)
            val2 = betweenness2.get(edge, 0.0)
            total_diff += abs(val1 - val2)
            
        avg_distance = total_diff / len(all_edges)
        
        return betweenness1, betweenness2, avg_distance


#################################
from typing import Dict, Set, Tuple, List
from copy import deepcopy

class EdgeWeightDistance(Distance):
    """
    A class to calculate the distance between two weighted graphs based on edge weights.
    Compares the weights of corresponding edges and handles cases where edges exist
    in one graph but not the other.
    
    Attributes:
        graph1 (Dict[str, Dict[str, float]]): First weighted graph represented as adjacency dict
        graph2 (Dict[str, Dict[str, float]]): Second weighted graph represented as adjacency dict
    """
    
    def __init__(self, graph1: Dict[str, Dict[str, float]], graph2: Dict[str, Dict[str, float]]):
        """
        Initialize the EdgeWeight calculator with two weighted graphs.
        
        Args:
            graph1: First weighted graph as adjacency dictionary
            graph2: Second weighted graph as adjacency dictionary
        """      
        super().__init__()
        self.type='graph'
        
        self.graph1 = deepcopy(graph1)
        self.graph2 = deepcopy(graph2)
    
    def get_all_edges(self, graph: Dict[str, Dict[str, float]]) -> Set[Tuple[str, str]]:
        """
        Get all unique edges from a graph.
        
        Args:
            graph: Weighted graph as adjacency dictionary
            
        Returns:
            Set of tuples representing edges (sorted node pairs)
        """
        edges = set()
        for source in graph:
            for target in graph[source]:
                # Store edges as sorted tuples to ensure consistent representation
                edge = tuple(sorted([source, target]))
                edges.add(edge)
        return edges
    
    def get_edge_weight(self, 
                       graph: Dict[str, Dict[str, float]], 
                       edge: Tuple[str, str]) -> float:
        """
        Get the weight of an edge in the graph.
        
        Args:
            graph: Weighted graph as adjacency dictionary
            edge: Tuple of (source, target) nodes
            
        Returns:
            Edge weight or 0.0 if edge doesn't exist
        """
        node1, node2 = edge
        if node1 in graph and node2 in graph[node1]:
            return graph[node1][node2]
        if node2 in graph and node1 in graph[node2]:
            return graph[node2][node1]
        return 0.0
    
    def get_edge_statistics(self, graph: Dict[str, Dict[str, float]]) -> Dict[str, float]:
        """
        Calculate various statistics about edge weights in the graph.
        
        Args:
            graph: Weighted graph as adjacency dictionary
            
        Returns:
            Dictionary containing edge weight statistics
        """
        weights = []
        for source in graph:
            weights.extend(graph[source].values())
            
        if not weights:
            return {
                'min': 0.0,
                'max': 0.0,
                'avg': 0.0,
                'total': 0.0,
                'count': 0
            }
            
        return {
            'min': min(weights),
            'max': max(weights),
            'avg': sum(weights) / len(weights),
            'total': sum(weights),
            'count': len(weights)
        }
    
    def calculate_absolute_distance(self) -> Tuple[Dict[Tuple[str, str], float], float]:
        """
        Calculate absolute differences between edge weights.
        
        Returns:
            Tuple containing:
            - Dictionary mapping edges to their weight differences
            - Average absolute difference across all edges
        """
        edges1 = self.get_all_edges(self.graph1)
        edges2 = self.get_all_edges(self.graph2)
        all_edges = edges1 | edges2
        
        edge_differences = {}
        total_difference = 0.0
        
        for edge in all_edges:
            weight1 = self.get_edge_weight(self.graph1, edge)
            weight2 = self.get_edge_weight(self.graph2, edge)
            difference = abs(weight1 - weight2)
            edge_differences[edge] = difference
            total_difference += difference
            
        avg_difference = total_difference / len(all_edges) if all_edges else 0.0
        
        return edge_differences, avg_difference
    
    def compute(self) -> Tuple[Dict[str, float], Dict[str, float], Dict[str, float]]:
        """
        Calculate comprehensive distance metrics between the two graphs.
        
        Returns:
            Tuple containing:
            - Statistics for first graph
            - Statistics for second graph
            - Dictionary of distance metrics
        """
        # Get statistics for both graphs
        stats1 = self.get_edge_statistics(self.graph1)
        stats2 = self.get_edge_statistics(self.graph2)
        
        # Calculate edge-by-edge differences
        differences, avg_difference = self.calculate_absolute_distance()
        
        # Calculate additional distance metrics
        metrics = {
            'average_absolute_difference': avg_difference,
            'total_weight_difference': abs(stats1['total'] - stats2['total']),
            'max_weight_difference': abs(stats1['max'] - stats2['max']),
            'edge_count_difference': abs(stats1['count'] - stats2['count']),
            'average_weight_difference': abs(stats1['avg'] - stats2['avg']),
            'number_of_different_edges': len(differences)
        }
        
        return stats1, stats2, metrics
        

##########################################
from typing import Dict, Set

class GraphDensity(Distance):
    """
    A class to calculate and compare graph densities for weighted graphs.
    Graphs are represented as adjacency lists using nested dictionaries.
    
    Graph structure format:
    {
        'node1': {'node2': weight1, 'node3': weight2, ...},
        'node2': {'node1': weight1, 'node4': weight3, ...},
        ...
    }
    """
    
    def __init__(self) -> None:
        """Initialize the GraphDensity calculator."""      
        super().__init__()
        self.type='graph'
            
    def get_nodes(self, graph: Dict[str, Dict[str, float]]) -> Set[str]:
        """
        Extract all unique nodes from the graph.
        
        Args:
            graph (Dict[str, Dict[str, float]]): Input graph as adjacency list
            
        Returns:
            Set[str]: Set of all unique nodes in the graph
        """
        nodes = set(graph.keys())
        for edges in graph.values():
            nodes.update(edges.keys())
        return nodes
    
    def calculate_density(self, graph: Dict[str, Dict[str, float]]) -> float:
        """
        Calculate the density of a weighted graph.
        Density = number of actual edges / maximum possible edges
        For a directed graph with n vertices, maximum edges = n * (n-1)
        
        Args:
            graph (Dict[str, Dict[str, float]]): Input graph as adjacency list
            
        Returns:
            float: Density value between 0 and 1
        """
        nodes = self.get_nodes(graph)
        n = len(nodes)
        
        if n <= 1:
            return 0.0
        
        # Count actual edges
        actual_edges = sum(len(edges) for edges in graph.values())
        
        # Calculate maximum possible edges for a directed graph
        max_possible_edges = n * (n - 1)
        
        # Compute density
        density = actual_edges / max_possible_edges
        return density
    
    def compute(self, graph1: Dict[str, Dict[str, float]], 
                         graph2: Dict[str, Dict[str, float]]) -> Dict[str, float]:
        """
        Compare the densities of two weighted graphs.
        
        Args:
            graph1 (Dict[str, Dict[str, float]]): First input graph
            graph2 (Dict[str, Dict[str, float]]): Second input graph
            
        Returns:
            Dict[str, float]: Dictionary containing both densities and their difference
        """
        density1 = self.calculate_density(graph1)
        density2 = self.calculate_density(graph2)
        
        return {
            'density_graph1': density1,
            'density_graph2': density2,
            'density_distance': abs(density1 - density2)
        }


########################################
from typing import Dict, List, Set, Tuple
import math

class GraphDiameter(Distance):
    """
    A class to calculate the diameter of weighted graphs and compare diameters between graphs.
    The diameter is defined as the longest shortest path between any two nodes.
    Uses Floyd-Warshall algorithm to compute all-pairs shortest paths.
    
    Graph structure format:
    {
        'node1': {'node2': weight1, 'node3': weight2, ...},
        'node2': {'node1': weight1, 'node4': weight3, ...},
        ...
    }
    """
    
    def __init__(self) -> None:
        """Initialize the GraphDiameter calculator."""      
        super().__init__()
        self.type='graph'
            
    def get_nodes(self, graph: Dict[str, Dict[str, float]]) -> Set[str]:
        """
        Extract all unique nodes from the graph.
        
        Args:
            graph (Dict[str, Dict[str, float]]): Input graph as adjacency list
            
        Returns:
            Set[str]: Set of all unique nodes in the graph
        """
        nodes = set(graph.keys())
        for edges in graph.values():
            nodes.update(edges.keys())
        return nodes
    
    def initialize_distance_matrix(self, graph: Dict[str, Dict[str, float]], 
                                 nodes: List[str]) -> List[List[float]]:
        """
        Initialize the distance matrix for Floyd-Warshall algorithm.
        
        Args:
            graph (Dict[str, Dict[str, float]]): Input graph
            nodes (List[str]): List of all nodes
            
        Returns:
            List[List[float]]: Initial distance matrix
        """
        n = len(nodes)
        # Create node to index mapping
        node_to_idx = {node: idx for idx, node in enumerate(nodes)}
        
        # Initialize with infinity
        dist = [[float('inf')] * n for _ in range(n)]
        
        # Set diagonal to 0
        for i in range(n):
            dist[i][i] = 0
            
        # Fill known distances
        for node1, edges in graph.items():
            for node2, weight in edges.items():
                i, j = node_to_idx[node1], node_to_idx[node2]
                dist[i][j] = weight
                
        return dist
    
    def floyd_warshall(self, graph: Dict[str, Dict[str, float]]) -> Tuple[float, List[str]]:
        """
        Implement Floyd-Warshall algorithm to find all-pairs shortest paths
        and determine the diameter of the graph.
        
        Args:
            graph (Dict[str, Dict[str, float]]): Input graph
            
        Returns:
            Tuple[float, List[str]]: Tuple containing:
                - diameter (float): Length of the longest shortest path
                - path (List[str]): Nodes in the diameter path
        """
        nodes = list(self.get_nodes(graph))
        if not nodes:
            return 0.0, []
            
        n = len(nodes)
        dist = self.initialize_distance_matrix(graph, nodes)
        
        # Store path information
        next_node = [[None] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if dist[i][j] < float('inf'):
                    next_node[i][j] = j
        
        # Floyd-Warshall algorithm
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if dist[i][k] < float('inf') and dist[k][j] < float('inf'):
                        if dist[i][j] > dist[i][k] + dist[k][j]:
                            dist[i][j] = dist[i][k] + dist[k][j]
                            next_node[i][j] = next_node[i][k]
        
        # Find diameter and corresponding path
        diameter = 0.0
        start_idx = end_idx = 0
        
        for i in range(n):
            for j in range(n):
                if dist[i][j] < float('inf') and dist[i][j] > diameter:
                    diameter = dist[i][j]
                    start_idx, end_idx = i, j
        
        # Reconstruct diameter path
        if diameter == 0.0:
            return 0.0, []
            
        path = []
        current = start_idx
        while current is not None and current != end_idx:
            path.append(nodes[current])
            current = next_node[current][end_idx]
        path.append(nodes[end_idx])
        
        return diameter, path
    
    def calculate_diameter(self, graph: Dict[str, Dict[str, float]]) -> Dict[str, any]:
        """
        Calculate the diameter of a weighted graph.
        
        Args:
            graph (Dict[str, Dict[str, float]]): Input graph
            
        Returns:
            Dict[str, any]: Dictionary containing the diameter value and the path
        """
        diameter, path = self.floyd_warshall(graph)
        return {
            'diameter': diameter,
            'diameter_path': path
        }
    
    def compute(self, graph1: Dict[str, Dict[str, float]], 
                         graph2: Dict[str, Dict[str, float]]) -> Dict[str, any]:
        """
        Compare the diameters of two weighted graphs.
        
        Args:
            graph1 (Dict[str, Dict[str, float]]): First input graph
            graph2 (Dict[str, Dict[str, float]]): Second input graph
            
        Returns:
            Dict[str, any]: Dictionary containing both diameters, their paths and difference
        """
        result1 = self.calculate_diameter(graph1)
        result2 = self.calculate_diameter(graph2)
        
        return {
            'diameter_graph1': result1['diameter'],
            'path_graph1': result1['diameter_path'],
            'diameter_graph2': result2['diameter'],
            'path_graph2': result2['diameter_path'],
            'diameter_difference': abs(result1['diameter'] - result2['diameter'])
        }
        


#################################################
from typing import Dict, List, Set, Tuple
from collections import defaultdict

class AveragePathLength(Distance):
    """
    A class to calculate the average path length in weighted graphs and compare
    between graphs. The average path length is the mean of all shortest paths
    between all pairs of nodes in the graph.
    
    Graph structure format:
    {
        'node1': {'node2': weight1, 'node3': weight2, ...},
        'node2': {'node1': weight1, 'node4': weight3, ...},
        ...
    }
    """
    
    def __init__(self) -> None:
        """Initialize the AveragePathLength calculator."""      
        super().__init__()
        self.type='graph'
        
    def get_nodes(self, graph: Dict[str, Dict[str, float]]) -> Set[str]:
        """
        Extract all unique nodes from the graph.
        
        Args:
            graph (Dict[str, Dict[str, float]]): Input graph as adjacency list
            
        Returns:
            Set[str]: Set of all unique nodes in the graph
        """
        nodes = set(graph.keys())
        for edges in graph.values():
            nodes.update(edges.keys())
        return nodes

    def dijkstra(self, graph: Dict[str, Dict[str, float]], 
                 start: str) -> Dict[str, float]:
        """
        Implement Dijkstra's algorithm to find shortest paths from a start node
        to all other nodes.
        
        Args:
            graph (Dict[str, Dict[str, float]]): Input graph
            start (str): Starting node
            
        Returns:
            Dict[str, float]: Dictionary of shortest distances to each node
        """
        nodes = self.get_nodes(graph)
        distances = {node: float('inf') for node in nodes}
        distances[start] = 0
        unvisited = set(nodes)
        
        while unvisited:
            # Find unvisited node with minimum distance
            current = min(unvisited, key=lambda node: distances[node])
            
            if distances[current] == float('inf'):
                break
                
            unvisited.remove(current)
            
            # Update distances to neighbors
            for neighbor, weight in graph.get(current, {}).items():
                if neighbor in unvisited:
                    new_distance = distances[current] + weight
                    if new_distance < distances[neighbor]:
                        distances[neighbor] = new_distance
        
        return distances

    def calculate_average_path(self, graph: Dict[str, Dict[str, float]]) -> Dict[str, float]:
        """
        Calculate the average path length of a weighted graph.
        
        Args:
            graph (Dict[str, Dict[str, float]]): Input graph
            
        Returns:
            Dict[str, float]: Dictionary containing average path length and total paths count
        """
        nodes = list(self.get_nodes(graph))
        if len(nodes) <= 1:
            return {
                'average_path_length': 0.0,
                'total_paths': 0,
                'connected_paths': 0
            }
        
        total_distance = 0.0
        total_possible_paths = len(nodes) * (len(nodes) - 1)  # Excluding self-paths
        connected_paths = 0
        
        # Calculate shortest paths between all pairs
        for start_node in nodes:
            distances = self.dijkstra(graph, start_node)
            for end_node, distance in distances.items():
                if start_node != end_node:  # Exclude self-paths
                    if distance != float('inf'):
                        total_distance += distance
                        connected_paths += 1
        
        # Calculate average path length
        average_length = (total_distance / connected_paths) if connected_paths > 0 else float('inf')
        
        return {
            'average_path_length': average_length,
            'total_possible_paths': total_possible_paths,
            'connected_paths': connected_paths
        }

    def compute(self, graph1: Dict[str, Dict[str, float]], 
                            graph2: Dict[str, Dict[str, float]]) -> Dict[str, float]:
        """
        Compare the average path lengths of two weighted graphs.
        
        Args:
            graph1 (Dict[str, Dict[str, float]]): First input graph
            graph2 (Dict[str, Dict[str, float]]): Second input graph
            
        Returns:
            Dict[str, float]: Dictionary containing both averages and their difference
        """
        result1 = self.calculate_average_path(graph1)
        result2 = self.calculate_average_path(graph2)
        
        return {
            'avg_path_length_graph1': result1['average_path_length'],
            'connected_paths_graph1': result1['connected_paths'],
            'avg_path_length_graph2': result2['average_path_length'],
            'connected_paths_graph2': result2['connected_paths'],
            'avg_length_difference': abs(result1['average_path_length'] - 
                                      result2['average_path_length'])
        }
        


#####################################################

from typing import Dict, Set, List
from itertools import combinations

class ClusteringCoefficient(Distance):
    """
    A class to calculate the clustering coefficient of weighted graphs and compare
    between graphs. The clustering coefficient measures the degree to which nodes
    tend to cluster together.
    
    For weighted graphs, we use a generalized version that takes edge weights
    into account when calculating triangles.
    
    Graph structure format:
    {
        'node1': {'node2': weight1, 'node3': weight2, ...},
        'node2': {'node1': weight1, 'node4': weight3, ...},
        ...
    }
    """
    
    def __init__(self) -> None:
        """Initialize the ClusteringCoefficient calculator."""      
        super().__init__()
        self.type='graph'
        
    def get_neighbors(self, graph: Dict[str, Dict[str, float]], 
                     node: str) -> Set[str]:
        """
        Get all neighbors of a given node.
        
        Args:
            graph (Dict[str, Dict[str, float]]): Input graph
            node (str): Node to find neighbors for
            
        Returns:
            Set[str]: Set of neighboring nodes
        """
        return set(graph.get(node, {}).keys())

    def calculate_node_clustering(self, graph: Dict[str, Dict[str, float]], 
                                node: str) -> float:
        """
        Calculate the clustering coefficient for a single node.
        For weighted graphs, we use the geometric mean of edge weights
        in triangles.
        
        Args:
            graph (Dict[str, Dict[str, float]]): Input graph
            node (str): Node to calculate clustering for
            
        Returns:
            float: Local clustering coefficient for the node
        """
        neighbors = self.get_neighbors(graph, node)
        if len(neighbors) < 2:
            return 0.0
        
        possible_triangles = len(neighbors) * (len(neighbors) - 1) / 2
        if possible_triangles == 0:
            return 0.0
        
        actual_triangles = 0.0
        
        # Check all possible pairs of neighbors
        for n1, n2 in combinations(neighbors, 2):
            # Check if there's an edge between neighbors
            n1_neighbors = self.get_neighbors(graph, n1)
            if n2 in n1_neighbors:
                # Calculate weighted contribution using geometric mean
                weight1 = graph[node][n1]
                weight2 = graph[node][n2]
                weight3 = graph[n1][n2]
                triangle_weight = (weight1 * weight2 * weight3) ** (1/3)
                actual_triangles += triangle_weight
        
        return actual_triangles / possible_triangles

    def calculate_average_clustering(self, graph: Dict[str, Dict[str, float]]) -> Dict[str, float]:
        """
        Calculate the average clustering coefficient for the entire graph.
        
        Args:
            graph (Dict[str, Dict[str, float]]): Input graph
            
        Returns:
            Dict[str, float]: Dictionary containing average clustering coefficient
                             and individual node coefficients
        """
        if not graph:
            return {
                'average_clustering': 0.0,
                'node_coefficients': {},
                'valid_nodes': 0
            }
        
        node_coefficients = {}
        valid_nodes = 0
        
        for node in graph:
            coeff = self.calculate_node_clustering(graph, node)
            node_coefficients[node] = coeff
            if len(self.get_neighbors(graph, node)) > 1:
                valid_nodes += 1
        
        average_clustering = (sum(node_coefficients.values()) / valid_nodes 
                            if valid_nodes > 0 else 0.0)
        
        return {
            'average_clustering': average_clustering,
            'node_coefficients': node_coefficients,
            'valid_nodes': valid_nodes
        }

    def compare_clustering(self, graph1: Dict[str, Dict[str, float]], 
                         graph2: Dict[str, Dict[str, float]]) -> Dict[str, float]:
        """
        Compare the clustering coefficients of two weighted graphs.
        
        Args:
            graph1 (Dict[str, Dict[str, float]]): First input graph
            graph2 (Dict[str, Dict[str, float]]): Second input graph
            
        Returns:
            Dict[str, float]: Dictionary containing both coefficients and their difference
        """
        result1 = self.calculate_average_clustering(graph1)
        result2 = self.calculate_average_clustering(graph2)
        
        return {
            'clustering_graph1': result1['average_clustering'],
            'valid_nodes_graph1': result1['valid_nodes'],
            'clustering_graph2': result2['average_clustering'],
            'valid_nodes_graph2': result2['valid_nodes'],
            'clustering_difference': abs(result1['average_clustering'] - 
                                      result2['average_clustering'])
        }

    def get_highly_clustered_nodes(self, graph: Dict[str, Dict[str, float]], 
                                 threshold: float = 0.7) -> List[str]:
        """
        Find nodes with clustering coefficient above a given threshold.
        
        Args:
            graph (Dict[str, Dict[str, float]]): Input graph
            threshold (float): Minimum clustering coefficient (default: 0.7)
            
        Returns:
            List[str]: List of nodes with high clustering coefficients
        """
        result = self.calculate_average_clustering(graph)
        return [node for node, coeff in result['node_coefficients'].items() 
                if coeff >= threshold]
                


############################################
from typing import Dict, List, Tuple
from collections import defaultdict

class GraphAssortativity(Distance):
    """
    A class to calculate degree assortativity in weighted graphs.
    Assortativity measures the tendency of nodes to connect to nodes with similar degrees.
    Values range from -1 (disassortative) to 1 (assortative).
    
    Graph structure format:
    {
        'node1': {'node2': weight1, 'node3': weight2, ...},
        'node2': {'node1': weight1, 'node4': weight3, ...},
        ...
    }
    """
    
    def __init__(self) -> None:
        """Initialize the GraphAssortativity calculator."""      
        super().__init__()
        self.type='graph'
        
    def calculate_node_degree(self, graph: Dict[str, Dict[str, float]], 
                            weighted: bool = True) -> Dict[str, float]:
        """
        Calculate the degree of each node in the graph.
        For weighted graphs, returns the sum of edge weights.
        
        Args:
            graph (Dict[str, Dict[str, float]]): Input graph
            weighted (bool): If True, use edge weights; if False, count edges
            
        Returns:
            Dict[str, float]: Dictionary mapping nodes to their degrees
        """
        degrees = defaultdict(float)
        
        for node, edges in graph.items():
            if weighted:
                degrees[node] = sum(edges.values())
            else:
                degrees[node] = len(edges)
                
            # Add incoming edges
            for target_node, weight in edges.items():
                if weighted:
                    degrees[target_node] += weight
                else:
                    degrees[target_node] += 1
                    
        return dict(degrees)

    def get_edge_pairs(self, graph: Dict[str, Dict[str, float]]) -> List[Tuple[str, str, float]]:
        """
        Get all edges in the graph as (source, target, weight) tuples.
        
        Args:
            graph (Dict[str, Dict[str, float]]): Input graph
            
        Returns:
            List[Tuple[str, str, float]]: List of edge tuples
        """
        edges = []
        for source, targets in graph.items():
            for target, weight in targets.items():
                edges.append((source, target, weight))
        return edges

    def calculate_assortativity(self, graph: Dict[str, Dict[str, float]], 
                              weighted: bool = True) -> Dict[str, float]:
        """
        Calculate the degree assortativity coefficient of the graph.
        
        Args:
            graph (Dict[str, Dict[str, float]]): Input graph
            weighted (bool): If True, use weighted degrees
            
        Returns:
            Dict[str, float]: Dictionary containing assortativity metrics
        """
        if not graph:
            return {
                'assortativity': 0.0,
                'edge_count': 0,
                'average_degree': 0.0
            }

        # Calculate node degrees
        degrees = self.calculate_node_degree(graph, weighted)
        edges = self.get_edge_pairs(graph)
        
        if not edges:
            return {
                'assortativity': 0.0,
                'edge_count': 0,
                'average_degree': 0.0
            }

        # Calculate sums for assortativity formula
        sum_ji = 0.0  # Sum of source * target degrees
        sum_j = 0.0   # Sum of source degrees
        sum_i = 0.0   # Sum of target degrees
        sum_sq_j = 0.0  # Sum of squared source degrees
        sum_sq_i = 0.0  # Sum of squared target degrees
        
        M = len(edges)  # Number of edges
        
        for source, target, weight in edges:
            source_degree = degrees[source]
            target_degree = degrees[target]
            
            if weighted:
                weight_factor = weight
            else:
                weight_factor = 1.0
                
            sum_ji += source_degree * target_degree * weight_factor
            sum_j += source_degree * weight_factor
            sum_i += target_degree * weight_factor
            sum_sq_j += source_degree * source_degree * weight_factor
            sum_sq_i += target_degree * target_degree * weight_factor

        # Normalize sums
        sum_ji /= M
        sum_j /= M
        sum_i /= M
        sum_sq_j /= M
        sum_sq_i /= M
        
        # Calculate assortativity coefficient
        numerator = sum_ji - sum_j * sum_i
        denominator = (sum_sq_j - sum_j * sum_j) * (sum_sq_i - sum_i * sum_i)
        denominator = denominator ** 0.5  # Square root
        
        assortativity = numerator / denominator if denominator != 0 else 0.0
        
        return {
            'assortativity': assortativity,
            'edge_count': M,
            'average_degree': sum(degrees.values()) / len(degrees)
        }

    def compute(self, graph1: Dict[str, Dict[str, float]], 
                            graph2: Dict[str, Dict[str, float]], 
                            weighted: bool = True) -> Dict[str, float]:
        """
        Compare the assortativity of two graphs.
        
        Args:
            graph1 (Dict[str, Dict[str, float]]): First input graph
            graph2 (Dict[str, Dict[str, float]]): Second input graph
            weighted (bool): If True, use weighted calculations
            
        Returns:
            Dict[str, float]: Dictionary containing comparison metrics
        """
        result1 = self.calculate_assortativity(graph1, weighted)
        result2 = self.calculate_assortativity(graph2, weighted)
        
        return {
            'assortativity_graph1': result1['assortativity'],
            'assortativity_graph2': result2['assortativity'],
            'assortativity_difference': abs(result1['assortativity'] - 
                                          result2['assortativity']),
            'avg_degree_graph1': result1['average_degree'],
            'avg_degree_graph2': result2['average_degree']
        }
        


################################################
from typing import Dict, Set, Tuple
import math

class GlobalEfficiency(Distance):
    """
    A class to calculate the global efficiency of weighted graphs.
    Global efficiency measures how efficiently information is exchanged across the network,
    calculated as the average of the inverse shortest path lengths between all pairs of nodes.
    
    Graph structure format:
    {
        'node1': {'node2': weight1, 'node3': weight2, ...},
        'node2': {'node1': weight1, 'node4': weight3, ...},
        ...
    }
    """
    
    def __init__(self) -> None:
        """Initialize the GlobalEfficiency calculator."""      
        super().__init__()
        self.type='graph'
        
    def get_nodes(self, graph: Dict[str, Dict[str, float]]) -> Set[str]:
        """
        Extract all unique nodes from the graph.
        
        Args:
            graph (Dict[str, Dict[str, float]]): Input graph as adjacency list
            
        Returns:
            Set[str]: Set of all unique nodes in the graph
        """
        nodes = set(graph.keys())
        for edges in graph.values():
            nodes.update(edges.keys())
        return nodes

    def dijkstra(self, graph: Dict[str, Dict[str, float]], 
                 start: str) -> Dict[str, float]:
        """
        Implement Dijkstra's algorithm to find shortest paths from a start node
        to all other nodes.
        
        Args:
            graph (Dict[str, Dict[str, float]]): Input graph
            start (str): Starting node
            
        Returns:
            Dict[str, float]: Dictionary of shortest distances to each node
        """
        nodes = self.get_nodes(graph)
        distances = {node: float('inf') for node in nodes}
        distances[start] = 0
        unvisited = set(nodes)
        
        while unvisited:
            # Find unvisited node with minimum distance
            current = min(unvisited, key=lambda node: distances[node])
            
            if distances[current] == float('inf'):
                break
                
            unvisited.remove(current)
            
            # Update distances to neighbors
            for neighbor, weight in graph.get(current, {}).items():
                if neighbor in unvisited:
                    new_distance = distances[current] + weight
                    if new_distance < distances[neighbor]:
                        distances[neighbor] = new_distance
        
        return distances

    def calculate_global_efficiency(self, graph: Dict[str, Dict[str, float]]) -> Dict[str, float]:
        """
        Calculate the global efficiency of a weighted graph.
        
        Args:
            graph (Dict[str, Dict[str, float]]): Input graph
            
        Returns:
            Dict[str, float]: Dictionary containing efficiency metrics
        """
        nodes = list(self.get_nodes(graph))
        n = len(nodes)
        
        if n <= 1:
            return {
                'global_efficiency': 0.0,
                'average_path_length': float('inf'),
                'connected_pairs': 0
            }

        total_efficiency = 0.0
        total_distance = 0.0
        connected_pairs = 0
        possible_pairs = n * (n - 1)  # Total possible pairs excluding self-pairs
        
        # Calculate shortest paths and efficiencies between all pairs
        for start_node in nodes:
            distances = self.dijkstra(graph, start_node)
            for end_node, distance in distances.items():
                if start_node != end_node:  # Exclude self-pairs
                    if distance != float('inf'):
                        efficiency = 1.0 / distance
                        total_efficiency += efficiency
                        total_distance += distance
                        connected_pairs += 1
        
        # Calculate global efficiency as average of inverse path lengths
        global_efficiency = total_efficiency / possible_pairs if possible_pairs > 0 else 0.0
        
        # Calculate average path length for connected pairs
        average_path_length = (total_distance / connected_pairs 
                             if connected_pairs > 0 else float('inf'))
        
        return {
            'global_efficiency': global_efficiency,
            'average_path_length': average_path_length,
            'connected_pairs': connected_pairs,
            'possible_pairs': possible_pairs,
            'connectivity_ratio': connected_pairs / possible_pairs if possible_pairs > 0 else 0.0
        }

    def calculate_node_efficiency(self, graph: Dict[str, Dict[str, float]], 
                                node: str) -> float:
        """
        Calculate the efficiency of a single node (local efficiency).
        
        Args:
            graph (Dict[str, Dict[str, float]]): Input graph
            node (str): Node to calculate efficiency for
            
        Returns:
            float: Local efficiency of the node
        """
        distances = self.dijkstra(graph, node)
        total_efficiency = 0.0
        valid_pairs = 0
        
        for target, distance in distances.items():
            if target != node and distance != float('inf'):
                total_efficiency += 1.0 / distance
                valid_pairs += 1
                
        return total_efficiency / valid_pairs if valid_pairs > 0 else 0.0

    def compute(self, graph1: Dict[str, Dict[str, float]], 
                         graph2: Dict[str, Dict[str, float]]) -> Dict[str, float]:
        """
        Compare the global efficiency of two weighted graphs.
        
        Args:
            graph1 (Dict[str, Dict[str, float]]): First input graph
            graph2 (Dict[str, Dict[str, float]]): Second input graph
            
        Returns:
            Dict[str, float]: Dictionary containing comparison metrics
        """
        result1 = self.calculate_global_efficiency(graph1)
        result2 = self.calculate_global_efficiency(graph2)
        
        return {
            'efficiency_graph1': result1['global_efficiency'],
            'efficiency_graph2': result2['global_efficiency'],
            'efficiency_difference': abs(result1['global_efficiency'] - 
                                      result2['global_efficiency']),
            'connectivity_ratio_graph1': result1['connectivity_ratio'],
            'connectivity_ratio_graph2': result2['connectivity_ratio']
        }


############################################
from typing import Dict, List, Set, DefaultDict
from collections import defaultdict
import random

class GraphModularity(Distance):
    """
    A class to calculate the modularity of weighted graphs using the Louvain method.
    Modularity measures how well a network is divided into communities.
    Values range from -1 to 1, where higher values indicate better community structure.
    
    Graph structure format:
    {
        'node1': {'node2': weight1, 'node3': weight2, ...},
        'node2': {'node1': weight1, 'node4': weight3, ...},
        ...
    }
    """
    
    def __init__(self) -> None:
        """Initialize the GraphModularity calculator."""      
        super().__init__()
        self.type='graph'
        
        self.MIN_IMPROVEMENT = 1e-6
    
    def get_nodes(self, graph: Dict[str, Dict[str, float]]) -> Set[str]:
        """
        Extract all unique nodes from the graph.
        
        Args:
            graph (Dict[str, Dict[str, float]]): Input graph
            
        Returns:
            Set[str]: Set of all nodes
        """
        nodes = set(graph.keys())
        for edges in graph.values():
            nodes.update(edges.keys())
        return nodes

    def calculate_total_weight(self, graph: Dict[str, Dict[str, float]]) -> float:
        """
        Calculate the total weight of all edges in the graph.
        
        Args:
            graph (Dict[str, Dict[str, float]]): Input graph
            
        Returns:
            float: Total edge weight
        """
        return sum(weight for edges in graph.values() for weight in edges.values())

    def get_node_strength(self, graph: Dict[str, Dict[str, float]], 
                         node: str) -> float:
        """
        Calculate the total weight of edges connected to a node.
        
        Args:
            graph (Dict[str, Dict[str, float]]): Input graph
            node (str): Target node
            
        Returns:
            float: Total weight of connected edges
        """
        strength = sum(graph.get(node, {}).values())
        # Add incoming edges
        strength += sum(edges[node] for edges in graph.values() if node in edges)
        return strength

    def initialize_communities(self, nodes: Set[str]) -> Dict[str, str]:
        """
        Initialize each node in its own community.
        
        Args:
            nodes (Set[str]): Set of all nodes
            
        Returns:
            Dict[str, str]: Mapping of nodes to their communities
        """
        return {node: str(idx) for idx, node in enumerate(nodes)}

    def calculate_modularity(self, graph: Dict[str, Dict[str, float]], 
                           communities: Dict[str, str]) -> float:
        """
        Calculate the modularity of the graph given a community assignment.
        
        Args:
            graph (Dict[str, Dict[str, float]]): Input graph
            communities (Dict[str, str]): Node to community mapping
            
        Returns:
            float: Modularity value
        """
        total_weight = self.calculate_total_weight(graph)
        if total_weight == 0:
            return 0.0
        
        modularity = 0.0
        
        for node1, edges in graph.items():
            node1_strength = self.get_node_strength(graph, node1)
            
            for node2, weight in edges.items():
                node2_strength = self.get_node_strength(graph, node2)
                expected = node1_strength * node2_strength / (2 * total_weight)
                
                if communities[node1] == communities[node2]:
                    modularity += weight - expected
                    
        return modularity / (2 * total_weight)

    def find_communities(self, graph: Dict[str, Dict[str, float]], 
                        max_iterations: int = 100) -> Dict[str, any]:
        """
        Find communities using the Louvain method.
        
        Args:
            graph (Dict[str, Dict[str, float]]): Input graph
            max_iterations (int): Maximum number of iterations
            
        Returns:
            Dict[str, any]: Dictionary containing community assignments and metrics
        """
        nodes = self.get_nodes(graph)
        communities = self.initialize_communities(nodes)
        
        total_weight = self.calculate_total_weight(graph)
        if total_weight == 0:
            return {
                'communities': communities,
                'modularity': 0.0,
                'num_communities': len(set(communities.values())),
                'iterations': 0
            }
        
        best_modularity = self.calculate_modularity(graph, communities)
        iteration = 0
        improved = True
        
        while improved and iteration < max_iterations:
            improved = False
            iteration += 1
            
            # Randomize node order for each iteration
            nodes_list = list(nodes)
            random.shuffle(nodes_list)
            
            for node in nodes_list:
                # Find best community for this node
                current_community = communities[node]
                best_gain = 0.0
                best_community = current_community
                
                # Calculate gains for moving to each neighbor's community
                neighbor_communities = set()
                for neighbor in graph.get(node, {}):
                    neighbor_communities.add(communities[neighbor])
                
                for target_community in neighbor_communities:
                    if target_community != current_community:
                        # Temporarily move node to new community
                        communities[node] = target_community
                        new_modularity = self.calculate_modularity(graph, communities)
                        gain = new_modularity - best_modularity
                        
                        if gain > best_gain:
                            best_gain = gain
                            best_community = target_community
                        
                        # Move back to original community
                        communities[node] = current_community
                
                # Make the best move if it improves modularity
                if best_gain > self.MIN_IMPROVEMENT:
                    communities[node] = best_community
                    best_modularity = best_modularity + best_gain
                    improved = True
        
        return {
            'communities': communities,
            'modularity': best_modularity,
            'num_communities': len(set(communities.values())),
            'iterations': iteration
        }

    def compute(self, graph1: Dict[str, Dict[str, float]], 
                          graph2: Dict[str, Dict[str, float]]) -> Dict[str, float]:
        """
        Compare the modularity of two graphs.
        
        Args:
            graph1 (Dict[str, Dict[str, float]]): First input graph
            graph2 (Dict[str, Dict[str, float]]): Second input graph
            
        Returns:
            Dict[str, float]: Dictionary containing comparison metrics
        """
        result1 = self.find_communities(graph1)
        result2 = self.find_communities(graph2)
        
        return {
            'modularity_graph1': result1['modularity'],
            'modularity_graph2': result2['modularity'],
            'modularity_difference': abs(result1['modularity'] - result2['modularity']),
            'communities_graph1': result1['num_communities'],
            'communities_graph2': result2['num_communities']
        }


###################################################
from typing import Dict, List, Set, Tuple, Optional
from collections import defaultdict
import random
import math

class ModularityOptimization(Distance):
    """
    A class to optimize community detection in weighted graphs using multiple
    methods and metrics. Implements several optimization strategies to find
    the best community structure.
    
    Graph structure format:
    {
        'node1': {'node2': weight1, 'node3': weight2, ...},
        'node2': {'node1': weight1, 'node4': weight3, ...},
        ...
    }
    """
    
    def __init__(self) -> None:
        """Initialize the ModularityOptimization calculator."""      
        super().__init__()
        self.type='graph'
        
        self.MIN_IMPROVEMENT = 1e-6
        self.MAX_ITERATIONS = 100
    
    def get_nodes(self, graph: Dict[str, Dict[str, float]]) -> Set[str]:
        """
        Extract all unique nodes from the graph.
        
        Args:
            graph (Dict[str, Dict[str, float]]): Input graph
            
        Returns:
            Set[str]: Set of all nodes
        """
        nodes = set(graph.keys())
        for edges in graph.values():
            nodes.update(edges.keys())
        return nodes

    def calculate_edge_weights(self, graph: Dict[str, Dict[str, float]]) -> Dict[str, float]:
        """
        Calculate total edge weights for each node.
        
        Args:
            graph (Dict[str, Dict[str, float]]): Input graph
            
        Returns:
            Dict[str, float]: Dictionary of node weights
        """
        weights = defaultdict(float)
        for node, edges in graph.items():
            weights[node] = sum(edges.values())
            # Add incoming edges
            for source, targets in graph.items():
                if node in targets:
                    weights[node] += targets[node]
        return dict(weights)

    def calculate_modularity_gain(self, graph: Dict[str, Dict[str, float]],
                                node: str,
                                community: str,
                                communities: Dict[str, str],
                                total_weight: float,
                                node_weights: Dict[str, float]) -> float:
        """
        Calculate the modularity gain for moving a node to a community.
        
        Args:
            graph (Dict[str, Dict[str, float]]): Input graph
            node (str): Node to move
            community (str): Target community
            communities (Dict[str, str]): Current community assignments
            total_weight (float): Total edge weight in graph
            node_weights (Dict[str, float]): Precomputed node weights
            
        Returns:
            float: Modularity gain
        """
        k_i = node_weights[node]
        k_i_in = 0.0
        
        # Calculate connections to target community
        for neighbor, weight in graph.get(node, {}).items():
            if communities[neighbor] == community:
                k_i_in += weight
        
        # Add incoming edges
        for source, edges in graph.items():
            if node in edges and communities[source] == community:
                k_i_in += edges[node]
        
        # Calculate total weight of target community
        k_c = sum(node_weights[n] for n, c in communities.items() if c == community)
        
        return (k_i_in - k_i * k_c / (2 * total_weight))

    def optimize_communities(self, graph: Dict[str, Dict[str, float]], 
                           initial_communities: Optional[Dict[str, str]] = None,
                           method: str = "louvain") -> Dict[str, any]:
        """
        Optimize community assignments using specified method.
        
        Args:
            graph (Dict[str, Dict[str, float]]): Input graph
            initial_communities (Optional[Dict[str, str]]): Initial community assignments
            method (str): Optimization method ("louvain" or "fast_greedy")
            
        Returns:
            Dict[str, any]: Optimization results
        """
        nodes = self.get_nodes(graph)
        if initial_communities is None:
            initial_communities = {node: str(i) for i, node in enumerate(nodes)}
            
        total_weight = sum(sum(edges.values()) for edges in graph.values())
        node_weights = self.calculate_edge_weights(graph)
        
        communities = initial_communities.copy()
        best_modularity = self.calculate_total_modularity(graph, communities)
        
        iterations = 0
        improved = True
        
        while improved and iterations < self.MAX_ITERATIONS:
            improved = False
            iterations += 1
            
            if method == "louvain":
                improved = self._louvain_iteration(graph, communities, total_weight, 
                                                 node_weights, best_modularity)
            elif method == "fast_greedy":
                improved = self._fast_greedy_iteration(graph, communities, total_weight, 
                                                     node_weights, best_modularity)
            
            if improved:
                best_modularity = self.calculate_total_modularity(graph, communities)
        
        # Calculate additional quality metrics
        metrics = self.calculate_quality_metrics(graph, communities)
        
        return {
            'communities': communities,
            'modularity': best_modularity,
            'num_communities': len(set(communities.values())),
            'iterations': iterations,
            'quality_metrics': metrics
        }

    def _louvain_iteration(self, graph: Dict[str, Dict[str, float]], 
                          communities: Dict[str, str],
                          total_weight: float,
                          node_weights: Dict[str, float],
                          current_modularity: float) -> bool:
        """
        Perform one iteration of Louvain optimization.
        
        Args:
            graph (Dict[str, Dict[str, float]]): Input graph
            communities (Dict[str, str]): Current community assignments
            total_weight (float): Total edge weight
            node_weights (Dict[str, float]): Node weights
            current_modularity (float): Current modularity value
            
        Returns:
            bool: True if improvements were made
        """
        improved = False
        nodes = list(self.get_nodes(graph))
        random.shuffle(nodes)
        
        for node in nodes:
            current_community = communities[node]
            best_community = current_community
            best_gain = 0
            
            # Try moving to neighboring communities
            neighbor_communities = set()
            for neighbor in graph.get(node, {}):
                neighbor_communities.add(communities[neighbor])
            
            for target_community in neighbor_communities:
                if target_community != current_community:
                    gain = self.calculate_modularity_gain(
                        graph, node, target_community, communities,
                        total_weight, node_weights
                    )
                    
                    if gain > best_gain:
                        best_gain = gain
                        best_community = target_community
            
            if best_gain > self.MIN_IMPROVEMENT:
                communities[node] = best_community
                improved = True
        
        return improved

    def calculate_quality_metrics(self, graph: Dict[str, Dict[str, float]], 
                                communities: Dict[str, str]) -> Dict[str, float]:
        """
        Calculate various quality metrics for community assignment.
        
        Args:
            graph (Dict[str, Dict[str, float]]): Input graph
            communities (Dict[str, str]): Community assignments
            
        Returns:
            Dict[str, float]: Quality metrics
        """
        # Calculate internal density of communities
        internal_density = defaultdict(float)
        external_density = defaultdict(float)
        community_sizes = defaultdict(int)
        
        for node, edges in graph.items():
            comm = communities[node]
            community_sizes[comm] += 1
            
            for target, weight in edges.items():
                if communities[target] == comm:
                    internal_density[comm] += weight
                else:
                    external_density[comm] += weight
        
        # Calculate metrics
        conductance = sum(
            external_density[c] / (internal_density[c] + external_density[c])
            for c in community_sizes if internal_density[c] + external_density[c] > 0
        ) / len(community_sizes) if community_sizes else 0
        
        coverage = sum(internal_density.values()) / (
            sum(internal_density.values()) + sum(external_density.values())
        ) if sum(internal_density.values()) + sum(external_density.values()) > 0 else 0
        
        return {
            'conductance': conductance,
            'coverage': coverage,
            'num_communities': len(community_sizes),
            'avg_community_size': sum(community_sizes.values()) / len(community_sizes)
                if community_sizes else 0
        }

    def calculate_total_modularity(self, graph: Dict[str, Dict[str, float]], 
                                 communities: Dict[str, str]) -> float:
        """
        Calculate total modularity of the graph.
        
        Args:
            graph (Dict[str, Dict[str, float]]): Input graph
            communities (Dict[str, str]): Community assignments
            
        Returns:
            float: Total modularity value
        """
        total_weight = sum(sum(edges.values()) for edges in graph.values())
        if total_weight == 0:
            return 0.0
            
        node_weights = self.calculate_edge_weights(graph)
        modularity = 0.0
        
        for node1, edges in graph.items():
            for node2, weight in edges.items():
                if communities[node1] == communities[node2]:
                    expected = node_weights[node1] * node_weights[node2] / (2 * total_weight)
                    modularity += weight - expected
                    
        return modularity / (2 * total_weight)
        


#############################################

from typing import Dict, Set, List, Optional
from collections import defaultdict

class ConductanceCalculator(Distance):
    """
    A class to calculate conductance-based distances between two weighted graphs.
    Graphs are represented as nested dictionaries where:
    - Outer key: source node
    - Inner key: target node
    - Value: edge weight
    
    Conductance measures how well-knit a community is by comparing internal 
    and external connections.
    """
    
    def __init__(self) -> None:
        """Initialize the conductance calculator."""      
        super().__init__()
        self.type='graph'
                
    def get_community_nodes(self, communities: Dict[str, int], 
                           community_id: int) -> Set[str]:
        """
        Get all nodes belonging to a specific community.
        
        Args:
            communities: Dictionary mapping node names to community IDs
            community_id: The ID of the community to extract
            
        Returns:
            Set of node names belonging to the specified community
        """
        return {node for node, comm_id in communities.items() if comm_id == community_id}
    
    def calculate_edge_weights(self, graph: Dict[str, Dict[str, float]], 
                             community: Set[str]) -> tuple[float, float]:
        """
        Calculate internal and external edge weights for a community.
        
        Args:
            graph: Weighted graph
            community: Set of nodes in the community
            
        Returns:
            Tuple of (internal_edge_weights, external_edge_weights)
        """
        internal_weights = 0.0
        external_weights = 0.0
        
        for node in community:
            if node not in graph:
                continue
                
            for neighbor, weight in graph[node].items():
                if neighbor in community:
                    # Count internal edges only once (undirected graph)
                    internal_weights += weight / 2
                else:
                    external_weights += weight
                    
        return internal_weights, external_weights
    
    def calculate_community_conductance(self, graph: Dict[str, Dict[str, float]], 
                                     community: Set[str]) -> float:
        """
        Calculate conductance for a single community.
        
        Args:
            graph: Weighted graph
            community: Set of nodes in the community
            
        Returns:
            Conductance score between 0 and 1:
            - 0: perfectly isolated community (only internal edges)
            - 1: poorly isolated community (only external edges)
        """
        internal_weights, external_weights = self.calculate_edge_weights(graph, community)
        
        # Handle edge cases
        if internal_weights == 0 and external_weights == 0:
            return 1.0  # Isolated nodes are considered worst case
        if external_weights == 0:
            return 0.0  # Perfect community with no external connections
            
        return external_weights / (2 * internal_weights + external_weights)
    
    def calculate_graph_conductance(self, graph: Dict[str, Dict[str, float]], 
                                  communities: Dict[str, int]) -> Dict[int, float]:
        """
        Calculate conductance for all communities in a graph.
        
        Args:
            graph: Weighted graph
            communities: Dictionary mapping nodes to community IDs
            
        Returns:
            Dictionary mapping community IDs to their conductance scores
        """
        community_ids = set(communities.values())
        conductances = {}
        
        for comm_id in community_ids:
            community_nodes = self.get_community_nodes(communities, comm_id)
            conductances[comm_id] = self.calculate_community_conductance(graph, community_nodes)
            
        return conductances
    
    def compute(self, graph1: Dict[str, Dict[str, float]], 
                                    graph2: Dict[str, Dict[str, float]],
                                    communities1: Dict[str, int],
                                    communities2: Dict[str, int]) -> float:
        """
        Calculate the conductance-based distance between two graphs.
        
        Args:
            graph1: First weighted graph
            graph2: Second weighted graph
            communities1: Community structure of first graph
            communities2: Community structure of second graph
            
        Returns:
            Average absolute difference in conductance scores between corresponding communities
        """
        # Calculate conductances for both graphs
        conductances1 = self.calculate_graph_conductance(graph1, communities1)
        conductances2 = self.calculate_graph_conductance(graph2, communities2)
        
        # Get all community IDs
        all_communities = set(conductances1.keys()).union(conductances2.keys())
        total_diff = 0.0
        
        # Compare conductances
        for comm_id in all_communities:
            score1 = conductances1.get(comm_id, 1.0)  # Default to worst conductance if community doesn't exist
            score2 = conductances2.get(comm_id, 1.0)
            total_diff += abs(score1 - score2)
            
        return total_diff / len(all_communities) if all_communities else 0.0
###################################
from typing import Dict, Set, List, Tuple
from collections import defaultdict

class NormalizedCutCalculator(Distance):
    """
    A class to calculate the Normalized Cut between two weighted graphs.
    The Normalized Cut measures how well-separated different subgraphs (communities) are.
    
    Graphs are represented as nested dictionaries where:
    - Outer key: source node
    - Inner key: target node
    - Value: edge weight
    
    The Normalized Cut (NCut) is defined as: sum(cut(A,V-A)/vol(A)) for all subgraphs A,
    where:
    - cut(A,B) is the sum of edge weights between subgraphs A and B
    - vol(A) is the sum of all edge weights connected to nodes in A
    """
    
    def __init__(self) -> None:
        """Initialize the Normalized Cut calculator."""      
        super().__init__()
        self.type='graph'
        
    def calculate_cut(self, graph: Dict[str, Dict[str, float]], 
                     subgraph: Set[str], 
                     complement: Set[str]) -> float:
        """
        Calculate the cut value between a subgraph and its complement.
        
        Args:
            graph: Weighted graph
            subgraph: Set of nodes in the subgraph
            complement: Set of nodes in the complement of the subgraph
            
        Returns:
            Sum of weights of edges crossing between subgraph and complement
        """
        cut_value = 0.0
        
        for node in subgraph:
            if node not in graph:
                continue
            
            for neighbor, weight in graph[node].items():
                if neighbor in complement:
                    cut_value += weight
                    
        return cut_value

    def calculate_volume(self, graph: Dict[str, Dict[str, float]], 
                        nodes: Set[str]) -> float:
        """
        Calculate the volume of a set of nodes (sum of all edge weights).
        
        Args:
            graph: Weighted graph
            nodes: Set of nodes to calculate volume for
            
        Returns:
            Sum of weights of all edges connected to the nodes
        """
        volume = 0.0
        
        for node in nodes:
            if node not in graph:
                continue
            
            volume += sum(graph[node].values())
            
        return volume

    def get_subgraphs(self, communities: Dict[str, int]) -> List[Set[str]]:
        """
        Convert community assignments to sets of nodes.
        
        Args:
            communities: Dictionary mapping nodes to community IDs
            
        Returns:
            List of sets, where each set contains nodes of one community
        """
        subgraphs: Dict[int, Set[str]] = defaultdict(set)
        
        for node, community_id in communities.items():
            subgraphs[community_id].add(node)
            
        return list(subgraphs.values())

    def calculate_normalized_cut(self, graph: Dict[str, Dict[str, float]], 
                               communities: Dict[str, int]) -> float:
        """
        Calculate the Normalized Cut value for a graph partition.
        
        Args:
            graph: Weighted graph
            communities: Dictionary mapping nodes to community IDs
            
        Returns:
            Normalized Cut value (lower is better, indicates better separation)
        """
        subgraphs = self.get_subgraphs(communities)
        all_nodes = set().union(*subgraphs)
        ncut = 0.0
        
        for subgraph in subgraphs:
            complement = all_nodes - subgraph
            cut_value = self.calculate_cut(graph, subgraph, complement)
            volume = self.calculate_volume(graph, subgraph)
            
            if volume > 0:  # Avoid division by zero
                ncut += cut_value / volume
                
        return ncut

    def compute(self, graph1: Dict[str, Dict[str, float]], 
                         graph2: Dict[str, Dict[str, float]],
                         communities1: Dict[str, int],
                         communities2: Dict[str, int]) -> float:
        """
        Calculate the distance between two graphs based on their Normalized Cut values.
        
        Args:
            graph1: First weighted graph
            graph2: Second weighted graph
            communities1: Community structure of first graph
            communities2: Community structure of second graph
            
        Returns:
            Absolute difference between the Normalized Cut values
        """
        ncut1 = self.calculate_normalized_cut(graph1, communities1)
        ncut2 = self.calculate_normalized_cut(graph2, communities2)
        
        return abs(ncut1 - ncut2)

    def analyze_partition_quality(self, graph: Dict[str, Dict[str, float]], 
                                communities: Dict[str, int]) -> Dict[str, float]:
        """
        Provide detailed analysis of partition quality for each community.
        
        Args:
            graph: Weighted graph
            communities: Dictionary mapping nodes to community IDs
            
        Returns:
            Dictionary containing quality metrics for the partition
        """
        subgraphs = self.get_subgraphs(communities)
        all_nodes = set().union(*subgraphs)
        metrics = {
            'total_ncut': 0.0,
            'community_cuts': [],
            'community_volumes': [],
            'community_ratios': []
        }
        
        for subgraph in subgraphs:
            complement = all_nodes - subgraph
            cut = self.calculate_cut(graph, subgraph, complement)
            volume = self.calculate_volume(graph, subgraph)
            
            metrics['community_cuts'].append(cut)
            metrics['community_volumes'].append(volume)
            
            if volume > 0:
                ratio = cut / volume
                metrics['community_ratios'].append(ratio)
                metrics['total_ncut'] += ratio
                
        return metrics
#########################################
from typing import Dict, List, Tuple
import math

class SpectralRadiusCalculator(Distance):
    """
    A class to calculate the spectral radius of weighted graphs.
    The spectral radius is the largest eigenvalue of the adjacency matrix.
    
    This implementation uses the power iteration method to compute
    the largest eigenvalue without requiring external linear algebra libraries.
    """
    
    def __init__(self, max_iterations: int = 100, tolerance: float = 1e-6) -> None:
        """
        Initialize the spectral radius calculator.
        
        Args:
            max_iterations: Maximum number of power iterations
            tolerance: Convergence tolerance for eigenvalue estimation
        """      
        super().__init__()
        self.type='graph'
        
        self.max_iterations = max_iterations
        self.tolerance = tolerance

    def create_adjacency_matrix(self, graph: Dict[str, Dict[str, float]]) -> List[List[float]]:
        """
        Convert graph dictionary to adjacency matrix.
        
        Args:
            graph: Weighted graph as nested dictionary
            
        Returns:
            2D list representing the adjacency matrix
        """
        # Get all nodes and create an ordered list
        nodes = sorted(list(graph.keys()))
        n = len(nodes)
        
        # Create node to index mapping
        node_to_index = {node: i for i, node in enumerate(nodes)}
        
        # Initialize adjacency matrix with zeros
        matrix = [[0.0 for _ in range(n)] for _ in range(n)]
        
        # Fill the matrix with edge weights
        for source in graph:
            for target, weight in graph[source].items():
                if target in node_to_index:  # Ensure target node exists
                    i = node_to_index[source]
                    j = node_to_index[target]
                    matrix[i][j] = weight
                    
        return matrix

    def matrix_vector_multiply(self, matrix: List[List[float]], 
                             vector: List[float]) -> List[float]:
        """
        Multiply a matrix by a vector.
        
        Args:
            matrix: 2D list representing a square matrix
            vector: 1D list representing a vector
            
        Returns:
            Resulting vector from multiplication
        """
        n = len(matrix)
        result = [0.0] * n
        
        for i in range(n):
            for j in range(n):
                result[i] += matrix[i][j] * vector[j]
                
        return result

    def normalize_vector(self, vector: List[float]) -> Tuple[List[float], float]:
        """
        Normalize a vector and return its norm.
        
        Args:
            vector: Input vector
            
        Returns:
            Tuple of (normalized vector, norm)
        """
        # Calculate L2 norm
        norm = math.sqrt(sum(x * x for x in vector))
        
        if norm < 1e-10:  # Avoid division by zero
            return [0.0] * len(vector), 0.0
            
        # Normalize vector
        normalized = [x / norm for x in vector]
        return normalized, norm

    def power_iteration(self, matrix: List[List[float]]) -> float:
        """
        Compute the largest eigenvalue using power iteration method.
        
        Args:
            matrix: Square matrix as 2D list
            
        Returns:
            Largest eigenvalue (spectral radius)
        """
        n = len(matrix)
        if n == 0:
            return 0.0
            
        # Start with random vector
        vector = [1.0] * n
        vector, _ = self.normalize_vector(vector)
        
        prev_eigenvalue = 0.0
        
        for _ in range(self.max_iterations):
            # Multiply matrix by vector
            product = self.matrix_vector_multiply(matrix, vector)
            
            # Normalize the resulting vector
            vector, eigenvalue = self.normalize_vector(product)
            
            # Check convergence
            if abs(eigenvalue - prev_eigenvalue) < self.tolerance:
                return eigenvalue
                
            prev_eigenvalue = eigenvalue
            
        return prev_eigenvalue

    def calculate_spectral_radius(self, graph: Dict[str, Dict[str, float]]) -> float:
        """
        Calculate the spectral radius of a graph.
        
        Args:
            graph: Weighted graph as nested dictionary
            
        Returns:
            Spectral radius (largest eigenvalue)
        """
        # Convert graph to matrix form
        matrix = self.create_adjacency_matrix(graph)
        
        # Calculate spectral radius using power iteration
        return self.power_iteration(matrix)

    def compute(self, graph1: Dict[str, Dict[str, float]], 
                         graph2: Dict[str, Dict[str, float]]) -> float:
        """
        Calculate the distance between two graphs based on their spectral radii.
        
        Args:
            graph1: First weighted graph
            graph2: Second weighted graph
            
        Returns:
            Absolute difference between spectral radii
        """
        radius1 = self.calculate_spectral_radius(graph1)
        radius2 = self.calculate_spectral_radius(graph2)
        
        return abs(radius1 - radius2)

    def analyze_graph_spectrum(self, graph: Dict[str, Dict[str, float]]) -> Dict[str, float]:
        """
        Provide detailed spectral analysis of the graph.
        
        Args:
            graph: Weighted graph
            
        Returns:
            Dictionary containing spectral metrics
        """
        matrix = self.create_adjacency_matrix(graph)
        spectral_radius = self.power_iteration(matrix)
        
        # Calculate additional spectral properties
        trace = sum(matrix[i][i] for i in range(len(matrix)))
        
        return {
            'spectral_radius': spectral_radius,
            'matrix_trace': trace,
            'average_degree': trace / len(matrix) if matrix else 0.0
        }
############################################
from typing import Dict, List, Tuple, Optional
import math

class GraphLaplacianCalculator(Distance):
    """
    A class to calculate and analyze the Graph Laplacian matrix.
    
    The Graph Laplacian L is defined as L = D - A where:
    - D is the degree matrix (diagonal matrix of vertex degrees)
    - A is the adjacency matrix
    
    The normalized Laplacian is defined as L_norm = I - D^(-1/2)AD^(-1/2)
    where I is the identity matrix.
    """
    
    def __init__(self, normalize: bool = True) -> None:
        """
        Initialize the Graph Laplacian calculator.
        
        Args:
            normalize: Whether to use normalized Laplacian (default: True)
        """      
        super().__init__()
        self.type='graph'
        
        self.normalize = normalize
        
    def create_adjacency_matrix(self, graph: Dict[str, Dict[str, float]]) -> Tuple[List[List[float]], List[str]]:
        """
        Convert graph dictionary to adjacency matrix.
        
        Args:
            graph: Weighted graph as nested dictionary
            
        Returns:
            Tuple of (adjacency matrix, ordered list of node labels)
        """
        nodes = sorted(list(graph.keys()))
        n = len(nodes)
        node_to_index = {node: i for i, node in enumerate(nodes)}
        
        matrix = [[0.0 for _ in range(n)] for _ in range(n)]
        
        for source in graph:
            for target, weight in graph[source].items():
                if target in node_to_index:
                    i = node_to_index[source]
                    j = node_to_index[target]
                    matrix[i][j] = weight
                    
        return matrix, nodes
        
    def calculate_degree_matrix(self, adjacency: List[List[float]]) -> List[List[float]]:
        """
        Calculate the degree matrix from the adjacency matrix.
        
        Args:
            adjacency: Adjacency matrix
            
        Returns:
            Degree matrix (diagonal matrix)
        """
        n = len(adjacency)
        degree_matrix = [[0.0 for _ in range(n)] for _ in range(n)]
        
        for i in range(n):
            degree = sum(adjacency[i])
            degree_matrix[i][i] = degree
            
        return degree_matrix
        
    def calculate_laplacian(self, graph: Dict[str, Dict[str, float]]) -> Tuple[List[List[float]], List[str]]:
        """
        Calculate the Graph Laplacian matrix.
        
        Args:
            graph: Weighted graph
            
        Returns:
            Tuple of (Laplacian matrix, ordered list of node labels)
        """
        adjacency, nodes = self.create_adjacency_matrix(graph)
        degree = self.calculate_degree_matrix(adjacency)
        n = len(adjacency)
        
        if self.normalize:
            # Calculate normalized Laplacian
            laplacian = [[0.0 for _ in range(n)] for _ in range(n)]
            for i in range(n):
                for j in range(n):
                    if i == j:
                        laplacian[i][j] = 1.0 if degree[i][i] > 0 else 0.0
                    elif degree[i][i] > 0 and degree[j][j] > 0:
                        laplacian[i][j] = -adjacency[i][j] / math.sqrt(degree[i][i] * degree[j][j])
        else:
            # Calculate standard Laplacian
            laplacian = [[0.0 for _ in range(n)] for _ in range(n)]
            for i in range(n):
                for j in range(n):
                    if i == j:
                        laplacian[i][j] = degree[i][i]
                    else:
                        laplacian[i][j] = -adjacency[i][j]
                        
        return laplacian, nodes
        
    def calculate_eigenvalues(self, matrix: List[List[float]], 
                            max_iterations: int = 100, 
                            tolerance: float = 1e-6) -> List[float]:
        """
        Calculate eigenvalues using QR algorithm with deflation.
        
        Args:
            matrix: Input matrix
            max_iterations: Maximum number of iterations
            tolerance: Convergence tolerance
            
        Returns:
            List of eigenvalues
        """
        n = len(matrix)
        current_matrix = [row[:] for row in matrix]
        eigenvalues = []
        
        for size in range(n, 0, -1):
            # Extract the largest eigenvalue using power iteration
            vector = [1.0] * size
            prev_eigenvalue = 0.0
            
            for _ in range(max_iterations):
                # Multiply matrix by vector
                new_vector = [0.0] * size
                for i in range(size):
                    for j in range(size):
                        new_vector[i] += current_matrix[i][j] * vector[j]
                
                # Normalize
                norm = math.sqrt(sum(x * x for x in new_vector))
                if norm < tolerance:
                    break
                    
                vector = [x / norm for x in new_vector]
                eigenvalue = sum(vector[i] * new_vector[i] for i in range(size)) / norm
                
                if abs(eigenvalue - prev_eigenvalue) < tolerance:
                    eigenvalues.append(eigenvalue)
                    break
                    
                prev_eigenvalue = eigenvalue
            
            # Deflate matrix
            if size > 1:
                deflated = [[0.0 for _ in range(size-1)] for _ in range(size-1)]
                for i in range(size-1):
                    for j in range(size-1):
                        deflated[i][j] = current_matrix[i][j]
                current_matrix = deflated
                
        return sorted(eigenvalues)
        
    def analyze_spectrum(self, graph: Dict[str, Dict[str, float]]) -> Dict[str, float]:
        """
        Analyze spectral properties of the graph Laplacian.
        
        Args:
            graph: Weighted graph
            
        Returns:
            Dictionary containing spectral properties
        """
        laplacian, _ = self.calculate_laplacian(graph)
        eigenvalues = self.calculate_eigenvalues(laplacian)
        
        if not eigenvalues:
            return {
                'algebraic_connectivity': 0.0,
                'spectral_gap': 0.0,
                'largest_eigenvalue': 0.0
            }
            
        # Sort eigenvalues
        eigenvalues.sort()
        
        # Calculate spectral properties
        return {
            'algebraic_connectivity': eigenvalues[1] if len(eigenvalues) > 1 else 0.0,
            'spectral_gap': eigenvalues[1] - eigenvalues[0] if len(eigenvalues) > 1 else 0.0,
            'largest_eigenvalue': eigenvalues[-1]
        }
        
    def compute(self, graph1: Dict[str, Dict[str, float]], 
                         graph2: Dict[str, Dict[str, float]]) -> float:
        """
        Calculate distance between two graphs based on Laplacian spectrum.
        
        Args:
            graph1: First weighted graph
            graph2: Second weighted graph
            
        Returns:
            Spectral distance between the graphs
        """
        spectrum1 = self.analyze_spectrum(graph1)
        spectrum2 = self.analyze_spectrum(graph2)
        
        # Calculate weighted difference of spectral properties
        distance = abs(spectrum1['algebraic_connectivity'] - spectrum2['algebraic_connectivity'])
        distance += abs(spectrum1['spectral_gap'] - spectrum2['spectral_gap'])
        distance += abs(spectrum1['largest_eigenvalue'] - spectrum2['largest_eigenvalue'])
        
        return distance
#####################################
from typing import Dict, List, Tuple, Optional
import math

class AlgebraicConnectivityCalculator(Distance):
    """
    A class to calculate and analyze the algebraic connectivity of weighted graphs.
    
    The algebraic connectivity is the second smallest eigenvalue of the Laplacian matrix.
    It provides a measure of graph robustness and connectivity, where:
    - Higher values indicate better connected graphs
    - Zero value indicates a disconnected graph
    - The magnitude reflects how difficult it is to split the graph into components
    """
    
    def __init__(self, tolerance: float = 1e-6, max_iterations: int = 100) -> None:
        """
        Initialize the calculator with numerical parameters.
        
        Args:
            tolerance: Convergence tolerance for eigenvalue computation
            max_iterations: Maximum iterations for power method
        """      
        super().__init__()
        self.type='graph'
        
        self.tolerance = tolerance
        self.max_iterations = max_iterations

    def construct_laplacian(self, graph: Dict[str, Dict[str, float]]) -> Tuple[List[List[float]], List[str]]:
        """
        Construct the Laplacian matrix from the input graph.
        
        Args:
            graph: Weighted graph as nested dictionary
            
        Returns:
            Tuple of (Laplacian matrix, ordered node labels)
        """
        # Create ordered node list for consistent indexing
        nodes = sorted(list(graph.keys()))
        n = len(nodes)
        node_indices = {node: i for i, node in enumerate(nodes)}
        
        # Initialize the Laplacian matrix
        laplacian = [[0.0 for _ in range(n)] for _ in range(n)]
        
        # Fill the Laplacian matrix
        for source in graph:
            source_idx = node_indices[source]
            # Add edge weights to degree (diagonal)
            laplacian[source_idx][source_idx] = sum(graph[source].values())
            
            # Add negative weights for edges
            for target, weight in graph[source].items():
                if target in node_indices:
                    target_idx = node_indices[target]
                    laplacian[source_idx][target_idx] = -weight
                    
        return laplacian, nodes

    def compute_smallest_eigenvalues(self, matrix: List[List[float]], 
                                   k: int = 2) -> List[float]:
        """
        Compute the k smallest eigenvalues using inverse power iteration.
        
        Args:
            matrix: Input matrix
            k: Number of eigenvalues to compute
            
        Returns:
            List of k smallest eigenvalues
        """
        n = len(matrix)
        eigenvalues = []
        eigenvectors = []
        
        for _ in range(k):
            # Initialize random vector
            vector = [1.0 / math.sqrt(n)] * n
            
            # Make vector orthogonal to previous eigenvectors
            for ev in eigenvectors:
                dot_product = sum(v1 * v2 for v1, v2 in zip(vector, ev))
                vector = [v1 - dot_product * v2 for v1, v2 in zip(vector, ev)]
            
            # Normalize vector
            norm = math.sqrt(sum(x * x for x in vector))
            if norm > self.tolerance:
                vector = [x / norm for x in vector]
            
            # Power iteration
            prev_eigenvalue = 0.0
            for _ in range(self.max_iterations):
                # Matrix-vector multiplication
                new_vector = [0.0] * n
                for i in range(n):
                    for j in range(n):
                        new_vector[i] += matrix[i][j] * vector[j]
                
                # Normalize
                norm = math.sqrt(sum(x * x for x in new_vector))
                if norm < self.tolerance:
                    break
                    
                vector = [x / norm for x in new_vector]
                eigenvalue = sum(vector[i] * new_vector[i] for i in range(n)) / norm
                
                # Check convergence
                if abs(eigenvalue - prev_eigenvalue) < self.tolerance:
                    eigenvalues.append(eigenvalue)
                    eigenvectors.append(vector)
                    break
                    
                prev_eigenvalue = eigenvalue
                
        return sorted(eigenvalues)

    def calculate_algebraic_connectivity(self, graph: Dict[str, Dict[str, float]]) -> float:
        """
        Calculate the algebraic connectivity of the graph.
        
        Args:
            graph: Weighted graph
            
        Returns:
            Algebraic connectivity value
        """
        laplacian, _ = self.construct_laplacian(graph)
        eigenvalues = self.compute_smallest_eigenvalues(laplacian, k=2)
        
        # The algebraic connectivity is the second smallest eigenvalue
        return eigenvalues[1] if len(eigenvalues) > 1 else 0.0

    def analyze_connectivity(self, graph: Dict[str, Dict[str, float]]) -> Dict[str, float]:
        """
        Provide comprehensive connectivity analysis of the graph.
        
        Args:
            graph: Weighted graph
            
        Returns:
            Dictionary containing connectivity metrics
        """
        laplacian, _ = self.construct_laplacian(graph)
        eigenvalues = self.compute_smallest_eigenvalues(laplacian, k=3)
        
        return {
            'algebraic_connectivity': eigenvalues[1] if len(eigenvalues) > 1 else 0.0,
            'first_eigenvalue': eigenvalues[0] if eigenvalues else 0.0,
            'third_eigenvalue': eigenvalues[2] if len(eigenvalues) > 2 else 0.0,
            'spectral_gap': eigenvalues[1] - eigenvalues[0] if len(eigenvalues) > 1 else 0.0,
            'is_connected': eigenvalues[1] > self.tolerance if len(eigenvalues) > 1 else False
        }

    def compute(self, graph1: Dict[str, Dict[str, float]], 
                         graph2: Dict[str, Dict[str, float]]) -> float:
        """
        Calculate the distance between two graphs based on algebraic connectivity.
        
        Args:
            graph1: First weighted graph
            graph2: Second weighted graph
            
        Returns:
            Absolute difference in algebraic connectivity
        """
        connectivity1 = self.calculate_algebraic_connectivity(graph1)
        connectivity2 = self.calculate_algebraic_connectivity(graph2)
        
        return abs(connectivity1 - connectivity2)
##################################
from typing import Dict, List, Set, Tuple, Optional
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass
class TemporalEdge:
    """
    Represents an edge that exists during a specific time interval.
    
    Attributes:
        source: Source node identifier
        target: Target node identifier
        weight: Edge weight
        start_time: Time when edge becomes active
        end_time: Time when edge becomes inactive
    """
    source: str
    target: str
    weight: float
    start_time: datetime
    end_time: datetime

class TemporalReachabilityAnalyzer(Distance):
    """
    Analyzes reachability in temporal networks where edges are active during
    specific time windows. Supports analysis of how nodes can be reached
    over time, considering edge weights and temporal constraints.
    """
    
    def __init__(self, time_window: timedelta = timedelta(hours=1)) -> None:
        """
        Initialize the temporal reachability analyzer.
        
        Args:
            time_window: Default time window for reachability analysis
        """      
        super().__init__()
        self.type='graph'
        
        self.time_window = time_window

    def create_temporal_graph(self, 
                            static_graph: Dict[str, Dict[str, float]],
                            edge_times: Dict[Tuple[str, str], List[Tuple[datetime, datetime]]]) -> List[TemporalEdge]:
        """
        Convert a static graph and temporal information into a list of temporal edges.
        
        Args:
            static_graph: Weighted graph structure
            edge_times: Dictionary mapping edge tuples to lists of active time intervals
            
        Returns:
            List of temporal edges with their properties
        """
        temporal_edges = []
        
        for source, targets in static_graph.items():
            for target, weight in targets.items():
                # Get time intervals for this edge
                intervals = edge_times.get((source, target), [])
                
                # Create temporal edge for each interval
                for start_time, end_time in intervals:
                    temporal_edges.append(TemporalEdge(
                        source=source,
                        target=target,
                        weight=weight,
                        start_time=start_time,
                        end_time=end_time
                    ))
                    
        return temporal_edges

    def find_temporal_paths(self,
                          edges: List[TemporalEdge],
                          source: str,
                          target: str,
                          start_time: datetime) -> List[List[TemporalEdge]]:
        """
        Find all temporally valid paths between source and target nodes.
        
        Args:
            edges: List of temporal edges
            source: Starting node
            target: Destination node
            start_time: Path search start time
            
        Returns:
            List of valid temporal paths (each path is a list of edges)
        """
        # Sort edges by start time
        sorted_edges = sorted(edges, key=lambda e: e.start_time)
        
        # Initialize path finding
        paths: List[List[TemporalEdge]] = []
        current_path: List[TemporalEdge] = []
        
        def explore_path(current_node: str, current_time: datetime) -> None:
            """Recursive helper function to explore temporal paths."""
            if current_node == target:
                paths.append(current_path[:])
                return
                
            # Find valid next edges
            for edge in sorted_edges:
                if (edge.source == current_node and
                    edge.start_time >= current_time and
                    edge.start_time <= start_time + self.time_window):
                    
                    current_path.append(edge)
                    explore_path(edge.target, edge.end_time)
                    current_path.pop()
        
        explore_path(source, start_time)
        return paths

    def calculate_reachability_metrics(self,
                                    edges: List[TemporalEdge],
                                    source: str,
                                    start_time: datetime) -> Dict[str, float]:
        """
        Calculate reachability metrics from a source node.
        
        Args:
            edges: List of temporal edges
            source: Starting node
            start_time: Analysis start time
            
        Returns:
            Dictionary containing reachability metrics
        """
        # Find all reachable nodes
        reachable_nodes: Set[str] = set()
        earliest_arrival: Dict[str, datetime] = {}
        
        # Get all nodes
        all_nodes = {edge.source for edge in edges}.union(
            {edge.target for edge in edges})
            
        # Initialize with source node
        reachable_nodes.add(source)
        earliest_arrival[source] = start_time
        
        # Process edges in temporal order
        sorted_edges = sorted(edges, key=lambda e: e.start_time)
        
        for edge in sorted_edges:
            if (edge.source in reachable_nodes and
                edge.start_time >= start_time and
                edge.start_time <= start_time + self.time_window):
                
                reachable_nodes.add(edge.target)
                
                arrival_time = edge.end_time
                if (edge.target not in earliest_arrival or
                    arrival_time < earliest_arrival[edge.target]):
                    earliest_arrival[edge.target] = arrival_time
        
        # Calculate metrics
        total_nodes = len(all_nodes)
        reachable_count = len(reachable_nodes) - 1  # Exclude source
        average_delay = timedelta()
        
        if reachable_count > 0:
            total_delay = sum(
                (arrival - start_time for node, arrival in earliest_arrival.items()
                 if node != source),
                timedelta())
            average_delay = total_delay / reachable_count
        
        return {
            'reachability_ratio': reachable_count / (total_nodes - 1),
            'average_delay_seconds': average_delay.total_seconds(),
            'reachable_nodes': len(reachable_nodes),
            'total_nodes': total_nodes
        }

    def compute(self,
                                 edges1: List[TemporalEdge],
                                 edges2: List[TemporalEdge],
                                 reference_time: datetime) -> float:
        """
        Calculate temporal distance between two graph snapshots.
        
        Args:
            edges1: Temporal edges of first graph
            edges2: Temporal edges of second graph
            reference_time: Time point for comparison
            
        Returns:
            Distance metric based on reachability differences
        """
        # Get all unique nodes
        nodes = {edge.source for edge in edges1 + edges2}.union(
            {edge.target for edge in edges1 + edges2})
        
        total_difference = 0.0
        
        # Compare reachability from each node
        for node in nodes:
            metrics1 = self.calculate_reachability_metrics(edges1, node, reference_time)
            metrics2 = self.calculate_reachability_metrics(edges2, node, reference_time)
            
            # Calculate weighted difference of metrics
            difference = abs(metrics1['reachability_ratio'] - metrics2['reachability_ratio'])
            delay_diff = abs(metrics1['average_delay_seconds'] - metrics2['average_delay_seconds'])
            
            # Normalize delay difference
            max_delay = self.time_window.total_seconds()
            normalized_delay_diff = delay_diff / max_delay if max_delay > 0 else 0
            
            total_difference += difference + 0.5 * normalized_delay_diff
            
        return total_difference / len(nodes)
#####################################

from typing import Dict, Set, List, Tuple, Optional
from collections import deque
import math

class GraphDistanceCalculatorV2(Distance):
    """
    A class to calculate various distance metrics between two weighted graphs.
    Graphs are represented as nested dictionaries where:
    - Outer key: source node (str)
    - Inner key: target node (str)
    - Value: edge weight (float)
    """

    def __init__(self, graph1: Dict[str, Dict[str, float]], graph2: Dict[str, Dict[str, float]]):
        """
        Initialize the calculator with two graphs to compare.

        Args:
            graph1: First graph as Dict[str, Dict[str, float]]
            graph2: Second graph as Dict[str, Dict[str, float]]
        """      
        super().__init__()
        self.type='graph'
        
        self.graph1 = graph1
        self.graph2 = graph2
        self.nodes1 = set(graph1.keys())
        self.nodes2 = set(graph2.keys())

    def get_edge_difference(self) -> float:
        """
        Calculate the total absolute difference in edge weights between the two graphs.
        Only considers edges present in both graphs.

        Returns:
            float: Sum of absolute differences in edge weights
        """
        total_diff = 0.0
        
        # Iterate through all possible edges in both graphs
        for source in self.nodes1.intersection(self.nodes2):
            for target in self.graph1[source].keys():
                if target in self.graph2.get(source, {}):
                    weight1 = self.graph1[source][target]
                    weight2 = self.graph2[source][target]
                    total_diff += abs(weight1 - weight2)
                    
        return total_diff

    def get_structural_difference(self) -> float:
        """
        Calculate structural difference based on presence/absence of edges.
        Uses Jaccard distance between edge sets.

        Returns:
            float: Structural difference score (0 = identical, 1 = completely different)
        """
        edges1 = self._get_edge_set(self.graph1)
        edges2 = self._get_edge_set(self.graph2)
        
        intersection = len(edges1.intersection(edges2))
        union = len(edges1.union(edges2))
        
        return 1 - (intersection / union if union > 0 else 0)

    def get_centrality_difference(self) -> Dict[str, float]:
        """
        Calculate the difference in degree centrality for nodes present in both graphs.

        Returns:
            Dict[str, float]: Dictionary mapping nodes to their centrality differences
        """
        centrality_diff = {}
        common_nodes = self.nodes1.intersection(self.nodes2)
        
        for node in common_nodes:
            centrality1 = sum(self.graph1[node].values())
            centrality2 = sum(self.graph2.get(node, {}).values())
            centrality_diff[node] = abs(centrality1 - centrality2)
            
        return centrality_diff

    def get_shortest_paths_difference(self) -> float:
        """
        Calculate the average difference in shortest path lengths between all pairs
        of nodes present in both graphs.

        Returns:
            float: Average difference in shortest path lengths
        """
        common_nodes = list(self.nodes1.intersection(self.nodes2))
        total_diff = 0.0
        count = 0
        
        for source in common_nodes:
            paths1 = self._dijkstra(self.graph1, source)
            paths2 = self._dijkstra(self.graph2, source)
            
            for target in common_nodes:
                if target in paths1 and target in paths2:
                    total_diff += abs(paths1[target] - paths2[target])
                    count += 1
                    
        return total_diff / count if count > 0 else float('inf')

    def _get_edge_set(self, graph: Dict[str, Dict[str, float]]) -> Set[Tuple[str, str]]:
        """
        Convert graph to a set of edge tuples.

        Args:
            graph: Input graph

        Returns:
            Set of tuples representing edges (source, target)
        """
        edges = set()
        for source in graph:
            for target in graph[source]:
                edges.add((source, target))
        return edges

    def _dijkstra(self, graph: Dict[str, Dict[str, float]], start: str) -> Dict[str, float]:
        """
        Implementation of Dijkstra's algorithm for shortest paths.

        Args:
            graph: Input graph
            start: Starting node

        Returns:
            Dictionary mapping nodes to shortest path distances from start
        """
        distances = {node: float('infinity') for node in graph}
        distances[start] = 0
        pq = [(0, start)]
        visited = set()

        while pq:
            current_distance, current_node = min(pq)
            pq.remove((current_distance, current_node))
            
            if current_node in visited:
                continue
                
            visited.add(current_node)
            
            for neighbor, weight in graph[current_node].items():
                distance = current_distance + weight
                
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    pq.append((distance, neighbor))
                    
        return distances
        
#######################################
from typing import Dict, List, Set, Tuple
from collections import defaultdict
import itertools

class TemporalClusteringCalculator(Distance):
    """
    Calculates temporal clustering coefficients for dynamic networks represented as temporal snapshots.
    Implements various temporal clustering metrics to analyze the evolution of network structure over time.
    
    The temporal network is represented as a sequence of weighted graph snapshots, where each snapshot
    is a dictionary mapping node pairs to edge weights.
    """

    def __init__(self, temporal_snapshots: List[Dict[str, Dict[str, float]]]):
        """
        Initialize the calculator with a sequence of network snapshots.

        Args:
            temporal_snapshots: List of graph snapshots, each represented as 
                              Dict[str, Dict[str, float]] for weighted edges
        """      
        super().__init__()
        self.type='graph'
        
        self.snapshots = temporal_snapshots
        self.time_steps = len(temporal_snapshots)
        
        # Extract all unique nodes across all timestamps
        self.all_nodes = set()
        for snapshot in temporal_snapshots:
            self.all_nodes.update(snapshot.keys())

    def get_temporal_clustering(self, window_size: int = 1) -> Dict[str, List[float]]:
        """
        Calculate temporal clustering coefficients for each node across time windows.

        Args:
            window_size: Number of consecutive snapshots to consider for each calculation

        Returns:
            Dictionary mapping node IDs to lists of clustering coefficients over time
        """
        clustering_coefficients = defaultdict(list)
        
        for t in range(self.time_steps - window_size + 1):
            window_snapshots = self.snapshots[t:t + window_size]
            
            # Calculate clustering coefficients for each node in current window
            for node in self.all_nodes:
                coeff = self._calculate_window_clustering(node, window_snapshots)
                clustering_coefficients[node].append(coeff)
                
        return dict(clustering_coefficients)

    def get_global_temporal_clustering(self, window_size: int = 1) -> List[float]:
        """
        Calculate global temporal clustering coefficients across time windows.

        Args:
            window_size: Number of consecutive snapshots to consider for each calculation

        Returns:
            List of global clustering coefficients for each time window
        """
        global_coefficients = []
        
        for t in range(self.time_steps - window_size + 1):
            window_snapshots = self.snapshots[t:t + window_size]
            
            # Calculate average clustering coefficient across all nodes
            window_clustering = 0.0
            valid_nodes = 0
            
            for node in self.all_nodes:
                coeff = self._calculate_window_clustering(node, window_snapshots)
                if coeff is not None:
                    window_clustering += coeff
                    valid_nodes += 1
            
            if valid_nodes > 0:
                global_coefficients.append(window_clustering / valid_nodes)
            else:
                global_coefficients.append(0.0)
                
        return global_coefficients

    def get_temporal_triangles(self, node: str, window_size: int = 1) -> List[int]:
        """
        Count the number of temporal triangles involving a specific node across time windows.

        Args:
            node: Target node ID
            window_size: Number of consecutive snapshots to consider

        Returns:
            List of temporal triangle counts for each time window
        """
        triangle_counts = []
        
        for t in range(self.time_steps - window_size + 1):
            window_snapshots = self.snapshots[t:t + window_size]
            count = self._count_temporal_triangles(node, window_snapshots)
            triangle_counts.append(count)
            
        return triangle_counts

    def _calculate_window_clustering(self, 
                                   node: str, 
                                   window_snapshots: List[Dict[str, Dict[str, float]]]) -> float:
        """
        Calculate clustering coefficient for a node within a specific time window.

        Args:
            node: Target node ID
            window_snapshots: List of graph snapshots in the current time window

        Returns:
            Temporal clustering coefficient for the node in the given window
        """
        # Get all neighbors across the time window
        neighbors = set()
        for snapshot in window_snapshots:
            if node in snapshot:
                neighbors.update(snapshot[node].keys())
        
        if len(neighbors) < 2:
            return 0.0
        
        # Count temporal triangles
        triangle_count = self._count_temporal_triangles(node, window_snapshots)
        
        # Calculate maximum possible triangles
        max_triangles = len(neighbors) * (len(neighbors) - 1) / 2
        
        return triangle_count / max_triangles if max_triangles > 0 else 0.0

    def _count_temporal_triangles(self, 
                                node: str, 
                                window_snapshots: List[Dict[str, Dict[str, float]]]) -> int:
        """
        Count the number of temporal triangles involving the target node in a time window.

        Args:
            node: Target node ID
            window_snapshots: List of graph snapshots in the current time window

        Returns:
            Number of temporal triangles found
        """
        triangle_count = 0
        
        # Get all temporal neighbors
        neighbors = set()
        for snapshot in window_snapshots:
            if node in snapshot:
                neighbors.update(snapshot[node].keys())
        
        # Check for triangles between each pair of neighbors
        for n1, n2 in itertools.combinations(neighbors, 2):
            # Check if edges exist in any snapshot
            edge1_exists = False
            edge2_exists = False
            edge3_exists = False
            
            for snapshot in window_snapshots:
                if node in snapshot:
                    if n1 in snapshot[node]:
                        edge1_exists = True
                    if n2 in snapshot[node]:
                        edge2_exists = True
                if n1 in snapshot and n2 in snapshot[n1]:
                    edge3_exists = True
                    
            if edge1_exists and edge2_exists and edge3_exists:
                triangle_count += 1
                
        return triangle_count

    def get_clustering_evolution(self) -> Dict[str, List[Tuple[int, float]]]:
        """
        Track the evolution of clustering coefficients for each node over time.

        Returns:
            Dictionary mapping node IDs to lists of (timestamp, coefficient) pairs
        """
        evolution = defaultdict(list)
        
        for t, snapshot in enumerate(self.snapshots):
            coefficients = self.get_temporal_clustering(window_size=1)
            
            for node in self.all_nodes:
                if node in coefficients and len(coefficients[node]) > t:
                    evolution[node].append((t, coefficients[node][t]))
                    
        return dict(evolution)
###########################################
from typing import Dict, List, Set, Tuple
from collections import defaultdict
import statistics

class EdgePersistenceCalculator(Distance):
    """
    Analyzes the persistence and stability of edges in temporal networks.
    Provides various metrics to measure how edges maintain their presence and weights over time.
    
    The temporal network is represented as a sequence of weighted graph snapshots, where each
    snapshot is a dictionary mapping nodes to their adjacent nodes and corresponding edge weights.
    """

    def __init__(self, temporal_snapshots: List[Dict[str, Dict[str, float]]]):
        """
        Initialize the calculator with a sequence of network snapshots.

        Args:
            temporal_snapshots: List of graph snapshots, each represented as 
                              Dict[str, Dict[str, float]] for weighted edges
        """      
        super().__init__()
        self.type='graph'
        
        self.snapshots = temporal_snapshots
        self.time_steps = len(temporal_snapshots)
        
        # Extract all unique edges across all timestamps
        self.all_edges = self._get_all_edges()
        
        # Create presence matrix for all edges across time
        self.presence_matrix = self._create_presence_matrix()

    def get_edge_lifetime(self) -> Dict[Tuple[str, str], float]:
        """
        Calculate the proportional lifetime of each edge across all snapshots.
        
        Returns:
            Dictionary mapping edge tuples to their lifetime ratios (0 to 1)
        """
        lifetimes = {}
        
        for edge in self.all_edges:
            presence_count = sum(1 for t in range(self.time_steps) 
                               if self._edge_exists(edge, t))
            lifetimes[edge] = presence_count / self.time_steps
            
        return lifetimes

    def get_edge_stability(self) -> Dict[Tuple[str, str], float]:
        """
        Calculate the stability of edge weights over time, accounting for both
        presence/absence and weight variations.
        
        Returns:
            Dictionary mapping edge tuples to their stability scores (0 to 1)
        """
        stabilities = {}
        
        for edge in self.all_edges:
            weights = self._get_edge_weights(edge)
            
            if not weights:
                stabilities[edge] = 0.0
                continue
                
            # Calculate coefficient of variation for weights
            if len(weights) > 1:
                mean_weight = statistics.mean(weights)
                std_weight = statistics.stdev(weights)
                cv = std_weight / mean_weight if mean_weight != 0 else float('inf')
                
                # Transform CV to a 0-1 scale where 1 means perfect stability
                stability = 1 / (1 + cv)
            else:
                stability = 1.0
                
            # Adjust stability by presence ratio
            presence_ratio = len(weights) / self.time_steps
            stabilities[edge] = stability * presence_ratio
            
        return stabilities

    def get_persistence_patterns(self) -> Dict[Tuple[str, str], List[int]]:
        """
        Identify consecutive time periods where edges persist.
        
        Returns:
            Dictionary mapping edge tuples to lists of consecutive presence durations
        """
        patterns = defaultdict(list)
        
        for edge in self.all_edges:
            current_streak = 0
            
            for t in range(self.time_steps):
                if self._edge_exists(edge, t):
                    current_streak += 1
                else:
                    if current_streak > 0:
                        patterns[edge].append(current_streak)
                    current_streak = 0
                    
            if current_streak > 0:
                patterns[edge].append(current_streak)
                
        return dict(patterns)

    def get_weight_consistency(self) -> Dict[Tuple[str, str], float]:
        """
        Measure the consistency of edge weights when edges are present.
        
        Returns:
            Dictionary mapping edge tuples to their weight consistency scores (0 to 1)
        """
        consistencies = {}
        
        for edge in self.all_edges:
            weights = self._get_edge_weights(edge)
            
            if not weights:
                consistencies[edge] = 0.0
                continue
                
            if len(weights) == 1:
                consistencies[edge] = 1.0
                continue
                
            # Calculate normalized weight differences
            max_weight = max(weights)
            min_weight = min(weights)
            weight_range = max_weight - min_weight
            
            if weight_range == 0:
                consistencies[edge] = 1.0
            else:
                diffs = []
                for i in range(len(weights) - 1):
                    normalized_diff = abs(weights[i] - weights[i + 1]) / weight_range
                    diffs.append(normalized_diff)
                
                avg_diff = statistics.mean(diffs)
                consistencies[edge] = 1 - avg_diff
                
        return consistencies

    def get_temporal_correlation(self, lag: int = 1) -> float:
        """
        Calculate temporal correlation of edge presence between consecutive time steps.
        
        Args:
            lag: Time difference between snapshots to compare

        Returns:
            Correlation coefficient (-1 to 1)
        """
        if lag >= self.time_steps:
            return 0.0
            
        correlations = []
        
        for t in range(self.time_steps - lag):
            present_t1 = set()
            present_t2 = set()
            
            for edge in self.all_edges:
                if self._edge_exists(edge, t):
                    present_t1.add(edge)
                if self._edge_exists(edge, t + lag):
                    present_t2.add(edge)
                    
            # Calculate Jaccard similarity between edge sets
            intersection = len(present_t1.intersection(present_t2))
            union = len(present_t1.union(present_t2))
            
            if union > 0:
                correlations.append(intersection / union)
                
        return statistics.mean(correlations) if correlations else 0.0

    def _get_all_edges(self) -> Set[Tuple[str, str]]:
        """Extract all unique edges that appear in any snapshot."""
        edges = set()
        for snapshot in self.snapshots:
            for source in snapshot:
                for target in snapshot[source]:
                    edges.add((source, target))
        return edges

    def _create_presence_matrix(self) -> Dict[Tuple[str, str], List[bool]]:
        """Create a matrix indicating edge presence across time."""
        matrix = defaultdict(lambda: [False] * self.time_steps)
        
        for t, snapshot in enumerate(self.snapshots):
            for source in snapshot:
                for target in snapshot[source]:
                    matrix[(source, target)][t] = True
                    
        return dict(matrix)

    def _edge_exists(self, edge: Tuple[str, str], time: int) -> bool:
        """Check if an edge exists at a specific timestamp."""
        source, target = edge
        snapshot = self.snapshots[time]
        return source in snapshot and target in snapshot[source]

    def _get_edge_weights(self, edge: Tuple[str, str]) -> List[float]:
        """Get list of weights for an edge across all timestamps where it exists."""
        source, target = edge
        weights = []
        
        for snapshot in self.snapshots:
            if source in snapshot and target in snapshot[source]:
                weights.append(snapshot[source][target])
                
        return weights
#########################################
from typing import Dict, List, Tuple
import math

class ResistanceDistanceCalculator(Distance):
    """
    Calculates resistance distances in weighted graphs using electrical network analogies.
    
    The resistance distance between two nodes is defined as the effective resistance
    when the graph is treated as an electrical network with edges as resistors.
    Edge weights are interpreted as conductances (inverse of resistance).
    """

    def __init__(self, graph: Dict[str, Dict[str, float]]):
        """
        Initialize calculator with a weighted graph.

        Args:
            graph: Dict[str, Dict[str, float]] where edge weights represent conductances
        """      
        super().__init__()
        self.type='graph'
        
        self.graph = graph
        self.nodes = list(graph.keys())
        self.n = len(self.nodes)
        self.node_to_index = {node: i for i, node in enumerate(self.nodes)}
        
        # Calculate the Laplacian matrix once during initialization
        self.laplacian = self._compute_laplacian()
        
        # Compute pseudo-inverse of Laplacian for efficiency
        self.laplacian_pinv = self._compute_moore_penrose_pinv()

    def get_resistance_distance(self, node1: str, node2: str) -> float:
        """
        Calculate the resistance distance between two nodes.

        Args:
            node1: First node identifier
            node2: Second node identifier

        Returns:
            Resistance distance between the nodes
        """
        if node1 not in self.node_to_index or node2 not in self.node_to_index:
            raise ValueError("Node not found in graph")
            
        i = self.node_to_index[node1]
        j = self.node_to_index[node2]
        
        # Use pre-computed pseudo-inverse
        resistance = (self.laplacian_pinv[i][i] + self.laplacian_pinv[j][j] - 
                     2 * self.laplacian_pinv[i][j])
        
        return max(resistance, 0.0)  # Handle numerical precision issues

    def get_all_pairs_distances(self) -> Dict[Tuple[str, str], float]:
        """
        Calculate resistance distances between all pairs of nodes.

        Returns:
            Dictionary mapping node pairs to their resistance distances
        """
        distances = {}
        
        for i, node1 in enumerate(self.nodes):
            for j, node2 in enumerate(self.nodes[i+1:], i+1):
                distance = self.get_resistance_distance(node1, node2)
                distances[(node1, node2)] = distance
                distances[(node2, node1)] = distance
                
        return distances

    def get_average_resistance(self) -> float:
        """
        Calculate the average resistance distance across all node pairs.

        Returns:
            Average resistance distance in the network
        """
        distances = self.get_all_pairs_distances()
        return sum(distances.values()) / len(distances)

    def get_resistance_centrality(self) -> Dict[str, float]:
        """
        Calculate resistance centrality for each node.
        Lower values indicate more central nodes in terms of electrical flow.

        Returns:
            Dictionary mapping nodes to their resistance centrality scores
        """
        centrality = {}
        for node in self.nodes:
            # Sum of resistance distances to all other nodes
            total_resistance = sum(self.get_resistance_distance(node, other)
                                 for other in self.nodes if other != node)
            centrality[node] = total_resistance / (self.n - 1)
        return centrality

    def _compute_laplacian(self) -> List[List[float]]:
        """
        Compute the Laplacian matrix of the graph.
        L = D - A where D is degree matrix and A is adjacency matrix.
        """
        # Initialize Laplacian with zeros
        laplacian = [[0.0] * self.n for _ in range(self.n)]
        
        # Fill in off-diagonal elements (negative conductances)
        for i, node1 in enumerate(self.nodes):
            for node2, weight in self.graph[node1].items():
                j = self.node_to_index[node2]
                laplacian[i][j] = -weight
                laplacian[j][i] = -weight
        
        # Fill in diagonal elements (sum of conductances)
        for i, node in enumerate(self.nodes):
            laplacian[i][i] = sum(self.graph[node].values())
            
        return laplacian

    def _compute_moore_penrose_pinv(self) -> List[List[float]]:
        """
        Compute Moore-Penrose pseudo-inverse of Laplacian matrix using SVD.
        This implementation uses a simplified SVD for demonstration.
        """
        n = len(self.laplacian)
        
        # Center the matrix by subtracting mean
        mean = sum(sum(row) for row in self.laplacian) / (n * n)
        centered = [[self.laplacian[i][j] - mean 
                    for j in range(n)] for i in range(n)]
        
        # Simple power iteration to approximate dominant eigenvector
        def power_iteration(matrix: List[List[float]], num_iterations: int = 100) -> List[float]:
            vector = [1.0] * n
            for _ in range(num_iterations):
                new_vector = [sum(matrix[i][j] * vector[j] 
                                for j in range(n)) for i in range(n)]
                norm = math.sqrt(sum(x * x for x in new_vector))
                if norm > 0:
                    vector = [x / norm for x in new_vector]
            return vector
        
        # Compute pseudo-inverse using dominant eigenvector
        eigenvector = power_iteration(centered)
        eigenvalue = sum(centered[i][j] * eigenvector[i] * eigenvector[j] 
                        for i in range(n) for j in range(n))
        
        if abs(eigenvalue) > 1e-10:
            pinv = [[eigenvector[i] * eigenvector[j] / eigenvalue 
                    for j in range(n)] for i in range(n)]
        else:
            # Handle singular case
            pinv = [[0.0] * n for _ in range(n)]
            
        return pinv

    def get_effective_conductance(self, node1: str, node2: str) -> float:
        """
        Calculate the effective conductance between two nodes.

        Args:
            node1: First node identifier
            node2: Second node identifier

        Returns:
            Effective conductance between the nodes
        """
        resistance = self.get_resistance_distance(node1, node2)
        return 1 / resistance if resistance > 0 else float('inf')
#####################################
from typing import Dict, List, Set, Tuple, Optional
from collections import defaultdict
import heapq

class NetworkFlowAnalyzer(Distance):
    """
    Analyzes flow networks to identify maximum flows, bottlenecks, and critical paths.
    Implements multiple flow algorithms including Ford-Fulkerson and push-relabel methods.
    
    The network is represented as a weighted directed graph where edge weights represent
    flow capacities between nodes.
    """

    def __init__(self, network: Dict[str, Dict[str, float]]):
        """
        Initialize the flow network analyzer.

        Args:
            network: Dict[str, Dict[str, float]] where edge weights represent flow capacities
        """      
        super().__init__()
        self.type='graph'
        
        self.network = network
        self.nodes = set(network.keys())
        self.residual_network = self._create_residual_network()

    def get_maximum_flow(self, source: str, sink: str) -> Tuple[float, Dict[str, Dict[str, float]]]:
        """
        Calculate the maximum flow from source to sink using the push-relabel algorithm.

        Args:
            source: Source node identifier
            sink: Sink node identifier

        Returns:
            Tuple of (maximum flow value, flow assignment dictionary)
        """
        if source not in self.nodes or sink not in self.nodes:
            raise ValueError("Source or sink node not found in network")

        # Initialize height and excess flow for each node
        height = {node: 0 for node in self.nodes}
        height[source] = len(self.nodes)
        
        excess = {node: 0 for node in self.nodes}
        flow = defaultdict(lambda: defaultdict(float))
        
        # Push flow from source to its neighbors
        for neighbor, capacity in self.network[source].items():
            flow[source][neighbor] = capacity
            flow[neighbor][source] = -capacity
            excess[neighbor] = capacity
            excess[source] -= capacity

        while self._exists_active_node(excess, height, source, sink):
            node = self._get_highest_active_node(excess, height, source, sink)
            
            if not self._push_flow(node, excess, height, flow):
                self._relabel_node(node, height, flow)

        max_flow = sum(flow[source][node] for node in self.network[source])
        return max_flow, dict(flow)

    def get_bottlenecks(self, source: str, sink: str) -> List[Tuple[str, str, float]]:
        """
        Identify network bottlenecks (minimum cuts) in the flow network.

        Args:
            source: Source node identifier
            sink: Sink node identifier

        Returns:
            List of tuples (node1, node2, capacity) representing bottleneck edges
        """
        # Get maximum flow and residual network
        _, flow = self.get_maximum_flow(source, sink)
        
        # Find nodes reachable from source in residual network
        reachable = self._get_reachable_nodes(source, flow)
        
        # Identify bottleneck edges
        bottlenecks = []
        for node in reachable:
            for neighbor, capacity in self.network[node].items():
                if neighbor not in reachable and capacity > 0:
                    bottlenecks.append((node, neighbor, capacity))
                    
        return sorted(bottlenecks, key=lambda x: x[2])

    def get_path_capacity(self, path: List[str]) -> float:
        """
        Calculate the minimum capacity (bottleneck) along a given path.

        Args:
            path: List of node identifiers representing a path

        Returns:
            Minimum capacity along the path
        """
        if len(path) < 2:
            return 0.0
            
        capacity = float('inf')
        for i in range(len(path) - 1):
            node1, node2 = path[i], path[i + 1]
            if node2 not in self.network[node1]:
                return 0.0
            capacity = min(capacity, self.network[node1][node2])
            
        return capacity

    def get_edge_utilization(self, source: str, sink: str) -> Dict[Tuple[str, str], float]:
        """
        Calculate edge utilization ratios based on maximum flow.

        Args:
            source: Source node identifier
            sink: Sink node identifier

        Returns:
            Dictionary mapping edge tuples to their utilization ratios (0 to 1)
        """
        _, flow = self.get_maximum_flow(source, sink)
        utilization = {}
        
        for node in self.network:
            for neighbor, capacity in self.network[node].items():
                if capacity > 0:
                    actual_flow = abs(flow[node][neighbor])
                    utilization[(node, neighbor)] = actual_flow / capacity
                    
        return utilization

    def get_node_throughput(self, source: str, sink: str) -> Dict[str, float]:
        """
        Calculate total flow throughput for each node in the network.

        Args:
            source: Source node identifier
            sink: Sink node identifier

        Returns:
            Dictionary mapping nodes to their total throughput values
        """
        _, flow = self.get_maximum_flow(source, sink)
        throughput = defaultdict(float)
        
        for node in self.network:
            for neighbor, _ in self.network[node].items():
                if flow[node][neighbor] > 0:
                    throughput[node] += flow[node][neighbor]
                    throughput[neighbor] += flow[node][neighbor]
                    
        return dict(throughput)

    def _create_residual_network(self) -> Dict[str, Dict[str, float]]:
        """Create initial residual network from capacity network."""
        residual = defaultdict(lambda: defaultdict(float))
        
        for node in self.network:
            for neighbor, capacity in self.network[node].items():
                residual[node][neighbor] = capacity
                residual[neighbor][node] = 0
                
        return dict(residual)

    def _exists_active_node(self, excess: Dict[str, float], height: Dict[str, int], 
                           source: str, sink: str) -> bool:
        """Check if there exists an active node in the network."""
        return any(excess[node] > 0 and node not in {source, sink} 
                  for node in self.nodes)

    def _get_highest_active_node(self, excess: Dict[str, float], height: Dict[str, int],
                                source: str, sink: str) -> str:
        """Find the active node with highest height."""
        max_height = -1
        max_node = None
        
        for node in self.nodes:
            if node not in {source, sink} and excess[node] > 0:
                if height[node] > max_height:
                    max_height = height[node]
                    max_node = node
                    
        return max_node

    def _push_flow(self, node: str, excess: Dict[str, float], height: Dict[str, int],
                   flow: Dict[str, Dict[str, float]]) -> bool:
        """Push excess flow from a node to its neighbors."""
        for neighbor in self.network[node]:
            if (height[node] > height[neighbor] and 
                flow[node][neighbor] < self.network[node].get(neighbor, 0)):
                
                push_amount = min(excess[node],
                                self.network[node][neighbor] - flow[node][neighbor])
                
                flow[node][neighbor] += push_amount
                flow[neighbor][node] -= push_amount
                excess[node] -= push_amount
                excess[neighbor] += push_amount
                
                if excess[node] == 0:
                    return True
                    
        return False

    def _relabel_node(self, node: str, height: Dict[str, int],
                      flow: Dict[str, Dict[str, float]]) -> None:
        """Relabel a node by increasing its height."""
        min_height = float('inf')
        
        for neighbor in self.network[node]:
            if flow[node][neighbor] < self.network[node].get(neighbor, 0):
                min_height = min(min_height, height[neighbor])
                
        height[node] = min_height + 1

    def _get_reachable_nodes(self, source: str, 
                            flow: Dict[str, Dict[str, float]]) -> Set[str]:
        """Find all nodes reachable from source in residual network."""
        reachable = {source}
        queue = [source]
        
        while queue:
            node = queue.pop(0)
            for neighbor in self.network[node]:
                if (neighbor not in reachable and 
                    flow[node][neighbor] < self.network[node][neighbor]):
                    reachable.add(neighbor)
                    queue.append(neighbor)
                    
        return reachable
#######################################
from typing import Dict, List, Set, Tuple
import random
import math
from collections import defaultdict, Counter

class RandomWalkCentrality(Distance):
    """
    Calculates various centrality metrics based on random walks in weighted networks.
    
    This implementation provides multiple approaches to analyze node importance through
    random walk probabilities, including steady-state distributions, hitting times,
    and return probabilities.
    """

    def __init__(self, network: Dict[str, Dict[str, float]], alpha: float = 0.85):
        """
        Initialize the random walk calculator.

        Args:
            network: Dict[str, Dict[str, float]] representing weighted edges
            alpha: Damping factor for PageRank-like calculations (default: 0.85)
        """      
        super().__init__()
        self.type='graph'
        
        self.network = network
        self.nodes = list(network.keys())
        self.alpha = alpha
        
        # Precompute transition probabilities
        self.transition_probs = self._compute_transition_probabilities()

    def get_stationary_distribution(self, num_iterations: int = 1000, 
                                  tolerance: float = 1e-6) -> Dict[str, float]:
        """
        Calculate the stationary distribution (limiting probabilities) for the random walk.

        Args:
            num_iterations: Maximum number of iterations for convergence
            tolerance: Convergence threshold for probability changes

        Returns:
            Dictionary mapping nodes to their stationary probabilities
        """
        # Initialize uniform distribution
        distribution = {node: 1.0 / len(self.nodes) for node in self.nodes}
        
        for _ in range(num_iterations):
            new_distribution = defaultdict(float)
            
            # Update probabilities using transition matrix
            for node in self.nodes:
                for neighbor, prob in self.transition_probs[node].items():
                    new_distribution[neighbor] += distribution[node] * prob
            
            # Check convergence
            max_diff = max(abs(new_distribution[node] - distribution[node]) 
                         for node in self.nodes)
            
            distribution = dict(new_distribution)
            
            if max_diff < tolerance:
                break
                
        return distribution

    def get_hitting_times(self, start_node: str, 
                         num_walks: int = 1000) -> Dict[str, float]:
        """
        Calculate average hitting times from start node to all other nodes.

        Args:
            start_node: Starting node for random walks
            num_walks: Number of random walks to simulate

        Returns:
            Dictionary mapping nodes to their average hitting times
        """
        hitting_times = defaultdict(list)
        
        for _ in range(num_walks):
            visited = {start_node}
            current = start_node
            steps = 0
            
            while len(visited) < len(self.nodes):
                steps += 1
                # Choose next node based on transition probabilities
                neighbors = self.transition_probs[current]
                next_node = random.choices(
                    list(neighbors.keys()),
                    weights=list(neighbors.values())
                )[0]
                
                if next_node not in visited:
                    hitting_times[next_node].append(steps)
                    visited.add(next_node)
                    
                current = next_node
        
        # Calculate average hitting times
        return {node: sum(times) / len(times) 
                for node, times in hitting_times.items()}

    def get_random_walk_centrality(self) -> Dict[str, float]:
        """
        Calculate random walk centrality based on stationary distribution and mixing time.

        Returns:
            Dictionary mapping nodes to their random walk centrality scores
        """
        stationary = self.get_stationary_distribution()
        mixing_times = self._estimate_mixing_times()
        
        centrality = {}
        max_mixing = max(mixing_times.values())
        
        for node in self.nodes:
            # Combine stationary probability and inverse mixing time
            centrality[node] = stationary[node] * (1 - mixing_times[node] / max_mixing)
            
        return centrality

    def get_return_probabilities(self, num_steps: List[int]) -> Dict[str, Dict[int, float]]:
        """
        Calculate return probabilities for different walk lengths.

        Args:
            num_steps: List of walk lengths to analyze

        Returns:
            Nested dictionary mapping nodes and steps to return probabilities
        """
        return_probs = defaultdict(dict)
        
        for node in self.nodes:
            for steps in num_steps:
                probability = self._calculate_return_probability(node, steps)
                return_probs[node][steps] = probability
                
        return dict(return_probs)

    def get_mixing_rate(self) -> float:
        """
        Calculate the mixing rate of the random walk process.

        Returns:
            Mixing rate (second largest eigenvalue approximation)
        """
        distributions = []
        current_dist = {node: 1.0 if node == self.nodes[0] else 0.0 
                       for node in self.nodes}
        
        for _ in range(100):  # Track 100 steps
            next_dist = defaultdict(float)
            for node in self.nodes:
                for neighbor, prob in self.transition_probs[node].items():
                    next_dist[neighbor] += current_dist[node] * prob
                    
            distributions.append(dict(next_dist))
            current_dist = next_dist
        
        # Approximate mixing rate using consecutive distributions
        rates = []
        for i in range(1, len(distributions)):
            diff = max(abs(distributions[i][node] - distributions[i-1][node]) 
                      for node in self.nodes)
            if diff > 0:
                rates.append(diff)
                
        return sum(rates) / len(rates) if rates else 0.0

    def _compute_transition_probabilities(self) -> Dict[str, Dict[str, float]]:
        """Compute transition probabilities from edge weights."""
        transitions = defaultdict(dict)
        
        for node in self.network:
            total_weight = sum(self.network[node].values())
            if total_weight > 0:
                for neighbor, weight in self.network[node].items():
                    transitions[node][neighbor] = weight / total_weight
            else:
                # Handle dangling nodes with uniform probability
                for other in self.nodes:
                    if other != node:
                        transitions[node][other] = 1.0 / (len(self.nodes) - 1)
                        
        return dict(transitions)

    def _estimate_mixing_times(self) -> Dict[str, float]:
        """Estimate mixing times for each starting node."""
        mixing_times = {}
        stationary = self.get_stationary_distribution()
        
        for start_node in self.nodes:
            current_dist = {node: 1.0 if node == start_node else 0.0 
                          for node in self.nodes}
            steps = 0
            
            while steps < 1000:  # Cap at 1000 steps
                steps += 1
                next_dist = defaultdict(float)
                
                for node in self.nodes:
                    for neighbor, prob in self.transition_probs[node].items():
                        next_dist[neighbor] += current_dist[node] * prob
                
                # Check convergence to stationary distribution
                max_diff = max(abs(next_dist[node] - stationary[node]) 
                             for node in self.nodes)
                
                if max_diff < 0.01:  # Convergence threshold
                    break
                    
                current_dist = dict(next_dist)
                
            mixing_times[start_node] = steps
            
        return mixing_times

    def _calculate_return_probability(self, node: str, steps: int,
                                   num_walks: int = 1000) -> float:
        """Calculate probability of returning to starting node after given steps."""
        returns = 0
        
        for _ in range(num_walks):
            current = node
            
            for _ in range(steps):
                neighbors = self.transition_probs[current]
                current = random.choices(
                    list(neighbors.keys()),
                    weights=list(neighbors.values())
                )[0]
            
            if current == node:
                returns += 1
                
        return returns / num_walks
        
#########################################
from typing import Dict, Set, List, Tuple
from collections import defaultdict
import math

class GraphDensityAnalyzer(Distance):
    """
    Analyzes graph density metrics for both directed and undirected weighted networks.
    
    Provides comprehensive density analysis including global density, local density,
    community density, and temporal density for dynamic networks. Handles both
    binary and weighted network representations.
    """

    def __init__(self, network: Dict[str, Dict[str, float]], is_directed: bool = False):
        """
        Initialize the density analyzer.

        Args:
            network: Dict[str, Dict[str, float]] representing edge weights
            is_directed: Boolean indicating if the network is directed
        """      
        super().__init__()
        self.type='graph'
        
        self.network = network
        self.is_directed = is_directed
        self.nodes = list(network.keys())
        self.num_nodes = len(self.nodes)

    def get_global_density(self) -> float:
        """
        Calculate global density of the network.
        
        For directed networks: |E| / (|V| * (|V| - 1))
        For undirected networks: 2 * |E| / (|V| * (|V| - 1))

        Returns:
            Float representing global density (0 to 1)
        """
        if self.num_nodes < 2:
            return 0.0
            
        total_edges = sum(len(neighbors) for neighbors in self.network.values())
        
        if not self.is_directed:
            total_edges //= 2  # Each edge counted twice in undirected network
            
        max_possible_edges = self.num_nodes * (self.num_nodes - 1)
        if not self.is_directed:
            max_possible_edges //= 2
            
        return total_edges / max_possible_edges if max_possible_edges > 0 else 0.0

    def get_weighted_density(self) -> float:
        """
        Calculate density considering edge weights.
        Normalized by maximum possible weight.

        Returns:
            Float representing weighted density (0 to 1)
        """
        if self.num_nodes < 2:
            return 0.0
            
        total_weight = sum(sum(weights.values()) 
                          for weights in self.network.values())
        
        if not self.is_directed:
            total_weight /= 2  # Each edge weight counted twice
            
        # Use maximum observed weight for normalization
        max_weight = max(max(weights.values()) if weights else 0 
                        for weights in self.network.values())
        
        if max_weight == 0:
            return 0.0
            
        max_possible_edges = self.num_nodes * (self.num_nodes - 1)
        if not self.is_directed:
            max_possible_edges //= 2
            
        return total_weight / (max_weight * max_possible_edges)

    def get_local_density(self, node: str) -> float:
        """
        Calculate local density (clustering coefficient) for a specific node.

        Args:
            node: Target node identifier

        Returns:
            Float representing local density (0 to 1)
        """
        if node not in self.network:
            raise ValueError(f"Node {node} not found in network")
            
        neighbors = set(self.network[node].keys())
        if len(neighbors) < 2:
            return 0.0
            
        # Count edges between neighbors
        neighbor_edges = 0
        for n1 in neighbors:
            for n2 in neighbors:
                if n1 != n2 and n2 in self.network.get(n1, {}):
                    neighbor_edges += 1
                    
        if not self.is_directed:
            neighbor_edges //= 2
            
        max_neighbor_edges = len(neighbors) * (len(neighbors) - 1)
        if not self.is_directed:
            max_neighbor_edges //= 2
            
        return neighbor_edges / max_neighbor_edges if max_neighbor_edges > 0 else 0.0

    def get_community_density(self, community: Set[str]) -> float:
        """
        Calculate density within a community of nodes.

        Args:
            community: Set of node identifiers in the community

        Returns:
            Float representing community density (0 to 1)
        """
        if not community.issubset(set(self.nodes)):
            raise ValueError("Community contains nodes not in network")
            
        if len(community) < 2:
            return 0.0
            
        internal_edges = sum(1 for node in community 
                           for neighbor in self.network[node] 
                           if neighbor in community)
        
        if not self.is_directed:
            internal_edges //= 2
            
        max_internal_edges = len(community) * (len(community) - 1)
        if not self.is_directed:
            max_internal_edges //= 2
            
        return internal_edges / max_internal_edges

    def get_density_distribution(self) -> Dict[str, float]:
        """
        Calculate density distribution across all nodes.

        Returns:
            Dictionary mapping nodes to their local densities
        """
        return {node: self.get_local_density(node) for node in self.nodes}

    def get_density_metrics(self) -> Dict[str, float]:
        """
        Calculate comprehensive set of density metrics.

        Returns:
            Dictionary containing various density measurements
        """
        metrics = {
            'global_density': self.get_global_density(),
            'weighted_density': self.get_weighted_density(),
            'average_local_density': sum(self.get_density_distribution().values()) / self.num_nodes,
            'density_variance': self._calculate_density_variance()
        }
        
        # Add degree-based metrics
        degree_sequence = [len(self.network[node]) for node in self.nodes]
        metrics['degree_density'] = sum(degree_sequence) / (self.num_nodes * (self.num_nodes - 1))
        
        return metrics

    def get_temporal_density(self, snapshots: List[Dict[str, Dict[str, float]]]) -> List[float]:
        """
        Calculate density evolution over temporal snapshots.

        Args:
            snapshots: List of network snapshots over time

        Returns:
            List of density values for each timestamp
        """
        temporal_densities = []
        
        for snapshot in snapshots:
            temp_analyzer = GraphDensityAnalyzer(snapshot, self.is_directed)
            temporal_densities.append(temp_analyzer.get_global_density())
            
        return temporal_densities

    def _calculate_density_variance(self) -> float:
        """Calculate variance in local density across nodes."""
        densities = list(self.get_density_distribution().values())
        mean_density = sum(densities) / len(densities)
        
        variance = sum((d - mean_density) ** 2 for d in densities) / len(densities)
        return variance
##################################
from typing import Dict, List, Set, Tuple
from collections import defaultdict

class AverageClusteringCoefficients(Distance):
    """
    A class to calculate distances between weighted graphs represented as dictionaries.
    Graphs are represented as Dict[str, Dict[str, float]] where:
    - Outer key: source node
    - Inner key: destination node
    - Value: edge weight
    """
    
    def __init__(self) -> None:
        """Initialize the GraphDistanceCalculator."""      
        super().__init__()
        self.type='graph'
            
    def get_neighbors(self, graph: Dict[str, Dict[str, float]], node: str) -> Set[str]:
        """
        Get all neighbors of a given node in the graph.
        
        Args:
            graph: The input graph
            node: The node to find neighbors for
            
        Returns:
            A set of neighboring nodes
        """
        return set(graph.get(node, {}).keys())
    
    def calculate_clustering_coefficient(self, graph: Dict[str, Dict[str, float]], node: str) -> float:
        """
        Calculate the clustering coefficient for a single node.
        
        The clustering coefficient measures how close the node's neighbors are to being
        a complete graph. It's calculated as:
        C(v) = (2 * L) / (k * (k-1))
        where L is the number of links between neighbors and k is the number of neighbors.
        
        Args:
            graph: The input graph
            node: The node to calculate clustering coefficient for
            
        Returns:
            Clustering coefficient value between 0 and 1
        """
        neighbors = self.get_neighbors(graph, node)
        if len(neighbors) < 2:
            return 0.0
        
        possible_connections = len(neighbors) * (len(neighbors) - 1) / 2
        actual_connections = 0
        
        # Count actual connections between neighbors
        for neighbor1 in neighbors:
            neighbor1_connections = self.get_neighbors(graph, neighbor1)
            for neighbor2 in neighbors:
                if neighbor1 < neighbor2 and neighbor2 in neighbor1_connections:
                    actual_connections += 1
        
        return actual_connections / possible_connections if possible_connections > 0 else 0.0
    
    def calculate_average_clustering(self, graph: Dict[str, Dict[str, float]]) -> float:
        """
        Calculate the average clustering coefficient for the entire graph.
        
        Args:
            graph: The input graph
            
        Returns:
            Average clustering coefficient for the graph
        """
        if not graph:
            return 0.0
        
        total_coefficient = 0.0
        for node in graph:
            total_coefficient += self.calculate_clustering_coefficient(graph, node)
        
        return total_coefficient / len(graph)
    
    def compute(self, graph1: Dict[str, Dict[str, float]], 
                               graph2: Dict[str, Dict[str, float]]) -> float:
        """
        Calculate the distance between two graphs based on their average clustering coefficients.
        
        The distance is calculated as the absolute difference between their average
        clustering coefficients. This provides a simple metric for how different the
        graphs are in terms of their clustering structure.
        
        Args:
            graph1: First input graph
            graph2: Second input graph
            
        Returns:
            Distance value between 0 and 1, where:
            - 0 means the graphs have identical clustering coefficients
            - 1 means maximum difference in clustering coefficients
        """
        acc1 = self.calculate_average_clustering(graph1)
        acc2 = self.calculate_average_clustering(graph2)
        
        return abs(acc1 - acc2)
#######################################
from typing import Dict, List, Set, Tuple
from collections import defaultdict
import math

class Diameter(Distance):
    """
    A class to calculate distances between weighted graphs represented as dictionaries.
    Graphs are represented as Dict[str, Dict[str, float]] where:
    - Outer key: source node
    - Inner key: destination node
    - Value: edge weight
    """
    
    def __init__(self) -> None:
        """Initialize the GraphDistanceCalculator."""      
        super().__init__()
        self.type='graph'
            
    def get_neighbors(self, graph: Dict[str, Dict[str, float]], node: str) -> Set[str]:
        """
        Get all neighbors of a given node in the graph.
        
        Args:
            graph: The input graph
            node: The node to find neighbors for
            
        Returns:
            A set of neighboring nodes
        """
        return set(graph.get(node, {}).keys())
    
    def calculate_clustering_coefficient(self, graph: Dict[str, Dict[str, float]], node: str) -> float:
        """
        Calculate the clustering coefficient for a single node.
        
        The clustering coefficient measures how close the node's neighbors are to being
        a complete graph. It's calculated as:
        C(v) = (2 * L) / (k * (k-1))
        where L is the number of links between neighbors and k is the number of neighbors.
        
        Args:
            graph: The input graph
            node: The node to calculate clustering coefficient for
            
        Returns:
            Clustering coefficient value between 0 and 1
        """
        neighbors = self.get_neighbors(graph, node)
        if len(neighbors) < 2:
            return 0.0
        
        possible_connections = len(neighbors) * (len(neighbors) - 1) / 2
        actual_connections = 0
        
        # Count actual connections between neighbors
        for neighbor1 in neighbors:
            neighbor1_connections = self.get_neighbors(graph, neighbor1)
            for neighbor2 in neighbors:
                if neighbor1 < neighbor2 and neighbor2 in neighbor1_connections:
                    actual_connections += 1
        
        return actual_connections / possible_connections if possible_connections > 0 else 0.0
    
    def calculate_average_clustering(self, graph: Dict[str, Dict[str, float]]) -> float:
        """
        Calculate the average clustering coefficient for the entire graph.
        
        Args:
            graph: The input graph
            
        Returns:
            Average clustering coefficient for the graph
        """
        if not graph:
            return 0.0
        
        total_coefficient = 0.0
        for node in graph:
            total_coefficient += self.calculate_clustering_coefficient(graph, node)
        
        return total_coefficient / len(graph)

    def calculate_diameter(self, graph: Dict[str, Dict[str, float]]) -> float:
        """
        Calculate the diameter of the graph using Floyd-Warshall algorithm.
        The diameter is the longest shortest path between any two nodes.
        
        Args:
            graph: The input graph
            
        Returns:
            The diameter of the graph. Returns infinity if graph is disconnected.
        """
        if not graph:
            return 0.0
            
        # Initialize distance matrix with infinity
        nodes = list(graph.keys())
        n = len(nodes)
        node_to_index = {node: i for i, node in enumerate(nodes)}
        
        # Initialize distances matrix with infinity
        distances = [[float('inf')] * n for _ in range(n)]
        
        # Set diagonal to 0 and fill known distances
        for i in range(n):
            distances[i][i] = 0
            node = nodes[i]
            for neighbor, weight in graph[node].items():
                j = node_to_index[neighbor]
                distances[i][j] = weight
        
        # Floyd-Warshall algorithm
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if distances[i][k] != float('inf') and distances[k][j] != float('inf'):
                        distances[i][j] = min(
                            distances[i][j],
                            distances[i][k] + distances[k][j]
                        )
        
        # Find the maximum finite distance (diameter)
        diameter = 0.0
        for i in range(n):
            for j in range(n):
                if distances[i][j] != float('inf'):
                    diameter = max(diameter, distances[i][j])
        
        return diameter if diameter != 0.0 else float('inf')
    
    def compute(self, graph1: Dict[str, Dict[str, float]], 
                               graph2: Dict[str, Dict[str, float]]) -> Tuple[float, float]:
        """
        Calculate the distance between two graphs based on their average clustering coefficients
        and diameters.
        
        The distance is calculated as a tuple of:
        1. The absolute difference between their average clustering coefficients
        2. The absolute difference between their normalized diameters
        
        Args:
            graph1: First input graph
            graph2: Second input graph
            
        Returns:
            A tuple of (clustering_distance, diameter_distance) where each value is between 0 and 1:
            - 0 means the graphs have identical metrics
            - 1 means maximum difference in metrics
        """
        # Calculate clustering coefficient distance
        acc1 = self.calculate_average_clustering(graph1)
        acc2 = self.calculate_average_clustering(graph2)
        clustering_distance = abs(acc1 - acc2)
        
        # Calculate diameter distance
        diam1 = self.calculate_diameter(graph1)
        diam2 = self.calculate_diameter(graph2)
        
        # Normalize diameters by taking their ratio (if both are finite)
        if diam1 != float('inf') and diam2 != float('inf'):
            max_diam = max(diam1, diam2)
            min_diam = min(diam1, diam2)
            diameter_distance = 0.0 if max_diam == 0 else (max_diam - min_diam) / max_diam
        else:
            # If one or both graphs are disconnected, set maximum distance
            diameter_distance = 1.0
        
        return (clustering_distance, diameter_distance)
##############################################
from typing import Dict, List, Set, Tuple
from collections import defaultdict
import math

class Radius(Distance):
    """
    A class to calculate distances between weighted graphs represented as dictionaries.
    Graphs are represented as Dict[str, Dict[str, float]] where:
    - Outer key: source node
    - Inner key: destination node
    - Value: edge weight
    """
    
    def __init__(self) -> None:
        """Initialize the GraphDistanceCalculator."""      
        super().__init__()
        self.type='graph'
            
    def get_neighbors(self, graph: Dict[str, Dict[str, float]], node: str) -> Set[str]:
        """
        Get all neighbors of a given node in the graph.
        
        Args:
            graph: The input graph
            node: The node to find neighbors for
            
        Returns:
            A set of neighboring nodes
        """
        return set(graph.get(node, {}).keys())
    
    def calculate_clustering_coefficient(self, graph: Dict[str, Dict[str, float]], node: str) -> float:
        """
        Calculate the clustering coefficient for a single node.
        
        The clustering coefficient measures how close the node's neighbors are to being
        a complete graph. It's calculated as:
        C(v) = (2 * L) / (k * (k-1))
        where L is the number of links between neighbors and k is the number of neighbors.
        
        Args:
            graph: The input graph
            node: The node to calculate clustering coefficient for
            
        Returns:
            Clustering coefficient value between 0 and 1
        """
        neighbors = self.get_neighbors(graph, node)
        if len(neighbors) < 2:
            return 0.0
        
        possible_connections = len(neighbors) * (len(neighbors) - 1) / 2
        actual_connections = 0
        
        # Count actual connections between neighbors
        for neighbor1 in neighbors:
            neighbor1_connections = self.get_neighbors(graph, neighbor1)
            for neighbor2 in neighbors:
                if neighbor1 < neighbor2 and neighbor2 in neighbor1_connections:
                    actual_connections += 1
        
        return actual_connections / possible_connections if possible_connections > 0 else 0.0
    
    def calculate_average_clustering(self, graph: Dict[str, Dict[str, float]]) -> float:
        """
        Calculate the average clustering coefficient for the entire graph.
        
        Args:
            graph: The input graph
            
        Returns:
            Average clustering coefficient for the graph
        """
        if not graph:
            return 0.0
        
        total_coefficient = 0.0
        for node in graph:
            total_coefficient += self.calculate_clustering_coefficient(graph, node)
        
        return total_coefficient / len(graph)

    def calculate_all_pairs_shortest_paths(self, graph: Dict[str, Dict[str, float]]) -> List[List[float]]:
        """
        Calculate all pairs shortest paths using Floyd-Warshall algorithm.
        
        Args:
            graph: The input graph
            
        Returns:
            A matrix of shortest paths distances and the mapping of nodes to indices
        """
        if not graph:
            return [], {}
            
        # Initialize distance matrix with infinity
        nodes = list(graph.keys())
        n = len(nodes)
        node_to_index = {node: i for i, node in enumerate(nodes)}
        
        # Initialize distances matrix with infinity
        distances = [[float('inf')] * n for _ in range(n)]
        
        # Set diagonal to 0 and fill known distances
        for i in range(n):
            distances[i][i] = 0
            node = nodes[i]
            for neighbor, weight in graph[node].items():
                j = node_to_index[neighbor]
                distances[i][j] = weight
        
        # Floyd-Warshall algorithm
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if distances[i][k] != float('inf') and distances[k][j] != float('inf'):
                        distances[i][j] = min(
                            distances[i][j],
                            distances[i][k] + distances[k][j]
                        )
        
        return distances, node_to_index

    def calculate_diameter(self, graph: Dict[str, Dict[str, float]]) -> float:
        """
        Calculate the diameter of the graph.
        The diameter is the longest shortest path between any two nodes.
        
        Args:
            graph: The input graph
            
        Returns:
            The diameter of the graph. Returns infinity if graph is disconnected.
        """
        distances, _ = self.calculate_all_pairs_shortest_paths(graph)
        if not distances:
            return 0.0
            
        # Find the maximum finite distance (diameter)
        diameter = 0.0
        for row in distances:
            for dist in row:
                if dist != float('inf'):
                    diameter = max(diameter, dist)
        
        return diameter if diameter != 0.0 else float('inf')

    def calculate_radius(self, graph: Dict[str, Dict[str, float]]) -> float:
        """
        Calculate the radius of the graph.
        The radius is the minimum eccentricity among all vertices, where eccentricity
        of a vertex is its maximum distance to any other vertex.
        
        Args:
            graph: The input graph
            
        Returns:
            The radius of the graph. Returns infinity if graph is disconnected.
        """
        distances, _ = self.calculate_all_pairs_shortest_paths(graph)
        if not distances:
            return 0.0
            
        # Calculate eccentricity for each node (maximum distance to any other node)
        # Radius is the minimum eccentricity
        radius = float('inf')
        for i, row in enumerate(distances):
            eccentricity = 0.0
            all_infinite = True
            
            for dist in row:
                if dist != float('inf'):
                    all_infinite = False
                    eccentricity = max(eccentricity, dist)
            
            # Only update radius if node can reach all other nodes
            if not all_infinite:
                radius = min(radius, eccentricity)
        
        return radius if radius != float('inf') else float('inf')
    
    def compute(self, graph1: Dict[str, Dict[str, float]], 
                               graph2: Dict[str, Dict[str, float]]) -> Tuple[float, float, float]:
        """
        Calculate the distance between two graphs based on their metrics:
        - Average clustering coefficients
        - Diameters
        - Radii
        
        Args:
            graph1: First input graph
            graph2: Second input graph
            
        Returns:
            A tuple of (clustering_distance, diameter_distance, radius_distance) where each value 
            is between 0 and 1:
            - 0 means the graphs have identical metrics
            - 1 means maximum difference in metrics
        """
        # Calculate clustering coefficient distance
        acc1 = self.calculate_average_clustering(graph1)
        acc2 = self.calculate_average_clustering(graph2)
        clustering_distance = abs(acc1 - acc2)
        
        # Calculate diameter distance
        diam1 = self.calculate_diameter(graph1)
        diam2 = self.calculate_diameter(graph2)
        
        # Calculate radius distance
        rad1 = self.calculate_radius(graph1)
        rad2 = self.calculate_radius(graph2)
        
        # Normalize diameter and radius distances
        def normalize_metric_distance(val1: float, val2: float) -> float:
            if val1 != float('inf') and val2 != float('inf'):
                max_val = max(val1, val2)
                min_val = min(val1, val2)
                return 0.0 if max_val == 0 else (max_val - min_val) / max_val
            return 1.0  # Maximum distance if one or both graphs are disconnected
        
        diameter_distance = normalize_metric_distance(diam1, diam2)
        radius_distance = normalize_metric_distance(rad1, rad2)
        
        return (clustering_distance, diameter_distance, radius_distance)
#########################################################
from typing import Dict, List, Set, Tuple, DefaultDict
from collections import defaultdict
import math
import random

class Modularity(Distance):
    """
    A class to calculate distances between weighted graphs represented as dictionaries,
    including community detection metrics.
    Graphs are represented as Dict[str, Dict[str, float]] where:
    - Outer key: source node
    - Inner key: destination node
    - Value: edge weight
    """
    
    def __init__(self) -> None:
        """Initialize the GraphDistanceCalculator."""      
        super().__init__()
        self.type='graph'
        
    # [Previous methods remain unchanged: get_neighbors, calculate_clustering_coefficient, 
    # calculate_average_clustering, calculate_all_pairs_shortest_paths, calculate_diameter, 
    # calculate_radius remain exactly as they were]

    def calculate_modularity(self, graph: Dict[str, Dict[str, float]]) -> Tuple[float, Dict[str, int]]:
        """
        Calculate the modularity of the graph using the Louvain algorithm.
        Modularity measures the strength of division of a network into communities.
        
        Args:
            graph: The input graph
            
        Returns:
            A tuple of (modularity_score, community_assignments) where:
            - modularity_score is between -1 and 1
            - community_assignments maps each node to its community ID
        """
        if not graph:
            return 0.0, {}

        # Calculate total edge weight and degree for each node
        total_weight = 0.0
        node_degrees: DefaultDict[str, float] = defaultdict(float)
        
        for node, neighbors in graph.items():
            for neighbor, weight in neighbors.items():
                node_degrees[node] += weight
                total_weight += weight / 2  # Divide by 2 as each edge is counted twice
        
        def calculate_modularity_gain(node: str, neighbor: str, community: Dict[str, int],
                                    current_comm: int, neighbor_comm: int) -> float:
            """Calculate the modularity gain of moving node to neighbor's community."""
            if current_comm == neighbor_comm:
                return 0.0
                
            # Sum of weights inside the communities
            ki_in = sum(graph[node].get(n, 0.0) 
                       for n in graph[node] if community.get(n) == neighbor_comm)
            ki = node_degrees[node]
            tot = sum(node_degrees[n] for n, c in community.items() if c == neighbor_comm)
            
            return (ki_in - ki * tot / (2 * total_weight))

        def one_level() -> Dict[str, int]:
            """Execute one level of the Louvain algorithm."""
            current_mod = 0.0
            community = {node: i for i, node in enumerate(graph)}
            improvement = True
            
            while improvement:
                improvement = False
                for node in graph:
                    current_comm = community[node]
                    best_comm = current_comm
                    best_gain = 0.0
                    
                    # Check all neighboring communities
                    for neighbor in graph[node]:
                        neighbor_comm = community[neighbor]
                        gain = calculate_modularity_gain(node, neighbor, community,
                                                       current_comm, neighbor_comm)
                        
                        if gain > best_gain:
                            best_gain = gain
                            best_comm = neighbor_comm
                    
                    # Move node to best community if there is an improvement
                    if best_comm != current_comm:
                        community[node] = best_comm
                        current_mod += best_gain
                        improvement = True
            
            return community

        # Execute the algorithm
        community = one_level()
        
        # Calculate final modularity
        modularity = 0.0
        for i in graph:
            for j in graph[i]:
                if community[i] == community[j]:
                    actual = graph[i][j]
                    expected = (node_degrees[i] * node_degrees[j]) / (2 * total_weight)
                    modularity += (actual - expected)
        
        modularity = modularity / (2 * total_weight)
        
        return modularity, community

    def compute(self, graph1: Dict[str, Dict[str, float]], 
                               graph2: Dict[str, Dict[str, float]]) -> Tuple[float, float, float, float]:
        """
        Calculate the distance between two graphs based on their metrics:
        - Average clustering coefficients
        - Diameters
        - Radii
        - Modularity
        
        Args:
            graph1: First input graph
            graph2: Second input graph
            
        Returns:
            modularity_distance
            where each value is between 0 and 1:
            - 0 means the graphs have identical metrics
            - 1 means maximum difference in metrics
        """

        
        # Calculate modularity
        mod1, _ = self.calculate_modularity(graph1)
        mod2, _ = self.calculate_modularity(graph2)
        
        # Normalize all metrics
        def normalize_metric_distance(val1: float, val2: float) -> float:
            if val1 != float('inf') and val2 != float('inf'):
                max_val = max(val1, val2)
                min_val = min(val1, val2)
                return 0.0 if max_val == 0 else (max_val - min_val) / max_val
            return 1.0
        
        modularity_distance = abs(mod1 - mod2)  # Modularity is already normalized between -1 and 1
        
        return modularity_distance
####################################################
from typing import Dict, List, Set, Tuple, DefaultDict
from collections import defaultdict
import math
import random

class Assortativity(Distance):
    """
    A class to calculate distances between weighted graphs represented as dictionaries,
    including advanced network metrics.
    Graphs are represented as Dict[str, Dict[str, float]] where:
    - Outer key: source node
    - Inner key: destination node
    - Value: edge weight
    """
    
    def __init__(self) -> None:
        """Initialize the GraphDistanceCalculator."""      
        super().__init__()
        self.type='graph'
        
    # [Previous methods remain unchanged]

    def calculate_node_degrees(self, graph: Dict[str, Dict[str, float]]) -> Dict[str, float]:
        """
        Calculate the degree (sum of edge weights) for each node in the graph.
        
        Args:
            graph: The input graph
            
        Returns:
            Dictionary mapping nodes to their degrees
        """
        degrees: DefaultDict[str, float] = defaultdict(float)
        for node, neighbors in graph.items():
            for neighbor, weight in neighbors.items():
                degrees[node] += weight
                degrees[neighbor] += weight  # Count both ends of each edge
        return dict(degrees)

    def calculate_assortativity(self, graph: Dict[str, Dict[str, float]]) -> float:
        """
        Calculate the degree assortativity coefficient of the graph.
        This measures the tendency of nodes to connect to other nodes with similar degrees.
        
        The coefficient ranges from -1 to 1:
        - Positive values indicate that nodes tend to connect to nodes of similar degree
        - Negative values indicate that nodes tend to connect to nodes of different degree
        - Values near 0 indicate no particular pattern
        
        Args:
            graph: The input graph
            
        Returns:
            Assortativity coefficient between -1 and 1
        """
        if not graph:
            return 0.0

        # Calculate node degrees
        degrees = self.calculate_node_degrees(graph)
        
        # Calculate statistics for assortativity
        num_edges = sum(len(neighbors) for neighbors in graph.values()) / 2
        if num_edges == 0:
            return 0.0

        # Calculate sums for the formula
        sum_products = 0.0  # sum of products of degrees at each edge
        sum_degrees1 = 0.0  # sum of degrees at first end of each edge
        sum_degrees2 = 0.0  # sum of degrees at second end of each edge
        sum_squares1 = 0.0  # sum of squared degrees at first end
        sum_squares2 = 0.0  # sum of squared degrees at second end
        
        # Iterate through all edges
        seen_edges = set()  # Keep track of edges we've counted
        for node1, neighbors in graph.items():
            degree1 = degrees[node1]
            for node2, weight in neighbors.items():
                # Avoid counting each edge twice
                edge = tuple(sorted([node1, node2]))
                if edge in seen_edges:
                    continue
                seen_edges.add(edge)
                
                degree2 = degrees[node2]
                
                # Accumulate sums
                sum_products += degree1 * degree2 * weight
                sum_degrees1 += degree1 * weight
                sum_degrees2 += degree2 * weight
                sum_squares1 += degree1 * degree1 * weight
                sum_squares2 += degree2 * degree2 * weight

        # Calculate assortativity coefficient using the formula:
        # r = (M⁻¹ sum(jk) - [M⁻¹ sum(j)][M⁻¹ sum(k)]) /
        #     (M⁻¹ sum(j²) - [M⁻¹ sum(j)]² * M⁻¹ sum(k²) - [M⁻¹ sum(k)]²)^(1/2)
        M = sum(weight for neighbors in graph.values() for weight in neighbors.values()) / 2
        if M == 0:
            return 0.0

        numerator = (sum_products/M - (sum_degrees1/M) * (sum_degrees2/M))
        denominator_term1 = sum_squares1/M - (sum_degrees1/M)**2
        denominator_term2 = sum_squares2/M - (sum_degrees2/M)**2
        denominator = math.sqrt(denominator_term1 * denominator_term2)
        
        if abs(denominator) < 1e-8:  # Handle numerical instability
            return 0.0
            
        return numerator / denominator

    def compute(self, graph1: Dict[str, Dict[str, float]], 
                               graph2: Dict[str, Dict[str, float]]) -> Tuple[float, float, float, float, float]:
        """
        Calculate the distance between two graphs based on their metrics:

        - Assortativity
        
        Args:
            graph1: First input graph
            graph2: Second input graph
            
        Returns:
            assortativity_distance
            is between 0 and 1:
            - 0 means the graphs have identical metrics
            - 1 means maximum difference in metrics
        """
        
        def normalize_metric_distance(val1: float, val2: float) -> float:
            if val1 != float('inf') and val2 != float('inf'):
                max_val = max(val1, val2)
                min_val = min(val1, val2)
                return 0.0 if max_val == 0 else (max_val - min_val) / max_val
            return 1.0
        
        # Calculate assortativity distance
        assort1 = self.calculate_assortativity(graph1)
        assort2 = self.calculate_assortativity(graph2)
        assortativity_distance = abs(assort1 - assort2) / 2  # Divide by 2 since assortativity range is [-1,1]
        
        return assortativity_distance
############################################
from typing import Dict, List, Set, Tuple, DefaultDict
from collections import defaultdict
import math
import random

class Eccentricity(Distance):
    """
    A class to calculate distances between weighted graphs represented as dictionaries,
    including advanced network metrics.
    Graphs are represented as Dict[str, Dict[str, float]] where:
    - Outer key: source node
    - Inner key: destination node
    - Value: edge weight
    """
    
    def __init__(self) -> None:
        """Initialize the GraphDistanceCalculator."""      
        super().__init__()
        self.type='graph'
        
    # [Previous methods remain unchanged until calculate_radius]
    def calculate_all_pairs_shortest_paths(self, graph: Dict[str, Dict[str, float]]) -> List[List[float]]:
        """
        Calculate all pairs shortest paths using Floyd-Warshall algorithm.
        
        Args:
            graph: The input graph
            
        Returns:
            A matrix of shortest paths distances and the mapping of nodes to indices
        """
        if not graph:
            return [], {}
            
        # Initialize distance matrix with infinity
        nodes = list(graph.keys())
        n = len(nodes)
        node_to_index = {node: i for i, node in enumerate(nodes)}
        
        # Initialize distances matrix with infinity
        distances = [[float('inf')] * n for _ in range(n)]
        
        # Set diagonal to 0 and fill known distances
        for i in range(n):
            distances[i][i] = 0
            node = nodes[i]
            for neighbor, weight in graph[node].items():
                j = node_to_index[neighbor]
                distances[i][j] = weight
        
        # Floyd-Warshall algorithm
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if distances[i][k] != float('inf') and distances[k][j] != float('inf'):
                        distances[i][j] = min(
                            distances[i][j],
                            distances[i][k] + distances[k][j]
                        )
        
        return distances, node_to_index
    def calculate_eccentricity(self, graph: Dict[str, Dict[str, float]]) -> Dict[str, float]:
        """
        Calculate the eccentricity of each node in the graph.
        The eccentricity of a node v is the maximum shortest path distance from v to any other node.
        
        Args:
            graph: The input graph
            
        Returns:
            Dictionary mapping each node to its eccentricity.
            Returns infinity for nodes in disconnected components.
        """
        if not graph:
            return {}
            
        distances, node_to_index = self.calculate_all_pairs_shortest_paths(graph)
        index_to_node = {i: node for node, i in node_to_index.items()}
        
        eccentricities = {}
        for i in range(len(distances)):
            node = index_to_node[i]
            max_distance = 0.0
            all_infinite = True
            
            for dist in distances[i]:
                if dist != float('inf'):
                    all_infinite = False
                    max_distance = max(max_distance, dist)
            
            eccentricities[node] = float('inf') if all_infinite else max_distance
            
        return eccentricities

    def calculate_radius(self, graph: Dict[str, Dict[str, float]]) -> float:
        """
        Calculate the radius of the graph.
        The radius is the minimum eccentricity among all vertices.
        
        Args:
            graph: The input graph
            
        Returns:
            The radius of the graph. Returns infinity if graph is disconnected.
        """
        eccentricities = self.calculate_eccentricity(graph)
        if not eccentricities:
            return float('inf')
        
        # Radius is the minimum eccentricity
        return min(eccentricities.values())

    def calculate_diameter(self, graph: Dict[str, Dict[str, float]]) -> float:
        """
        Calculate the diameter of the graph.
        The diameter is the maximum eccentricity among all vertices.
        
        Args:
            graph: The input graph
            
        Returns:
            The diameter of the graph. Returns infinity if graph is disconnected.
        """
        eccentricities = self.calculate_eccentricity(graph)
        if not eccentricities:
            return float('inf')
            
        # Diameter is the maximum eccentricity
        finite_eccentricities = [e for e in eccentricities.values() if e != float('inf')]
        return max(finite_eccentricities) if finite_eccentricities else float('inf')

    def compute(self, graph1: Dict[str, Dict[str, float]], 
                               graph2: Dict[str, Dict[str, float]]) -> float:
        """
        Calculate the distance between two graphs based on their metrics:

        - eccentricity
        
        Args:
            graph1: First input graph
            graph2: Second input graph
            
        Returns:
            eccentricity
        """

        
        # Calculate average eccentricity for both graphs
        def avg_eccentricity(ecc_dict: Dict[str, float]) -> float:
            finite_eccs = [e for e in ecc_dict.values() if e != float('inf')]
            return sum(finite_eccs) / len(finite_eccs) if finite_eccs else float('inf')
            
        ecc1 = avg_eccentricity(self.calculate_eccentricity(graph1))
        ecc2 = avg_eccentricity(self.calculate_eccentricity(graph2))
        
        return abs(ecc1-ecc2)
        
##############################################
from typing import Dict, List, Set, Tuple
import math
from collections import defaultdict

class GraphEntropy(Distance):
    """
    A class to calculate various distance metrics between two weighted graphs.
    Graphs are represented as nested dictionaries where:
    - Outer key: source node (str)
    - Inner key: target node (str)
    - Value: edge weight (float)
    """
    
    def __init__(self) -> None:
        """Initialize the calculator."""      
        super().__init__()
        self.type='graph'
            
    @staticmethod
    def get_nodes(graph: Dict[str, Dict[str, float]]) -> Set[str]:
        """
        Get all unique nodes in the graph.
        
        Args:
            graph: Input graph as adjacency dictionary
            
        Returns:
            Set of all nodes in the graph
        """
        nodes = set(graph.keys())
        for edges in graph.values():
            nodes.update(edges.keys())
        return nodes
    
    def calculate_entropy(self, graph: Dict[str, Dict[str, float]]) -> float:
        """
        Calculate the entropy of a graph based on edge weights.
        
        Args:
            graph: Input graph as adjacency dictionary
            
        Returns:
            Entropy value of the graph
        """
        total_weight = 0.0
        weights: List[float] = []
        
        # Collect all weights
        for edges in graph.values():
            weights.extend(edges.values())
            total_weight += sum(edges.values())
        
        if not weights or total_weight == 0:
            return 0.0
            
        # Calculate probability distribution and entropy
        entropy = 0.0
        for weight in weights:
            prob = weight / total_weight
            if prob > 0:  # Avoid log(0)
                entropy -= prob * math.log2(prob)
                
        return entropy
    
    def calculate_degree_distribution(self, graph: Dict[str, Dict[str, float]]) -> Dict[str, Tuple[float, float]]:
        """
        Calculate in-degree and out-degree for each node.
        
        Args:
            graph: Input graph as adjacency dictionary
            
        Returns:
            Dictionary mapping node to tuple of (in_degree, out_degree)
        """
        nodes = self.get_nodes(graph)
        degrees: Dict[str, Tuple[float, float]] = {}
        
        for node in nodes:
            # Calculate out-degree
            out_degree = sum(graph.get(node, {}).values())
            
            # Calculate in-degree
            in_degree = 0.0
            for source, edges in graph.items():
                if node in edges:
                    in_degree += edges[node]
                    
            degrees[node] = (in_degree, out_degree)
            
        return degrees
    
    def compute(self, graph1: Dict[str, Dict[str, float]], 
                         graph2: Dict[str, Dict[str, float]]) -> float:
        """
        Calculate the distance between two graphs using a combination of metrics:
        - Entropy difference
        - Degree distribution difference
        - Node set difference
        
        Args:
            graph1: First graph as adjacency dictionary
            graph2: Second graph as adjacency dictionary
            
        Returns:
            Distance value between the two graphs
        """
        # Component 1: Entropy difference
        entropy1 = self.calculate_entropy(graph1)
        entropy2 = self.calculate_entropy(graph2)
        entropy_diff = abs(entropy1 - entropy2)
        
        # Component 2: Node set difference
        nodes1 = self.get_nodes(graph1)
        nodes2 = self.get_nodes(graph2)
        node_diff = len(nodes1.symmetric_difference(nodes2)) / max(len(nodes1), len(nodes2)) if nodes1 or nodes2 else 0
        
        # Component 3: Degree distribution difference
        degrees1 = self.calculate_degree_distribution(graph1)
        degrees2 = self.calculate_degree_distribution(graph2)
        
        degree_diff = 0.0
        all_nodes = nodes1.union(nodes2)
        for node in all_nodes:
            d1 = degrees1.get(node, (0.0, 0.0))
            d2 = degrees2.get(node, (0.0, 0.0))
            degree_diff += abs(d1[0] - d2[0]) + abs(d1[1] - d2[1])
        
        if all_nodes:
            degree_diff /= len(all_nodes)
        
        # Combine metrics with equal weights
        return (entropy_diff + node_diff + degree_diff) / 3.0
