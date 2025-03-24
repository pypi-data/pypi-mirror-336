# torch-rolx - PyTorch Implementation of RolX Algorithm

A PyTorch implementation of the RolX (Role eXtraction) algorithm for role discovery in graphs. This package provides efficient, GPU-accelerated tools for extracting structural roles from network data using feature-based approaches.

## Overview

RolX is an unsupervised learning approach that discovers roles in networks based on recursive feature extraction and non-negative matrix factorization. This implementation provides:

- **ReFeX**: Recursive Feature Extraction to generate node features based on local and neighborhood properties
- **RolX**: Role extraction using Non-negative Matrix Factorization (NMF) on the extracted features
- **GPU Acceleration**: Leverages PyTorch for efficient computation on both CPU and GPU

## Installation

```bash
pip install torch-rolx
```

## Requirements

- Python 3.6+
- PyTorch
- NetworkX
- NumPy

## Usage

### Basic Example

```python
import networkx as nx
from torch_rolx.rolx import RolX

# Create a sample graph
G = nx.karate_club_graph()

# Initialize RolX with 4 roles
rolx = RolX(n_roles=4, device='cpu')  # Use 'cuda' for GPU acceleration

# Extract roles
role_assignments = rolx.fit_transform(G)

# Print role assignments for the first 5 nodes
print(role_assignments[:5])

# Get role features
role_features = rolx.get_role_features()
print(role_features)
```

### Advanced Configuration

```python
from torch_rolx.rolx import RolX

# Create RolX with custom parameters
rolx = RolX(
    n_roles=5,                 # Number of roles to extract
    max_iterations=3,          # Maximum iterations for feature extraction
    n_epochs=2000,             # Training epochs for NMF
    learning_rate=0.005,       # Learning rate for optimizer
    device='cuda'              # Use GPU if available
)

# The rest of your code...
```

## API Overview

### RolX Class

The main class for role extraction.

```python
rolx = RolX(
    n_roles=4,             # Number of roles to discover
    max_iterations=4,      # Maximum iterations for ReFeX
    refex_params=None,     # Additional parameters for ReFeX
    n_epochs=1000,         # Number of epochs for NMF training
    learning_rate=0.01,    # Learning rate
    device='cpu'           # Computation device ('cpu' or 'cuda')
)
```

#### Methods:

- `fit(G)`: Train the RolX model on graph G
- `transform()`: Get role assignments for nodes
- `fit_transform(G)`: Train the model and return node role assignments
- `get_role_features()`: Get feature vectors for each role

### ReFeX Class

Extracts recursive features from graphs.

```python
refex = ReFeX(
    max_iterations=2,      # Maximum number of recursive iterations
    normalize=True,        # Whether to normalize features
    device='cpu'           # Computation device
)
```

## References

- Henderson, K., Gallagher, B., Eliassi-Rad, T., Tong, H., Basu, S., Akoglu, L., Koutra, D., Faloutsos, C., & Li, L. (2012). RolX: Structural Role Extraction & Mining in Large Graphs. Proceedings of the 18th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining.

- Henderson, K., Gallagher, B., Li, L., Akoglu, L., Eliassi-Rad, T., Tong, H., & Faloutsos, C. (2011). It's Who You Know: Graph Mining Using Recursive Structural Features. Proceedings of the 17th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining.
