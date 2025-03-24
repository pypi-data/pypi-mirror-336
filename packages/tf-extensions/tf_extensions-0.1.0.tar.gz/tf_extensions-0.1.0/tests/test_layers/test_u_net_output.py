import numpy as np
import pytest
import tensorflow as tf

from tf_extensions import layers as cl
from tf_extensions.layers import conv_configs as cc


class TestUNetOutputLayer:

    @pytest.mark.parametrize(
        (
            'vector_length',
            'conv2d_config',
        ),
        [
            (None, None),
            (None, cc.Conv2DConfig()),
            (2, None),
            (2, cc.Conv2DConfig()),
        ],
    )
    def test_init(
        self,
        vector_length: int,
        conv2d_config: cc.Conv2DConfig,
    ) -> None:
        layer = cl.UNetOutputLayer(
            vector_length=vector_length,
            conv2d_config=conv2d_config,
        )
        assert layer.config.vector_length == vector_length
        assert isinstance(layer.config.conv2d_config, cc.Conv2DConfig)
        if layer.config.vector_length:
            assert isinstance(layer.out_layer, tf.keras.layers.Conv1D)
        else:
            assert isinstance(layer.out_layer, tf.keras.layers.Conv2D)

    @pytest.mark.parametrize(
        (
            'input_shape',
            'vector_length',
            'conv2d_config',
            'exp_shape',
        ),
        [
            ((3, 128, 128, 1), None, None, (3, 128, 128, 1)),
            ((3, 128, 128, 1), None, cc.Conv2DConfig(), (3, 128, 128, 1)),
            ((3, 128, 128, 1), 2, None, (3, 128, 1, 1)),
            ((3, 128, 128, 1), 2, cc.Conv2DConfig(), (3, 128, 1, 1)),
        ],
    )
    def test_call(
        self,
        input_shape: tuple[int, ...],
        vector_length: int,
        conv2d_config: cc.Conv2DConfig,
        exp_shape: tuple[int, ...],
    ) -> None:
        output = cl.UNetOutputLayer(
            vector_length=vector_length,
            conv2d_config=conv2d_config,
        )(inputs=np.random.random(input_shape))
        assert output.shape == exp_shape
