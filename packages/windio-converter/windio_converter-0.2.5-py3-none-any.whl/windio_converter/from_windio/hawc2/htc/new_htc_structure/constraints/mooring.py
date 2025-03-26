from ..common import new_htc_structure_base


class mooring(new_htc_structure_base):
    def convert(self):
        # Create the constraints
        allNodes = self.windio_dict["components"]["mooring"]["nodes"]
        constraints_all_lines = []
        for node_ in allNodes:
            constraints_all_lines.append(
                dict(dll="ESYSMooring.dll", **self.get_node_constraints(node_["name"]))
            )

        return constraints_all_lines

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
