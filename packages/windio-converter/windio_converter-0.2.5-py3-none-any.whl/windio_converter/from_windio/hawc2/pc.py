import numpy as np

from ...utils import airfoils2polars, warn
from .common import windio_to_hawc2_child


class pc(windio_to_hawc2_child):
    """Settings for the PC-file conversion"""

    def convert(self):
        warn(
            "windio_to_hawc2.pc",
            self.get_no_warnings(),
            "missing options for AoA interpolation and polar selection (using airfoils2polars)",
        )

        pc_file_list = []
        rt = []
        for iair, airfoil in enumerate(self.windio_dict["airfoils"]):
            rt.append(airfoil["relative_thickness"] * 100)
        iair_sorted = list(np.argsort(rt))
        airfoils = airfoils2polars(self.windio_dict["airfoils"])
        for iair in iair_sorted:
            prof = dict()

            prof["tc"] = airfoils[iair]["relative_thickness"] * 100

            # Interpolate cl, cd, cm
            prof["aoa"] = airfoils[iair]["polar"]["aoa_deg"]

            # Check if the values of the first AoS and the last AoA
            # in the list is close to +/-180 deg.
            # If yes, set the values to +/-180 deg to avoid HAWC2 issue
            # when reading AoA in pc-file
            if np.abs(np.abs(prof["aoa"][0]) - 180.0) < 0.1:
                prof["aoa"][0] = -180.0  # first AoA
            if np.abs(np.abs(prof["aoa"][-1]) - 180.0) < 0.1:
                prof["aoa"][-1] = 180.0  # last AoA

            prof["c_l"] = airfoils[iair]["polar"]["c_l"]
            prof["c_d"] = airfoils[iair]["polar"]["c_d"]
            prof["c_m"] = airfoils[iair]["polar"]["c_m"]
            # Add to list
            pc_file_list.append(prof)
        return pc_file_list
