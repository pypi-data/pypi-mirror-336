from tensorflow import keras
from tensorflow.keras import layers

class AttentionLayer(layers.Layer):
    def __init__(self, **kwargs):
        super(AttentionLayer, self).__init__(**kwargs)

    def call(self, inputs):
        encoder_outputs, decoder_outputs = inputs
        decoder_state = decoder_outputs[:, -1, :]
        decoder_state_expanded = keras.backend.expand_dims(decoder_state, 1)
        score = keras.backend.sum(encoder_outputs * decoder_state_expanded, axis=2, keepdims=True)
        attention_weights = keras.backend.softmax(score, axis=1)
        context_vector = keras.backend.sum(encoder_outputs * attention_weights, axis=1)
        return context_vector

def create_tacotron2_model(vocab_size, embedding_dim, lstm_units, max_decoder_length):
    input_text = layers.Input(shape=(None,), name='input_text')
    embedded_text = layers.Embedding(vocab_size, embedding_dim)(input_text)

    encoder_lstm = layers.LSTM(lstm_units, return_sequences=True, return_state=True, name='encoder_lstm')
    encoder_outputs, state_h, state_c = encoder_lstm(embedded_text)

    decoder_inputs = layers.Input(shape=(None, 80), name='decoder_inputs')
    decoder_lstm = layers.LSTM(lstm_units, return_sequences=True, return_state=True, name='decoder_lstm')
    decoder_outputs, _, _ = decoder_lstm(decoder_inputs, initial_state=[state_h, state_c])

    context_vector = AttentionLayer()([encoder_outputs, decoder_outputs])
    context_vector = layers.Dense(lstm_units, activation="tanh")(context_vector)
    context_vector = layers.RepeatVector(max_decoder_length)(context_vector)

    decoder_concat = layers.Concatenate(axis=-1)([decoder_outputs, context_vector])
    output = layers.Dense(80, activation='linear', name='output_audio')(decoder_concat)

    model = keras.Model(inputs=[input_text, decoder_inputs], outputs=output)
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model