from .mainClass import *
from .tools import TreeNode

class ByteLevelDistance(Distance):

	def __init__(self) -> None:
		super().__init__()
		self.type='file'

		"""
		This class computes the byte-level distance between two files by comparing
		the bytes of both files and summing their absolute differences.
		"""

	def compute(self, file_path1: str, file_path2: str) -> int:
		"""
		Compute the byte-level distance between two files.

		:param file_path1: Path to the first file.
		:param file_path2: Path to the second file.
		:return: The byte-level distance as an integer.
		"""
		with open(file_path1, 'rb') as file1, open(file_path2, 'rb') as file2:
			data1: bytes = file1.read()
			data2: bytes = file2.read()

		# Take the minimum length of both files to avoid out-of-bound errors
		min_length: int = min(len(data1), len(data2))

		# Calculate byte-level distance by summing the absolute differences between byte values
		# a adapter avec ses distances :#############################################################
		#Hamming Distance : Compare deux fichiers au niveau binaire ou des octets en comptant le nombre de bits différents.
		#Levenshtein Distance (Edit Distance) : Mesure le nombre minimum d'opérations nécessaires pour transformer un fichier en un autre (insertion, suppression, ou substitution de caractères/bytes).
		#Jaccard Index : Compare la similarité entre deux ensembles d’octets ou de segments en calculant le rapport des éléments en commun.
		#Manhattan Distance : Somme des différences absolues entre les octets correspondants des deux fichiers.
		#Euclidean Distance : Racine carrée de la somme des carrés des différences des octets entre deux fichiers.
		distance: int = sum(abs(data1[i] - data2[i]) for i in range(min_length))

		# If the files have different lengths, add the extra bytes from the longer file
		distance += abs(len(data1) - len(data2))

		return distance

import hashlib

class HashComparison(Distance):

	"""
	This class computes the cryptographic hash (MD5 or SHA256) of two files and compares them to determine similarity.
	"""

	def __init__(self, algorithm: str = 'md5') -> None:
		"""
		Initializes the class with the selected hashing algorithm (default is 'md5').
		Supported algorithms: 'md5', 'sha256'
		"""
		super().__init__()
		self.type='file'

		self.algorithm: str = algorithm.lower()

	def _compute_hash(self, file_path: str) -> str:
		"""
		Computes the hash of the given file using the specified algorithm.
        
		:param file_path: The path to the file.
		:return: The computed hash in hexadecimal form.
		"""
		hash_func = None
		if self.algorithm == 'md5':
			hash_func = hashlib.md5()
		elif self.algorithm == 'sha256':
			hash_func = hashlib.sha256()
		else:
			raise ValueError(f"Unsupported algorithm: {self.algorithm}")

		with open(file_path, 'rb') as file:
			while chunk := file.read(4096):
				hash_func.update(chunk)

		return hash_func.hexdigest()

	def compute(self, file_path1: str, file_path2: str) -> bool:
		"""
		Compares the hash values of two files.
        
		:param file_path1: The path to the first file.
		:param file_path2: The path to the second file.
		:return: True if the files have the same hash, False otherwise.
		"""
		hash1: str = self._compute_hash(file_path1)
		hash2: str = self._compute_hash(file_path2)

		return hash1 == hash2



import zlib
from typing import Union

class NormalizedCompression(Distance):

	def __init__(self) -> None:
		super().__init__()
		self.type='file'

		"""
		A class to compute the Normalized Compression Distance (NCD) between two files.
		The NCD is based on the change in compression size when two files are concatenated.
		"""

	def _compress(self, data: Union[bytes, str]) -> int:
		"""
		Compresses the input data using zlib and returns the size of the compressed data.

		:param data: The input data (as bytes or string) to be compressed.
		:return: The size of the compressed data in bytes.
		"""
		if isinstance(data, str):
			data = data.encode('utf-8')
		compressed_data: bytes = zlib.compress(data)
		return len(compressed_data)

	def compute(self, file1_data: Union[bytes, str], file2_data: Union[bytes, str]) -> float:
		"""
		Computes the Normalized Compression Distance (NCD) between two files.

		:param file1_data: The content of the first file as bytes or string.
		:param file2_data: The content of the second file as bytes or string.
		:return: The NCD between the two files as a float value.
		"""
		# Compress file1 and file2 individually
		Cx: int = self._compress(file1_data)
		Cy: int = self._compress(file2_data)

		# Compress the concatenation of file1 and file2
		Cxy: int = self._compress(file1_data + file2_data)

		# Compute the Normalized Compression Distance
		NCD: float = (Cxy - min(Cx, Cy)) / max(Cx, Cy)

		return NCD


import zlib
from typing import Union

class KolmogorovComplexity(Distance):

	def __init__(self) -> None:
		super().__init__()
		self.type='file'

		"""
		A class to approximate the Kolmogorov Complexity between two files.
		It measures the amount of shared information between the files based on their compressibility.
		"""

	def _compress(self, data: Union[bytes, str]) -> int:
		"""
		Compresses the input data using zlib and returns the size of the compressed data.

		:param data: The input data (as bytes or string) to be compressed.
		:return: The size of the compressed data in bytes.
		"""
		if isinstance(data, str):
			data = data.encode('utf-8')
		compressed_data: bytes = zlib.compress(data)
		return len(compressed_data)

	def compute(self, file1_data: Union[bytes, str], file2_data: Union[bytes, str]) -> float:
		"""
		Computes the Kolmogorov complexity between two files based on their compressibility.

		:param file1_data: The content of the first file as bytes or string.
		:param file2_data: The content of the second file as bytes or string.
		:return: The Kolmogorov complexity as a float value.
		"""
		# Compress file1 and file2 individually
		Cx: int = self._compress(file1_data)
		Cy: int = self._compress(file2_data)

		# Compress the concatenation of file1 and file2
		Cxy: int = self._compress(file1_data + file2_data)

		# Approximate the Kolmogorov complexity (shared information)
		kolmogorov_complexity: float = (Cxy - min(Cx, Cy)) / max(Cx, Cy)

		return kolmogorov_complexity


import subprocess
from typing import List, Dict

class DynamicBinaryInstrumentation(Distance):

	def __init__(self) -> None:
		super().__init__()
		self.type='file'

		"""
		A class to simulate Dynamic Binary Instrumentation (DBI) for measuring the difference in execution behavior
		between two executable files.
		"""

	def _run_and_trace(self, executable_path: str) -> List[str]:
		"""
		Executes the binary and collects a simplified trace of its execution.
        
		:param executable_path: Path to the executable binary file.
		:return: A list of strings representing the trace (a simplified simulation).
		"""
		try:
			# Run the executable and capture the output (simulating the behavior tracing)
			process = subprocess.Popen([executable_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			stdout, stderr = process.communicate()
            
			# Convert stdout and stderr to strings and split them into lines for "trace" simulation
			output_trace: List[str] = stdout.decode('utf-8').splitlines() + stderr.decode('utf-8').splitlines()
			return output_trace
		except Exception as e:
			print(f"Error executing {executable_path}: {e}")
		return []

	def compute(self, executable1: str, executable2: str) -> Dict[str, int]:
		"""
		Compares the execution behavior of two executable files by analyzing their traces.

		:param executable1: Path to the first executable file.
		:param executable2: Path to the second executable file.
		:return: A dictionary with the number of unique and common trace lines.
		"""
		# Run both executables and collect their traces
		trace1: List[str] = self._run_and_trace(executable1)
		trace2: List[str] = self._run_and_trace(executable2)

		# Compare traces: unique to each and common
		unique_to_trace1: int = len(set(trace1) - set(trace2))
		unique_to_trace2: int = len(set(trace2) - set(trace1))
		common_traces: int = len(set(trace1) & set(trace2))

		# Return the comparison result
		return {
			"unique_to_executable1": unique_to_trace1,
			"unique_to_executable2": unique_to_trace2,
			"common_trace_lines": common_traces
			}
	def example(self):
		# Paths to the two executable files (this is just an example, adapt paths for real executables)
		executable1: str = "../sample/script1"
		executable2: str = "../sample/script2"

		# Compare the execution behavior of the two executables
		behavior_comparison: Dict[str, int] = self.compute(executable1, executable2)

		# Print the comparison results
		print(f"Behavior Comparison Results: {behavior_comparison}")

'''
import subprocess
from typing import List, Tuple

class SystemCallTraceDistance:
    def __init__(self, trace1: List[str], trace2: List[str]) -> None:
        """
        Initialize the SystemCallTraceDistance class with two system call traces.

        :param trace1: A list of system calls for the first executable.
        :param trace2: A list of system calls for the second executable.
        """
        self.trace1 = trace1
        self.trace2 = trace2

    def get_trace(self, executable_path: str) -> List[str]:
        """
        Run the executable and capture its system call trace using strace.

        :param executable_path: Path to the executable file.
        :return: A list of system calls made by the executable.
        """
        try:
            # Run the executable with strace to capture the system call trace
            result = subprocess.run(
                ['strace', '-c', executable_path],
                stderr=subprocess.PIPE, 
                text=True
            )
            # Extract system call trace from stderr
            trace_output = result.stderr.splitlines()
            return trace_output
        except Exception as e:
            print(f"Error capturing system call trace: {e}")
            return []

    def compute_distance(self) -> float:
        """
        Compute the distance between the two system call traces.
        
        The distance is calculated based on the difference in system calls.
        
        :return: A floating-point value representing the distance between the two traces.
        """
        set_trace1 = set(self.trace1)
        set_trace2 = set(self.trace2)

        # Calculate the Jaccard distance between the two system call sets
        intersection = len(set_trace1.intersection(set_trace2))
        union = len(set_trace1.union(set_trace2))

        if union == 0:
            return 1.0  # No system calls in either trace, return max distance
        return 1.0 - (intersection / union)

    @staticmethod
    def compare_executables(executable1: str, executable2: str) -> Tuple[float, List[str], List[str]]:
        """
        Compare the system call traces of two executables and compute the distance.

        :param executable1: Path to the first executable.
        :param executable2: Path to the second executable.
        :return: A tuple containing the distance and the traces of both executables.
        """
        distance_calculator = SystemCallTraceDistance([], [])
        
        # Capture system call traces for both executables
        trace1 = distance_calculator.get_trace(executable1)
        trace2 = distance_calculator.get_trace(executable2)
        
        # Initialize the calculator with the captured traces
        distance_calculator.trace1 = trace1
        distance_calculator.trace2 = trace2
        
        # Compute the system call trace distance
        distance = distance_calculator.compute_distance()
        
        return distance, trace1, trace2


if __name__ == "__main__":
    # Example usage comparing two executables
    executable_path_1: str = "./script1"
    executable_path_2: str = "./script2"
    
    distance, trace1, trace2 = SystemCallTraceDistance.compare_executables(executable_path_1, executable_path_2)
    
    print(f"System call trace distance: {distance}")
    print(f"Trace 1: {trace1}")
    print(f"Trace 2: {trace2}")
'''
import os
from typing import Tuple

class FileMetadataComparison(Distance):

	def __init__(self) -> None:
		"""
		Initialize the FileMetadataComparison class with the metadata of two files.

		:param file1_metadata: Metadata of the first file (size, creation time, modification time, permissions).
		:param file2_metadata: Metadata of the second file (size, creation time, modification time, permissions).
		"""
		super().__init__()
		self.type='file'

	def get_metadata(self, file_path: str) -> Tuple[int, float, float, int]:
		"""
		Get the metadata of a file.

		:param file_path: Path to the file.
		:return: A tuple containing the file size, creation time, modification time, and permissions.
		"""
		try:
			# Get file size in bytes
			file_size: int = os.path.getsize(file_path)
            
			# Get file creation time (Unix timestamp)
			file_creation_time: float = os.path.getctime(file_path)
            
			# Get file modification time (Unix timestamp)
			file_modification_time: float = os.path.getmtime(file_path)
            
			# Get file permissions (mode)
			file_permissions: int = os.stat(file_path).st_mode

			return file_size, file_creation_time, file_modification_time, file_permissions
		except Exception as e:
			print(f"Error retrieving metadata for {file_path}: {e}")
		return (0, 0.0, 0.0, 0)
		
	@staticmethod
	def compute_metadata_similarity(file1_metadata,file2_metadata) -> float:
		"""
		Compute the similarity between the metadata of two files.

		:return: A floating-point value representing the similarity between the metadata of the two files.
		"""
		size_similarity: float = 1.0 if file1_metadata[0] == file2_metadata[0] else 0.0
		creation_time_similarity: float = 1.0 if file1_metadata[1] == file2_metadata[1] else 0.0
		modification_time_similarity: float = 1.0 if file1_metadata[2] == file2_metadata[2] else 0.0
		permissions_similarity: float = 1.0 if file1_metadata[3] == file2_metadata[3] else 0.0
        
		# Average similarity score
		return (size_similarity + creation_time_similarity + modification_time_similarity + permissions_similarity) / 4

	def compute(self,file1_path: str, file2_path: str) -> Tuple[float, Tuple[int, float, float, int], Tuple[int, float, float, int]]:
		"""
		Compare the metadata of two files.

		:param file1_path: Path to the first file.
		:param file2_path: Path to the second file.
		:return: A tuple containing the similarity score and the metadata of both files.
		"""
        
		# Get metadata for both files
		file1_metadata = self.get_metadata(file1_path)
		file2_metadata = self.get_metadata(file2_path)
                
		# Compute the similarity between the two files' metadata
		similarity = self.compute_metadata_similarity(file1_metadata,file2_metadata)
        
		return 1 - similarity#, file1_metadata, file2_metadata

from typing import Optional, Tuple

class FileTypeDistance(Distance):

	def __init__(self) -> None:
		"""
		Initialize the FileTypeDistance class with the types of two files.

		:param file1_type: File type or signature of the first file.
		:param file2_type: File type or signature of the second file.
		"""
		super().__init__()
		self.type='file'
		
	@staticmethod
	def get_file_signature(file_path: str) -> Optional[str]:
		"""
		Get the file type or signature based on the file's magic bytes.

		:param file_path: Path to the file.
		:return: The file type or signature as a string, or None if it cannot be determined.
		"""
		try:
			with open(file_path, 'rb') as f:
				# Read the first few bytes of the file (magic number)
				file_header: bytes = f.read(8)

			# Dictionary of common file signatures (magic numbers)
			magic_dict = {
				b'\xFF\xD8\xFF': "JPEG",
				b'\x89PNG': "PNG",
				b'\x25\x50\x44\x46': "PDF",
				b'\x50\x4B\x03\x04': "ZIP",
				b'\x1F\x8B': "GZIP",
				b'\x49\x49\x2A\x00': "TIFF",
				b'\x4D\x5A': "EXE",
			}

			# Check for known signatures
			for magic, file_type in magic_dict.items():
				if file_header.startswith(magic):
					return file_type

			return None
		except Exception as e:
			print(f"Error reading file {file_path}: {e}")
		return None

	def compute(self,file_path1,file_path2) -> float:
		"""
		Compute the distance between the file types of two files.

		:return: A floating-point value representing the distance between the file types (1.0 for same, 0.0 for different).
		"""
		return 0.0 if self.get_file_signature(file_path1) == self.get_file_signature(file_path2) else 1.0

	@staticmethod
	def compare_files(file1_path: str, file2_path: str) -> Tuple[float, Optional[str], Optional[str]]:
		"""
		Compare the types of two files.

		:param file1_path: Path to the first file.
		:param file2_path: Path to the second file.
		:return: A tuple containing the similarity score and the file types of both files.
		"""
		comparator = FileTypeDistance(None, None)
        
		# Get file types based on their signatures
		file1_type = comparator.get_file_signature(file1_path)
		file2_type = comparator.get_file_signature(file2_path)
        
		# Initialize the comparator with the retrieved file types
		comparator.file1_type = file1_type
		comparator.file2_type = file2_type
        
		# Compute the similarity between the two files' types
		similarity = comparator.compute_file_type_similarity()
        
		return similarity, file1_type, file2_type

from typing import Any, Dict, List, Tuple

class TreeEditDistance(Distance):

	def __init__(self) -> None:
		super().__init__()
		self.type='file'

	def _edit_distance(self, tree1: TreeNode, tree2: TreeNode) -> int:
		"""
		Recursively computes the tree edit distance between two nodes.

		:param tree1: The root node of the first tree.
		:param tree2: The root node of the second tree.
		:return: The edit distance between the two trees.
		"""
		if tree1 is None and tree2 is None:
			return 0
		if tree1 is None:
			return 1 + sum(self._edit_distance(None, child) for child in tree2.children)
		if tree2 is None:
			return 1 + sum(self._edit_distance(child, None) for child in tree1.children)
        
		cost: int = 0 if tree1.value == tree2.value else 1

		dist_matrix: List[List[int]] = [[0] * (len(tree2.children) + 1) for _ in range(len(tree1.children) + 1)]
        
		# Initialize the distance matrix
		for i in range(1, len(tree1.children) + 1):
			dist_matrix[i][0] = dist_matrix[i - 1][0] + self._edit_distance(tree1.children[i - 1], None)
		for j in range(1, len(tree2.children) + 1):
			dist_matrix[0][j] = dist_matrix[0][j - 1] + self._edit_distance(None, tree2.children[j - 1])

		# Fill the distance matrix
		for i in range(1, len(tree1.children) + 1):
			for j in range(1, len(tree2.children) + 1):
				dist_matrix[i][j] = min(
					dist_matrix[i - 1][j] + self._edit_distance(tree1.children[i - 1], None),  # Deletion
					dist_matrix[i][j - 1] + self._edit_distance(None, tree2.children[j - 1]),  # Insertion
					dist_matrix[i - 1][j - 1] + self._edit_distance(tree1.children[i - 1], tree2.children[j - 1])  # Substitution
				)
        
		return cost + dist_matrix[len(tree1.children)][len(tree2.children)]

	def compute(self, tree1: TreeNode, tree2: TreeNode) -> int:
		"""
		Computes the tree edit distance between two trees.

		:param tree1: The root of the first tree.
		:param tree2: The root of the second tree.
		:return: The tree edit distance between the two trees.
		"""
		return self._edit_distance(tree1, tree2)

	@staticmethod
	def parse_tree_from_dict(data: Dict) -> TreeNode:
		"""
		Parses a tree structure from a dictionary (e.g., from JSON or XML).

		:param data: The dictionary representing the tree structure.
		:return: The root TreeNode of the parsed tree.
		"""
		if isinstance(data, dict):
			root_value = list(data.keys())[0]
			children_data = data[root_value]
			children = [TreeEditDistance.parse_tree_from_dict(child) for child in children_data] if isinstance(children_data, list) else []
			return TreeNode(root_value, children)
		else:
			return TreeNode(data)
	def example(self):
		# Example usage with JSON-like data structures
		tree_data_1: Dict = {"root": [{"child1": []},{"child2": [{"grandchild1": []}]}]}
		tree_data_2: Dict = {"root": [{"child1": []},{"child3": [{"grandchild1": []}]}]}

		tree1: TreeNode = TreeEditDistance.parse_tree_from_dict(tree_data_1)
		tree2: TreeNode = TreeEditDistance.parse_tree_from_dict(tree_data_2)

		ted = TreeEditDistance()
		distance: int = ted.compute(tree1, tree2)

		print(f"Tree Edit Distance: {distance}")

import zlib
from typing import Union

class ZlibBasedDistance(Distance):

	def __init__(self) -> None:
		super().__init__()
		self.type='file'

		"""
		Initializes the ZlibBasedDistance class to compare the structural differences
		between two files using zlib compression.
		"""

	def compress_data(self, data: bytes) -> int:
		"""
		Compresses the given data using zlib and returns the compressed size.

		:param data: The data to be compressed, in bytes.
		:return: The size of the compressed data.
		"""
		compressed_data: bytes = zlib.compress(data)
		return len(compressed_data)

	def compute(self, file1: Union[str, bytes], file2: Union[str, bytes]) -> float:
		"""
		Computes the Zlib-based distance between two files by comparing the compression
		size of the concatenated files with the individual compressed sizes.

		:param file1: Path to the first file or the raw byte data of the first file.
		:param file2: Path to the second file or the raw byte data of the second file.
		:return: The Zlib-based distance as a float value.
		"""
		if isinstance(file1, str):
			with open(file1, 'rb') as f1:
				data1: bytes = f1.read()
		else:
			data1: bytes = file1

		if isinstance(file2, str):
			with open(file2, 'rb') as f2:
				data2: bytes = f2.read()
		else:
			data2: bytes = file2

		compressed_size_1: int = self.compress_data(data1)
		compressed_size_2: int = self.compress_data(data2)

		combined_data: bytes = data1 + data2
		compressed_combined_size: int = self.compress_data(combined_data)

		distance: float = (compressed_combined_size - min(compressed_size_1, compressed_size_2)) / max(compressed_size_1, compressed_size_2)

		return distance

####################################################
from typing import Dict, List, Set, Tuple, Optional, Union, Any
import os
import re
import hashlib
from dataclasses import dataclass
from collections import defaultdict, deque

@dataclass
class Node:
    """
    Represents a node in the control flow graph.
    
    Attributes:
        id (str): Unique identifier for the node
        type (str): Type of node (e.g., 'function', 'block', 'condition')
        content_hash (str): Hash of the node's content
        attributes (Dict): Additional node attributes
    """
    id: str
    type: str
    content_hash: str
    attributes: Dict[str, Any]

@dataclass
class Edge:
    """
    Represents an edge in the control flow graph.
    
    Attributes:
        source (str): ID of the source node
        target (str): ID of the target node
        type (str): Type of edge (e.g., 'call', 'jump', 'fallthrough')
        attributes (Dict): Additional edge attributes
    """
    source: str
    target: str
    type: str
    attributes: Dict[str, Any]

@dataclass
class ControlFlowGraph:
    """
    Represents a control flow graph.
    
    Attributes:
        nodes (Dict[str, Node]): Map of node IDs to Node objects
        edges (List[Edge]): List of edges in the graph
        entry_points (Set[str]): Set of entry point node IDs
        exit_points (Set[str]): Set of exit point node IDs
    """
    nodes: Dict[str, Node]
    edges: List[Edge]
    entry_points: Set[str]
    exit_points: Set[str]
    
    def get_successors(self, node_id: str) -> List[str]:
        """
        Get IDs of successor nodes for a given node.
        
        Args:
            node_id (str): ID of the node
            
        Returns:
            List[str]: List of successor node IDs
        """
        return [edge.target for edge in self.edges if edge.source == node_id]
    
    def get_predecessors(self, node_id: str) -> List[str]:
        """
        Get IDs of predecessor nodes for a given node.
        
        Args:
            node_id (str): ID of the node
            
        Returns:
            List[str]: List of predecessor node IDs
        """
        return [edge.source for edge in self.edges if edge.target == node_id]

@dataclass
class GraphSimilarityResult:
    """
    Contains the results of control flow graph similarity calculation.
    
    Attributes:
        distance (float): Normalized distance between graphs (0-1, lower means more similar)
        node_similarity (float): Similarity score based on node matching
        structure_similarity (float): Similarity score based on graph structure
        entry_exit_similarity (float): Similarity score based on entry/exit points
        matched_nodes (Dict[str, str]): Mapping between matched nodes in both graphs
        details (Dict): Additional comparison details
    """
    distance: float
    node_similarity: float
    structure_similarity: float
    entry_exit_similarity: float
    matched_nodes: Dict[str, str]
    details: Dict[str, Any]

class CFGFileAnalyzer:
    """
    Base class for analyzing files and generating control flow graphs.
    Subclasses should implement file-specific analysis logic.
    """
    
    def __init__(self):
        """Initialize the file analyzer."""
        pass
    
    def analyze_file(self, file_path: str) -> ControlFlowGraph:
        """
        Analyze a file and generate its control flow graph.
        
        Args:
            file_path (str): Path to the file
            
        Returns:
            ControlFlowGraph: The generated control flow graph
            
        Raises:
            NotImplementedError: This method should be implemented by subclasses
        """
        raise NotImplementedError("Subclasses must implement analyze_file method")

class TextFileCFGAnalyzer(CFGFileAnalyzer):
    """
    Analyzer for text-based files such as source code.
    Generates a basic control flow graph based on text structure.
    """
    
    def __init__(
        self,
        block_size: int = 5,
        ignore_whitespace: bool = True,
        ignore_case: bool = False
    ):
        """
        Initialize the text file analyzer.
        
        Args:
            block_size (int): Number of lines to group into a block (default: 5)
            ignore_whitespace (bool): Whether to ignore whitespace in comparison (default: True)
            ignore_case (bool): Whether to ignore case in comparison (default: False)
        """
        super().__init__()
        self.type='file'

        self.block_size = block_size
        self.ignore_whitespace = ignore_whitespace
        self.ignore_case = ignore_case
    
    def _normalize_line(self, line: str) -> str:
        """
        Normalize a line of text based on configuration.
        
        Args:
            line (str): Line of text
            
        Returns:
            str: Normalized line
        """
        if self.ignore_whitespace:
            line = re.sub(r'\s+', ' ', line.strip())
        if self.ignore_case:
            line = line.lower()
        return line
    
    def _hash_content(self, content: str) -> str:
        """
        Generate a hash for the given content.
        
        Args:
            content (str): Content to hash
            
        Returns:
            str: Hash string
        """
        return hashlib.md5(content.encode('utf-8')).hexdigest()
    
    def analyze_file(self, file_path: str) -> ControlFlowGraph:
        """
        Analyze a text file and generate its control flow graph.
        
        Args:
            file_path (str): Path to the file
            
        Returns:
            ControlFlowGraph: The generated control flow graph
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        nodes = {}
        edges = []
        
        # Read and normalize file content
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            lines = [self._normalize_line(line) for line in f]
        
        # Generate blocks of lines
        blocks = []
        for i in range(0, len(lines), self.block_size):
            block_lines = lines[i:i+self.block_size]
            if block_lines:
                blocks.append('\n'.join(block_lines))
        
        # Create nodes for each block
        for i, block in enumerate(blocks):
            node_id = f"block_{i}"
            content_hash = self._hash_content(block)
            
            nodes[node_id] = Node(
                id=node_id,
                type='block',
                content_hash=content_hash,
                attributes={'line_start': i * self.block_size, 'content': block[:100] + '...'}
            )
        
        # Create edges between consecutive blocks
        for i in range(len(blocks) - 1):
            source_id = f"block_{i}"
            target_id = f"block_{i+1}"
            
            edges.append(Edge(
                source=source_id,
                target=target_id,
                type='sequential',
                attributes={}
            ))
        
        # Set entry and exit points
        entry_points = {'block_0'} if blocks else set()
        exit_points = {f"block_{len(blocks)-1}"} if blocks else set()
        
        return ControlFlowGraph(
            nodes=nodes,
            edges=edges,
            entry_points=entry_points,
            exit_points=exit_points
        )

class BinaryFileCFGAnalyzer(CFGFileAnalyzer):
    """
    Analyzer for binary files.
    Generates a basic control flow graph based on binary structure and patterns.
    """
    
    def __init__(
        self,
        chunk_size: int = 256,
        pattern_detection: bool = True
    ):
        """
        Initialize the binary file analyzer.
        
        Args:
            chunk_size (int): Size of binary chunks to analyze (default: 256)
            pattern_detection (bool): Whether to detect patterns in binary (default: True)
        """
        super().__init__()
        self.type='file'

        self.chunk_size = chunk_size
        self.pattern_detection = pattern_detection
    
    def _detect_patterns(self, data: bytes) -> List[Tuple[int, str]]:
        """
        Detect common patterns in binary data.
        
        Args:
            data (bytes): Binary data
            
        Returns:
            List[Tuple[int, str]]: List of (offset, pattern_type) tuples
        """
        patterns = []
        
        # Detect potential function headers (very simple heuristic)
        for i in range(len(data) - 4):
            # Simple pattern detection - just an example
            if data[i:i+3] == b'\x55\x89\xe5':  # Common x86 function prologue
                patterns.append((i, 'function_start'))
            elif data[i:i+2] == b'\xc3\x90':  # Common x86 return with nop
                patterns.append((i, 'function_end'))
        
        return patterns
    
    def analyze_file(self, file_path: str) -> ControlFlowGraph:
        """
        Analyze a binary file and generate its control flow graph.
        
        Args:
            file_path (str): Path to the file
            
        Returns:
            ControlFlowGraph: The generated control flow graph
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        nodes = {}
        edges = []
        
        # Read file in binary mode
        with open(file_path, 'rb') as f:
            data = f.read()
        
        # Detect patterns if enabled
        patterns = self._detect_patterns(data) if self.pattern_detection else []
        pattern_offsets = {offset for offset, _ in patterns}
        
        # Create nodes for each chunk and detected pattern
        chunk_nodes = {}
        for i in range(0, len(data), self.chunk_size):
            chunk = data[i:i+self.chunk_size]
            node_id = f"chunk_{i}"
            content_hash = hashlib.md5(chunk).hexdigest()
            
            nodes[node_id] = Node(
                id=node_id,
                type='binary_chunk',
                content_hash=content_hash,
                attributes={'offset': i, 'size': len(chunk)}
            )
            chunk_nodes[i] = node_id
        
        # Create nodes for patterns
        pattern_nodes = {}
        for offset, pattern_type in patterns:
            node_id = f"pattern_{offset}"
            # Get a window of data around the pattern
            window_start = max(0, offset - 8)
            window_end = min(len(data), offset + 16)
            pattern_data = data[window_start:window_end]
            
            nodes[node_id] = Node(
                id=node_id,
                type=pattern_type,
                content_hash=hashlib.md5(pattern_data).hexdigest(),
                attributes={'offset': offset}
            )
            pattern_nodes[offset] = node_id
        
        # Create edges between consecutive chunks
        chunk_offsets = sorted(chunk_nodes.keys())
        for i in range(len(chunk_offsets) - 1):
            source_offset = chunk_offsets[i]
            target_offset = chunk_offsets[i+1]
            
            edges.append(Edge(
                source=chunk_nodes[source_offset],
                target=chunk_nodes[target_offset],
                type='sequential',
                attributes={}
            ))
        
        # Create edges from chunks to patterns and between related patterns
        for offset in pattern_nodes:
            # Find which chunk this pattern belongs to
            chunk_offset = (offset // self.chunk_size) * self.chunk_size
            if chunk_offset in chunk_nodes:
                edges.append(Edge(
                    source=chunk_nodes[chunk_offset],
                    target=pattern_nodes[offset],
                    type='contains',
                    attributes={}
                ))
            
            # Connect function_start to function_end
            if nodes[pattern_nodes[offset]].type == 'function_start':
                # Find the next function_end
                for end_offset, end_type in patterns:
                    if end_offset > offset and end_type == 'function_end':
                        edges.append(Edge(
                            source=pattern_nodes[offset],
                            target=pattern_nodes[end_offset],
                            type='function_body',
                            attributes={'length': end_offset - offset}
                        ))
                        break
        
        # Set entry and exit points
        entry_points = {chunk_nodes[0]} if chunk_nodes else set()
        exit_points = {chunk_nodes[chunk_offsets[-1]]} if chunk_nodes else set()
        
        # Add pattern-based entry/exit points
        for offset, pattern_type in patterns:
            if pattern_type == 'function_start':
                entry_points.add(pattern_nodes[offset])
            elif pattern_type == 'function_end':
                exit_points.add(pattern_nodes[offset])
        
        return ControlFlowGraph(
            nodes=nodes,
            edges=edges,
            entry_points=entry_points,
            exit_points=exit_points
        )

class ControlFlowGraphDistance:
    """
    A class that computes the distance between two files based on their control flow graphs.
    This implementation analyzes file structure and creates a graph representation for comparison.
    """
    
    def __init__(
        self,
        node_weight: float = 0.4,
        structure_weight: float = 0.4,
        entry_exit_weight: float = 0.2,
        analyzer_type: str = 'auto'
    ):
        """
        Initialize the control flow graph distance calculator.
        
        Args:
            node_weight (float): Weight for node similarity (default: 0.4)
            structure_weight (float): Weight for structure similarity (default: 0.4)
            entry_exit_weight (float): Weight for entry/exit point similarity (default: 0.2)
            analyzer_type (str): Type of analyzer to use ('text', 'binary', or 'auto')
        """
        super().__init__()
        self.type='file'
        
        self.weights = {
            'node': node_weight,
            'structure': structure_weight,
            'entry_exit': entry_exit_weight
        }
        self.analyzer_type = analyzer_type
    
    def _get_analyzer(self, file_path: str) -> CFGFileAnalyzer:
        """
        Get appropriate analyzer based on file type.
        
        Args:
            file_path (str): Path to the file
            
        Returns:
            CFGFileAnalyzer: Appropriate analyzer instance
        """
        if self.analyzer_type == 'text':
            return TextFileCFGAnalyzer()
        elif self.analyzer_type == 'binary':
            return BinaryFileCFGAnalyzer()
        
        # Auto-detect file type
        try:
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                # Try to read first 1024 bytes as text
                text = f.read(1024)
                # If more than 10% of characters are non-printable, treat as binary
                non_printable = sum(1 for c in text if not (32 <= ord(c) <= 126) and c not in '\r\n\t')
                if non_printable / len(text) > 0.1:
                    return BinaryFileCFGAnalyzer()
                else:
                    return TextFileCFGAnalyzer()
        except UnicodeDecodeError:
            # File couldn't be decoded as text, so treat as binary
            return BinaryFileCFGAnalyzer()
    
    def _compute_node_similarity(
        self,
        graph1: ControlFlowGraph,
        graph2: ControlFlowGraph
    ) -> Tuple[float, Dict[str, str]]:
        """
        Compute similarity based on node content.
        
        Args:
            graph1 (ControlFlowGraph): First graph
            graph2 (ControlFlowGraph): Second graph
            
        Returns:
            Tuple containing:
                - Node similarity score (0-1)
                - Dictionary mapping node IDs from graph1 to matching nodes in graph2
        """
        # Group nodes by content hash
        hash_to_nodes1 = defaultdict(list)
        hash_to_nodes2 = defaultdict(list)
        
        for node_id, node in graph1.nodes.items():
            hash_to_nodes1[node.content_hash].append(node_id)
        
        for node_id, node in graph2.nodes.items():
            hash_to_nodes2[node.content_hash].append(node_id)
        
        # Match nodes with same content hash
        matched_nodes = {}
        matched_count = 0
        
        for content_hash, nodes1 in hash_to_nodes1.items():
            nodes2 = hash_to_nodes2.get(content_hash, [])
            
            # Greedy matching
            for node1 in nodes1:
                if nodes2:
                    matched_nodes[node1] = nodes2.pop(0)
                    matched_count += 1
        
        # Calculate similarity score
        total_nodes = max(len(graph1.nodes), len(graph2.nodes))
        similarity = matched_count / total_nodes if total_nodes > 0 else 1.0
        
        return similarity, matched_nodes
    
    def _compute_structure_similarity(
        self,
        graph1: ControlFlowGraph,
        graph2: ControlFlowGraph,
        node_mapping: Dict[str, str]
    ) -> float:
        """
        Compute similarity based on graph structure.
        
        Args:
            graph1 (ControlFlowGraph): First graph
            graph2 (ControlFlowGraph): Second graph
            node_mapping (Dict[str, str]): Mapping from nodes in graph1 to nodes in graph2
            
        Returns:
            float: Structure similarity score (0-1)
        """
        # Compute matched edges
        matched_edges = 0
        total_edges = max(len(graph1.edges), len(graph2.edges))
        
        if total_edges == 0:
            return 1.0
        
        # Create edge sets for efficient lookup
        edges1 = {(e.source, e.target, e.type) for e in graph1.edges}
        edges2 = {(e.source, e.target, e.type) for e in graph2.edges}
        
        # Check how many edges in graph1 have a corresponding edge in graph2
        for source1, target1, type1 in edges1:
            if source1 in node_mapping and target1 in node_mapping:
                source2 = node_mapping[source1]
                target2 = node_mapping[target1]
                
                if (source2, target2, type1) in edges2:
                    matched_edges += 1
        
        return matched_edges / total_edges
    
    def _compute_entry_exit_similarity(
        self,
        graph1: ControlFlowGraph,
        graph2: ControlFlowGraph,
        node_mapping: Dict[str, str]
    ) -> float:
        """
        Compute similarity based on entry and exit points.
        
        Args:
            graph1 (ControlFlowGraph): First graph
            graph2 (ControlFlowGraph): Second graph
            node_mapping (Dict[str, str]): Mapping from nodes in graph1 to nodes in graph2
            
        Returns:
            float: Entry/exit similarity score (0-1)
        """
        # Map entry points from graph1 to graph2
        mapped_entries = {node_mapping.get(entry) for entry in graph1.entry_points if entry in node_mapping}
        mapped_exits = {node_mapping.get(exit_pt) for exit_pt in graph1.exit_points if exit_pt in node_mapping}
        
        # Calculate similarity scores
        entry_similarity = len(mapped_entries & graph2.entry_points) / max(len(graph1.entry_points), len(graph2.entry_points)) if graph1.entry_points and graph2.entry_points else 1.0
        exit_similarity = len(mapped_exits & graph2.exit_points) / max(len(graph1.exit_points), len(graph2.exit_points)) if graph1.exit_points and graph2.exit_points else 1.0
        
        return (entry_similarity + exit_similarity) / 2
    
    def compute(
        self,
        file1_path: str,
        file2_path: str
    ) -> GraphSimilarityResult:
        """
        Compute the control flow graph distance between two files.
        
        Args:
            file1_path (str): Path to the first file
            file2_path (str): Path to the second file
            
        Returns:
            GraphSimilarityResult: Object containing distance metrics
            
        Raises:
            FileNotFoundError: If either file doesn't exist
        """
        # Check files exist
        if not os.path.exists(file1_path):
            raise FileNotFoundError(f"File not found: {file1_path}")
        if not os.path.exists(file2_path):
            raise FileNotFoundError(f"File not found: {file2_path}")
        
        # Get appropriate analyzers
        analyzer1 = self._get_analyzer(file1_path)
        analyzer2 = self._get_analyzer(file2_path)
        
        # Generate control flow graphs
        graph1 = analyzer1.analyze_file(file1_path)
        graph2 = analyzer2.analyze_file(file2_path)
        
        # Compute similarity components
        node_similarity, matched_nodes = self._compute_node_similarity(graph1, graph2)
        structure_similarity = self._compute_structure_similarity(graph1, graph2, matched_nodes)
        entry_exit_similarity = self._compute_entry_exit_similarity(graph1, graph2, matched_nodes)
        
        # Compute weighted total similarity
        total_similarity = (
            self.weights['node'] * node_similarity +
            self.weights['structure'] * structure_similarity +
            self.weights['entry_exit'] * entry_exit_similarity
        )
        
        # Normalize total_similarity to distance (0-1)
        distance = 1.0 - total_similarity
        
        # Collect detailed metrics
        details = {
            'num_nodes_file1': len(graph1.nodes),
            'num_nodes_file2': len(graph2.nodes),
            'num_edges_file1': len(graph1.edges),
            'num_edges_file2': len(graph2.edges),
            'num_matched_nodes': len(matched_nodes),
            'node_types_file1': self._count_node_types(graph1),
            'node_types_file2': self._count_node_types(graph2)
        }
        
        return GraphSimilarityResult(
            distance=distance,
            node_similarity=node_similarity,
            structure_similarity=structure_similarity,
            entry_exit_similarity=entry_exit_similarity,
            matched_nodes=matched_nodes,
            details=details
        )
    
    def _count_node_types(self, graph: ControlFlowGraph) -> Dict[str, int]:
        """
        Count nodes by type in a graph.
        
        Args:
            graph (ControlFlowGraph): Graph to analyze
            
        Returns:
            Dict[str, int]: Dictionary mapping node types to counts
        """
        type_counts = defaultdict(int)
        for node in graph.nodes.values():
            type_counts[node.type] += 1
        return dict(type_counts)
#################################################
import ast
import os
from typing import Dict, List, Set, Tuple, Union, Any, Optional
import difflib

class ASTDistanceCalculator:
    """
    A class that calculates the distance between two Python files based on their
    Abstract Syntax Tree (AST) structures.
    
    This implementation compares the syntactic structure of code files by:
    1. Parsing each file into its AST representation
    2. Comparing the ASTs for structural differences
    3. Calculating a similarity score based on these differences
    """
    
    def __init__(self, normalize_names: bool = True, ignore_comments: bool = True) -> None:
        """
        Initialize the AST Distance Calculator.
        
        Args:
            normalize_names: Whether to normalize variable/function names (treats different names as same)
            ignore_comments: Whether to ignore comments when comparing files
        """
        super().__init__()
        self.type='file'
        
        self.normalize_names = normalize_names
        self.ignore_comments = ignore_comments
    
    def parse_file_to_ast(self, file_path: str) -> Optional[ast.AST]:
        """
        Parse a Python file into its AST representation.
        
        Args:
            file_path: Path to the Python file
            
        Returns:
            AST object or None if parsing failed
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            return ast.parse(content)
        except Exception as e:
            print(f"Error parsing file {file_path}: {e}")
            return None
    
    def get_ast_structure(self, tree: ast.AST) -> List[Dict[str, Any]]:
        """
        Convert an AST into a structured representation that captures its
        essential elements while ignoring variable naming differences if normalize_names is True.
        
        Args:
            tree: AST object to convert
            
        Returns:
            List of dictionaries representing the structure
        """
        structures = []
        
        class ASTVisitor(ast.NodeVisitor):
            def generic_visit(self, node: ast.AST) -> None:
                node_info = {
                    'type': type(node).__name__,
                    'fields': {}
                }
                
                # Extract relevant fields from the node
                for field_name, field_value in ast.iter_fields(node):
                    # Skip unimportant details or normalize if needed
                    if field_name == 'ctx' or (self.normalize_names and field_name in ('id', 'name')):
                        continue
                    
                    # Handle different types of field values
                    if isinstance(field_value, list):
                        # For lists (like body of a function), just record the length and types
                        types = [type(item).__name__ for item in field_value if isinstance(item, ast.AST)]
                        node_info['fields'][field_name] = types
                    elif isinstance(field_value, ast.AST):
                        # For nested AST nodes, record their type
                        node_info['fields'][field_name] = type(field_value).__name__
                    elif field_value is not None:
                        # For literals and other values
                        node_info['fields'][field_name] = str(type(field_value).__name__)
                
                structures.append(node_info)
                super().generic_visit(node)
        
        # Create a visitor with our normalization settings
        visitor = ASTVisitor()
        visitor.normalize_names = self.normalize_names
        
        # Visit all nodes in the tree
        visitor.visit(tree)
        return structures
    
    def calculate_similarity(self, struct1: List[Dict[str, Any]], struct2: List[Dict[str, Any]]) -> float:
        """
        Calculate the similarity between two AST structures.
        
        Args:
            struct1: First AST structure
            struct2: Second AST structure
            
        Returns:
            Similarity score between 0.0 (completely different) and 1.0 (identical)
        """
        # Convert structures to strings for comparison
        str1 = str(struct1)
        str2 = str(struct2)
        
        # Use difflib's SequenceMatcher to get similarity ratio
        matcher = difflib.SequenceMatcher(None, str1, str2)
        return matcher.ratio()
    
    def compute(self, file1_path: str, file2_path: str) -> Dict[str, Any]:
        """
        Calculate the AST-based distance between two Python files.
        
        Args:
            file1_path: Path to the first Python file
            file2_path: Path to the second Python file
            
        Returns:
            Dictionary with similarity score and other metrics
        """
        # Parse files to ASTs
        ast1 = self.parse_file_to_ast(file1_path)
        ast2 = self.parse_file_to_ast(file2_path)
        
        if ast1 is None or ast2 is None:
            return {
                "error": "Failed to parse one or both files",
                "similarity": 0.0,
                "distance": 1.0
            }
        
        # Get structural representations
        struct1 = self.get_ast_structure(ast1)
        struct2 = self.get_ast_structure(ast2)
        
        # Calculate similarity
        similarity = self.calculate_similarity(struct1, struct2)
        
        # Get node type counts for additional metrics
        node_types1 = self._count_node_types(struct1)
        node_types2 = self._count_node_types(struct2)
        
        # Find common and different node types
        common_types = set(node_types1.keys()) & set(node_types2.keys())
        diff_types = set(node_types1.keys()) ^ set(node_types2.keys())
        
        return {
            "similarity": similarity,
            "distance": 1.0 - similarity,
            "file1_nodes": len(struct1),
            "file2_nodes": len(struct2),
            "common_node_types": len(common_types),
            "different_node_types": len(diff_types),
            "details": {
                "file1_node_types": node_types1,
                "file2_node_types": node_types2
            }
        }
    
    def _count_node_types(self, structure: List[Dict[str, Any]]) -> Dict[str, int]:
        """
        Count the occurrences of each node type in the AST structure.
        
        Args:
            structure: AST structure as a list of dictionaries
            
        Returns:
            Dictionary mapping node types to their counts
        """
        counts = {}
        for node in structure:
            node_type = node["type"]
            if node_type in counts:
                counts[node_type] += 1
            else:
                counts[node_type] = 1
        return counts


############################################
import os
from typing import Dict, List, Set, Tuple, Union, Optional, Any
import math
from collections import Counter

class CharacterFrequencyDistance:
    """
    A class that calculates the distance between two files based on their
    character frequency distributions.
    
    This implementation evaluates differences in character distributions by:
    1. Counting the frequency of each character in both files
    2. Creating normalized frequency distributions
    3. Calculating distance metrics between these distributions
    """
    
    def __init__(self, 
                 case_sensitive: bool = True, 
                 include_whitespace: bool = True,
                 include_special_chars: bool = True,
                 chunk_size: Optional[int] = None) -> None:
        """
        Initialize the Character Frequency Distance calculator.
        
        Args:
            case_sensitive: Whether to treat uppercase and lowercase letters as distinct
            include_whitespace: Whether to include whitespace characters in the analysis
            include_special_chars: Whether to include special characters in the analysis
            chunk_size: If provided, reads files in chunks of this size to handle large files efficiently
        """
        super().__init__()
        self.type='file'
        
        self.case_sensitive = case_sensitive
        self.include_whitespace = include_whitespace
        self.include_special_chars = include_special_chars
        self.chunk_size = chunk_size
    
    def get_char_frequencies(self, file_path: str) -> Dict[str, float]:
        """
        Calculate the normalized frequency distribution of characters in a file.
        
        Args:
            file_path: Path to the file to analyze
            
        Returns:
            Dictionary mapping characters to their normalized frequencies
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        char_counts: Dict[str, int] = {}
        total_chars = 0
        
        try:
            # Process file in chunks if chunk_size is specified
            if self.chunk_size:
                with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
                    while True:
                        chunk = file.read(self.chunk_size)
                        if not chunk:
                            break
                        self._process_text(chunk, char_counts)
                        total_chars += len(chunk)
            else:
                # Process entire file at once
                with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
                    text = file.read()
                    self._process_text(text, char_counts)
                    total_chars = len(text)
                    
            # Normalize frequencies
            char_frequencies = {char: count / total_chars for char, count in char_counts.items()}
            return char_frequencies
            
        except UnicodeDecodeError:
            # If text decoding fails, try binary mode
            return self._process_binary_file(file_path)
    
    def _process_text(self, text: str, char_counts: Dict[str, int]) -> None:
        """
        Process a text string and update character counts.
        
        Args:
            text: Text to process
            char_counts: Dictionary to update with character counts
        """
        # Convert to lowercase if not case sensitive
        if not self.case_sensitive:
            text = text.lower()
            
        for char in text:
            # Skip whitespace if configured to do so
            if not self.include_whitespace and char.isspace():
                continue
                
            # Skip special characters if configured to do so
            if not self.include_special_chars and not char.isalnum() and not char.isspace():
                continue
                
            if char in char_counts:
                char_counts[char] += 1
            else:
                char_counts[char] = 1
    
    def _process_binary_file(self, file_path: str) -> Dict[str, float]:
        """
        Process a file in binary mode for non-text files.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Dictionary mapping byte values (as hex strings) to their normalized frequencies
        """
        byte_counts: Dict[str, int] = {}
        total_bytes = 0
        
        # Process file in chunks if chunk_size is specified
        if self.chunk_size:
            with open(file_path, 'rb') as file:
                while True:
                    chunk = file.read(self.chunk_size)
                    if not chunk:
                        break
                    for byte in chunk:
                        byte_hex = hex(byte)
                        byte_counts[byte_hex] = byte_counts.get(byte_hex, 0) + 1
                    total_bytes += len(chunk)
        else:
            # Process entire file at once
            with open(file_path, 'rb') as file:
                content = file.read()
                for byte in content:
                    byte_hex = hex(byte)
                    byte_counts[byte_hex] = byte_counts.get(byte_hex, 0) + 1
                total_bytes = len(content)
                
        # Normalize frequencies
        return {byte: count / total_bytes for byte, count in byte_counts.items()}
    
    def calculate_euclidean_distance(self, freq1: Dict[str, float], freq2: Dict[str, float]) -> float:
        """
        Calculate the Euclidean distance between two frequency distributions.
        
        Args:
            freq1: First frequency distribution
            freq2: Second frequency distribution
            
        Returns:
            Euclidean distance between the distributions
        """
        # Get all unique characters from both distributions
        all_chars = set(freq1.keys()) | set(freq2.keys())
        
        # Calculate squared differences
        squared_diff_sum = 0.0
        for char in all_chars:
            f1 = freq1.get(char, 0.0)
            f2 = freq2.get(char, 0.0)
            squared_diff_sum += (f1 - f2) ** 2
            
        return math.sqrt(squared_diff_sum)
    
    def calculate_manhattan_distance(self, freq1: Dict[str, float], freq2: Dict[str, float]) -> float:
        """
        Calculate the Manhattan distance between two frequency distributions.
        
        Args:
            freq1: First frequency distribution
            freq2: Second frequency distribution
            
        Returns:
            Manhattan distance between the distributions
        """
        # Get all unique characters from both distributions
        all_chars = set(freq1.keys()) | set(freq2.keys())
        
        # Calculate absolute differences
        abs_diff_sum = 0.0
        for char in all_chars:
            f1 = freq1.get(char, 0.0)
            f2 = freq2.get(char, 0.0)
            abs_diff_sum += abs(f1 - f2)
            
        return abs_diff_sum
    
    def calculate_cosine_similarity(self, freq1: Dict[str, float], freq2: Dict[str, float]) -> float:
        """
        Calculate the cosine similarity between two frequency distributions.
        
        Args:
            freq1: First frequency distribution
            freq2: Second frequency distribution
            
        Returns:
            Cosine similarity between the distributions (1.0 = identical, 0.0 = completely different)
        """
        # Get all unique characters from both distributions
        all_chars = set(freq1.keys()) | set(freq2.keys())
        
        # Calculate dot product
        dot_product = 0.0
        for char in all_chars:
            f1 = freq1.get(char, 0.0)
            f2 = freq2.get(char, 0.0)
            dot_product += f1 * f2
            
        # Calculate magnitudes
        magnitude1 = math.sqrt(sum(f ** 2 for f in freq1.values()))
        magnitude2 = math.sqrt(sum(f ** 2 for f in freq2.values()))
        
        # Handle potential division by zero
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
            
        return dot_product / (magnitude1 * magnitude2)
    
    def calculate_kl_divergence(self, freq1: Dict[str, float], freq2: Dict[str, float], 
                               smoothing: float = 1e-10) -> float:
        """
        Calculate the Kullback-Leibler divergence from freq1 to freq2.
        Note: KL divergence is asymmetric.
        
        Args:
            freq1: First frequency distribution (treated as P)
            freq2: Second frequency distribution (treated as Q)
            smoothing: Small value to add to frequencies to avoid division by zero
            
        Returns:
            KL divergence from freq1 to freq2
        """
        # Get all unique characters from both distributions
        all_chars = set(freq1.keys()) | set(freq2.keys())
        
        # Calculate KL divergence
        kl_divergence = 0.0
        for char in all_chars:
            p = freq1.get(char, 0.0) + smoothing
            q = freq2.get(char, 0.0) + smoothing
            kl_divergence += p * math.log(p / q)
            
        return kl_divergence
    
    def calculate_jensen_shannon_distance(self, freq1: Dict[str, float], freq2: Dict[str, float]) -> float:
        """
        Calculate the Jensen-Shannon distance between two frequency distributions.
        This is a symmetric version based on KL divergence.
        
        Args:
            freq1: First frequency distribution
            freq2: Second frequency distribution
            
        Returns:
            Jensen-Shannon distance between the distributions
        """
        # Create the average distribution M
        all_chars = set(freq1.keys()) | set(freq2.keys())
        m_dist = {}
        for char in all_chars:
            f1 = freq1.get(char, 0.0)
            f2 = freq2.get(char, 0.0)
            m_dist[char] = (f1 + f2) / 2.0
            
        # Calculate JS distance using KL divergence
        kl1 = self.calculate_kl_divergence(freq1, m_dist)
        kl2 = self.calculate_kl_divergence(freq2, m_dist)
        js_divergence = (kl1 + kl2) / 2.0
        
        # Convert to distance (square root of divergence)
        return math.sqrt(js_divergence)
    
    def compute(self, file1_path: str, file2_path: str) -> Dict[str, Any]:
        """
        Calculate various distance metrics between two files based on character frequency.
        
        Args:
            file1_path: Path to the first file
            file2_path: Path to the second file
            
        Returns:
            Dictionary containing various distance metrics
        """
        # Get character frequencies
        try:
            freq1 = self.get_char_frequencies(file1_path)
            freq2 = self.get_char_frequencies(file2_path)
            
            # Calculate various distance metrics
            euclidean = self.calculate_euclidean_distance(freq1, freq2)
            manhattan = self.calculate_manhattan_distance(freq1, freq2)
            cosine_sim = self.calculate_cosine_similarity(freq1, freq2)
            js_distance = self.calculate_jensen_shannon_distance(freq1, freq2)
            
            # Get top characters in each file
            top_chars1 = self._get_top_chars(freq1, 10)
            top_chars2 = self._get_top_chars(freq2, 10)
            
            # Calculate unique characters
            unique_chars1 = set(freq1.keys()) - set(freq2.keys())
            unique_chars2 = set(freq2.keys()) - set(freq1.keys())
            
            return {
                "euclidean_distance": euclidean,
                "manhattan_distance": manhattan, 
                "cosine_similarity": cosine_sim,
                "cosine_distance": 1.0 - cosine_sim,
                "jensen_shannon_distance": js_distance,
                "unique_chars_file1": len(unique_chars1),
                "unique_chars_file2": len(unique_chars2),
                "details": {
                    "top_chars_file1": top_chars1,
                    "top_chars_file2": top_chars2,
                    "char_count_file1": len(freq1),
                    "char_count_file2": len(freq2)
                }
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    def _get_top_chars(self, freq: Dict[str, float], n: int = 10) -> List[Tuple[str, float]]:
        """
        Get the top N most frequent characters from a frequency distribution.
        
        Args:
            freq: Character frequency distribution
            n: Number of top characters to return
            
        Returns:
            List of (character, frequency) tuples for the top N characters
        """
        sorted_chars = sorted(freq.items(), key=lambda x: x[1], reverse=True)
        return sorted_chars[:n]
#########################################################
import os
import math
from typing import Dict, Optional, Tuple, Union, List, Any


class FileSizeDistance:
    """
    A class that calculates distance metrics between two files based on their sizes.
    
    This simple comparison is based on the size of the two files, indicating differences 
    in the amount of stored data. Several metrics are provided to quantify the size difference
    in different ways that might be useful for different applications.
    """
    
    def __init__(self, 
                 normalize: bool = False,
                 max_file_size: Optional[int] = None,
                 use_log_scale: bool = False) -> None:
        """
        Initialize the File Size Distance calculator.
        
        Args:
            normalize: Whether to normalize the distance to a 0-1 scale
            max_file_size: Maximum file size to use for normalization (if None, uses the larger of the two files)
            use_log_scale: Whether to use logarithmic scale for comparing file sizes
        """
        super().__init__()
        self.type='file'
        
        self.normalize = normalize
        self.max_file_size = max_file_size
        self.use_log_scale = use_log_scale
    
    def get_file_size(self, file_path: str) -> int:
        """
        Get the size of a file in bytes.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Size of the file in bytes
            
        Raises:
            FileNotFoundError: If the file does not exist
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
            
        return os.path.getsize(file_path)
    
    def absolute_difference(self, size1: int, size2: int) -> int:
        """
        Calculate the absolute difference between two file sizes.
        
        Args:
            size1: Size of the first file in bytes
            size2: Size of the second file in bytes
            
        Returns:
            Absolute difference in bytes
        """
        return abs(size1 - size2)
    
    def relative_difference(self, size1: int, size2: int) -> float:
        """
        Calculate the relative difference between two file sizes.
        
        Args:
            size1: Size of the first file in bytes
            size2: Size of the second file in bytes
            
        Returns:
            Relative difference (|size1 - size2| / max(size1, size2))
        """
        if size1 == 0 and size2 == 0:
            return 0.0
            
        max_size = max(size1, size2)
        return abs(size1 - size2) / max_size
    
    def ratio_difference(self, size1: int, size2: int) -> float:
        """
        Calculate the ratio between two file sizes.
        
        Args:
            size1: Size of the first file in bytes
            size2: Size of the second file in bytes
            
        Returns:
            Ratio (larger / smaller) - 1, or 0 if both sizes are 0
        """
        if size1 == 0 and size2 == 0:
            return 0.0
            
        # Avoid division by zero
        if size1 == 0:
            return float('inf')
        if size2 == 0:
            return float('inf')
            
        # Calculate ratio so it's always >= 1
        ratio = max(size1, size2) / min(size1, size2)
        
        # Return ratio - 1 so that identical files have a distance of 0
        return ratio - 1.0
    
    def logarithmic_difference(self, size1: int, size2: int) -> float:
        """
        Calculate the logarithmic difference between two file sizes.
        Useful when comparing files with vastly different sizes.
        
        Args:
            size1: Size of the first file in bytes
            size2: Size of the second file in bytes
            
        Returns:
            Logarithmic difference (|log(size1) - log(size2)|) or 0 if both sizes are 0
        """
        if size1 == 0 and size2 == 0:
            return 0.0
            
        # Avoid logarithm of zero
        safe_size1 = max(1, size1)
        safe_size2 = max(1, size2)
        
        return abs(math.log(safe_size1) - math.log(safe_size2))
    
    def size_category_difference(self, size1: int, size2: int) -> int:
        """
        Calculate difference in size categories between two files.
        Categories are defined in powers of 2 (0-1KB, 1-2KB, 2-4KB, etc.)
        
        Args:
            size1: Size of the first file in bytes
            size2: Size of the second file in bytes
            
        Returns:
            Absolute difference in size categories
        """
        if size1 == 0 and size2 == 0:
            return 0
            
        # Avoid logarithm of zero
        safe_size1 = max(1, size1)
        safe_size2 = max(1, size2)
        
        # Calculate log base 2 and floor to get size category
        category1 = int(math.log2(safe_size1))
        category2 = int(math.log2(safe_size2))
        
        return abs(category1 - category2)
    
    def normalized_distance(self, 
                          difference: Union[int, float], 
                          max_difference: Union[int, float]) -> float:
        """
        Normalize a distance value to a 0-1 scale.
        
        Args:
            difference: The calculated difference
            max_difference: The maximum possible difference
            
        Returns:
            Normalized distance between 0 and 1
        """
        if max_difference == 0:
            return 0.0
            
        normalized = difference / max_difference
        
        # Ensure the result is between 0 and 1
        return min(1.0, max(0.0, normalized))
    
    def compute(self, file1_path: str, file2_path: str) -> Dict[str, Any]:
        """
        Calculate various distance metrics between two files based on their sizes.
        
        Args:
            file1_path: Path to the first file
            file2_path: Path to the second file
            
        Returns:
            Dictionary containing various distance metrics and file information
        """
        try:
            # Get file sizes
            size1 = self.get_file_size(file1_path)
            size2 = self.get_file_size(file2_path)
            
            # Calculate absolute difference
            abs_diff = self.absolute_difference(size1, size2)
            
            # Calculate relative difference
            rel_diff = self.relative_difference(size1, size2)
            
            # Calculate ratio difference
            ratio_diff = self.ratio_difference(size1, size2)
            
            # Calculate logarithmic difference
            log_diff = self.logarithmic_difference(size1, size2)
            
            # Calculate size category difference
            category_diff = self.size_category_difference(size1, size2)
            
            # Determine which metric to use as the primary distance
            if self.use_log_scale:
                primary_distance = log_diff
            else:
                primary_distance = rel_diff
            
            # Format results for human-readable output
            size1_formatted = self._format_file_size(size1)
            size2_formatted = self._format_file_size(size2)
            abs_diff_formatted = self._format_file_size(abs_diff)
            
            # Put together the results
            result = {
                "primary_distance": primary_distance,
                "absolute_difference": abs_diff,
                "absolute_difference_formatted": abs_diff_formatted,
                "relative_difference": rel_diff,
                "ratio_difference": ratio_diff,
                "logarithmic_difference": log_diff,
                "category_difference": category_diff,
                "file1_size": size1,
                "file2_size": size2,
                "file1_size_formatted": size1_formatted,
                "file2_size_formatted": size2_formatted,
                "same_size": size1 == size2
            }
            
            # Calculate percentage difference
            if max(size1, size2) > 0:
                result["percentage_difference"] = (abs_diff / max(size1, size2)) * 100
            else:
                result["percentage_difference"] = 0.0
                
            return result
            
        except Exception as e:
            return {"error": str(e)}
    
    def _format_file_size(self, size_in_bytes: int) -> str:
        """
        Format a file size in bytes to a human-readable string.
        
        Args:
            size_in_bytes: Size in bytes
            
        Returns:
            Formatted string (e.g., "1.23 MB")
        """
        # Define size units
        units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
        
        # Handle zero size
        if size_in_bytes == 0:
            return "0 B"
            
        # Calculate the appropriate unit
        i = 0
        while size_in_bytes >= 1024 and i < len(units) - 1:
            size_in_bytes /= 1024.0
            i += 1
            
        # Round to 2 decimal places and format
        return f"{size_in_bytes:.2f} {units[i]}"
    
    def size_similarity(self, file1_path: str, file2_path: str) -> float:
        """
        Calculate a similarity score based on file sizes, where 1.0 means identical sizes
        and 0.0 means maximally different sizes.
        
        Args:
            file1_path: Path to the first file
            file2_path: Path to the second file
            
        Returns:
            Similarity score between 0.0 and 1.0
        """
        try:
            # Get file sizes
            size1 = self.get_file_size(file1_path)
            size2 = self.get_file_size(file2_path)
            
            # If both files are empty, they are identical
            if size1 == 0 and size2 == 0:
                return 1.0
                
            # Calculate relative difference
            rel_diff = self.relative_difference(size1, size2)
            
            # Convert to similarity (1.0 - difference)
            return 1.0 - rel_diff
            
        except Exception:
            return 0.0  # Return minimum similarity on error

#########################################
import os
import re
import math
from typing import Dict, List, Set, Tuple, Union, Optional, Any, Callable
from collections import Counter
import json
import pickle
import hashlib
import logging
from pathlib import Path

class EmbeddingBasedDistance:
    """
    A class that calculates the semantic distance between two files
    using pre-trained word embeddings like FastText or GloVe.
    
    This implementation measures semantic differences by:
    1. Tokenizing text from each file
    2. Looking up word embeddings for each token
    3. Creating document embeddings by aggregating word embeddings
    4. Calculating distance metrics between document embeddings
    """
    
    def __init__(self, 
                 embedding_path: str,
                 embedding_type: str = "glove",
                 cache_dir: Optional[str] = None,
                 max_tokens: int = 10000,
                 aggregation_method: str = "mean",
                 lowercase: bool = True,
                 remove_stopwords: bool = True,
                 vector_dim: int = 300) -> None:
        """
        Initialize the Embedding-Based Distance calculator.
        
        Args:
            embedding_path: Path to the pre-trained embedding file
            embedding_type: Type of embeddings ('glove', 'fasttext', or 'word2vec')
            cache_dir: Directory to cache processed embeddings (None for no caching)
            max_tokens: Maximum number of tokens to process per file
            aggregation_method: Method to aggregate word vectors ('mean', 'max', or 'sum')
            lowercase: Whether to convert all text to lowercase
            remove_stopwords: Whether to remove common stopwords
            vector_dim: Dimension of the embedding vectors
        """
        super().__init__()
        self.type='file'
        
        self.embedding_path = embedding_path
        self.embedding_type = embedding_type.lower()
        self.cache_dir = cache_dir
        self.max_tokens = max_tokens
        self.aggregation_method = aggregation_method
        self.lowercase = lowercase
        self.remove_stopwords = remove_stopwords
        self.vector_dim = vector_dim
        
        # Set up logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        
        # Initialize embeddings and stopwords
        self.embeddings = None
        self.stopwords = self._load_stopwords()
        
        # Create cache directory if needed
        if self.cache_dir:
            os.makedirs(self.cache_dir, exist_ok=True)
    
    def _load_stopwords(self) -> Set[str]:
        """
        Load a set of common English stopwords.
        
        Returns:
            Set of stopwords
        """
        # Common English stopwords
        stopwords = {
            "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", 
            "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", 
            "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", 
            "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", 
            "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", 
            "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", 
            "than", "too", "very", "s", "t", "can", "will", "just", "don", "don't", "should", 
            "now", "d", "ll", "m", "o", "re", "ve", "y", "ain", "aren", "aren't", "couldn", 
            "couldn't", "didn", "didn't", "doesn", "doesn't", "hadn", "hadn't", "hasn", "hasn't", 
            "haven", "haven't", "isn", "isn't", "ma", "mightn", "mightn't", "mustn", "mustn't", 
            "needn", "needn't", "shan", "shan't", "shouldn", "shouldn't", "wasn", "wasn't", 
            "weren", "weren't", "won", "won't", "wouldn", "wouldn't", "i", "me", "my", "myself", 
            "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", 
            "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", 
            "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", 
            "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", 
            "being", "have", "has", "had", "having", "do", "does", "did", "doing"
        }
        return stopwords
    
    def _get_cache_path(self, embedding_path: str) -> str:
        """
        Get the cache file path for embeddings.
        
        Args:
            embedding_path: Path to the original embedding file
            
        Returns:
            Path to the cache file
        """
        if not self.cache_dir:
            return None
            
        # Create a hash of the embedding path to use in the cache filename
        file_hash = hashlib.md5(embedding_path.encode()).hexdigest()
        return os.path.join(self.cache_dir, f"emb_cache_{file_hash}.pkl")
    
    def _load_embeddings(self) -> Dict[str, List[float]]:
        """
        Load pre-trained word embeddings from file.
        
        Returns:
            Dictionary mapping words to their embedding vectors
        """
        if self.embeddings is not None:
            return self.embeddings
            
        # Check if a cached version exists
        cache_path = self._get_cache_path(self.embedding_path)
        if cache_path and os.path.exists(cache_path):
            self.logger.info(f"Loading embeddings from cache: {cache_path}")
            with open(cache_path, 'rb') as f:
                self.embeddings = pickle.load(f)
            return self.embeddings
            
        self.logger.info(f"Loading embeddings from: {self.embedding_path}")
        embeddings = {}
        
        # Check if file exists
        if not os.path.exists(self.embedding_path):
            raise FileNotFoundError(f"Embedding file not found: {self.embedding_path}")
            
        # Load embeddings based on type
        if self.embedding_type == "glove":
            # GloVe format: word v1 v2 v3 ...
            with open(self.embedding_path, 'r', encoding='utf-8') as f:
                for line in f:
                    values = line.strip().split()
                    word = values[0]
                    vector = [float(x) for x in values[1:]]
                    if len(vector) == self.vector_dim:
                        embeddings[word] = vector
        
        elif self.embedding_type == "fasttext":
            # FastText format: word v1 v2 v3 ...
            # Skip first line if it contains metadata
            with open(self.embedding_path, 'r', encoding='utf-8') as f:
                first_line = f.readline()
                # If first line contains metadata (dimensions), skip it
                if len(first_line.split()) == 2:
                    pass
                else:
                    values = first_line.strip().split()
                    word = values[0]
                    vector = [float(x) for x in values[1:]]
                    if len(vector) == self.vector_dim:
                        embeddings[word] = vector
                
                # Process the rest of the file
                for line in f:
                    values = line.strip().split()
                    word = values[0]
                    vector = [float(x) for x in values[1:]]
                    if len(vector) == self.vector_dim:
                        embeddings[word] = vector
        
        elif self.embedding_type == "word2vec":
            # Word2Vec format: word v1 v2 v3 ...
            # Skip first line as it contains metadata
            with open(self.embedding_path, 'r', encoding='utf-8') as f:
                f.readline()  # Skip header
                for line in f:
                    values = line.strip().split()
                    word = values[0]
                    vector = [float(x) for x in values[1:]]
                    if len(vector) == self.vector_dim:
                        embeddings[word] = vector
        
        else:
            raise ValueError(f"Unsupported embedding type: {self.embedding_type}")
            
        self.logger.info(f"Loaded {len(embeddings)} word vectors")
        
        # Cache embeddings if cache directory is specified
        if cache_path:
            self.logger.info(f"Caching embeddings to: {cache_path}")
            with open(cache_path, 'wb') as f:
                pickle.dump(embeddings, f)
                
        self.embeddings = embeddings
        return embeddings
    
    def _tokenize_text(self, text: str) -> List[str]:
        """
        Tokenize text into words.
        
        Args:
            text: Input text
            
        Returns:
            List of tokens
        """
        # Convert to lowercase if specified
        if self.lowercase:
            text = text.lower()
            
        # Basic tokenization - split on whitespace and punctuation
        tokens = re.findall(r'\b\w+\b', text)
        
        # Remove stopwords if specified
        if self.remove_stopwords:
            tokens = [t for t in tokens if t not in self.stopwords]
            
        # Limit the number of tokens
        return tokens[:self.max_tokens]
    
    def _read_file(self, file_path: str) -> str:
        """
        Read text from a file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Text content of the file
            
        Raises:
            FileNotFoundError: If the file does not exist
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
            
        try:
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                return f.read()
        except Exception as e:
            self.logger.warning(f"Error reading file {file_path}: {e}")
            # Try reading as binary and decode with permissive error handling
            with open(file_path, 'rb') as f:
                return f.read().decode('utf-8', errors='replace')
    
    def _create_document_embedding(self, tokens: List[str]) -> List[float]:
        """
        Create a document embedding by aggregating word embeddings.
        
        Args:
            tokens: List of word tokens
            
        Returns:
            Document embedding vector
        """
        # Ensure embeddings are loaded
        embeddings = self._load_embeddings()
        
        # Filter tokens to those that have embeddings
        token_vectors = [embeddings[token] for token in tokens if token in embeddings]
        
        # If no tokens have embeddings, return a zero vector
        if not token_vectors:
            return [0.0] * self.vector_dim
            
        # Aggregate the vectors based on the specified method
        if self.aggregation_method == "mean":
            # Calculate the mean of all word vectors
            doc_vector = [sum(col) / len(token_vectors) for col in zip(*token_vectors)]
            
        elif self.aggregation_method == "max":
            # Take the maximum value for each dimension
            doc_vector = [max(col) for col in zip(*token_vectors)]
            
        elif self.aggregation_method == "sum":
            # Sum all word vectors
            doc_vector = [sum(col) for col in zip(*token_vectors)]
            
        else:
            raise ValueError(f"Unsupported aggregation method: {self.aggregation_method}")
            
        return doc_vector
    
    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """
        Calculate the cosine similarity between two vectors.
        
        Args:
            vec1: First vector
            vec2: Second vector
            
        Returns:
            Cosine similarity (between -1 and 1, where 1 means identical direction)
        """
        # Calculate dot product
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        
        # Calculate magnitudes
        magnitude1 = math.sqrt(sum(a * a for a in vec1))
        magnitude2 = math.sqrt(sum(b * b for b in vec2))
        
        # Handle zero magnitude
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
            
        return dot_product / (magnitude1 * magnitude2)
    
    def _euclidean_distance(self, vec1: List[float], vec2: List[float]) -> float:
        """
        Calculate the Euclidean distance between two vectors.
        
        Args:
            vec1: First vector
            vec2: Second vector
            
        Returns:
            Euclidean distance
        """
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(vec1, vec2)))
    
    def _get_most_important_words(self, 
                                tokens: List[str], 
                                embedding: List[float], 
                                n: int = 10) -> List[Tuple[str, float]]:
        """
        Find the words that contribute most to the document embedding.
        
        Args:
            tokens: List of tokens in the document
            embedding: Document embedding vector
            n: Number of top words to return
            
        Returns:
            List of (word, importance_score) tuples
        """
        embeddings = self._load_embeddings()
        word_scores = []
        
        # Count token frequency
        token_counts = Counter(tokens)
        
        # Calculate each word's contribution to the document embedding
        for token, count in token_counts.items():
            if token in embeddings:
                # Calculate cosine similarity to the document vector
                similarity = self._cosine_similarity(embeddings[token], embedding)
                # Weight by frequency
                score = similarity * count
                word_scores.append((token, score))
                
        # Sort by score in descending order
        word_scores.sort(key=lambda x: x[1], reverse=True)
        
        return word_scores[:n]
    
    def calculate_file_embedding(self, file_path: str) -> Tuple[List[float], List[str]]:
        """
        Calculate the embedding for a file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Tuple of (document_embedding, tokens)
        """
        # Read file content
        text = self._read_file(file_path)
        
        # Tokenize the text
        tokens = self._tokenize_text(text)
        
        # Create document embedding
        doc_embedding = self._create_document_embedding(tokens)
        
        return doc_embedding, tokens
    
    def compute(self, file1_path: str, file2_path: str) -> Dict[str, Any]:
        """
        Calculate the semantic distance between two files using embeddings.
        
        Args:
            file1_path: Path to the first file
            file2_path: Path to the second file
            
        Returns:
            Dictionary containing distance metrics and other information
        """
        try:
            # Calculate embeddings for both files
            embedding1, tokens1 = self.calculate_file_embedding(file1_path)
            embedding2, tokens2 = self.calculate_file_embedding(file2_path)
            
            # Calculate cosine similarity
            cosine_sim = self._cosine_similarity(embedding1, embedding2)
            
            # Calculate euclidean distance
            euclidean_dist = self._euclidean_distance(embedding1, embedding2)
            
            # Get most important words for each document
            important_words1 = self._get_most_important_words(tokens1, embedding1)
            important_words2 = self._get_most_important_words(tokens2, embedding2)
            
            # Calculate shared important words
            important_words1_set = {word for word, _ in important_words1}
            important_words2_set = {word for word, _ in important_words2}
            shared_important_words = important_words1_set.intersection(important_words2_set)
            
            # Calculate token overlap
            tokens1_set = set(tokens1)
            tokens2_set = set(tokens2)
            common_tokens = tokens1_set.intersection(tokens2_set)
            
            # Calculate Jaccard similarity
            jaccard_sim = len(common_tokens) / len(tokens1_set.union(tokens2_set)) if tokens1 and tokens2 else 0.0
            
            return {
                "cosine_similarity": cosine_sim,
                "cosine_distance": 1.0 - cosine_sim,
                "euclidean_distance": euclidean_dist,
                "jaccard_similarity": jaccard_sim,
                "token_count_file1": len(tokens1),
                "token_count_file2": len(tokens2),
                "unique_tokens_file1": len(tokens1_set),
                "unique_tokens_file2": len(tokens2_set),
                "common_tokens": len(common_tokens),
                "semantic_distance": 1.0 - cosine_sim,  # Primary distance metric
                "details": {
                    "important_words_file1": important_words1,
                    "important_words_file2": important_words2,
                    "shared_important_words": list(shared_important_words),
                    "token_overlap_ratio": len(common_tokens) / max(len(tokens1), len(tokens2)) if tokens1 and tokens2 else 0.0
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error calculating distance: {e}")
            return {"error": str(e)}

########################################
from typing import Optional, Tuple, BinaryIO
import zlib
import os

class CRCDistanceCalculator:
    """
    A class to calculate the Cyclic Redundancy Check (CRC) distance between two files.
    
    This class computes CRC-32 checksums for files and determines their "distance" 
    (i.e., whether they are identical or different based on their checksums).
    The CRC-32 algorithm is used to detect accidental changes/errors in data.
    """
    
    def __init__(self, buffer_size: int = 65536) -> None:
        """
        Initialize the CRC Distance Calculator.
        
        Args:
            buffer_size: Size of the buffer used when reading files (default: 64KB)
        """
        super().__init__()
        self.type='file'
        
        self.buffer_size = buffer_size
    
    def calculate_crc(self, file_path: str) -> int:
        """
        Calculate the CRC-32 checksum of a file.
        
        Args:
            file_path: Path to the file to calculate the checksum for
            
        Returns:
            The CRC-32 checksum as an integer
            
        Raises:
            FileNotFoundError: If the specified file does not exist
            PermissionError: If the file cannot be accessed due to permissions
            IOError: If an I/O error occurs while reading the file
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if not os.path.isfile(file_path):
            raise ValueError(f"Not a file: {file_path}")
        
        crc = 0
        with open(file_path, 'rb') as file:
            while True:
                data = file.read(self.buffer_size)
                if not data:
                    break
                crc = zlib.crc32(data, crc)
        
        return crc & 0xFFFFFFFF  # Ensure the result is unsigned 32-bit
    
    def compute(self, file_path1: str, file_path2: str) -> Tuple[bool, int, int]:
        """
        Calculate the CRC distance between two files.
        
        Args:
            file_path1: Path to the first file
            file_path2: Path to the second file
            
        Returns:
            A tuple containing:
            - A boolean indicating if the files are identical (True) or different (False)
            - The CRC-32 checksum of the first file
            - The CRC-32 checksum of the second file
            
        Raises:
            FileNotFoundError: If either specified file does not exist
            PermissionError: If either file cannot be accessed due to permissions
            IOError: If an I/O error occurs while reading either file
        """
        crc1 = self.calculate_crc(file_path1)
        crc2 = self.calculate_crc(file_path2)
        
        return (crc1 == crc2, crc1, crc2)
    
    def get_formatted_result(self, file_path1: str, file_path2: str) -> str:
        """
        Get a formatted string describing the CRC distance result.
        
        Args:
            file_path1: Path to the first file
            file_path2: Path to the second file
            
        Returns:
            A formatted string describing the results of the CRC comparison
        """
        try:
            identical, crc1, crc2 = self.compute(file_path1, file_path2)
            
            if identical:
                result = f"Files are identical (CRC-32: {crc1:08x})"
            else:
                result = (f"Files are different:\n"
                         f"  - {os.path.basename(file_path1)}: CRC-32 = {crc1:08x}\n"
                         f"  - {os.path.basename(file_path2)}: CRC-32 = {crc2:08x}")
            
            return result
            
        except Exception as e:
            return f"Error comparing files: {str(e)}"
    
    @staticmethod
    def stream_crc(file_obj: BinaryIO, buffer_size: int = 65536) -> int:
        """
        Calculate the CRC-32 checksum of a file stream.
        
        This is a static method that can be used to calculate the CRC of an already opened file.
        
        Args:
            file_obj: An open file object in binary mode
            buffer_size: Size of the buffer used when reading the stream
            
        Returns:
            The CRC-32 checksum as an integer
        """
        crc = 0
        while True:
            data = file_obj.read(buffer_size)
            if not data:
                break
            crc = zlib.crc32(data, crc)
        
        return crc & 0xFFFFFFFF  # Ensure the result is unsigned 32-bit
###############################################
from typing import Tuple, Optional, BinaryIO, Dict
import zlib
import os
from math import log2

class Adler32SimilarityCalculator:
    """
    A class to calculate the Adler-32 checksum similarity between two files.
    
    Adler-32 is a lightweight checksum algorithm that runs faster than CRC-32
    but with a slightly higher risk of undetected errors. This class uses
    Adler-32 to compute checksums for files and determines their similarity
    based on the checksum values.
    """
    
    def __init__(self, buffer_size: int = 65536, chunk_size: int = 4096) -> None:
        """
        Initialize the Adler-32 Similarity Calculator.
        
        Args:
            buffer_size: Size of the buffer used when reading entire files (default: 64KB)
            chunk_size: Size of chunks to calculate progressive checksums (default: 4KB)
        """
        super().__init__()
        self.type='file'
        
        self.buffer_size = buffer_size
        self.chunk_size = chunk_size
    
    def calculate_adler32(self, file_path: str) -> int:
        """
        Calculate the Adler-32 checksum of a file.
        
        Args:
            file_path: Path to the file to calculate the checksum for
            
        Returns:
            The Adler-32 checksum as an integer
            
        Raises:
            FileNotFoundError: If the specified file does not exist
            PermissionError: If the file cannot be accessed due to permissions
            IOError: If an I/O error occurs while reading the file
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if not os.path.isfile(file_path):
            raise ValueError(f"Not a file: {file_path}")
        
        adler = 1  # Initial value for Adler-32
        
        with open(file_path, 'rb') as file:
            while True:
                data = file.read(self.buffer_size)
                if not data:
                    break
                adler = zlib.adler32(data, adler)
        
        return adler & 0xFFFFFFFF  # Convert to unsigned 32-bit integer
    
    def calculate_chunked_adler32(self, file_path: str) -> Dict[int, int]:
        """
        Calculate Adler-32 checksums for chunks of a file.
        
        This method divides the file into chunks and calculates
        an Adler-32 checksum for each chunk, allowing for a more
        granular comparison between files.
        
        Args:
            file_path: Path to the file to calculate the checksums for
            
        Returns:
            Dictionary mapping chunk index to Adler-32 checksum
            
        Raises:
            FileNotFoundError: If the specified file does not exist
            PermissionError: If the file cannot be accessed due to permissions
            IOError: If an I/O error occurs while reading the file
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if not os.path.isfile(file_path):
            raise ValueError(f"Not a file: {file_path}")
        
        chunk_checksums = {}
        chunk_index = 0
        
        with open(file_path, 'rb') as file:
            while True:
                data = file.read(self.chunk_size)
                if not data:
                    break
                
                # Calculate Adler-32 for this chunk
                chunk_adler = zlib.adler32(data) & 0xFFFFFFFF
                chunk_checksums[chunk_index] = chunk_adler
                chunk_index += 1
        
        return chunk_checksums
    
    def calculate_similarity(self, file_path1: str, file_path2: str) -> Tuple[float, int, int]:
        """
        Calculate the Adler-32 similarity between two files.
        
        The similarity is calculated as a normalized score where:
        - 1.0 means identical files (same Adler-32 checksum)
        - 0.0 means completely different files
        
        For non-identical files, the similarity is calculated based on
        the Hamming weight of the XOR of the two checksums, providing a
        rough measure of how many bits differ between the checksums.
        
        Args:
            file_path1: Path to the first file
            file_path2: Path to the second file
            
        Returns:
            A tuple containing:
            - A float between 0.0 and 1.0 representing the similarity
            - The Adler-32 checksum of the first file
            - The Adler-32 checksum of the second file
            
        Raises:
            FileNotFoundError: If either specified file does not exist
            PermissionError: If either file cannot be accessed due to permissions
            IOError: If an I/O error occurs while reading either file
        """
        adler1 = self.calculate_adler32(file_path1)
        adler2 = self.calculate_adler32(file_path2)
        
        if adler1 == adler2:
            return (1.0, adler1, adler2)
        
        # Calculate bit difference as a similarity measure
        xor_result = adler1 ^ adler2
        bit_count = bin(xor_result).count('1')
        
        # Normalize to a similarity score between 0 and 1
        # 32 is the maximum number of different bits in a 32-bit value
        similarity = 1.0 - (bit_count / 32.0)
        
        return (similarity, adler1, adler2)
    
    def calculate_chunked_similarity(self, file_path1: str, file_path2: str) -> float:
        """
        Calculate a more detailed similarity score based on file chunks.
        
        This method divides both files into chunks and compares the
        checksums of corresponding chunks, providing a more granular
        measure of similarity than the whole-file checksum comparison.
        
        Args:
            file_path1: Path to the first file
            file_path2: Path to the second file
            
        Returns:
            A float between 0.0 and 1.0 representing the chunk-based similarity
            
        Raises:
            FileNotFoundError: If either specified file does not exist
            PermissionError: If either file cannot be accessed due to permissions
            IOError: If an I/O error occurs while reading either file
        """
        chunks1 = self.calculate_chunked_adler32(file_path1)
        chunks2 = self.calculate_chunked_adler32(file_path2)
        
        # Get the maximum number of chunks between the two files
        max_chunks = max(len(chunks1), len(chunks2))
        
        if max_chunks == 0:
            # Both files are empty
            return 1.0
        
        # Count matching chunks
        matching_chunks = 0
        for chunk_idx in set(chunks1.keys()).intersection(set(chunks2.keys())):
            if chunks1[chunk_idx] == chunks2[chunk_idx]:
                matching_chunks += 1
        
        # Calculate similarity as the ratio of matching chunks to total chunks
        return matching_chunks / max_chunks
    
    def get_formatted_result(self, file_path1: str, file_path2: str, use_chunks: bool = False) -> str:
        """
        Get a formatted string describing the Adler-32 similarity result.
        
        Args:
            file_path1: Path to the first file
            file_path2: Path to the second file
            use_chunks: Whether to use chunk-based similarity (default: False)
            
        Returns:
            A formatted string describing the results of the similarity comparison
        """
        try:
            if use_chunks:
                similarity = self.calculate_chunked_similarity(file_path1, file_path2)
                result = (f"Chunk-based Adler-32 similarity: {similarity:.4f} "
                         f"({similarity * 100:.2f}%)")
            else:
                similarity, adler1, adler2 = self.calculate_similarity(file_path1, file_path2)
                
                if similarity == 1.0:
                    result = f"Files are identical (Adler-32: {adler1:08x})"
                else:
                    result = (f"Adler-32 similarity: {similarity:.4f} ({similarity * 100:.2f}%)\n"
                             f"  - {os.path.basename(file_path1)}: Adler-32 = {adler1:08x}\n"
                             f"  - {os.path.basename(file_path2)}: Adler-32 = {adler2:08x}")
            
            return result
            
        except Exception as e:
            return f"Error comparing files: {str(e)}"
    
    @staticmethod
    def stream_adler32(file_obj: BinaryIO, buffer_size: int = 65536) -> int:
        """
        Calculate the Adler-32 checksum of a file stream.
        
        This is a static method that can be used to calculate the Adler-32
        of an already opened file.
        
        Args:
            file_obj: An open file object in binary mode
            buffer_size: Size of the buffer used when reading the stream
            
        Returns:
            The Adler-32 checksum as an integer
        """
        adler = 1  # Initial value for Adler-32
        
        while True:
            data = file_obj.read(buffer_size)
            if not data:
                break
            adler = zlib.adler32(data, adler)
        
        return adler & 0xFFFFFFFF  # Convert to unsigned 32-bit integer
        
    def compute(self, file_path1: str, file_path2: str) -> float:
        """
        Estimate file similarity using information theory principles.
        
        This method uses entropy-based measurements over chunk checksums
        to provide a more sophisticated similarity measure that can detect
        partial matches and rearrangements.
        
        Args:
            file_path1: Path to the first file
            file_path2: Path to the second file
            
        Returns:
            A float between 0.0 and 1.0 representing the entropy-based similarity
            
        Raises:
            FileNotFoundError: If either specified file does not exist
            PermissionError: If either file cannot be accessed due to permissions
            IOError: If an I/O error occurs while reading either file
        """
        chunks1 = self.calculate_chunked_adler32(file_path1)
        chunks2 = self.calculate_chunked_adler32(file_path2)
        
        if not chunks1 and not chunks2:
            # Both files are empty
            return 1.0
            
        if not chunks1 or not chunks2:
            # One file is empty, one is not
            return 0.0
            
        # Get the set of unique checksums in each file
        checksums1 = set(chunks1.values())
        checksums2 = set(chunks2.values())
        
        # Calculate the Jaccard similarity of the checksum sets
        intersection = len(checksums1.intersection(checksums2))
        union = len(checksums1.union(checksums2))
        
        return intersection / union if union > 0 else 0.0



