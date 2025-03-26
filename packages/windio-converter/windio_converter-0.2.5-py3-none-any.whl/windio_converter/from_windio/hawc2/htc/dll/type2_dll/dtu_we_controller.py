import numpy as np
from aesoptparam.utils import copy_param_ref

from ....common import dtu_we_controller as dtu_we_controller_options
from ....common import windio_to_hawc2_child


class dtu_we_controller(windio_to_hawc2_child):
    TSR_design = copy_param_ref(
        dtu_we_controller_options.param.TSR_design,
        "........dtu_we_controller.TSR_design",
    )
    CP_design = copy_param_ref(
        dtu_we_controller_options.param.CP_design,
        "........dtu_we_controller.CP_design",
    )

    def convert(self):
        out = dict(name="dtu_we_controller", init=dict(constant=[]))
        if not self.TSR_design is None:
            out["init"]["constant"].append([11, self.constant11()])
        return out

    def constant11(self):
        R = self.windio_dict["assembly"]["rotor_diameter"] / 2
        air_density = self.windio_dict["environment"]["air_density"]
        gearbox_efficiency = self.windio_dict["components"]["nacelle"][
            "drivetrain"
        ].get("gearbox_efficiency", 1.0)
        gear_ratio = self.windio_dict["components"]["nacelle"]["drivetrain"].get(
            "gear_ratio", 1.0
        )
        A = np.pi * R**2
        return (gearbox_efficiency * air_density * A * (R**3) * self.CP_design) / (
            2 * gear_ratio * (self.TSR_design**3)
        )  # constant 11
