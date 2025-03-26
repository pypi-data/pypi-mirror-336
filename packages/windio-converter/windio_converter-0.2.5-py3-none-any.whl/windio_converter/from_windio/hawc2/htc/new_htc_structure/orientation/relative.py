import aesoptparam as apm

from ......utils import rad2deg
from ....common import init_blade_pitch, init_rotor_speed
from ....common import mbdy_names as _mbdy_names
from ..common import new_htc_structure_base


class mbdy_names(apm.AESOptParameterized):
    tower = apm.copy_param_ref(_mbdy_names.param.tower, "...........mbdy_names.tower")
    towertop = apm.copy_param_ref(
        _mbdy_names.param.towertop, "...........mbdy_names.towertop"
    )
    connector = apm.copy_param_ref(
        _mbdy_names.param.connector, "...........mbdy_names.connector"
    )
    shaft = apm.copy_param_ref(_mbdy_names.param.shaft, "...........mbdy_names.shaft")
    hub = apm.copy_param_ref(_mbdy_names.param.hub, "...........mbdy_names.hub")
    blade = apm.copy_param_ref(_mbdy_names.param.blade, "...........mbdy_names.blade")
    monopile = apm.copy_param_ref(
        _mbdy_names.param.monopile, "...........mbdy_names.monopile"
    )


class relative(new_htc_structure_base):
    init_blade_pitch = apm.copy_param_ref(init_blade_pitch, "........init_blade_pitch")
    init_rotor_speed = apm.copy_param_ref(init_rotor_speed, "........init_rotor_speed")
    mbdy_names = apm.SubParameterized(mbdy_names)

    def convert(self):
        rel = []
        # Monopile
        if self.has_monopile():
            rel += [
                self.get_base_relative_straight(
                    self.mbdy_names.monopile, self.mbdy_names.tower
                )
            ]

        # Floating platform
        if self.has_floater():
            member_with_transition_piece, transition_piece_node_number = (
                self.get_floating_platform_member_with_transition()
            )
            rel += [
                self.get_base_relative_straight(
                    member_with_transition_piece,
                    self.mbdy_names.tower,
                    transition_piece_node_number,
                    1,
                )
            ]

            allMembers = self.windio_dict["components"]["floating_platform"][
                "members"
            ].copy()

            # Remove the member_with_transition_piece from the allMembers list
            # All other members are going to be defined relative to that one
            member_with_transition_piece_objRef = (
                self.get_floating_platform_item_by_name(
                    "members", member_with_transition_piece
                )
            )
            allMembers.remove(member_with_transition_piece_objRef)

            for member_ in allMembers:
                current_member_name = member_["name"]
                node1_xyz_this_member = member_["jointObjRef"][0]["xyz"]
                rel += [
                    self.get_base_relative_straight(
                        member_with_transition_piece,
                        current_member_name,
                        0,
                        0,
                        relpos=[0.0, 0.0, 0.0],
                    )
                ]

        # Tower->Towertop
        rel += [
            self.get_base_relative_straight(
                self.mbdy_names.tower, self.mbdy_names.towertop
            )
        ]

        # Towertop->connector
        rel += [self.get_towertop_connector()]

        # Connector->Shaft
        rel += [
            self.get_base_relative_straight(
                self.mbdy_names.connector, self.mbdy_names.shaft
            )
        ]
        if self.init_rotor_speed is None:
            raise ValueError("`init_rotor_speed` need to be set")
        rel[-1]["mbdy2_ini_rotvec_d1"] = [0.0, 0.0, -1.0, self.init_rotor_speed]

        # Shaft->hubs
        for i in range(self.windio_dict["assembly"]["number_of_blades"]):
            rel += [self.get_shaft_hub(i)]

        # hubs->blade
        for i in range(self.windio_dict["assembly"]["number_of_blades"]):
            rel += [
                self.get_base_relative_straight(
                    self.get_full_mbdy_name(self.mbdy_names.hub, i + 1),
                    self.get_full_mbdy_name(self.mbdy_names.blade, i + 1),
                    angle=self.init_blade_pitch,
                )
            ]
        return rel

    def get_base_relative_straight(
        self,
        mbdy1,
        mbdy2,
        inode1="last",
        inode2=1,
        relpos=None,
        angle=0.0,
    ):

        out = dict(
            mbdy1=[mbdy1, inode1],
            mbdy2=[mbdy2, inode2],
            mbdy2_eulerang=[[0.0, 0.0, -angle]],
        )
        if relpos is not None:
            out["relpos"] = [relpos]
        return out

    def get_towertop_connector(self):
        tt_s = self.get_base_relative_straight(
            self.mbdy_names.towertop, self.mbdy_names.connector
        )
        tilt_deg = rad2deg(
            self.windio_dict["components"]["nacelle"]["drivetrain"]["uptilt"]
        )
        tt_s["mbdy2_eulerang"] = [
            [90.0, 0.0, 0.0],
            [tilt_deg, 0.0, 0.0],
        ]
        return tt_s

    def get_shaft_hub(self, i):
        cone = rad2deg(self.windio_dict["components"]["hub"]["cone_angle"])
        nb = self.windio_dict["assembly"]["number_of_blades"]
        ang = 180 - i * 360 / nb
        s_hub = self.get_base_relative_straight(
            self.mbdy_names.shaft, self.get_full_mbdy_name(self.mbdy_names.hub, i + 1)
        )
        s_hub["mbdy2_eulerang"] = [
            [-90.0, 0.0, 0.0],
            [0.0, ang, 0.0],
            [cone, 0.0, 0.0],
        ]
        return s_hub
