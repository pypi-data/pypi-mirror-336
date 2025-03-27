import numpy.testing as npt
import pytest
import numpy as np
from helica.Likelihood.LensLikelihood.dependent_param_likelihood import (
    DependentParamLikelihood,
)


class TestDependentParamLikelihood(object):

    def setup_method(self):

        q_mass_scaling_factor = 1.2
        q_light = 0.6

        self._q_mass_scaling_factor = q_mass_scaling_factor
        self._q_light = q_light

        self._dependent_param_likelihood = DependentParamLikelihood(
            q_mass_scaling=True,
            q_mass_scaling_factor=q_mass_scaling_factor,
            q_mass_intr_scatter=0.1,
            q_light=q_light,
        )

    def test_q_mass_model(self):

        q_mass_model = self._dependent_param_likelihood.q_mass_model(
            with_intr_scatter=False
        )
        npt.assert_almost_equal(
            np.clip(self._q_mass_scaling_factor * self._q_light, 0, 1),
            np.clip(q_mass_model, 0, 1),
        )

    def test_logL_q_mass_scaling(self):

        q_mass = 1.2

        assert self._dependent_param_likelihood.logL_q_mass_scaling(q_mass) == -np.inf

        q_mass = -0.5

        assert self._dependent_param_likelihood.logL_q_mass_scaling(q_mass) == -np.inf

        q_mass = np.linspace(0, 1, 1000)

        logL = self._dependent_param_likelihood.logL_q_mass_array_scaling(q_mass)
        ind = np.argmin(logL)
        npt.assert_almost_equal(
            q_mass[ind], self._q_mass_scaling_factor * self._q_light, decimal=3
        )
