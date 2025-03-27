import pennylane as qml
import numpy as np

class ZZFeatureMap:
    """
    ZZ Feature Map: Maps classical data to quantum states with entanglement.
    """
    
    def __init__(self, n_qubits=None):
        """
        Initialize the ZZ Feature Map.
        
        Args:
            n_qubits (int, optional): Number of qubits. If None, will be inferred dynamically.
        """
        self.n_qubits = n_qubits
    
    def __call__(self, x):
        """
        Apply the ZZ feature map to input features.
        
        Args:
            x (np.ndarray): Input features
        """
        # Dynamically set number of qubits if not specified
        if self.n_qubits is None:
            self.n_qubits = len(x)
        
        # First order expansion
        for i in range(self.n_qubits):
            qml.Hadamard(wires=i)
            qml.RZ(x[i % len(x)], wires=i)
        
        # Second order expansion with ZZ entanglement
        for i in range(self.n_qubits):
            for j in range(i+1, self.n_qubits):
                qml.CNOT(wires=[i, j])
                qml.RZ(np.pi * x[i % len(x)] * x[j % len(x)], wires=j)
                qml.CNOT(wires=[i, j])