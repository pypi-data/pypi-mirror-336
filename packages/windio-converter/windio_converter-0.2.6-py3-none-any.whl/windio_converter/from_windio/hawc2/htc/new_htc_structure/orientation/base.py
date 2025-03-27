import aesoptparam as apm

from ....common import base_inipos, mbdy_names
from ..common import new_htc_structure_base


class base(new_htc_structure_base):
    base_inipos = apm.copy_param_ref(base_inipos, "........base_inipos")
    tower_mbdy_name = apm.copy_param_ref(
        mbdy_names.param.tower, "........mbdy_names.tower"
    )
    monopile_mbdy_name = apm.copy_param_ref(
        mbdy_names.param.monopile, "........mbdy_names.monopile"
    )

    def convert(self):
        if self.has_monopile():
            def_name = self.monopile_mbdy_name
        elif self.has_floater():
            def_name, _ = self.get_floating_platform_member_with_transition()
        else:
            def_name = self.tower_mbdy_name
        return [
            dict(
                mbdy=def_name,
                inipos=self.base_inipos,
                mbdy_eulerang=[0.0, 0.0, 0.0],
            )
        ]
