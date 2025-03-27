from lenstronomy.Sampling.Likelihoods.position_likelihood import PositionLikelihood
from lenstronomy.PointSource.point_source import PointSource
from lenstronomy.LensModel.lens_model import LensModel

__all__ = ['ImagePositionLikelihood']

class ImagePositionLikelihood(PositionLikelihood):

    def __init__(
        self,
        point_source_type_list,
        kwargs_ps,
        lens_model_list,
        kwargs_lens,
        source_position_sigma=0.005,
        source_position_tolerance=None,
        restrict_image_number=False,
        max_num_images=None,
        image_position_likelihood=True,
        ra_image_list=None,
        dec_image_list=None,
    ):

        point_source_class = PointSource(
            point_source_type_list=point_source_type_list,
            lens_model=LensModel(lens_model_list),
        )

        self.point_source_class = point_source_class

        PositionLikelihood.__init__(
            self,
            point_source_class=point_source_class,
            source_position_tolerance=source_position_tolerance,
            source_position_sigma=source_position_sigma,
            restrict_image_number=restrict_image_number,
            max_num_images=max_num_images,
            image_position_likelihood=image_position_likelihood,
            ra_image_list=ra_image_list,
            dec_image_list=dec_image_list,
        )

        self._kwargs_ps = kwargs_ps
        self._kwargs_lens = kwargs_lens

    def log_likelihood(self, kwargs_special=[], verbose=False):

        return self.logL(
            self._kwargs_lens,
            self._kwargs_ps,
            kwargs_special=kwargs_special,
            verbose=verbose,
        )
