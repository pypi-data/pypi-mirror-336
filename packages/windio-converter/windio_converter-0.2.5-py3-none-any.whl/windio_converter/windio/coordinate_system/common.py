import aesoptparam as apm

from ...common import windio_converter_base
from ...utils import change_coord_sys


class cs_transform(apm.AESOptParameterized):
    """Coordinate system transformation to apply to a WindIO data structure"""

    x = apm.AESOptString(
        lambda self: self.get_cs_transform()["x"],
        doc="Transformation of the x-axis",
    )
    y = apm.AESOptString(
        lambda self: self.get_cs_transform()["y"],
        doc="Transformation of the y-axis",
    )
    z = apm.AESOptString(
        lambda self: self.get_cs_transform()["z"],
        doc="Transformation of the z-axis",
    )
    desc = apm.AESOptString(
        lambda self: self.get_cs_transform()["desc"],
        doc="Description of the transformation",
    )
    coordinate_system = apm.AESOptString(
        lambda self: self.get_cs_transform()["coordinate_system"],
        doc="Resulting coordinate system (after the transformation)",
    )

    def get_cs_transform(self):
        if self.has_parent():
            return self["..get_cs_transform"]()
        else:
            return dict(x=None, y=None, z=None, desc=None, coordinate_system=None)


class cs_base(windio_converter_base):
    cs_transform_name = apm.AESOptString(
        lambda self: self.get_cs_transform_name(),
        doc="Name of the coordinate system transform (e.g. `windio_to_hawc2`, `hawc2_to_windio`, ..)",
    )
    cs_transform = apm.SubParameterized(cs_transform)
    no_warnings = apm.Boolean(False, doc="Flag for turning warnings on/off")

    def get_cs_transform(self):
        if self.has_parent():
            return self["..get_cs_transform"]()
        return None

    def get_cs_transform_name(self):
        if "cs_transform_name" in self._param__private.values:
            return self.cs_transform_name
        elif self.has_parent():
            return self["..get_cs_transform_name"]()
        return None

    def change_reference_axis(self, ref_axis):
        coord_trans = self.get_cs_transform()
        ref_axis_out = change_coord_sys(ref_axis, coord_trans)
        if "coordinate_system" in coord_trans:
            ref_axis_out["coordinate_system"] = coord_trans["coordinate_system"]
        else:
            ref_axis_out["coordinate_system"] = (
                f"{coord_trans['x']},{coord_trans['y']},{coord_trans['z']}"
            )
        if ref_axis_out["coordinate_system"] == "windio":
            ref_axis_out.pop("coordinate_system")
        return ref_axis_out

    def get_windio_dict(self):
        if callable(self._param__private.values["windio_dict"]):
            if self.has_parent():
                parent_windio = self.parent_object.get_windio_dict()
                if not parent_windio is None:
                    name = type(self).__name__
                    if name in parent_windio:
                        return parent_windio[name]
            return None
        return self._param__private.values["windio_dict"]


class grids(apm.AESOptParameterized):
    """Grids used for interpolation of various components"""

    blade = apm.AESOptArray(
        doc="Grid used for all of the blade grids, `outer_shape_bem`, `elastic_properties_mb`, `internal_structure_2d_fem` (default to `z`-grid in the `reference_axis` of each of them)",
        bounds=(0, 1),
    )
