# src/models/autoencoder.py
import tensorflow as tf
from tensorflow.keras import layers, Model

class StudentAutoencoder:
    def __init__(self, input_dim, encoding_dim=32):
        self.input_dim = input_dim
        self.encoding_dim = encoding_dim
        self.autoencoder = self._build_autoencoder()
        self.encoder = self._build_encoder()
        
    def _build_autoencoder(self):
        # Encoder
        input_layer = layers.Input(shape=(self.input_dim,))
        encoded = layers.Dense(64, activation='relu')(input_layer)
        encoded = layers.Dense(self.encoding_dim, activation='relu')(encoded)
        
        # Decoder
        decoded = layers.Dense(64, activation='relu')(encoded)
        decoded = layers.Dense(self.input_dim, activation='sigmoid')(decoded)
        
        # Full autoencoder
        autoencoder = Model(input_layer, decoded)
        autoencoder.compile(optimizer='adam', loss='mse')
        
        return autoencoder
    
    def _build_encoder(self):
        # Separate encoder model
        encoder_input = self.autoencoder.input
        encoder_output = self.autoencoder.layers[2].output
        encoder = Model(encoder_input, encoder_output)
        
        return encoder
    
    def train(self, X, epochs=50, batch_size=32, validation_split=0.2):
        """Train the autoencoder"""
        history = self.autoencoder.fit(
            X, X,
            epochs=epochs,
            batch_size=batch_size,
            validation_split=validation_split,
            verbose=1
        )
        return history
    
    def encode(self, X):
        """Encode the input data to the latent space"""
        return self.encoder.predict(X)