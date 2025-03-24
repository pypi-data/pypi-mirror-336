import torch
import networkx as nx
import numpy as np
import scipy.sparse as sp
import warnings

class ReFeX:
    """
    PyTorch implementation of Recursive Feature eXtraction (ReFeX)
    
    ReFeX generates structural feature descriptions of nodes by recursively aggregating
    features from neighboring nodes.
    """
    
    def __init__(self, max_iterations=4, aggregations=None, device='cpu'):
        """
        Initialize the ReFeX algorithm
        
        Parameters:
            max_iterations (int): Maximum number of recursive aggregation iterations
            aggregations (list): List of functions for feature aggregation (default: sum, mean, max)
            device (str): Computation device ('cpu' or 'cuda')
        """
        self.max_iterations = max_iterations
        self.device = device
        
        if aggregations is None:
            self.aggregations = [torch.sum, torch.mean, torch.max]
        else:
            self.aggregations = aggregations
        
    def extract_local_features(self, G):
        """
        Extract local features of nodes
        
        Parameters:
            G (networkx.Graph): Input graph
            
        Returns:
            torch.Tensor: Local feature matrix of nodes
        """
        n = G.number_of_nodes()
        
        # Raise an exception if the graph is empty
        if n == 0:
            raise ValueError("Cannot process an empty graph (no nodes)")
        
        # Extract basic features: degree, clustering coefficient, two-hop neighbor count
        degrees = torch.tensor([G.degree(i) for i in range(n)], dtype=torch.float32)
        clustering = torch.tensor([nx.clustering(G, i) for i in range(n)], dtype=torch.float32)
        
        # Two-hop neighbor count (excluding direct neighbors)
        two_hop_counts = []
        for i in range(n):
            neighbors = set(G.neighbors(i))
            two_hop = set()
            for neighbor in neighbors:
                two_hop.update(G.neighbors(neighbor))
            # Remove the node itself and direct neighbors
            two_hop.discard(i)
            two_hop -= neighbors
            two_hop_counts.append(len(two_hop))
        
        two_hop_counts = torch.tensor(two_hop_counts, dtype=torch.float32)
        
        # Combine local features into a feature matrix
        features = torch.stack([degrees, clustering, two_hop_counts], dim=1)
        return features.to(self.device)
    
    def recursive_feature_extraction(self, G, initial_features):
        """
        Recursive feature extraction process
        
        Parameters:
            G (networkx.Graph): Input graph
            initial_features (torch.Tensor): Initial node features
            
        Returns:
            torch.Tensor: Enhanced node feature matrix
        """
        # Check if the graph is empty or only has isolated nodes
        if G.number_of_edges() == 0:
            # If there are no edges, return only the initial features without recursive feature extraction
            return initial_features
        
        # Convert adjacency matrix to SciPy sparse matrix, ensuring CSR format
        adj = nx.to_scipy_sparse_array(G, format='csr')
        
        # Normalize adjacency matrix A'
        rowsum = np.array(adj.sum(1)).flatten()
        
        # Prevent division by zero: set rowsum to 1 for zero-degree nodes (these nodes won't pass features)
        rowsum[rowsum == 0] = 1.0
        
        d_inv_sqrt = np.power(rowsum, -0.5)
        d_mat_inv_sqrt = sp.diags(d_inv_sqrt)
        normalized_adj = adj.dot(d_mat_inv_sqrt).transpose().dot(d_mat_inv_sqrt)
        
        # Convert to COO format to access row and col attributes
        normalized_adj_coo = normalized_adj.tocoo()
        
        # Convert to PyTorch sparse tensor
        indices = torch.from_numpy(
            np.vstack((normalized_adj_coo.row, normalized_adj_coo.col)).astype(np.int64))
        values = torch.from_numpy(normalized_adj_coo.data.astype(np.float32))
        shape = torch.Size(normalized_adj_coo.shape)
        
        normalized_adj_torch = torch.sparse_coo_tensor(indices, values, shape, dtype=torch.float32, device=self.device)
        
        # Start recursive feature extraction
        all_features = [initial_features]
        current_features = initial_features
        
        for _ in range(self.max_iterations):
            # Aggregate neighboring features for each node
            neighbor_features = torch.sparse.mm(normalized_adj_torch, current_features)
            
            # Apply different aggregation functions
            aggregated_features = []
            
            for agg_func in self.aggregations:
                if agg_func == torch.max:
                    # torch.max returns (values, indices), we only need values
                    agg_features = agg_func(neighbor_features, dim=0)[0]
                    # Expand to match the shape of neighbor_features
                    agg_features = agg_features.expand_as(neighbor_features)
                else:
                    agg_features = agg_func(neighbor_features, dim=0)
                    # Expand to match the shape of neighbor_features
                    agg_features = agg_features.expand_as(neighbor_features)
                    
                aggregated_features.append(agg_features)
            
            # Add new features
            aggregated_tensor = torch.cat(aggregated_features, dim=1)
            all_features.append(aggregated_tensor)
            current_features = aggregated_tensor
        
        # Combine features from all iterations
        combined_features = torch.cat(all_features, dim=1)
        
        return combined_features
    
    def fit_transform(self, G):
        """
        Apply the ReFeX algorithm to extract node features
        
        Parameters:
            G (networkx.Graph): Input graph
            
        Returns:
            torch.Tensor: Final node feature matrix
        """
        # Check if the graph is empty
        if G.number_of_nodes() == 0:
            raise ValueError("Cannot process an empty graph (no nodes)")
            
        # 1. Extract local features
        local_features = self.extract_local_features(G)
        
        # 2. Recursively aggregate features
        combined_features = self.recursive_feature_extraction(G, local_features)
        
        # 3. Feature normalization
        mean = combined_features.mean(dim=0, keepdim=True)
        
        # Use std with epsilon to avoid division by zero
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            std = combined_features.std(dim=0, keepdim=True)
        
        # Avoid division by zero: replace zero standard deviation with 1
        std[std < 1e-6] = 1.0
        
        normalized_features = (combined_features - mean) / std
        
        return normalized_features
