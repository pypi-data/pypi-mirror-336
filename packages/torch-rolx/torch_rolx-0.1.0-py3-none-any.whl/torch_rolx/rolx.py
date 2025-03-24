import torch
import torch.nn as nn
import torch.optim as optim
import networkx as nx
import numpy as np
from torch_rolx.refex import ReFeX

class NMF(nn.Module):
    """
    PyTorch implementation of Non-negative Matrix Factorization
    """
    def __init__(self, n_components, n_features, device='cpu'):
        """
        Initialize the NMF model
        
        Parameters:
            n_components (int): Number of components to extract (number of roles)
            n_features (int): Number of input features
            device (str): Computation device ('cpu' or 'cuda')
        """
        super(NMF, self).__init__()
        
        # Initialize W matrix (node-role) and H matrix (role-feature)
        # In traditional NMF: V ≈ WH, where V is the node-feature matrix
        self.W = nn.Parameter(torch.rand(n_features, n_components, device=device) * 0.1)
        self.H = nn.Parameter(torch.rand(n_components, n_features, device=device) * 0.1)
        
        # Ensure weights are non-negative
        with torch.no_grad():
            self.W.abs_()
            self.H.abs_()
            
    def forward(self, x):
        """
        Forward pass: compute reconstruction matrix
        
        Parameters:
            x (torch.Tensor): Input feature matrix [n_samples, n_features]
            
        Returns:
            torch.Tensor: Reconstruction matrix
        """
        # V ≈ WH reconstruction
        reconstruction = torch.mm(torch.mm(x, self.W), self.H)
        return reconstruction
    
    def get_node_roles(self, x):
        """
        Compute role assignments for nodes
        
        Parameters:
            x (torch.Tensor): Input feature matrix [n_samples, n_features]
            
        Returns:
            torch.Tensor: Node role assignments [n_samples, n_components]
        """
        node_roles = torch.mm(x, self.W)
        # Ensure non-negativity
        node_roles = torch.relu(node_roles)
        # Use softmax normalization to ensure each row sums to 1
        node_roles = torch.nn.functional.softmax(node_roles, dim=1)
        return node_roles

class RolX:
    """
    PyTorch implementation of the RolX role discovery algorithm
    
    RolX uses ReFeX for feature extraction, then applies NMF to discover node roles
    """
    
    def __init__(self, n_roles=4, max_iterations=4, refex_params=None, 
                 n_epochs=1000, learning_rate=0.01, device='cpu'):
        """
        Initialize the RolX algorithm
        
        Parameters:
            n_roles (int): Number of roles to discover
            max_iterations (int): Maximum iterations for ReFeX
            refex_params (dict): Additional parameters for ReFeX
            n_epochs (int): Number of epochs for NMF training
            learning_rate (float): Learning rate
            device (str): Computation device ('cpu' or 'cuda')
        """
        self.n_roles = n_roles
        self.n_epochs = n_epochs
        self.learning_rate = learning_rate
        self.device = device
        
        # Initialize ReFeX
        if refex_params is None:
            refex_params = {}
        
        self.refex = ReFeX(max_iterations=max_iterations, 
                          device=device, 
                          **refex_params)
        
        self.model = None
        self.node_roles = None
        self.features = None
        
    def fit(self, G):
        """
        Train the RolX model
        
        Parameters:
            G (networkx.Graph): Input graph
            
        Returns:
            self
        """
        # Check if the graph is empty
        if G.number_of_nodes() == 0:
            raise ValueError("Cannot process an empty graph (no nodes)")
            
        # Check if the graph has edges
        if G.number_of_edges() == 0 and G.number_of_nodes() > 1:
            raise ValueError("The provided graph does not contain edges, cannot extract role information")
        
        # 1. Extract features using ReFeX
        try:
            self.features = self.refex.fit_transform(G)
        except Exception as e:
            raise ValueError(f"Feature extraction failed: {str(e)}")
        
        # 2. Create and train the NMF model
        n_nodes, n_features = self.features.shape
        self.model = NMF(n_components=self.n_roles, 
                         n_features=n_features,
                         device=self.device)
        
        optimizer = optim.Adam(self.model.parameters(), lr=self.learning_rate)
        criterion = nn.MSELoss()
        
        # Save final loss value for testing convergence
        self.final_loss = None
        
        # Train the model
        self.model.train()
        for epoch in range(self.n_epochs):
            optimizer.zero_grad()
            reconstruction = self.model(self.features)
            loss = criterion(reconstruction, self.features)
            
            # Add L1 regularization term to promote sparsity
            l1_lambda = 0.001
            l1_norm = sum(torch.sum(torch.abs(param)) for param in self.model.parameters())
            loss += l1_lambda * l1_norm
            
            loss.backward()
            optimizer.step()
            
            # Ensure weights are non-negative
            with torch.no_grad():
                self.model.W.data.clamp_(0)
                self.model.H.data.clamp_(0)
            
            # Save loss value from the final round
            if epoch == self.n_epochs - 1:
                self.final_loss = loss.item()
            
            if (epoch + 1) % 100 == 0:
                print(f'Epoch {epoch+1}/{self.n_epochs}, Loss: {loss.item():.4f}')
        
        # 3. Extract role assignments for each node
        with torch.no_grad():
            self.node_roles = self.model.get_node_roles(self.features)
        
        return self
    
    def transform(self, G=None):
        """
        Get role assignments for nodes
        
        Parameters:
            G (networkx.Graph, optional): If provided, recompute roles
            
        Returns:
            torch.Tensor: Node-to-role assignment matrix [n_nodes, n_roles]
        """
        if G is not None:
            self.fit(G)
            
        if self.node_roles is None:
            raise ValueError("Model not trained, call fit() method first")
            
        return self.node_roles
    
    def get_role_features(self):
        """
        Get feature vectors for each role
        
        Returns:
            torch.Tensor: Role feature matrix [n_roles, n_features]
        """
        if self.model is None:
            raise ValueError("Model not trained, call fit() method first")
            
        return self.model.H
    
    def fit_transform(self, G):
        """
        Train the model and return node role assignments
        
        Parameters:
            G (networkx.Graph): Input graph
            
        Returns:
            torch.Tensor: Node-to-role assignment matrix [n_nodes, n_roles]
        """
        return self.fit(G).transform()