import pandas as pd
import numpy as np
from collections import deque
from typing import List, Dict, Set, Tuple, Optional, Union, Callable
import networkx as nx
from sentence_transformers import SentenceTransformer, util
import matplotlib.pyplot as plt
from .ctg_api import ClinicalTrialsAPI


class ClinicalTrialsNavigator:
    """Class to navigate through clinical trials data using graph traversal algorithms"""
    
    def __init__(self, api: Optional[ClinicalTrialsAPI] = None):
        """
        Initialize the navigator with API access
        
        Args:
            api (ClinicalTrialsAPI, optional): API client for clinical trials data
        """
        self.api = api or ClinicalTrialsAPI()
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.graph = nx.Graph()
        self.embeddings_cache = {}  # Cache for embeddings
        self.df_cache = None  # Cache for the most recent dataframe
        
    def build_similarity_graph(
        self,
        studies_df: pd.DataFrame,
        similarity_threshold: float = 0.7,
        max_edges_per_node: int = 5
    ) -> nx.Graph:
        """
        Build a graph where nodes are studies and edges represent semantic similarity
        
        Args:
            studies_df (pd.DataFrame): DataFrame containing studies with 'NCTId' and 'briefSummary' columns
            similarity_threshold (float): Minimum cosine similarity to create an edge
            max_edges_per_node (int): Maximum number of edges per node
            
        Returns:
            nx.Graph: A graph representing study similarities
        """
        # Reset the graph
        self.graph = nx.Graph()
        self.df_cache = studies_df.copy()
        
        # Extract brief summaries and compute embeddings
        summaries = studies_df['briefSummary'].fillna('').tolist()
        study_ids = studies_df['NCTId'].tolist()
        
        # Compute embeddings for all studies
        embeddings = self.model.encode(summaries, convert_to_tensor=True)
        
        # Store embeddings in cache
        for idx, study_id in enumerate(study_ids):
            self.embeddings_cache[study_id] = embeddings[idx]
        
        # Add nodes (studies) to the graph
        for idx, study_id in enumerate(study_ids):
            self.graph.add_node(study_id, 
                                idx=idx, 
                                title=studies_df['briefTitle'].iloc[idx] if 'briefTitle' in studies_df.columns else '',
                                summary=summaries[idx])
        
        # Compute pairwise similarities
        similarity_matrix = util.pytorch_cos_sim(embeddings, embeddings).cpu().numpy()
        
        # Add edges between similar studies
        for i in range(len(study_ids)):
            # Get indices of top similar studies (excluding self)
            similarities = similarity_matrix[i]
            similarities[i] = -1  # Exclude self-similarity
            
            # Get top similar study indices above threshold
            top_indices = np.argsort(similarities)[::-1]
            top_indices = [idx for idx in top_indices if similarities[idx] >= similarity_threshold][:max_edges_per_node]
            
            # Add edges to the graph
            for j in top_indices:
                self.graph.add_edge(study_ids[i], study_ids[j], weight=similarities[j])
        
        return self.graph
    
    def breadth_first_search(
        self,
        start_id: str,
        max_depth: int = 3,
        visited_limit: int = 20
    ) -> List[Dict]:
        """
        Perform Breadth-First Search from a starting clinical trial
        
        Args:
            start_id (str): NCTId of the starting clinical trial
            max_depth (int): Maximum depth to traverse
            visited_limit (int): Maximum number of nodes to visit
            
        Returns:
            List[Dict]: List of visited trials with traversal information
        """
        if start_id not in self.graph:
            raise ValueError(f"Start node {start_id} not found in the graph")
        
        queue = deque([(start_id, 0)])  # (node_id, depth)
        visited = {start_id: 0}  # node_id: depth
        result = []
        
        while queue and len(visited) < visited_limit:
            current_id, depth = queue.popleft()
            
            # Get node data
            node_data = self.graph.nodes[current_id]
            result.append({
                'NCTId': current_id,
                'depth': depth,
                'title': node_data.get('title', ''),
                'summary': node_data.get('summary', ''),
                'neighbors': len(list(self.graph.neighbors(current_id)))
            })
            
            # Don't explore further if we've reached max depth
            if depth >= max_depth:
                continue
                
            # Add neighbors to the queue
            for neighbor in self.graph.neighbors(current_id):
                if neighbor not in visited:
                    visited[neighbor] = depth + 1
                    queue.append((neighbor, depth + 1))
        
        return result
    
    def depth_first_search(
        self,
        start_id: str,
        max_depth: int = 3,
        visited_limit: int = 20
    ) -> List[Dict]:
        """
        Perform Depth-First Search from a starting clinical trial
        
        Args:
            start_id (str): NCTId of the starting clinical trial
            max_depth (int): Maximum depth to traverse
            visited_limit (int): Maximum number of nodes to visit
            
        Returns:
            List[Dict]: List of visited trials with traversal information
        """
        if start_id not in self.graph:
            raise ValueError(f"Start node {start_id} not found in the graph")
        
        visited = {}  # node_id: depth
        result = []
        
        def dfs_recursive(node_id: str, depth: int):
            # Stop if we've reached the limits
            if len(visited) >= visited_limit or depth > max_depth:
                return
            
            # Mark as visited
            visited[node_id] = depth
            
            # Get node data
            node_data = self.graph.nodes[node_id]
            result.append({
                'NCTId': node_id,
                'depth': depth,
                'title': node_data.get('title', ''),
                'summary': node_data.get('summary', ''),
                'neighbors': len(list(self.graph.neighbors(node_id)))
            })
            
            # Visit neighbors
            if depth < max_depth:
                for neighbor in self.graph.neighbors(node_id):
                    if neighbor not in visited:
                        dfs_recursive(neighbor, depth + 1)
        
        # Start DFS from the start node
        dfs_recursive(start_id, 0)
        return result
    
    def find_path(
        self,
        start_id: str,
        target_id: str,
        algorithm: str = 'bfs'
    ) -> List[str]:
        """
        Find a path between two clinical trials
        
        Args:
            start_id (str): Starting trial NCTId
            target_id (str): Target trial NCTId
            algorithm (str): Algorithm to use ('bfs' or 'dfs')
            
        Returns:
            List[str]: List of NCTIds representing the path
        """
        if start_id not in self.graph or target_id not in self.graph:
            missing = []
            if start_id not in self.graph:
                missing.append(start_id)
            if target_id not in self.graph:
                missing.append(target_id)
            raise ValueError(f"Node(s) not found in the graph: {', '.join(missing)}")
        
        if algorithm.lower() == 'bfs':
            # Use BFS to find shortest path
            queue = deque([(start_id, [start_id])])  # (current_node, path_so_far)
            visited = {start_id}
            
            while queue:
                current_id, path = queue.popleft()
                
                if current_id == target_id:
                    return path
                
                for neighbor in self.graph.neighbors(current_id):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append((neighbor, path + [neighbor]))
                        
            # No path found
            return []
        
        elif algorithm.lower() == 'dfs':
            # Use DFS to find a path
            visited = set()
            path = []
            
            def dfs_path(current_id: str) -> bool:
                visited.add(current_id)
                path.append(current_id)
                
                if current_id == target_id:
                    return True
                
                for neighbor in self.graph.neighbors(current_id):
                    if neighbor not in visited:
                        if dfs_path(neighbor):
                            return True
                
                # Backtrack if no path found
                path.pop()
                return False
            
            dfs_path(start_id)
            return path
        
        else:
            raise ValueError("Algorithm must be either 'bfs' or 'dfs'")
    
    def get_connected_component(self, node_id: str) -> List[str]:
        """
        Get all nodes in the same connected component as the given node
        
        Args:
            node_id (str): NCTId of the node
            
        Returns:
            List[str]: List of NCTIds in the same connected component
        """
        if node_id not in self.graph:
            raise ValueError(f"Node {node_id} not found in the graph")
        
        return list(nx.node_connected_component(self.graph, node_id))
    
    def visualize_graph(
        self,
        highlight_nodes: List[str] = None,
        highlight_path: List[str] = None,
        figsize: Tuple[int, int] = (12, 10)
    ) -> None:
        """
        Visualize the similarity graph with optional node/path highlighting
        
        Args:
            highlight_nodes (List[str], optional): List of node IDs to highlight
            highlight_path (List[str], optional): List of node IDs forming a path to highlight
            figsize (Tuple[int, int]): Figure size
        """
        plt.figure(figsize=figsize)
        
        # Position nodes using force-directed layout
        pos = nx.spring_layout(self.graph)
        
        # Draw all nodes and edges
        nx.draw_networkx_nodes(self.graph, pos, node_size=100, alpha=0.7)
        nx.draw_networkx_edges(self.graph, pos, alpha=0.3)
        
        # Highlight specific nodes if provided
        if highlight_nodes:
            valid_nodes = [n for n in highlight_nodes if n in self.graph]
            nx.draw_networkx_nodes(self.graph, pos, nodelist=valid_nodes, 
                                  node_color='red', node_size=200)
        
        # Highlight a path if provided
        if highlight_path and len(highlight_path) > 1:
            valid_path = [n for n in highlight_path if n in self.graph]
            if len(valid_path) > 1:
                path_edges = [(valid_path[i], valid_path[i+1]) for i in range(len(valid_path)-1)]
                nx.draw_networkx_edges(self.graph, pos, edgelist=path_edges, 
                                      edge_color='red', width=2)
        
        # Add labels for important nodes
        labels = {}
        if highlight_nodes:
            for node in highlight_nodes:
                if node in self.graph:
                    labels[node] = node
                    
        if highlight_path:
            for node in highlight_path:
                if node in self.graph:
                    labels[node] = node
                    
        nx.draw_networkx_labels(self.graph, pos, labels=labels, font_size=10)
        
        plt.title("Clinical Trials Similarity Graph")
        plt.axis('off')
        plt.tight_layout()
        plt.show()
    
    def search_and_build_graph(
        self,
        search_expr: str,
        max_studies: int = 100,
        similarity_threshold: float = 0.7,
        max_edges_per_node: int = 5
    ) -> nx.Graph:
        """
        Search for studies and build a similarity graph in one step
        
        Args:
            search_expr (str): Search expression
            max_studies (int): Maximum number of studies
            similarity_threshold (float): Minimum similarity threshold
            max_edges_per_node (int): Maximum edges per node
            
        Returns:
            nx.Graph: The constructed similarity graph
        """
        # Search for studies
        df = self.api.search_to_dataframe(search_expr, max_studies=max_studies)
        
        # Build similarity graph
        return self.build_similarity_graph(
            df, 
            similarity_threshold=similarity_threshold,
            max_edges_per_node=max_edges_per_node
        )
    
    def get_trial_details(self, nct_id: str) -> Dict:
        """
        Get detailed information about a specific trial
        
        Args:
            nct_id (str): NCTId of the trial
            
        Returns:
            Dict: Trial details
        """
        if self.df_cache is not None and nct_id in self.df_cache['NCTId'].values:
            # Get from cache
            row = self.df_cache[self.df_cache['NCTId'] == nct_id].iloc[0]
            return row.to_dict()
        else:
            # Get from API
            return self.api.get_study_fields(nct_id, ['NCTId', 'BriefTitle', 'BriefSummary'])
