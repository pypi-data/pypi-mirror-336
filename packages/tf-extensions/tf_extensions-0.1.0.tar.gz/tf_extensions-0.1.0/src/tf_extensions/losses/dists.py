"""Module providing a class for DISTS loss function."""
from dataclasses import dataclass

import tensorflow as tf

from tf_extensions.losses.ssim_calculator import SSIMCalculator
from tf_extensions.losses.vgg_base import VGGBase, VGGBaseConfig


@dataclass
class DISTSConfig(VGGBaseConfig):
    """
    Configuration class for the DISTS loss function.

    Attributes
    ----------
    name : str, default: "dists"
        Name of the loss function.
    texture_weight : float, default: 0.5
        Weight for the texture loss component, should be in the range [0, 1].
    texture_stability_constant : float, default: 1e-6
        Small constant to stabilize texture similarity calculation.
    structure_stability_constant : float, default: 1e-6
        Small constant to stabilize structure similarity calculation.

    """

    name: str = 'dists'
    texture_weight: float = 0.5
    texture_stability_constant: float = 1e-6
    structure_stability_constant: float = 1e-6

    def __post_init__(self) -> None:
        """
        Update config properties after initialization.

        Raises
        ------
        ValueError
            If texture weight is out of range [0; 1].

        """
        super().__post_init__()
        texture_weight = self.texture_weight
        if texture_weight < 0 or texture_weight > 1:
            msg = f'Texture weight {texture_weight} is out of range [0; 1].'
            raise ValueError(msg)


class DISTS(VGGBase):
    """
    Deep Image Structure and Texture Similarity (DISTS) loss function.

    This loss function evaluates perceptual similarity by considering both
    structural and textural differences between images.

    Attributes
    ----------
    config : DISTSConfig
        The configuration of the DISTS loss function.

    """

    config_type = DISTSConfig

    def _get_features(
        self,
        y_true: tf.Tensor,
        y_pred: tf.Tensor,
    ) -> tuple[list[tf.Tensor], list[tf.Tensor]]:
        """
        Extract features from the input tensors.

        Parameters
        ----------
        y_true : tf.Tensor
            Ground truth image tensor.
        y_pred : tf.Tensor
            Predicted image tensor.

        Returns
        -------
        true_features, pred_features : tuple of lists
            true_features : list of tf.Tensor
                List of feature tensors extracted from the ground truth image.
            pred_features : list of tf.Tensor
                List of feature tensors extracted from the predicted image.

        """
        true_features, pred_features = super()._get_features(
            y_true=y_true,
            y_pred=y_pred,
        )
        true_features = [y_true, *true_features]
        pred_features = [y_pred, *pred_features]
        return true_features, pred_features

    def _compute_loss(
        self,
        true_features: list[tf.Tensor],
        pred_features: list[tf.Tensor],
    ) -> tf.Tensor:
        """
        Return the DISTS loss based on structure and texture similarity.

        Parameters
        ----------
        true_features : list of tf.Tensor
            List of feature tensors extracted from the ground truth image.
        pred_features : list of tf.Tensor
            List of feature tensors extracted from the predicted image.

        Returns
        -------
        tf.Tensor
            The computed DISTS loss value.

        """
        structure_loss = 0
        texture_loss = 0

        feat_number = len(true_features)
        for true_feat, pred_feat in zip(true_features, pred_features):
            texture, structure = SSIMCalculator(
                tensor1=tf.cast(true_feat, self.config.dtype),
                tensor2=tf.cast(pred_feat, self.config.dtype),
                c1=self.config.texture_stability_constant,
                c2=self.config.structure_stability_constant,
                averaging='reduce_mean',
                averaging_kwargs={'axis': (1, 2)},
            ).calculate()
            texture_loss += tf.reduce_mean(texture, axis=-1) / feat_number
            structure_loss += tf.reduce_mean(structure, axis=-1) / feat_number

        texture_loss *= self.config.texture_weight
        structure_loss *= (1 - self.config.texture_weight)
        return 1 - (structure_loss + texture_loss)
