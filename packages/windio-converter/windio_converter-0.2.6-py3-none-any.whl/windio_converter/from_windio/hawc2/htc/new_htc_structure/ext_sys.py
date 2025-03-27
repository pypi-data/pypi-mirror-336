import numpy as np

from .....utils import jp
from .common import new_htc_structure_base


class ext_sys(new_htc_structure_base):
    def convert(self):

        rho_water = self.windio_dict["environment"]["water_density"]
        allLines = self.windio_dict["components"]["mooring"]["lines"]

        # Create the line objects
        ext_sys_all_lines = []

        for line_ in allLines:

            line_type = line_["line_type"]
            mooringSystem = self.windio_dict["components"]["mooring"]
            line_props = jp(f"line_types[?name=='{line_type}']|[0]", mooringSystem)
            mass_per_length_air = line_props["mass_density"]
            mass_per_length_water = (
                line_props["mass_density"]
                - 0.25 * np.pi * line_props["diameter"] ** 2 * rho_water
            )

            data = dict()
            node1 = np.array([*line_["nodeObjRef"][0]["jointObjRef"]["xyz"]])
            node2 = np.array([*line_["nodeObjRef"][1]["jointObjRef"]["xyz"]])
            direction = (node2 - node1) / np.linalg.norm(node2 - node1)
            node2flat = node1 + direction * line_["unstretched_length"]
            node2flat[2] = node1[2]

            data["data start_pos"] = [
                node1[1],
                node1[0],
                -node1[2],
            ]  # Change to HAWC2 coordinates
            # data["data end_pos"] = [node2[1], node2[0], -node2[2]] # Change to HAWC2 coordinates
            data["data end_pos"] = [
                node2flat[1],
                node2flat[0],
                -node2flat[2],
            ]  # Change to HAWC2 coordinates
            data["data cdp_cdl_cm"] = [
                line_props["transverse_drag"],
                line_props["tangential_drag"],
                line_props["transverse_added_mass"],
            ]
            data["data axial_stiff"] = line_props["stiffness"]
            data["data mass"] = [mass_per_length_air, mass_per_length_water]

            data["data bottom_prop"] = [
                self.windio_dict["environment"]["water_depth"],
                0.01,
                0.01,
            ]  # TODO: how to make this general?
            data["data damping_ratio"] = line_props["damping"] / (
                2
                * np.sqrt(
                    mass_per_length_water
                    * 0.25
                    * np.pi
                    * line_props["diameter"] ** 2
                    * line_props["stiffness"]
                )
            )  # BA / 2*sqrt(m/L*A * EA)
            data["data nelem"] = line_["number_of_nodes"]
            data["data end"] = ""

            ext_sys = dict()
            ext_sys["module"] = "elasticbar"
            ext_sys["name"] = line_["name"]
            ext_sys["dll"] = "ESYSMooring.dll"

            ext_sys["ndata"] = len([e_ for e_ in data.keys() if e_.startswith("data")])

            # The data dictionary needs to be preceded by the ndata keyword
            # otherwise ESYSMooring does not know how many lines to expect.
            ext_sys_all_lines.append({**ext_sys, **data})

        return ext_sys_all_lines
