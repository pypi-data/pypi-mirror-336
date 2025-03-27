from copy import deepcopy

import aesoptparam as apm
import numpy as np

from ....utils import change_pitch_axis, interp, warn
from ..common import cs_base


def get_grid(self):
    grid = None
    if self.has_parent():
        if self.parent_object.has_parent():
            if self.parent_object.has_parent():
                grid = self.parent_object.parent_object.parent_object.grids.blade
    if grid is None:
        return self.windio_dict["reference_axis"]["z"]["grid"]
    return grid


class pitch_axis_out(apm.AESOptParameterized):
    """Output pitch axis. Default to pitch axis 0.5 according to C2-def"""

    grid = apm.AESOptArray(
        lambda self: self.get_pitch_axis()["grid"], doc="Grid for the output pitch axis"
    )
    values = apm.AESOptArray(
        lambda self: self.get_pitch_axis()["values"],
        doc="Values for the output pitch axis",
        shape=".grid",
    )

    def get_pitch_axis(self):
        if self["..cs_transform_name"] == "windio_to_hawc2":
            return dict(grid=np.array([0, 1]), values=np.array([0.5, 0.5]))
        return self["..windio_dict"]["pitch_axis"]


class outer_shape_bem(cs_base):
    grid = apm.AESOptArray(
        lambda self: self.get_grid(), doc="Grid used for `blade.outer_shape_bem`"
    )
    pitch_axis_out = apm.SubParameterized(pitch_axis_out)

    def convert(self):
        osb = deepcopy(self.windio_dict)
        changed_pitch_axis = False
        # Change pitch axis (if input coordinate system is WindIO)
        if change_pitch_axis and (
            osb["reference_axis"].get("coordinate_system", "windio") == "windio"
        ):
            osb.update(self.change_pitch_axis(osb))
            changed_pitch_axis = True
        # Change coordinate system
        osb["reference_axis"] = self.change_reference_axis(osb["reference_axis"])
        # Change pitch axis (if output coordinate system is WindIO)
        if not changed_pitch_axis and change_pitch_axis:
            if osb["reference_axis"].get("coordinate_system", "windio") != "windio":
                raise RuntimeError(
                    "The coordinate system need to be in WindIO before or after coordinate transformation to do pitch-axis change"
                )
            osb.update(self.change_pitch_axis(osb))
            changed_pitch_axis = True
        return osb

    def change_pitch_axis(self, osb):
        grid = self.grid
        inp_data = dict(
            x=interp(
                grid,
                osb["reference_axis"]["x"]["grid"],
                osb["reference_axis"]["x"]["values"],
            ),
            y=interp(
                grid,
                osb["reference_axis"]["y"]["grid"],
                osb["reference_axis"]["y"]["values"],
            ),
            z=interp(
                grid,
                osb["reference_axis"]["z"]["grid"],
                osb["reference_axis"]["z"]["values"],
            ),
            chord=interp(
                grid,
                osb["chord"]["grid"],
                osb["chord"]["values"],
            ),
            twist_rad=-np.asarray(
                interp(
                    grid,
                    osb["twist"]["grid"],
                    osb["twist"]["values"],
                )
            ),
            pitch_axis_in=interp(
                grid,
                osb["pitch_axis"]["grid"],
                osb["pitch_axis"]["values"],
            ),
            pitch_axis_out=interp(
                grid,
                self.pitch_axis_out.grid,
                self.pitch_axis_out.values,
            ),
        )
        # Change pitch axis to be at half chord
        x, y, z = change_pitch_axis(**inp_data)
        return dict(
            reference_axis=dict(
                x=dict(grid=grid, values=x),
                y=dict(grid=grid, values=y),
                z=dict(grid=grid, values=z),
            ),
            pitch_axis=dict(
                grid=self.pitch_axis_out.grid, values=self.pitch_axis_out.values
            ),
        )

    def get_grid(self):
        return get_grid(self)


class elastic_properties_mb(cs_base):
    def convert(self):
        warn(
            "convert_coordinate_system.components.blade.elastic_properties_mb",
            self.no_warnings,
        )
        return self.windio_dict


class internal_structure_2d_fem(cs_base):
    def convert(self):
        is2dfem = deepcopy(self.windio_dict)
        is2dfem["reference_axis"] = self.change_reference_axis(
            is2dfem["reference_axis"]
        )
        return is2dfem


class blade(cs_base):
    outer_shape_bem = apm.SubParameterized(outer_shape_bem)
    elastic_properties_mb = apm.SubParameterized(elastic_properties_mb)
    internal_structure_2d_fem = apm.SubParameterized(internal_structure_2d_fem)

    def convert(self):
        blade = deepcopy(self.windio_dict)
        if "outer_shape_bem" in blade:
            blade["outer_shape_bem"] = self.outer_shape_bem.convert()
        if "elastic_properties_mb" in blade:
            blade["elastic_properties_mb"] = self.elastic_properties_mb.convert()
        if "internal_structure_2d_fem" in blade:
            blade["internal_structure_2d_fem"] = (
                self.internal_structure_2d_fem.convert()
            )
        return blade

    def get_cs_transform(self):
        transform_name = self.cs_transform_name
        if transform_name == "windio_to_hawc2":
            return dict(
                x="-y",
                y="x",
                z="z",
                desc="-y,x,z (windio to hawc2 blade)",
                coordinate_system="hawc2 blade",
            )
        elif transform_name == "hawc2_to_windio":
            return dict(
                x="y",
                y="-x",
                z="z",
                desc="y,-x,z (hawc2 to windio)",
                coordinate_system="windio",
            )
        return self["..get_cs_transform"]()
