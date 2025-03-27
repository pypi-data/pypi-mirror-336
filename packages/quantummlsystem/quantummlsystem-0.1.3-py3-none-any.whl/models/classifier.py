import pennylane as qml
import numpy as np
from sklearn.metrics import accuracy_score, confusion_matrix
from .core.base_model import BaseQuantumModel

class QuantumClassifier(BaseQuantumModel):
    """
    Quantum Machine Learning Classifier using Variational Quantum Circuits.
    """
    
    def __init__(self, *args, **kwargs):
        """
        Initialize the Quantum Classifier.
        """
        super().__init__(*args, **kwargs)
        self.training_history = []
    
    def _circuit(self, x, weights):
        """
        Quantum circuit for binary classification.
        
        Args:
            x: Input features
            weights: Trainable circuit parameters
        
        Returns:
            Expectation value for classification
        """
        # Apply feature map
        if self.feature_map:
            self.feature_map(x)
        
        # Apply variational ansatz
        if self.ansatz:
            self.ansatz(weights)
        
        # Measure expectation value of Z on the first qubit
        return qml.expval(qml.PauliZ(0))
    
    def _cost_function(self, weights, X, y):
        """
        Cost function for training.
        
        Args:
            weights: Circuit parameters
            X: Input features
            y: Target labels
            
        Returns:
            Binary cross-entropy loss
        """
        predictions = np.array([self.qnode(x, weights) for x in X])
        
        # Convert from [-1,1] to [0,1] for binary classification
        predictions = (predictions + 1) / 2
        
        # Binary cross-entropy loss
        epsilon = 1e-12  # To avoid log(0)
        predictions = np.clip(predictions, epsilon, 1 - epsilon)
        loss = -np.mean(y * np.log(predictions) + (1 - y) * np.log(1 - predictions))
        return loss
    
    def fit(self, X, y, batch_size=32, epochs=100, optimizer='adam', learning_rate=0.01, verbose=1):
        """
        Train the quantum machine learning model.
        
        Args:
            X: Training features
            y: Training labels
            batch_size: Batch size for training
            epochs: Number of training epochs
            optimizer: Optimization algorithm
            learning_rate: Learning rate for the optimizer
            verbose: Verbosity level
            
        Returns:
            Training history
        """
        # Scale the input features
        X_scaled = self.scaler.fit_transform(X)
        
        # Initialize weights for the ansatz
        self.weights = self.ansatz.initialize_weights()
        
        # Set up the optimizer
        if optimizer == 'adam':
            opt = qml.AdamOptimizer(stepsize=learning_rate)
        else:
            opt = qml.GradientDescentOptimizer(stepsize=learning_rate)
        
        # Training loop
        self.training_history = []
        for epoch in range(epochs):
            # Shuffle data
            permutation = np.random.permutation(len(X_scaled))
            X_shuffled = X_scaled[permutation]
            y_shuffled = y[permutation]
            
            epoch_loss = 0
            num_batches = int(np.ceil(len(X_scaled) / batch_size))
            
            for i in range(num_batches):
                batch_indices = slice(i * batch_size, min((i + 1) * batch_size, len(X_scaled)))
                X_batch = X_shuffled[batch_indices]
                y_batch = y_shuffled[batch_indices]
                
                # Cost function for the current batch
                def cost_fn(weights):
                    return self._cost_function(weights, X_batch, y_batch)
                
                # Update weights
                self.weights = opt.step(cost_fn, self.weights)
                
                batch_loss = cost_fn(self.weights)
                epoch_loss += batch_loss
            
            # Average epoch loss
            epoch_loss /= num_batches
            self.training_history.append(epoch_loss)
            
            # Verbose output
            if verbose and (epoch % 10 == 0 or epoch == epochs - 1):
                print(f"Epoch {epoch+1}/{epochs} - Loss: {epoch_loss:.4f}")
        
        self.trained = True
        return self.training_history
    
    def predict(self, X, return_proba=False):
        """
        Make predictions using the trained quantum model.
        
        Args:
            X: Input features
            return_proba: Whether to return probabilities
            
        Returns:
            Predictions or probabilities
        """
        if not self.trained:
            raise ValueError("Model has not been trained yet")
        
        # Scale the input features
        X_scaled = self.scaler.transform(X)
        
        # Make predictions
        predictions = np.array([self.qnode(x, self.weights) for x in X_scaled])
        
        # Convert from [-1,1] to [0,1] for binary classification probabilities
        probabilities = (predictions + 1) / 2
        
        if return_proba:
            return probabilities
        else:
            return (probabilities > 0.5).astype(int)
    
    def evaluate(self, X, y):
        """
        Evaluate the model on test data.
        
        Args:
            X: Test features
            y: Test labels
            
        Returns:
            Dictionary of evaluation metrics
        """
        # Make predictions
        y_pred = self.predict(X)
        y_proba = self.predict(X, return_proba=True)
        
        # Calculate metrics
        acc = accuracy_score(y, y_pred)
        conf_matrix = confusion_matrix(y, y_pred)
        
        return {
            "accuracy": acc,
            "confusion_matrix": conf_matrix,
            "predictions": y_pred,
            "probabilities": y_proba
        }