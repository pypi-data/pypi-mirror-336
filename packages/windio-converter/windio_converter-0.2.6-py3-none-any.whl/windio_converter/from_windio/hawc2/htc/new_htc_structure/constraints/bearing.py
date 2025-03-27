import aesoptparam as apm

from ....common import init_rotor_speed, mbdy_names, use_constant_rotor_speed
from ..common import new_htc_structure_base


class bearing(new_htc_structure_base):
    def get_bearing(self, bname, mbdy1, mbdy2, omegas=None):
        bearing = dict(name=bname)
        bearing.update(self.get_fix1(mbdy1, mbdy2))
        bearing["bearing_vector"] = [2, 0.0, 0.0, -1.0]
        if not omegas is None:
            bearing["omegas"] = omegas
        return bearing


class bearing1(bearing):
    connector_mbdy_name = apm.copy_param_ref(
        mbdy_names.param.connector, "........mbdy_names.connector"
    )
    shaft_mbdy_name = apm.copy_param_ref(
        mbdy_names.param.shaft, "........mbdy_names.shaft"
    )
    use_constant_rotor_speed = apm.copy_param_ref(
        use_constant_rotor_speed, "........use_constant_rotor_speed"
    )

    def convert(self):
        bearing1 = []
        if not self.use_constant_rotor_speed:
            bearing1 += [
                self.get_bearing(
                    "shaft_rotation", self.connector_mbdy_name, self.shaft_mbdy_name
                )
            ]
        return bearing1


class bearing2(bearing):
    hub_mbdy_name = apm.copy_param_ref(mbdy_names.param.hub, "........mbdy_names.hub")
    blade_mbdy_name = apm.copy_param_ref(
        mbdy_names.param.blade, "........mbdy_names.blade"
    )

    def convert(self):
        bearing2 = []
        for i in range(1, self.windio_dict["assembly"]["number_of_blades"] + 1):
            bearing2 += [
                self.get_bearing(
                    f"pitch{i}",
                    self.get_full_mbdy_name(self.hub_mbdy_name, i),
                    self.get_full_mbdy_name(self.blade_mbdy_name, i),
                )
            ]
        return bearing2


class bearing3(bearing):
    init_rotor_speed = apm.copy_param_ref(init_rotor_speed, "........init_rotor_speed")
    connector_mbdy_name = apm.copy_param_ref(
        mbdy_names.param.connector, "........mbdy_names.connector"
    )
    shaft_mbdy_name = apm.copy_param_ref(
        mbdy_names.param.shaft, "........mbdy_names.shaft"
    )
    use_constant_rotor_speed = apm.copy_param_ref(
        use_constant_rotor_speed, "........use_constant_rotor_speed"
    )

    def convert(self):
        bearing3 = []
        if self.use_constant_rotor_speed:
            bearing3 += [
                self.get_bearing(
                    "shaft_rotation",
                    self.connector_mbdy_name,
                    self.shaft_mbdy_name,
                    omegas=self.init_rotor_speed,
                )
            ]
        return bearing3
