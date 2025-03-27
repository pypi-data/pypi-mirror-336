import pennylane as qml
import numpy as np

class StronglyEntanglingAnsatz:
    """
    Strongly Entangling Layers Ansatz for Variational Quantum Circuits.
    """
    
    def __init__(self, n_layers=2, n_qubits=None):
        """
        Initialize the Strongly Entangling Ansatz.
        
        Args:
            n_layers (int): Number of layers in the variational circuit
            n_qubits (int, optional): Number of qubits. If None, will be inferred dynamically.
        """
        self.n_layers = n_layers
        self.n_qubits = n_qubits
    
    def initialize_weights(self):
        """
        Initialize random weights for the ansatz.
        
        Returns:
            np.ndarray: Random weights for the circuit
        """
        # Dynamically set number of qubits if not specified
        if self.n_qubits is None:
            raise ValueError("Number of qubits must be specified")
        
        # Three rotation parameters per qubit per layer
        return np.random.uniform(0, 2*np.pi, size=(self.n_layers, self.n_qubits, 3))
    
    def __call__(self, weights):
        """
        Apply the Strongly Entangling Ansatz.
        
        Args:
            weights (np.ndarray): Trainable circuit parameters
        """
        qml.StronglyEntanglingLayers(weights, wires=range(self.n_qubits))