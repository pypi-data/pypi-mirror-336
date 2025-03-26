import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, LSTM, Embedding, Layer, Concatenate, RepeatVector

class AttentionLayer(Layer):
    def __init__(self, **kwargs):
        super(AttentionLayer, self).__init__(**kwargs)
        # This dense layer is not used in this simple dot-product attention.
        # Remove it or keep it for more complex attention.

    def call(self, inputs):
        encoder_outputs, decoder_outputs = inputs
        # Use the last decoder output as the query vector.
        # decoder_outputs shape: (batch, dec_time, lstm_units)
        decoder_state = decoder_outputs[:, -1, :]  # shape: (batch, lstm_units)
        # Expand dims so that we can perform element-wise multiplication.
        # decoder_state_expanded shape: (batch, 1, lstm_units)
        decoder_state_expanded = tf.expand_dims(decoder_state, 1)
        # Compute dot-product similarity between each encoder time step and the decoder state.
        # This yields a score for each encoder time step.
        # score shape: (batch, enc_time, 1)
        score = tf.reduce_sum(encoder_outputs * decoder_state_expanded, axis=2, keepdims=True)
        # Compute attention weights with softmax over the encoder time axis.
        attention_weights = tf.nn.softmax(score, axis=1)
        # Multiply encoder outputs by the attention weights and sum over time to get a context vector.
        # context_vector shape: (batch, lstm_units)
        context_vector = tf.reduce_sum(encoder_outputs * attention_weights, axis=1)
        return context_vector

def create_tacotron2_model(vocab_size, embedding_dim, lstm_units, max_decoder_length):
    # Input for text
    input_text = Input(shape=(None,), name='input_text')
    embedded_text = Embedding(vocab_size, embedding_dim)(input_text)

    # Encoder: returns outputs for all time steps and the final state.
    encoder_lstm = LSTM(lstm_units, return_sequences=True, return_state=True, name='encoder_lstm')
    encoder_outputs, state_h, state_c = encoder_lstm(embedded_text)

    # Decoder: takes audio features as input.
    decoder_inputs = Input(shape=(None, 80), name='decoder_inputs')
    decoder_lstm = LSTM(lstm_units, return_sequences=True, return_state=True, name='decoder_lstm')
    decoder_outputs, _, _ = decoder_lstm(decoder_inputs, initial_state=[state_h, state_c])

    # Attention mechanism: compute context vector from encoder outputs using the last decoder state.
    context_vector = AttentionLayer()([encoder_outputs, decoder_outputs])
    # Now context_vector has shape: (batch, lstm_units)

    # (Optional) Further process the context vector via a Dense layer.
    context_vector = Dense(lstm_units, activation="tanh")(context_vector)

    # Repeat the context vector to match the decoder sequence length.
    # Now RepeatVector expects a 2D input (batch, feature) and outputs (batch, max_decoder_length, feature)
    context_vector = RepeatVector(max_decoder_length)(context_vector)

    # Concatenate repeated context vector with the decoder outputs.
    decoder_concat = Concatenate(axis=-1)([decoder_outputs, context_vector])

    # Final output layer for audio features.
    output = Dense(80, activation='linear', name='output_audio')(decoder_concat)

    model = Model(inputs=[input_text, decoder_inputs], outputs=output)
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model
