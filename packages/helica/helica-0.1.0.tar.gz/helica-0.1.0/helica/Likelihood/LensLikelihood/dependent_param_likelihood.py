import numpy as np

__all__ = ["DependentParamLikelihood"]


class DependentParamLikelihood(object):

    def __init__(
        self,
        q_mass_scaling=True,
        q_mass_scaling_factor=1.0,
        q_mass_intr_scatter=0.01,
        q_light=1.0,
    ):
        """Class to manage the likelihood of dependent lens parameters

        Args:
            q_mass_scaling (bool, optional): whether to evaluate the likelihood of q_mass conditioned on a q_light and scaling factor. Defaults to True.
            q_mass_scaling_factor (float, optional): scaling factor in q_mass = scaling_factor * q_light + Gaussian intrinsic scatter. Defaults to 1.0.
            q_mass_intr_scatter (float, optional): dispersion of the Gaussian intrinsic scatter in q_mass = scaling_factor * q_light + Gaussian intrinsic scatter. Defaults to 0.01.
            q_light (float, optional): axis ratio of isophote. Defaults to 1.0.
        """
        self.q_mass_scaling = q_mass_scaling
        self.q_mass_scaling_factor = q_mass_scaling_factor
        self.q_mass_intr_scatter = q_mass_intr_scatter
        self.q_light = q_light

    def q_mass_model(self, with_intr_scatter=True):
        """Calculate the q_mass model conditioned on q_light, the scaling factor and a Gaussian intrinsic scatter

        Args:
            with_intr_scatter (bool, optional): whether to include the intrinsic scatter in the modeled q_mass. Defaults to True.

        Returns:
            _type_: q_mass model
        """
        if with_intr_scatter:
            scale = self.q_mass_intr_scatter
        else:
            scale = 0.0

        q_mass_modeled = np.clip(
            self.q_mass_scaling_factor * self.q_light + np.random.normal(0, scale), 0, 1
        )

        return q_mass_modeled

    def logL_q_mass_scaling(self, q_mass):
        """Calculate the negative log likelihood of an input q_mass under a q_light, the scaling factor and the Gaussian intrinsic scatter

        Args:
            q_mass (_type_): _description_

        Returns:
            _type_: _description_
        """
        q_mass_mean = self.q_mass_model(with_intr_scatter=False)

        if (q_mass > 0) and (q_mass < 1):
            log_likelihood = 0.5 * (
                q_mass - q_mass_mean
            ) ** 2 / self.q_mass_intr_scatter**2 + np.log(self.q_mass_intr_scatter)
        else:
            log_likelihood = -np.inf

        return log_likelihood

    def logL_q_mass_array_scaling(self, q_mass_array):
        """Calculate the negative log likelihood of an input q_mass array under a q_light, the scaling factor and the Gaussian intrinsic scatter

        Args:
            q_mass_array (_type_): _description_

        Returns:
            _type_: array of -logL
        """
        q_mass_mean = self.q_mass_model(with_intr_scatter=False)

        log_likelihood = 0.5 * (
            q_mass_array - q_mass_mean
        ) ** 2 / self.q_mass_intr_scatter**2 + np.log(self.q_mass_intr_scatter)

        ind = np.where((q_mass_array < 0) | (q_mass_array > 1))

        log_likelihood[ind] = -np.inf

        return log_likelihood

    def log_likelihood(self, q_mass=None):

        logL = 0.0

        if self.q_mass_scaling:
            logL += self.logL_q_mass_scaling(q_mass)

        return logL
