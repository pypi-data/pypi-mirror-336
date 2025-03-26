# Example of Using Layers in `kdl_pre_built`

## Introduction

The following example demonstrates how to use different layers from the `kdl_pre_built` library with `Keras`. The model utilizes `GMPLPBlock` and `PolynomialDense` layers to showcase their capabilities.

---

## Installation

First, install the required libraries if you haven't already:

```bash
pip install tensorflow keras kdl_pre_built
```

---

## Loading the MNIST Dataset

The MNIST dataset consists of handwritten digits from 0 to 9. We will load the data using `keras.datasets`:

```python
import keras
(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()
```

---

## Example Model Using `kdl_pre_built` Layers

This example model includes the following components:
- **Rescaling**: Normalizes image data to the [0, 1] range.
- **GMPLPBlock**: An advanced neural network layer from `kdl_pre_built`.
- **Flatten**: Flattens the input before passing it to dense layers.
- **Dropout**: Helps prevent overfitting.
- **PolynomialDense**: A dense layer with nonlinear processing capabilities.
- **Dense (Softmax)**: The output layer with 10 units corresponding to the 10 MNIST digits.

### Model Creation Function

```python
import kdl_pre_built as kdl
import keras

def create_model(input_shape, num_blocks, output_shape):
    inputs = keras.layers.Input(shape=input_shape)
    x = keras.layers.Rescaling(scale=1./255)(inputs)
    
    for _ in range(num_blocks):
        x = kdl.layers.gmplp.GMPLPBlock(
            units=64,
            activation="gelu",
            drop_rate=0.1,
            extra_args={"kernel_initializer": "random_normal"}
        )(x)
    
    x = keras.layers.Flatten()(x)
    x = keras.layers.Dropout(0.5)(x)
    x = kdl.layers.gmplp.PolynomialDense(units=64, activation="gelu", degree=2)(x)
    outputs = keras.layers.Dense(units=output_shape, activation="softmax")(x)
    
    return keras.models.Model(inputs=inputs, outputs=outputs)
```

---

## Training the Example Model

We initialize the model with an input size of 28x28 (MNIST images) and use 2 `GMPLPBlock` layers. Then, we compile the model and start training:

```python
model = create_model(input_shape=(28, 28), num_blocks=2, output_shape=10)
model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=1e-4),
    loss=keras.losses.SparseCategoricalCrossentropy(),
    metrics=["accuracy"]
)

history = model.fit(
    x=x_train, y=y_train,
    batch_size=32,
    epochs=10,
    validation_data=(x_test, y_test)
)
```

---

## Evaluation

After training, evaluate the model on the test set:

```python
loss, accuracy = model.evaluate(x_test, y_test)
print(f"Test Accuracy: {accuracy * 100:.2f}%")
```

To visualize the training process:

```python
import matplotlib.pyplot as plt

plt.plot(history.history['accuracy'], label='Train Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()
plt.show()
```

---

## Conclusion

- This example demonstrates how to use `GMPLPBlock` and `PolynomialDense` from `kdl_pre_built`.
- This is an example of two layers in `kdl_pre_built`. You can explore other layers and experiment with different parameters to achieve better results.

Happy coding! 🚀
