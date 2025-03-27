from helica.Likelihood.LensLikelihood.image_position_likelihood import (
    ImagePositionLikelihood,
)
import numpy.testing as npt
import pytest
import numpy as np


class TestImagePositionLikelihood(object):

    def setup_method(self):
        pass

    def test_log_likelihood(self):

        image_position_likelihood = ImagePositionLikelihood(
            point_source_type_list=["LENSED_POSITION"],
            kwargs_ps=[
                {
                    "ra_image": [-1.09821568, 0.7139033],
                    "dec_image": [0.56263298, -0.46393098],
                }
            ],
            lens_model_list=["SIE", "SHEAR"],
            kwargs_lens=[
                {
                    "theta_E": 1.0,
                    "e1": 0.09952952990673791,
                    "e2": 0.10247944155707468,
                    "center_x": 0,
                    "center_y": 0,
                },
                {
                    "gamma1": np.float64(0.09800665778412417),
                    "gamma2": np.float64(0.019866933079506124),
                },
            ],
            source_position_sigma=0.005,
            restrict_image_number=True,
            max_num_images=2,
            image_position_likelihood=True,
            ra_image_list=[[-1.09821568, 0.7139033]],
            dec_image_list=[[0.56263298, -0.46393098]],
            source_position_tolerance=0.001,
        )
        npt.assert_almost_equal(
            image_position_likelihood.log_likelihood(), 0.0, decimal=8
        )
