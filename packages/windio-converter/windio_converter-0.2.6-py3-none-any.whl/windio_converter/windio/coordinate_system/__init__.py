from copy import deepcopy

import aesoptparam as apm

from .common import cs_base, grids
from .components import components


class convert_coordinate_system(cs_base):

    grids = apm.SubParameterized(grids)
    components = apm.SubParameterized(components)

    def convert(self):
        # Copy the input windio dict
        wio_out = deepcopy(self.windio_dict)
        transform = self.get_cs_transform()
        if transform["coordinate_system"] is not None:
            wio_out["coordinate_system"] = transform["coordinate_system"]
        # Components
        wio_out["components"] = self.components.convert()
        return wio_out

    def get_cs_transform(self):
        transform_name = self.cs_transform_name
        if isinstance(transform_name, str):
            if transform_name == "windio_to_hawc2":
                return dict(
                    x="y",
                    y="x",
                    z="-z",
                    desc="y,x,-z (windio to hawc2 base)",
                    coordinate_system="hawc2 base",
                )
            elif transform_name == "hawc2_to_windio":
                return dict(
                    x="y",
                    y="x",
                    z="-z",
                    desc="y,x,-z (hawc2 base to windio)",
                    coordinate_system="windio",
                )
            elif transform_name is not None:
                raise ValueError(
                    f"Unknown coordinate transformation name {transform_name}"
                )
        return dict(x=None, y=None, z=None, desc=None, coordinate_system=None)
