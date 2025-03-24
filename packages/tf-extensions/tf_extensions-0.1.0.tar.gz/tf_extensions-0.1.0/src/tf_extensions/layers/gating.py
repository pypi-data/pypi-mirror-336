"""The module contains Gating signal layer for attention mechanism."""
from dataclasses import dataclass

import tensorflow as tf

from tf_extensions.auxiliary.base_config import BaseConfig
from tf_extensions.layers.base_layer import BaseLayer


@dataclass
class GatingSignalConfig(BaseConfig):
    """
    Config for Gating signal layer.

    Parameters
    ----------
    filters : int
        Number of filters for the convolutional layer.
    with_bn : bool, optional, default: True
        Whether to apply batch normalization after the convolution.
    activation : str, optional, default: 'relu'
        Activation function applied at the end of the layer.

    """

    filters: int
    with_bn: bool = True
    activation: str = 'relu'


class GatingSignal(BaseLayer):
    """
    Gating signal layer for attention mechanism.

    This layer processes the gating signal,
    which helps in controlling attention mechanisms
    by applying a 1x1 convolution,
    optional batch normalization, and activation.

    Attributes
    ----------
    config: GatingSignalConfig
        Config of Gating signal layer.

    """

    config_type = GatingSignalConfig

    def __init__(self, **kwargs) -> None:
        """Initialize self. See help(type(self)) for accurate signature."""
        super().__init__(**kwargs)
        conv_kwargs = {
            'filters': self.config.filters,
            'kernel_size': 1,
            'padding': 'same',
        }
        self.convolution = tf.keras.layers.Conv2D(**conv_kwargs)
        self.bn = tf.keras.layers.BatchNormalization()
        self.activation = tf.keras.layers.Activation(
            activation=self.config.activation,
        )

    def call(self, inputs: tf.Tensor, *args, **kwargs) -> tf.Tensor:
        """
        Forward pass of the GatingSignal layer.

        Parameters
        ----------
        inputs : tf.Tensor
            Input tensor representing the gating signal.

        Returns
        -------
        tf.Tensor
            The processed gating signal tensor after applying convolution,
            optional batch normalization, and activation.

        """
        out = self.convolution(inputs)
        if self.config.with_bn:
            out = self.bn(out)
        return self.activation(out)
