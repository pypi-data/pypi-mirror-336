import copy
import random

import aesoptparam as apm
import numpy as np

from ...common import windio_converter_base
from ...utils import compute_curve_length, interp, jp, rad2deg


class _windio_to_hawc2_base(apm.AESOptParameterized):

    def get_blade_c2def(self, grid):
        bos = self.windio_dict["components"]["blade"]["outer_shape_bem"]
        # Extract data from windio
        x = interp(grid, *jp("reference_axis.x.[grid, values]", bos))
        y = interp(grid, *jp("reference_axis.y.[grid, values]", bos))
        z = interp(grid, *jp("reference_axis.z.[grid, values]", bos))
        twist_deg = rad2deg(interp(grid, *jp("twist.[grid, values]", bos)))
        return (x, y, z, twist_deg)

    def get_curve_length(self, name, grid):
        axis = self.windio_dict["components"][name]["outer_shape_bem"]["reference_axis"]

        # Compute axis length
        x = interp(grid, axis["x"]["grid"], axis["x"]["values"])
        y = interp(grid, axis["y"]["grid"], axis["y"]["values"])
        z = interp(grid, axis["z"]["grid"], axis["z"]["values"])
        s = compute_curve_length(x, y, z)
        return s

    def get_connector_shaft_length(self):
        tilt_rad = self.windio_dict["components"]["nacelle"]["drivetrain"]["uptilt"]
        overhang = self.windio_dict["components"]["nacelle"]["drivetrain"]["overhang"]
        return overhang / np.cos(tilt_rad)

    def get_towertop_length(self):
        tilt_rad = self.windio_dict["components"]["nacelle"]["drivetrain"]["uptilt"]
        con_shaft_len = self.get_connector_shaft_length()
        return self.windio_dict["components"]["nacelle"]["drivetrain"][
            "distance_tt_hub"
        ] - con_shaft_len * np.sin(tilt_rad)

    def get_full_mbdy_name(self, mbdy_name, imbdy=None):
        if not imbdy is None:
            return mbdy_name + str(imbdy)
        return mbdy_name

    def has_monopile(self):
        return "monopile" in self.windio_dict["components"]

    def has_floater(self):
        return "floating_platform" in self.windio_dict["components"]

    def has_mooring(self):
        return "mooring" in self.windio_dict["components"]

    def get_no_warnings(self):
        if self.has_parent():
            return self.parent_object.get_no_warnings()
        return self.no_warnings


class floater_mooring_base:
    def preprocessFloatingPlatformBodyMembers(self):
        # See the following link for an explanation of the taxonomy
        # https://windio.readthedocs.io/en/latest/source/floating.html

        # Step 1: get joints.
        # Dictionary of joints with name, location in xyz coordinates,
        # material, thickness, hydro coefficients.
        joints = self.windio_dict["components"]["floating_platform"]["joints"]
        for joint_ in joints:

            isCylindricalCoordinates = joint_.get("cylindrical", False)
            if isCylindricalCoordinates:
                r, theta, z = joint_.get("location")
                x = r * np.cos(theta)
                y = r * np.sin(theta)
            else:
                x, y, z = joint_.get("location")

            joint_["xyz"] = np.array([x, y, z])
            joint_["memberObjRef"] = []

        # Step 2: get the axial joints and store them in dictionary.
        # They are nested inside members. Some members are defined
        # by joints hosted by other members, so we need to do some kind of an iterative
        # procedure to find out what joints are relative to which member.

        members = self.windio_dict["components"]["floating_platform"]["members"]
        membersSolved = np.full(len(members), False)
        imembers = np.arange(len(members))

        allJoints = self.windio_dict["components"]["floating_platform"]["joints"]

        while not np.all(membersSolved):

            for imember in imembers:
                member_ = members[imember]
                if membersSolved[imember]:  # Skip if already solved
                    continue
                try:
                    # Get the endpoint joints
                    joint1Name, joint2Name = member_["joint1"], member_["joint2"]
                    # TODO: replace with jmespath syntax
                    joint1 = [j_ for j_ in allJoints if j_["name"] == joint1Name][0]
                    joint2 = [j_ for j_ in allJoints if j_["name"] == joint2Name][0]

                    # Save a reference to the members connected to the joint
                    # I need to use the "get_floating_platform_item" as I want a reference to the original member dict,
                    # and not the  the membersToBeProcessed which is just a working copy.
                    joint1["memberObjRef"].append(
                        self.get_floating_platform_item_by_name(
                            "members", member_["name"]
                        )
                    )
                    joint2["memberObjRef"].append(
                        self.get_floating_platform_item_by_name(
                            "members", member_["name"]
                        )
                    )

                    # The position of the axial joints is linearly interpolated
                    # from the endpoint joints.
                    if "axial_joints" in member_:
                        for axial_joint_ in member_["axial_joints"]:

                            j1Coord, j2Coord = joint1["xyz"], joint2["xyz"]

                            newJoint = dict()

                            # Save a reference to the members connected to the axial joint
                            newJoint["memberObjRef"] = []
                            newJoint["memberObjRef"].append(
                                self.get_floating_platform_item_by_name(
                                    "members", member_["name"]
                                )
                            )

                            newJoint["name"] = axial_joint_["name"]
                            newJoint["xyz"] = j1Coord + axial_joint_["grid"] * (
                                j2Coord - j1Coord
                            )

                            allJoints.append(newJoint)
                    membersSolved[imember] = True
                except (
                    KeyError
                ) as e:  # ouch, the member is defined by axial joints thare are not defined yet
                    pass

            random.shuffle(imembers)

        # Save an object reference inside the member dictionary
        # for later use.
        members = self.windio_dict["components"]["floating_platform"]["members"]
        for member_ in members:
            joint1Name, joint2Name = member_["joint1"], member_["joint2"]
            # TODO: replace with jmespath syntax
            joint1 = [j_ for j_ in allJoints if j_["name"] == joint1Name][0]
            joint2 = [j_ for j_ in allJoints if j_["name"] == joint2Name][0]

            member_["length"] = np.linalg.norm(joint1["xyz"] - joint2["xyz"], ord=2)
            member_["unit_axial_vector"] = (joint2["xyz"] - joint1["xyz"]) / member_[
                "length"
            ]
            member_["hasCircularSection"] = (
                member_["outer_shape"]["shape"] == "circular"
            )

            if member_["hasCircularSection"]:
                member_["reference_axis"] = {}
                member_["reference_axis"]["grid"] = np.array(
                    member_["outer_shape"]["outer_diameter"]["grid"]
                )
                member_["reference_axis"]["values"] = (
                    member_["length"] * member_["reference_axis"]["grid"]
                )
            else:
                raise NotImplementedError(
                    "Non-cylindrical floater bodies not implemented yet."
                )

            # Create an array to store the joints references
            member_["jointObjRef"] = np.empty(
                len(member_["reference_axis"]["grid"]), dtype=type(joint1)
            )
            member_["jointObjRef"][0] = joint1
            member_["jointObjRef"][-1] = joint2

            # Make a node, i.e. a grid point, where axial joints are located.
            # It will be useful to specify the constraints of the members later.
            if self.has_axial_joints(member_["name"]):
                for axj_ in member_["axial_joints"]:
                    # add the point to the grid
                    if axj_["grid"] not in member_["reference_axis"]["grid"]:
                        indexOfInsertion = np.searchsorted(
                            member_["reference_axis"]["grid"], axj_["grid"]
                        )
                        member_["reference_axis"]["grid"] = np.insert(
                            member_["reference_axis"]["grid"],
                            indexOfInsertion,
                            axj_["grid"],
                        )
                        member_["jointObjRef"] = np.insert(
                            member_["jointObjRef"], indexOfInsertion, axj_
                        )
                        member_["reference_axis"]["values"] = (
                            member_["length"] * member_["reference_axis"]["grid"]
                        )

    def preprocessMooringMembers(self):
        # Step 1: find out nodes.
        # Nodes are defined based on joints.
        # Nodes can be fixed (fixed to global)
        # or vessel (fixed to body)

        allNodes = self.windio_dict["components"]["mooring"]["nodes"]

        floatingPlatform = self.windio_dict["components"]["floating_platform"]
        mooringSystem = self.windio_dict["components"]["mooring"]

        for node_ in allNodes:
            this_joint_name = node_["joint"]
            this_node_name = node_["name"]
            joint_at_this_node = jp(
                f"joints[?name=='{this_joint_name}']|[0]", floatingPlatform
            )

            # Each node => 1 joint only.
            node_["jointObjRef"] = joint_at_this_node

        # Find all lines for each joint
        allJoints = self.windio_dict["components"]["floating_platform"]["joints"]
        for joint_ in allJoints:
            # Each joint => 1 node
            this_joint_name = joint_["name"]
            node_at_this_joint = jp(
                f"nodes[?joint=='{this_joint_name}']|[0]",
                mooringSystem,
                return_value=False,
            )

            # Each node => can connect multiple lines
            if node_at_this_joint is not None:
                this_node_name = node_at_this_joint["name"]
                lines_with_this_node = jp(
                    f"lines[?node1=='{this_node_name}'||node2=='{this_node_name}']",
                    mooringSystem,
                )
                joint_["lineObjRef"] = lines_with_this_node

        # Step 2: find out lines.
        # Lines are defined between nodes.
        # Lines have unstretched length.
        # Lines have a volume equivalent diameter => estimate mass in water.
        # Lines have a type. A type defines the mass and hydro properties.

        allLines = self.windio_dict["components"]["mooring"]["lines"]

        for line_ in allLines:
            node1Name, node2Name = line_["node1"], line_["node2"]
            # TODO: replace with jmespath syntax
            node1 = [j_ for j_ in allNodes if j_["name"] == node1Name][0]
            node2 = [j_ for j_ in allNodes if j_["name"] == node2Name][0]
            line_["nodeObjRef"] = []
            line_["nodeObjRef"].append(node1)
            line_["nodeObjRef"].append(node2)
            line_["number_of_nodes"] = 20

    def get_floating_platform_item_by_name(self, item_type, name_of_item):
        return [
            member_
            for member_ in self.windio_dict["components"]["floating_platform"][
                item_type
            ]
            if member_["name"] == name_of_item
        ][0]

    def get_mooring_system_item_by_name(self, item_type, name_of_item):
        return [
            member_
            for member_ in self.windio_dict["components"]["mooring"][item_type]
            if member_["name"] == name_of_item
        ][0]

    def has_axial_joints(self, name_of_floater_member):
        this_member = [
            member_
            for member_ in self.windio_dict["components"]["floating_platform"][
                "members"
            ]
            if member_["name"] == name_of_floater_member
        ][0]
        axial_joints_list = this_member.get("axial_joints", None)
        if axial_joints_list is None:
            return False
        else:
            return True

    def get_joint_type(self, jointName):

        jointObjRef = self.get_floating_platform_item_by_name("joints", jointName)
        reactions = jointObjRef.get("reactions", None)

        if reactions is None:
            return "fix1"
        else:
            if all(reactions.values()):
                return "fix1"
            else:
                raise NotImplementedError(
                    "Only fix1 joints are implemented for the floater at the moment"
                )

    def get_node_constraints(self, nodeName):
        nodeObjRef = self.get_mooring_system_item_by_name("nodes", nodeName)

        if nodeObjRef["node_type"] == "fixed":  # Line to global.
            esys_node = []
            init = "cstrbarfixedtoglobal_init"
            update = "cstrbarfixedtoglobal_update"
            nbodies, nesys = 0, 1

            this_nodes_line = nodeObjRef["jointObjRef"]["lineObjRef"][0]
            lineNodeNumber = (
                1
                if this_nodes_line["node1"] == nodeObjRef["name"]
                else 1 + line_["number_of_nodes"]
            )
            esys_node.append([this_nodes_line["name"], lineNodeNumber])

        elif nodeObjRef["node_type"] == "vessel":  # Line to body.
            init = "cstrbarsfixedtobody_init"
            update = "cstrbarsfixedtobody_update"

            # Each node => 1 joint only.
            this_nodes_joint = nodeObjRef["jointObjRef"]
            # 1 joint => can connect multiple bodies
            # 1 joint => can connect multiple lines
            this_nodes_bodies = nodeObjRef["jointObjRef"]["memberObjRef"]
            this_nodes_lines = nodeObjRef["jointObjRef"]["lineObjRef"]

            nbodies, nesys = len(this_nodes_bodies), len(this_nodes_lines)

            # I know the correspondance between joint name and mbody HAWC2 nodes.
            mbdy_node = []
            for member_ in this_nodes_bodies:
                print(this_nodes_joint["name"])
                memberNodeNumber = 1 + [
                    j_["name"] for j_ in member_["jointObjRef"]
                ].index(this_nodes_joint["name"])
                mbdy_node.append([member_["name"], memberNodeNumber])

            esys_node = []
            for line_ in this_nodes_lines:
                # Line: element 1 => node1
                #       element last => node2
                lineNodeNumber = (
                    1
                    if line_["node1"] == nodeObjRef["name"]
                    else 1 + line_["number_of_nodes"]
                )
                esys_node.append([line_["name"], lineNodeNumber])

        elif nodeObjRef["node_type"] == "connection":  # Line to line.
            init = "cstrbarfixedtobar_init"
            update = "cstrbarfixedtobar_update"
            # Each node => multiple lines

            this_nodes_lines = nodeObjRef["jointObjRef"]["lineObjRef"]
            nbodies, nesys = 0, len(this_nodes_lines)

            esys_node = []
            for line_ in this_nodes_lines:
                # Line: element 1 => node1
                #       element last => node2
                lineNodeNumber = (
                    1
                    if line_["node1"] == nodeObjRef["name"]
                    else 1 + line_["number_of_nodes"]
                )
                esys_node.append([line_["name"], lineNodeNumber])

        constraint = dict()
        constraint["ID"] = 10.0
        constraint["neq"] = 3
        constraint["nesys"] = nesys
        if nesys > 0:
            for e_n_ in esys_node:
                constraint["esys_node"] = e_n_
        constraint["nbodies"] = nbodies
        if nbodies > 0:
            for m_n_ in mbdy_node:
                constraint["mbdy_node"] = m_n_
        constraint["init"] = init
        constraint["update"] = update

        return constraint

    def get_floating_platform_member_with_transition(self):
        allMembers = self.windio_dict["components"]["floating_platform"]["members"]

        # Find out where to install the tower
        for i_this, this_member in enumerate(allMembers):
            for j_this, joint_this_member in enumerate(this_member["jointObjRef"], 1):
                try:
                    if joint_this_member["transition"]:
                        member_with_transition_piece = this_member["name"]
                        transition_piece_node_number = j_this
                        break
                except KeyError:
                    pass

        return member_with_transition_piece, transition_piece_node_number

    def get_fix1(self, mbdy1, mbdy2):
        return dict(
            mbdy1=[mbdy1, "last"],
            mbdy2=[mbdy2, 1],
        )


class windio_to_hawc2_base(
    windio_converter_base, _windio_to_hawc2_base, floater_mooring_base
):
    pass


class windio_to_hawc2_child(_windio_to_hawc2_base):
    @property
    def windio_dict(self):
        if self.has_parent():
            return self.parent_object.windio_dict
        return self.windio_dict


class mbdy_names(apm.AESOptParameterized):
    """Main body names"""

    monopile = apm.AESOptString(
        "monopile",
        doc="`main_body` name for the monopile body",
        precedence=0.20,
    )
    tower = apm.AESOptString(
        "tower",
        doc="`main_body` name for the tower body",
        precedence=0.21,
    )
    towertop = apm.AESOptString(
        "towertop",
        doc="`main_body` name for the towertop body",
        precedence=0.22,
    )
    connector = apm.AESOptString(
        "connector",
        doc="`main_body` name for the connector body",
        precedence=0.23,
    )
    shaft = apm.AESOptString(
        "shaft",
        doc="`main_body` name for the shaft body",
        precedence=0.24,
    )
    hub = apm.AESOptString(
        "hub",
        doc="`main_body` name for the hub bodies (base name for hub1, hub2, ..)",
        precedence=0.25,
    )
    blade = apm.AESOptString(
        "blade",
        doc="`main_body` name for the blade body (base name for blade1, blade2, ..)",
        precedence=0.26,
    )


class grids(apm.AESOptParameterized):
    """Settings for grids used doing the conversion"""

    ae = apm.AESOptArray(
        lambda self: self.get_grid("ae"), doc="For AE-file (default `blade`)"
    )
    monopile = apm.AESOptArray(
        lambda self: self.get_grid("monopile"),
        doc="For monopile C2-def (default `.monopile.outer_shape_bem.z.grid`)",
    )
    monopile_st = apm.AESOptArray(
        lambda self: self.get_grid("monopile_st"),
        doc="For monopile ST (default `monopile`)",
    )
    tower = apm.AESOptArray(
        lambda self: self.get_grid("tower"),
        doc="For tower C2-def (default `.tower.z.grid`)",
    )
    tower_st = apm.AESOptArray(
        lambda self: self.get_grid("tower_st"), doc="For tower ST (default `tower`)"
    )
    tower_drag = apm.AESOptArray(
        lambda self: self.get_grid("tower_drag"),
        doc="Aerodrag for the tower (default `.tower.drag_coefficient.grid`)",
    )
    connector_drag = apm.AESOptArray(
        lambda self: self.get_grid("connector_drag"),
        doc="Aerodrag connector body (nacelle drag)",
    )
    shaft_drag = apm.AESOptArray(
        lambda self: self.get_grid("shaft_drag"),
        doc="Aerodrag shaft body (nacelle drag)",
    )
    blade = apm.AESOptArray(
        lambda self: self.get_grid("blade"),
        doc="For blade C2-def grid (default `.blade.outer_shape_bem.z.grid`)",
    )
    blade_st = apm.AESOptArray(
        lambda self: self.get_grid("blade_st"),
        doc="For blade ST-file (default `blade`)",
    )

    def get_grid(self, name):
        if name == "monopile":
            return self.parent_object.windio_dict["components"]["monopile"][
                "outer_shape_bem"
            ]["reference_axis"]["z"]["grid"]
        elif name == "tower":
            return self.parent_object.windio_dict["components"]["tower"][
                "outer_shape_bem"
            ]["reference_axis"]["z"]["grid"]
        elif name == "blade":
            return self.parent_object.windio_dict["components"]["blade"][
                "outer_shape_bem"
            ]["reference_axis"]["z"]["grid"]
        elif name.endswith("_st"):
            return self.get_grid(name[:-3])
        elif name == "ae":
            return self.get_grid("blade")
        elif name == "tower_drag":
            return self.parent_object.windio_dict["components"]["tower"][
                "outer_shape_bem"
            ]["drag_coefficient"]["grid"]
        elif name in ["connector_drag", "shaft_drag"]:
            return np.array([0, 1])
        else:
            raise NotImplementedError(f"Unknown grid for '{name}'")


class filenames(apm.AESOptParameterized):
    """Setting for output filenames"""

    base_name = apm.AESOptString(
        None,
        doc="Base name used for filenames (e.g. base_name_htc.dat, base_name_pc.dat, ..). None will not use any base name (e.g. htc.dat, pc.dat, ..)",
        precedence=0.0,
    )
    data_path = apm.AESOptString(
        "data",
        doc="Base path used for all data files except for HTC-file",
        precedence=0.01,
    )
    htc = apm.AESOptString(
        lambda self: self.get_filename("htc"),
        doc="HTC-filename for the output HTC-file.",
        precedence=0.02,
    )
    ae = apm.AESOptString(
        lambda self: self.get_data_filename("ae"),
        doc="AE-filename for the output AE-file.",
        precedence=0.03,
    )
    pc = apm.AESOptString(
        lambda self: self.get_data_filename("pc"),
        doc="PC-filename for the output PC-file.",
        precedence=0.04,
    )
    tower = apm.AESOptString(
        lambda self: self.get_st_filename("tower"),
        doc="Tower ST-filename.",
        precedence=0.05,
    )
    towertop = apm.AESOptString(
        lambda self: self.get_st_filename("towertop"),
        doc="Tower-top ST-filename.",
        precedence=0.06,
    )
    connector = apm.AESOptString(
        lambda self: self.get_st_filename("connector"),
        doc="Connector ST-filename.",
        precedence=0.07,
    )
    shaft = apm.AESOptString(
        lambda self: self.get_st_filename("shaft"),
        doc="Shaft ST-filename.",
        precedence=0.08,
    )
    hub = apm.AESOptString(
        lambda self: self.get_st_filename("hub"),
        doc="Hub ST-filename.",
        precedence=0.09,
    )
    blade = apm.AESOptString(
        lambda self: self.get_st_filename("blade"),
        doc="Blade ST-filename.",
        precedence=0.10,
    )
    monopile = apm.AESOptString(
        lambda self: self.get_st_filename("monopile"),
        doc="Monopile ST-filename.",
        precedence=0.11,
    )
    floater = apm.AESOptString(
        lambda self: self.get_st_filename("floater"),
        doc="Floater platform ST-filename.",
        precedence=0.12,
    )

    def get_filename(self, ftype, name=None):
        names = []
        if self.base_name is not None:
            names.append(self.base_name)
        if name is not None:
            names.append(name)
        names.append(ftype)
        return "_".join(names) + ".dat"

    def get_data_filename(self, ftype, name=None):
        fname = ""
        if not self.data_path is None:
            fname += "./" + self.data_path + "/"
        return fname + self.get_filename(ftype, name)

    def get_st_filename(self, name):
        return self.get_data_filename("st", name)


class nbodies(apm.AESOptParameterized):
    """`nbodies` used for each of the `main_body`s"""

    monopile = apm.AESOptNumber(
        lambda self: self.get_nbodies("monopile"), doc="`nbodies` for the monopile"
    )
    tower = apm.AESOptNumber(
        lambda self: self.get_nbodies("tower"), doc="`nbodies` for the tower"
    )
    towertop = apm.AESOptNumber(1, doc="`nbodies` for the towertop")
    connector = apm.AESOptNumber(1, doc="`nbodies` for the connector")
    shaft = apm.AESOptNumber(1, doc="`nbodies` for the monopile")
    hub = apm.AESOptNumber(1, doc="`nbodies` for the hub")
    blade = apm.AESOptNumber(
        lambda self: self.get_nbodies("blade"), doc="`nbodies` for the monopile"
    )

    def get_nbodies(self, name):
        if self.has_parent():
            return len(self.parent_object.grids[name]) - 1
        else:
            raise RuntimeError("`nbodies` need to be a ``.SubParametrized` instance")


def get_design_TSR_from_windIO(self):
    """Get design TSR from the windIO dict if present - otherwise return `None`"""
    return self[".."].windio_dict.get("control", {}).get("torque", {}).get("tsr", None)


class dtu_we_controller(apm.AESOptParameterized):
    """Settings for creating input for the DTU WE Controller"""

    TSR_design = apm.AESOptNumber(
        get_design_TSR_from_windIO, doc="Design TSR related to the design CP"
    )
    CP_design = apm.AESOptNumber(0.48, doc="Design CP")
    add_controller_block = apm.AESOptBoolean(
        lambda self: not self.TSR_design is None,
        doc="Flag for adding the DTU WE Controller block to the HTC",
    )


# Default methods for parameters
def get_inipos(self):
    if self.has_monopile():
        return [
            0.0,
            0.0,
            -self.windio_dict["components"]["monopile"]["outer_shape_bem"][
                "reference_axis"
            ]["z"]["values"][0],
        ]
    return np.array([0.0, 0.0, 0.0])


# Parameters
init_blade_pitch = apm.AESOptNumber(0, doc="Initial blade pitch angle", units="deg")
init_rotor_speed = apm.AESOptNumber(doc="Initial rotor speed", units="rad/s")
base_inipos = apm.AESOptArray(
    lambda self: get_inipos(self),
    shape=(3,),
    doc="Initial position of the base body",
)
shaft_length = apm.AESOptNumber(
    doc="Length of the shaft. Using `connector_shaft_ratio` if not set.",
    units="m",
)
connector_shaft_ratio = apm.AESOptNumber(
    0.5,
    doc="Ratio between the connector and shaft (`shaft_length=connector_shaft_ratio*connector_shaft_length`). Only used if `shaft_length` is not set.",
    bounds=(0, 1),
    inclusive_bounds=(False, False),
)
use_blade_FPM = apm.AESOptBoolean(
    True, doc="Flag for using Fully-Populated-Matrix (FPM) for blade ST-file"
)
use_constant_rotor_speed = apm.AESOptBoolean(
    False, doc="Flag for enabling constant rotor speed"
)
# class polar(apm.AESOptParameterized):
#    polar_index = apm.AESOptNumber()
#
#
# class airfoil(apm.AESOptParameterized):
#    use_airfoil = apm.Boolean(True)
#
#
# class airfoils2polar(windio_converter_base):
#    aoa_rad = apm.AESOptArray()
#    polar = apm.SubParameterized()
#
#    def convert(self):
#        pass
