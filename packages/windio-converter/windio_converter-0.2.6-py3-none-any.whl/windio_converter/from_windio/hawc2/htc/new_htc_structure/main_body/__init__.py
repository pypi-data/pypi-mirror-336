import aesoptparam as apm

from ....common import mbdy_names
from .blade import blade
from .common import main_body_base
from .floating_platform import floating_platform
from .monopile import monopile
from .shaft import shaft
from .simple_bodies import connector, hub
from .tower import tower
from .towertop import towertop


class main_body(main_body_base):
    tower = apm.SubParameterized(tower, precedence=0.20)
    towertop = apm.SubParameterized(towertop, precedence=0.21)
    connector = apm.SubParameterized(connector, precedence=0.22)
    shaft = apm.SubParameterized(shaft, precedence=0.23)
    hub = apm.SubParameterized(hub, precedence=0.24)
    blade = apm.SubParameterized(blade, precedence=0.25)
    monopile = apm.SubParameterized(monopile, precedence=0.26)
    floating_platform = apm.SubParameterized(floating_platform, precedence=0.27)
    hub_mbdy_name = apm.copy_param_ref(mbdy_names.param.hub, "......mbdy_names.hub")
    blade_mbdy_name = apm.copy_param_ref(
        mbdy_names.param.blade, "......mbdy_names.blade"
    )

    def convert(self):
        nb = self.windio_dict["assembly"]["number_of_blades"]
        mbdy = []
        if self.has_floater():
            mbdy += self.floating_platform.convert()

        if self.has_monopile():
            mbdy += [self.monopile.convert()]
        mbdy += [self.tower.convert()]
        mbdy += [self.towertop.convert()]
        mbdy += [self.connector.convert()]
        mbdy += [self.shaft.convert()]
        mbdy += [self.hub.convert()]
        for i in range(2, nb + 1):
            mbdy += [
                self.get_copy_main_body(
                    self.get_full_mbdy_name(self.hub_mbdy_name, i),
                    self.get_full_mbdy_name(self.hub_mbdy_name, 1),
                )
            ]
        mbdy += [self.blade.convert()]
        for i in range(2, nb + 1):
            mbdy += [
                self.get_copy_main_body(
                    self.get_full_mbdy_name(self.blade_mbdy_name, i),
                    self.get_full_mbdy_name(self.blade_mbdy_name, 1),
                )
            ]
        return mbdy

    def get_copy_main_body(self, name, name_of_copy):
        return dict(name=name, copy_main_body=name_of_copy)
