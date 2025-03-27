import aesoptparam as apm

from ......utils import interp
from ....common import filenames, grids, mbdy_names, nbodies
from .common import main_body_base


class monopile(main_body_base):
    grid = apm.copy_param_ref(grids.param.monopile, "........grids.monopile")
    filename = apm.copy_param_ref(
        filenames.param.monopile, "........filenames.monopile"
    )
    mbdy_name = apm.copy_param_ref(
        mbdy_names.param.monopile, "........mbdy_names.monopile"
    )
    nbodies = apm.copy_param_ref(nbodies.param.monopile, "........nbodies.monopile")

    def convert(self):
        mono_axis = self.windio_dict["components"]["monopile"]["outer_shape_bem"][
            "reference_axis"
        ]
        # Get grid
        grid = self.grid

        # Ensure that z is from 0 to monopile length
        z_val = mono_axis["z"]["values"]
        z_val = [z - z_val[0] for z in z_val]

        # Interpolate x, y, z
        x_out = interp(grid, mono_axis["x"]["grid"], mono_axis["x"]["values"])
        y_out = interp(grid, mono_axis["y"]["grid"], mono_axis["y"]["values"])
        z_out = interp(grid, mono_axis["z"]["grid"], z_val)

        # Add concentrated mass (transition)
        nsec = len(grid)
        mono = self.get_mbdy_base()
        mono["concentrated_mass"] = [
            [
                nsec,
                0.0,
                0.0,
                0.0,
                self.windio_dict["components"]["monopile"]["transition_piece_mass"],
                0.0,
                0.0,
                0.0,
            ]
        ]

        # Add sec and nsec
        sec = [None] * nsec
        for i, (x, y, z) in enumerate(zip(x_out, y_out, z_out)):
            sec[i] = [i + 1, x, y, -z, 0.0]
        mono["c2_def"]["nsec"] = nsec
        mono["c2_def"]["sec"] = sec
        return mono
