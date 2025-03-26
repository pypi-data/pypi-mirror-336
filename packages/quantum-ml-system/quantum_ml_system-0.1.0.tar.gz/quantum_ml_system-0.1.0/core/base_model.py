import pennylane as qml
import numpy as np
from sklearn.preprocessing import StandardScaler
from abc import ABC, abstractmethod

class BaseQuantumModel(ABC):
    """
    Abstract base class for quantum machine learning models.
    
    Provides a standard interface for quantum ML models with 
    core functionality and abstract methods for implementation.
    """
    
    def __init__(self, 
                 n_qubits, 
                 feature_map=None, 
                 ansatz=None, 
                 device='default.qubit', 
                 shots=None):
        """
        Initialize the base quantum model.
        
        Args:
            n_qubits (int): Number of qubits to use
            feature_map (FeatureMap, optional): Quantum feature map
            ansatz (Ansatz, optional): Variational circuit ansatz
            device (str): Quantum device to use
            shots (int): Number of shots for simulation
        """
        self.n_qubits = n_qubits
        self.feature_map = feature_map
        self.ansatz = ansatz
        self.device = qml.device(device, wires=n_qubits, shots=shots)
        
        self.scaler = StandardScaler()
        self.weights = None
        self.trained = False
        
        # Create quantum node with numpy interface
        self.qnode = qml.QNode(self._circuit, self.device, interface="numpy")
    
    @abstractmethod
    def _circuit(self, x, weights):
        """
        Abstract method for defining the quantum circuit.
        
        Must be implemented by subclasses.
        
        Args:
            x: Input features
            weights: Trainable circuit parameters
        
        Returns:
            Quantum circuit output
        """
        pass
    
    @abstractmethod
    def fit(self, X, y, **kwargs):
        """
        Abstract method for training the model.
        
        Must be implemented by subclasses.
        
        Args:
            X: Training features
            y: Training labels
        """
        pass
    
    @abstractmethod
    def predict(self, X, **kwargs):
        """
        Abstract method for making predictions.
        
        Must be implemented by subclasses.
        
        Args:
            X: Input features
        """
        pass
    
    def preprocess(self, X):
        """
        Preprocess input features using StandardScaler.
        
        Args:
            X: Input features
        
        Returns:
            Scaled features
        """
        return self.scaler.transform(X)
    
    def save_model(self, filename):
        """
        Save the model parameters to a file.
        
        Args:
            filename: Path to save the model
        """
        if not self.trained:
            raise ValueError("Model has not been trained yet")
        
        model_data = {
            'weights': self.weights,
            'scaler_mean': self.scaler.mean_,
            'scaler_scale': self.scaler.scale_,
            'n_qubits': self.n_qubits
        }
        
        np.save(filename, model_data)
    
    @classmethod
    def load_model(cls, filename, **kwargs):
        """
        Load a saved model.
        
        Args:
            filename: Path to the saved model
        
        Returns:
            Loaded model
        """
        model_data = np.load(filename, allow_pickle=True).item()
        
        # Create a new model with the saved parameters
        model = cls(n_qubits=model_data['n_qubits'], **kwargs)
        
        # Restore the weights
        model.weights = model_data['weights']
        
        # Restore the scaler
        model.scaler.mean_ = model_data['scaler_mean']
        model.scaler.scale_ = model_data['scaler_scale']
        
        model.trained = True
        
        return model