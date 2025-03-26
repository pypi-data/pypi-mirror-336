import aesoptparam as apm

from ......utils import interp
from ....common import filenames, grids, mbdy_names, nbodies
from .common import main_body_base


class tower(main_body_base):
    grid = apm.copy_param_ref(grids.param.tower, "........grids.tower")
    filename = apm.copy_param_ref(filenames.param.tower, "........filenames.tower")
    mbdy_name = apm.copy_param_ref(mbdy_names.param.tower, "........mbdy_names.tower")
    nbodies = apm.copy_param_ref(nbodies.param.tower, "........nbodies.tower")

    def convert(self):
        tower_axis = self.windio_dict["components"]["tower"]["outer_shape_bem"][
            "reference_axis"
        ]
        # Get grid
        grid = self.grid

        # Ensure that z is from 0 to tower length
        z_val = tower_axis["z"]["values"]
        z_val = [z - z_val[0] for z in z_val]

        # Interpolate x, y, z
        x_out = interp(grid, tower_axis["x"]["grid"], tower_axis["x"]["values"])
        y_out = interp(grid, tower_axis["y"]["grid"], tower_axis["y"]["values"])
        z_out = interp(grid, tower_axis["z"]["grid"], z_val)

        # Add sec and nsec
        nsec = len(grid)
        sec = [None] * nsec
        for i, (x, y, z) in enumerate(zip(x_out, y_out, z_out)):
            sec[i] = [i + 1, x, y, -z, 0.0]
        tower = self.get_mbdy_base()
        tower["c2_def"]["nsec"] = nsec
        tower["c2_def"]["sec"] = sec
        return tower
