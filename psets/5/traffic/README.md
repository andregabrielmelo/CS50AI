# Traffica model

Firstly, I implemented the functions load_data() ahd get_model() until it compiled

## Experimentation

I began with 1 convolution layer, 1 max-pooling layer, 1 flatten layer, 1 dense layer with 8 units, and 1 dense layer with all the categories (outputs), but the accurracy did not go above 0.0556. So, began doubling the number of units with one layer. So I began to double the number of units in the layer between the flatten and the final dense layer

The final categorical_accuracy in each test:
8 --> 333/333 - 1s - 3ms/step - categorical_accuracy: 0.0550 - loss: 3.4956
16 --> 333/333 - 1s - 4ms/step - categorical_accuracy: 0.0553 - loss: 3.4967
32 --> 333/333 - 1s - 4ms/step - categorical_accuracy: 0.0570 - loss: 3.4927
64 --> 333/333 - 2s - 7ms/step - categorical_accuracy: 0.6962 - loss: 0.9268
128 --> 333/333 - 2s - 5ms/step - categorical_accuracy: 0.9248 - loss: 0.5900

Well, that is not doing much, just showing that more units more acurracy I guess. But, why so?

Lets trying putting more Dense layers.

keras.layers.Dense(64, activation="relu"),
keras.layers.Dense(128, activation="relu"),
keras.layers.Dense(256, activation="relu"),

333/333 - 1s - 4ms/step - categorical_accuracy: 0.8587 - loss: 0.5894

It has a worse result than before. Well, let see if something changes by adding dropouts to prevent overfitting

keras.layers.Dense(64, activation="relu"),
keras.layers.Dropout(0.3),
keras.layers.Dense(128, activation="relu"),
keras.layers.Dropout(0.2),
keras.layers.Dense(256, activation="relu"),

333/333 - 1s - 3ms/step - categorical_accuracy: 0.0534 - loss: 3.5076

It is getting worse? Maybe this cannot be deep, just wide.

keras.layers.Dense(256, activation="relu"),
keras.layers.Dropout(0.3),

333/333 - 2s - 5ms/step - categorical_accuracy: 0.8970 - loss: 0.4171

Wide with dropout looks like the answer. There is not much disparity between training and evaluation acurracy, 
so there I do not think there is a underfitting or overfitting going on

Epoch 9/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 5s 9ms/step - categorical_accuracy: 0.8088 - loss: 0.6166  
Epoch 10/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 6s 12ms/step - categorical_accuracy: 0.8306 - loss: 0.5647 
333/333 - 2s - 5ms/step - categorical_accuracy: 0.8970 - loss: 0.4171
