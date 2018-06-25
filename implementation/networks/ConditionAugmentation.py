""" Module implementing the Condition Augmentation """

import torch as th


class ConditionAugmentor(th.nn.Module):
    """ Perform conditioning augmentation
        from the paper -> https://arxiv.org/abs/1710.10916 (StackGAN++)
        uses the reparameterization trick from VAE paper.
    """

    def __init__(self, input_size, latent_size):
        """
        constructor of the class
        :param input_size: input size to the augmentor
        :param latent_size: required output size
        """
        super(ConditionAugmentor, self).__init__()

        assert latent_size % 2 == 0, "Latent manifold has odd number of dimensions"

        # state of the object
        self.input_size = input_size
        self.latent_size = latent_size

        # required modules:
        self.transformer = th.nn.Linear(self.input_size, 2 * self.latent_size)

    def forward(self, x):
        """
        forward pass (computations)
        :param x: input
        :return: c_not_hat => augmented text embeddings
        """
        # apply the feed forward layer:
        combined = self.transformer(x)

        # use the reparameterization trick
        mid_point = self.latent_size
        mus, sigmas = combined[:, :mid_point], combined[:, mid_point:]

        epsilon = th.randn(*mus.shape)
        c_not_hat = (epsilon * sigmas) + mus

        return c_not_hat
