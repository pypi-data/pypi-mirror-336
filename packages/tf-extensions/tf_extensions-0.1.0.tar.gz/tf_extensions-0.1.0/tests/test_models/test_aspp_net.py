import pytest
import tensorflow as tf

from tf_extensions import layers as cl
from tf_extensions.layers import conv_configs as cc
from tf_extensions.layers.aspp_layer import ASPPLayerConfig
from tf_extensions.models.aspp_net import ASPPNet, ASPPNetConfig
from tf_extensions.models.base_net import BaseNetConfig

aspp_net_properties = [
    (
        64,
        (3, 3),
        'relu',
        True,
        False,
        False,
        'glorot_uniform',
    ),
]


class TestASPPNetConfig:

    def test_init(self) -> None:
        config = ASPPNetConfig()
        assert config.aspp_config == ASPPLayerConfig()
        assert config.middle_filters == 48

    def test_config_name(self) -> None:
        config = ASPPNetConfig()
        config_name = config.get_config_name()
        assert config_name == 'aspp256middle48'


class TestASPPNet:

    def test_init_without_args(self) -> None:
        model = ASPPNet()
        assert isinstance(model.config, BaseNetConfig)

    @pytest.mark.parametrize(
        (
            'filters',
            'kernel',
            'activation',
            'bias',
            'bn',
            'dropout',
            'initializer',
        ),
        aspp_net_properties,
    )
    def test_init(
        self,
        filters: int,
        kernel: tuple[int, ...],
        activation: str,
        bias: bool,
        bn: bool,
        dropout: bool,
        initializer: str,
    ) -> None:
        model = ASPPNet(
            initial_filters_number=filters,
            conv_block_config=cc.ConvolutionalBlockConfig(
                conv2d_config=cc.Conv2DConfig(
                    kernel_size=kernel,
                    use_bias=bias,
                    kernel_initializer=initializer,
                ),
                activation=activation,
                with_bn=bn,
                with_dropout=dropout,
            ),
        )
        scales = [1, 2, 3, 4, 4, 3]
        for i, conv_block in enumerate(model.conv_blocks):
            assert isinstance(conv_block, cl.ConvolutionalBlock)
            assert conv_block.filters == filters * scales[i]
            assert conv_block.config.with_bn == bn
            assert conv_block.config.with_dropout == dropout
            assert conv_block.config.activation == activation
            conv2d_config = conv_block.config.conv2d_config
            assert conv2d_config.padding == 'same'
            assert conv2d_config.use_bias == bias
            assert conv2d_config.kernel_initializer == initializer
        for conv_layer in (
            model.conv_middle,
            model.conv_out,
        ):
            assert isinstance(conv_layer, tf.keras.layers.Conv2D)
            assert conv_layer.padding == 'same'
            assert conv_layer.use_bias == bias
            assert conv_layer.kernel_size == (1, 1)
        assert model.conv_middle.filters == 48
        assert model.conv_out.filters == 1
        assert isinstance(model.aspp, cl.ASPPLayer)
        assert model.aspp.conv_kwargs['filters'] == 256
        assert model.aspp.conv_kwargs['padding'] == 'same'
        assert model.aspp.conv_kwargs['activation'] == 'relu'
        assert len(model.aspp.dilated_layers) == 4
        for layer_id, layer in enumerate(model.aspp.dilated_layers):
            if layer_id:
                assert layer.kernel_size == kernel
                assert layer.dilation_rate == (6 * layer_id, 6 * layer_id)
            else:
                assert layer.kernel_size == (1, 1)
            assert layer.filters == 256
            assert layer.padding == 'same'
        assert model.aspp.conv_out.filters == 256
        assert model.aspp.conv_out.kernel_size == (1, 1)
        assert model.aspp.conv_out.padding == 'same'

    @pytest.mark.parametrize(
        (
            'input_shape',
            'filters',
            'kernel',
            'activation',
            'bias',
            'bn',
            'dropout',
            'initializer',
        ),
        [((3, 128, 128, 1), *item) for item in aspp_net_properties],
    )
    def test_call(
        self,
        input_shape: tuple[int, ...],
        filters: int,
        kernel: tuple[int, ...],
        activation: str,
        bias: bool,
        bn: bool,
        dropout: bool,
        initializer: str,
    ) -> None:
        model = ASPPNet(
            initial_filters_number=filters,
            conv_block_config=cc.ConvolutionalBlockConfig(
                conv2d_config=cc.Conv2DConfig(
                    kernel_size=kernel,
                    use_bias=bias,
                    kernel_initializer=initializer,
                ),
                activation=activation,
                with_bn=bn,
                with_dropout=dropout,
            ),
        )
        output = model.call(inputs=tf.random.normal(shape=input_shape))
        assert output.shape == input_shape
