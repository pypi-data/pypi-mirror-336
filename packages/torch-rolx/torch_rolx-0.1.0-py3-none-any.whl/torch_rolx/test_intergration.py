import unittest
import torch
import networkx as nx
import matplotlib.pyplot as plt
from torch_rolx.refex import ReFeX
from torch_rolx.rolx import RolX

class TestIntegration(unittest.TestCase):
    
    def setUp(self):
        # 创建空手道俱乐部图
        self.G = nx.karate_club_graph()
        
        # 设置设备
        self.device = torch.device('cpu')
        
    def test_end_to_end(self):
        """测试完整的端到端流程"""
        # 1. 通过ReFeX提取特征
        refex = ReFeX(max_iterations=2, device=self.device)
        features = refex.fit_transform(self.G)
        
        # 验证特征形状
        self.assertEqual(features.shape[0], self.G.number_of_nodes())
        
        # 2. 使用RolX发现角色
        rolx = RolX(n_roles=4, max_iterations=2, n_epochs=50, device=self.device)
        node_roles = rolx.fit_transform(self.G)
        
        # 验证角色分配形状
        self.assertEqual(node_roles.shape, (self.G.number_of_nodes(), 4))
        
        # 验证角色分配是非负的
        self.assertTrue(torch.all(node_roles >= 0))
        
        # 验证每个节点的角色分配和为1
        row_sums = node_roles.sum(dim=1)
        self.assertTrue(torch.allclose(row_sums, torch.ones_like(row_sums), atol=1e-6))
        
        # 3. 确保为每个节点分配了主要角色
        primary_roles = torch.argmax(node_roles, dim=1).cpu().numpy()
        unique_roles = set(primary_roles)
        
        # 验证至少使用了2个不同的角色
        self.assertGreaterEqual(len(unique_roles), 2)

if __name__ == '__main__':
    unittest.main()
    