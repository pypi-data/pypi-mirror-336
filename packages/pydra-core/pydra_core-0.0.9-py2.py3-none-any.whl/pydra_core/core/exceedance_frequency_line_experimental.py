import numpy as np

from .calculation import Calculation
from .datamodels.frequency_line import FrequencyLine
from ..location.location import Location


class ExceedanceFrequencyLineExperimental(Calculation):
    """
    Calculate a frequency line for a result variable (e.g. h (waterlevel), hs (significant wave height)) for a location
    """

    def __init__(
        self,
        result_variable: str,
        model_uncertainty: bool = True,
        levels: list = None,
        step_size: float = 0.1,
    ):
        """
        The __init__ method initializes an instance of the ExceedanceFrequencyLine class. It takes in several parameters to configure the calculation of the frequency line.

        Parameters
        ----------
        result_variable : str
            The result variable for which the frequency line will be calculated.
        model_uncertainty : bool (optional)
            Enable or disable the use of model uncertainties when calculating the frequency line. Default is True.
        levels : list (optional):
            The levels at which the exceedance probability has to be calculated. If not specified, the levels will be chosen between the 1st and 99th percentile of the values in the HRDatabase.
        step_size : float (optional)
            The step size of the frequency line. Default is 0.1.
        """
        # Inherit
        super().__init__()

        # Warning
        print(
            "Experimental version may give different results for water levels when applying model uncertainty."
        )

        # Save settings
        self.set_result_variable(result_variable.lower())
        self.use_model_uncertainty(model_uncertainty)
        self.set_levels(levels)
        self.set_step_size(step_size)

    def calculate_location(self, location: Location) -> FrequencyLine:
        """
        Calculate the exceedance probability of the variable at a given set of levels.
        If the levels are not specified, they will be chosen at the 1st and 99th percentile of all values in the database.

        Parameter
        ---------
        location : Location
            The Location object

        Returns
        -------
        FrequencyLine
            Frequency line of the result variable
        """
        # Copy the levels
        levels = self.levels

        # Obtain location object
        model = location.get_model()
        loading = model.get_loading()

        # Check if the levels are defined, if not, define it between the 1st and 99th percentile
        if levels is None:
            lower, upper = loading.get_quantile_range(
                self.result_variable, 0.01, 0.99, 3
            )
            levels = np.arange(lower, upper + 0.5 * self.step_size, self.step_size)

        # Repair
        loading.repair_loadingmodels(self.result_variable)

        # Splits uit naar trage stochasten en windrichting
        p_h_slow = model.calculate_probability_loading(
            result_variable=self.result_variable,
            levels=levels,
            model_uncertainty=self.model_uncertainty,
            split_input_variables=list(model.statistics.stochastics_slow.keys()),
            given=list(model.statistics.stochastics_slow.keys()),
        )

        # Reken kansen om naar overschrijdingskansen door over de eerste te sommeren
        ep_h_slow = np.cumsum(p_h_slow[::-1], axis=0)[-2::-1]

        # Process slow stochastics (they are always at the last axes of the matrix)
        if len(list(model.statistics.stochastics_slow.keys())) > 0:
            p_trapezoidal = model.process_slow_stochastics(ep_h_slow)
            exceedance_probability = (
                p_trapezoidal * location.get_settings().periods_base_duration
            )

        # Zo niet, geef de overschrijdingskansen direct terug
        else:
            exceedance_probability = (
                ep_h_slow * location.settings.periods_block_duration
            )

        # Return the frequency line
        return FrequencyLine(levels, exceedance_probability)

    def set_result_variable(self, result_variable: str):
        """
        Change the result variable for which the frequency line will be calculated.

        Parameters
        ----------
        result_variable : str
            The result variable for which the frequency line will be calculated
        """
        # Raise an error when assigning the wave direction (dir)
        if result_variable == "dir":
            raise ValueError(
                "[ERROR] Cannot calculate a frequency line for the wave direction (dir)."
            )

        # Save result variable
        self.result_variable = result_variable

    def set_levels(self, levels: list = None):
        """
        Change the levels.
        If levels is not defined, the frequency line is calculated based upon the 1st and 99th percentile.

        Parameters
        ----------
        levels : list, optional
            The levels at which the exceedance probability has to be calculated
        """
        self.levels = levels

    def set_step_size(self, step_size: float):
        """
        Change the step size of the frequency line.

        Parameters
        ----------
        step_size : float
            The step size of the frequency line
        """
        # Cannot be smaller or equal to 0
        if step_size <= 0:
            raise ValueError("[ERROR] Step size should be larger than 0.")

        # Save step size
        self.step_size = step_size

    def use_model_uncertainty(self, model_uncertainty: bool):
        """
        Use model uncertainty when calculating a frequency line.

        Parameters
        ----------
        model_uncertainty : bool
            Enable or disable the use of model uncertainties
        """
        self.model_uncertainty = model_uncertainty
