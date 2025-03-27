from copy import deepcopy

import aesoptparam as apm

from ..common import cs_base


class outer_shape_bem(cs_base):

    def convert(self):
        osb = deepcopy(self.windio_dict)
        # Change coordinate system
        osb["reference_axis"] = self.change_reference_axis(osb["reference_axis"])
        return osb


class internal_structure_2d_fem(outer_shape_bem):
    pass


class tower(cs_base):
    outer_shape_bem = apm.SubParameterized(outer_shape_bem)
    internal_structure_2d_fem = apm.SubParameterized(internal_structure_2d_fem)

    def convert(self):
        comp = deepcopy(self.windio_dict)
        comp["outer_shape_bem"] = self.outer_shape_bem.convert()
        comp["internal_structure_2d_fem"] = self.internal_structure_2d_fem.convert()
        return comp


class monopile(tower):
    pass
