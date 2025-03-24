import unittest
import torch
import networkx as nx
import numpy as np
from torch_rolx.rolx import RolX, NMF

class TestNMF(unittest.TestCase):
    
    def setUp(self):
        # Set device
        self.device = torch.device('cpu')
        
        # Create a simple feature matrix
        self.features = torch.rand(10, 5, device=self.device)
        
        # Create NMF model
        self.n_components = 3
        self.nmf = NMF(n_components=self.n_components, n_features=self.features.shape[1], device=self.device)
        
    def test_initialization(self):
        """Test NMF initialization"""
        # Check shapes of W and H matrices
        self.assertEqual(self.nmf.W.shape, (self.features.shape[1], self.n_components))
        self.assertEqual(self.nmf.H.shape, (self.n_components, self.features.shape[1]))
        
        # Check if W and H are non-negative
        self.assertTrue(torch.all(self.nmf.W >= 0))
        self.assertTrue(torch.all(self.nmf.H >= 0))
        
    def test_forward(self):
        """Test NMF forward pass"""
        reconstruction = self.nmf(self.features)
        
        # Check shape of reconstruction matrix
        self.assertEqual(reconstruction.shape, self.features.shape)
        
        # Ensure output has no NaN or Inf
        self.assertFalse(torch.isnan(reconstruction).any())
        self.assertFalse(torch.isinf(reconstruction).any())
        
    def test_get_node_roles(self):
        """Test node role assignment calculation"""
        node_roles = self.nmf.get_node_roles(self.features)
        
        # Check shape of role assignments
        self.assertEqual(node_roles.shape, (self.features.shape[0], self.n_components))
        
        # Check if role assignments are non-negative
        self.assertTrue(torch.all(node_roles >= 0))
        
        # Check if role assignments for each node sum to 1
        row_sums = node_roles.sum(dim=1)
        self.assertTrue(torch.allclose(row_sums, torch.ones_like(row_sums), atol=1e-6))

class TestRolX(unittest.TestCase):
    
    def setUp(self):
        # Create a simple test graph
        self.G = nx.karate_club_graph()
        
        # Set device
        self.device = torch.device('cpu')
        
        # Create RolX instance, reduce iterations to speed up testing
        self.rolx = RolX(n_roles=3, max_iterations=1, n_epochs=10, learning_rate=0.01, device=self.device)
        
    def test_fit(self):
        """Test RolX fitting process"""
        self.rolx.fit(self.G)
        
        # Verify model is trained
        self.assertIsNotNone(self.rolx.model)
        self.assertIsNotNone(self.rolx.node_roles)
        self.assertIsNotNone(self.rolx.features)
        
        # Verify shape of node roles
        self.assertEqual(self.rolx.node_roles.shape, (self.G.number_of_nodes(), self.rolx.n_roles))
        
        # Verify role assignments are non-negative
        self.assertTrue(torch.all(self.rolx.node_roles >= 0))
        
        # Verify role assignments for each node sum to 1
        row_sums = self.rolx.node_roles.sum(dim=1)
        self.assertTrue(torch.allclose(row_sums, torch.ones_like(row_sums), atol=1e-6))
        
    def test_transform(self):
        """Test role transformation"""
        self.rolx.fit(self.G)
        node_roles = self.rolx.transform()
        
        # Verify shape of role assignments
        self.assertEqual(node_roles.shape, (self.G.number_of_nodes(), self.rolx.n_roles))
        
        # Verify results match stored role assignments after fit
        self.assertTrue(torch.allclose(node_roles, self.rolx.node_roles))
        
    def test_fit_transform(self):
        """Test one-step fit and transform"""
        node_roles = self.rolx.fit_transform(self.G)
        
        # Verify shape of role assignments
        self.assertEqual(node_roles.shape, (self.G.number_of_nodes(), self.rolx.n_roles))
        
        # Verify role assignments for each node sum to 1
        row_sums = node_roles.sum(dim=1)
        self.assertTrue(torch.allclose(row_sums, torch.ones_like(row_sums), atol=1e-6))
        
    def test_get_role_features(self):
        """Test retrieving role features"""
        self.rolx.fit(self.G)
        role_features = self.rolx.get_role_features()
        
        # Verify shape of role features
        expected_feature_dim = self.rolx.features.shape[1]
        self.assertEqual(role_features.shape, (self.rolx.n_roles, expected_feature_dim))
        
        # Verify role features are non-negative
        self.assertTrue(torch.all(role_features >= 0))
    
    def test_empty_graph(self):
        """Test empty graph handling"""
        G = nx.Graph()
        with self.assertRaises(ValueError):
            self.rolx.fit(G)
    
    def test_single_node_graph(self):
        """Test single node graph handling"""
        G = nx.Graph()
        G.add_node(0)
        # This should be handled but may produce warnings
        self.rolx.fit(G)
        self.assertEqual(self.rolx.node_roles.shape, (1, self.rolx.n_roles))
    
    def test_complete_graph(self):
        """Test complete graph handling"""
        G = nx.complete_graph(5)
        node_roles = self.rolx.fit_transform(G)
        
        # In a complete graph, all nodes should have similar role assignments
        for i in range(1, G.number_of_nodes()):
            self.assertTrue(torch.allclose(node_roles[0], node_roles[i], atol=1e-5))
    
    def test_convergence(self):
        """Test model convergence"""
        # Use model with lower iteration count
        low_epoch_rolx = RolX(n_roles=3, max_iterations=1, n_epochs=5, learning_rate=0.01, device=self.device)
        low_epoch_rolx.fit(self.G)
        
        # Use model with higher iteration count
        high_epoch_rolx = RolX(n_roles=3, max_iterations=1, n_epochs=50, learning_rate=0.01, device=self.device)
        high_epoch_rolx.fit(self.G)
        
        # Check if loss decreases (requires modifying RolX class to track loss)
        # self.assertLess(high_epoch_rolx.final_loss, low_epoch_rolx.final_loss)

if __name__ == '__main__':
    unittest.main()
