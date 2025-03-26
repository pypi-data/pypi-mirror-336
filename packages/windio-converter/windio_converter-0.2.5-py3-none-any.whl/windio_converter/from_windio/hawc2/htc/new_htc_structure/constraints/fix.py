import warnings

import aesoptparam as apm
import numpy as np

from ....common import mbdy_names
from ..common import new_htc_structure_base


class fix0(new_htc_structure_base):
    tower_mbdy_name = apm.copy_param_ref(
        mbdy_names.param.tower, "........mbdy_names.tower"
    )
    monopile_mbdy_name = apm.copy_param_ref(
        mbdy_names.param.monopile, "........mbdy_names.monopile"
    )

    def convert(self):
        if self.has_monopile():
            return [dict(mbdy=self.monopile_mbdy_name)]
        elif self.has_floater():
            return None
        else:
            return [dict(mbdy=self.tower_mbdy_name)]


class fix1(new_htc_structure_base):
    tower_mbdy_name = apm.copy_param_ref(
        mbdy_names.param.tower, "........mbdy_names.tower"
    )
    monopile_mbdy_name = apm.copy_param_ref(
        mbdy_names.param.monopile, "........mbdy_names.monopile"
    )
    towertop_mbdy_name = apm.copy_param_ref(
        mbdy_names.param.towertop, "........mbdy_names.towertop"
    )
    connector_mbdy_name = apm.copy_param_ref(
        mbdy_names.param.connector, "........mbdy_names.connector"
    )
    shaft_mbdy_name = apm.copy_param_ref(
        mbdy_names.param.shaft, "........mbdy_names.shaft"
    )
    hub_mbdy_name = apm.copy_param_ref(mbdy_names.param.hub, "........mbdy_names.hub")

    def convert(self):
        fix1 = []
        if self.has_monopile():
            fix1 += [self.get_fix1(self.monopile_mbdy_name, self.tower_mbdy_name)]
        if self.has_floater():
            fix1 += self.get_fix1_floating_platform()
        fix1 += [self.get_fix1(self.tower_mbdy_name, self.towertop_mbdy_name)]
        fix1 += [self.get_fix1(self.towertop_mbdy_name, self.connector_mbdy_name)]
        for i in range(1, self.windio_dict["assembly"]["number_of_blades"] + 1):
            fix1 += [
                self.get_fix1(
                    self.shaft_mbdy_name, self.get_full_mbdy_name(self.hub_mbdy_name, i)
                )
            ]
        return fix1

    def get_fix1_floating_platform(self):
        members_to_be_constrained, node_number_of_constraint = self.build_fix1_pairs()

        all_constraints = []

        for multibodies, nodes in zip(
            members_to_be_constrained, node_number_of_constraint
        ):
            all_constraints.append(
                dict(
                    mbdy1=[multibodies[0], nodes[0]],
                    mbdy2=[multibodies[1], nodes[1]],
                )
            )

        return all_constraints

    def build_fix1_pairs(self):
        allMembers = self.windio_dict["components"]["floating_platform"]["members"]
        allJoints = self.windio_dict["components"]["floating_platform"]["joints"]

        members_to_be_constrained, node_number_of_constraint = [], []

        for joint_ in allJoints:
            if self.get_joint_type(joint_["name"]) == "fix1":
                # Connect the base member with the other members
                # that share the joint.
                try:
                    baseMember_ = joint_["memberObjRef"][0]
                except IndexError:
                    jointName = joint_["name"]
                    warnings.warn(
                        f"The joint {jointName} is not connected to any member."
                    )
                    continue

                (baseNodenumber,) = (
                    1
                    + np.argwhere(
                        [
                            bm_["name"] == joint_["name"]
                            for bm_ in baseMember_["jointObjRef"]
                        ]
                    )[0]
                )
                for otherMember_ in joint_["memberObjRef"][1:]:
                    (otherNodeNumber,) = (
                        1
                        + np.argwhere(
                            [
                                bm_["name"] == joint_["name"]
                                for bm_ in otherMember_["jointObjRef"]
                            ]
                        )[0]
                    )
                    members_to_be_constrained.append(
                        [baseMember_["name"], otherMember_["name"]]
                    )
                    node_number_of_constraint.append([baseNodenumber, otherNodeNumber])

        # A special fix1 joint for the connection between the tower and the transition piece
        member_with_transition_piece, transition_piece_node_number = (
            self.get_floating_platform_member_with_transition()
        )

        members_to_be_constrained.append(["tower", member_with_transition_piece])
        node_number_of_constraint.append([1, transition_piece_node_number])

        return members_to_be_constrained, node_number_of_constraint
