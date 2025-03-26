import aesoptparam as apm

from ...utils import compute_curve_length, interp, jp
from .common import grids, windio_to_hawc2_child


class ae(windio_to_hawc2_child):
    """Settings for the AE-file conversion"""

    grid = apm.copy_param_ref(grids.param.ae, "..grids.ae")

    def convert(self):
        # Setting variables
        # Getting z grid
        [z_grid, z_val] = jp(
            "components.blade.outer_shape_bem.reference_axis.z.[grid, values]",
            self.windio_dict,
        )
        # AE-grid (default to z-grid from windio)
        grid = self.grid

        # Get profile thickness and name from WindIO
        if "rthick" in self.windio_dict["components"]["blade"]["outer_shape_bem"]:
            rthick = self.windio_dict["components"]["blade"]["outer_shape_bem"][
                "rthick"
            ]
            grid_air, prof_loc = rthick["grid"], rthick["values"]
            prof_loc = [_val * 100 for _val in prof_loc]
        else:
            prof_dat = dict(
                jp("airfoils[*].[name, relative_thickness]", self.windio_dict)
            )
            # Get airfoil along the span
            [grid_air, prof_loc] = jp(
                "components.blade.outer_shape_bem.airfoil_position.[grid, labels]",
                self.windio_dict,
            )
            # Replace name by tc
            for i, name in enumerate(prof_loc):
                prof_loc[i] = prof_dat[name] * 100  # Converting to %

        # Computing curve length
        x_in = interp(
            grid,
            *jp(
                "components.blade.outer_shape_bem.reference_axis.x.[grid, values]",
                self.windio_dict,
            ),
        )
        y_in = interp(
            grid,
            *jp(
                "components.blade.outer_shape_bem.reference_axis.y.[grid, values]",
                self.windio_dict,
            ),
        )
        z_in = interp(grid, z_grid, z_val)
        s = compute_curve_length(x_in, y_in, z_in)
        chord = interp(
            grid,
            *jp(
                "components.blade.outer_shape_bem.chord.[grid, values]",
                self.windio_dict,
            ),
        )
        tc = interp(grid, grid_air, prof_loc)

        return [
            dict(
                s=s,
                chord=chord,
                tc=tc,
                pc_set=[1] * len(s),
            )
        ]
