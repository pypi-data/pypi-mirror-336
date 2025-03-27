import aesoptparam as apm

from ..common import connector_shaft_ratio
from ..common import mbdy_names as _mbdy_names
from ..common import shaft_length
from .blade import blade
from .circular_bodies import floater, monopile, tower
from .common import st_base
from .stiff_bodies import connector, hub, shaft, towertop


class mbdy_names(apm.AESOptParameterized):
    tower = apm.copy_param_ref(_mbdy_names.param.tower, "....mbdy_names.tower")
    towertop = apm.copy_param_ref(_mbdy_names.param.towertop, "....mbdy_names.towertop")
    connector = apm.copy_param_ref(
        _mbdy_names.param.connector, "....mbdy_names.connector"
    )
    shaft = apm.copy_param_ref(_mbdy_names.param.shaft, "....mbdy_names.shaft")
    hub = apm.copy_param_ref(_mbdy_names.param.hub, "....mbdy_names.hub")
    blade = apm.copy_param_ref(_mbdy_names.param.blade, "....mbdy_names.blade")
    monopile = apm.copy_param_ref(_mbdy_names.param.monopile, "....mbdy_names.monopile")


class st(st_base):
    """Settings for the ST-files conversion"""

    tower = apm.SubParameterized(tower, precedence=0.20)
    towertop = apm.SubParameterized(towertop, precedence=0.21)
    connector = apm.SubParameterized(connector, precedence=0.22)
    shaft = apm.SubParameterized(shaft, precedence=0.23)
    hub = apm.SubParameterized(hub, precedence=0.24)
    blade = apm.SubParameterized(blade, precedence=0.25)
    monopile = apm.SubParameterized(monopile, precedence=0.26)
    floater = apm.SubParameterized(floater, precedence=0.27)
    mbdy_names = apm.SubParameterized(mbdy_names)

    def convert(self):
        st_data = dict()

        if self.has_monopile():
            st_data[self.mbdy_names.monopile] = self.monopile.convert()
        if self.has_floater():
            allBodies = self.floater.convert()
            for aB_ in allBodies:
                st_data[aB_] = allBodies[aB_]

        st_data[self.mbdy_names.tower] = self.tower.convert()
        st_data[self.mbdy_names.towertop] = self.towertop.convert()
        st_data[self.mbdy_names.connector] = self.connector.convert()
        st_data[self.mbdy_names.shaft] = self.shaft.convert()
        st_data[self.get_full_mbdy_name(self.mbdy_names.hub, 1)] = self.hub.convert()
        st_data[self.get_full_mbdy_name(self.mbdy_names.blade, 1)] = (
            self.blade.convert()
        )
        return st_data
