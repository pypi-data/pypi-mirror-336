import aesoptparam as apm
import numpy as np

from ....utils import interp, jp
from ..common import grids
from .common import st_base


class circular_body(st_base):
    def convert(self):
        name = type(self).__name__
        data = self.windio_dict["components"][name]
        grid = self.grid
        s = self.get_curve_length(name, grid)

        # Get outer diameter
        D = interp(
            grid,
            data["outer_shape_bem"]["outer_diameter"]["grid"],
            data["outer_shape_bem"]["outer_diameter"]["values"],
        )

        # Get wall thickness
        layer = data["internal_structure_2d_fem"]["layers"][0]
        t = interp(grid, layer["thickness"]["grid"], layer["thickness"]["values"])

        # Get matertial properties
        mat_name = layer["material"]
        mat_props = jp(f"materials[?name=='{mat_name}'] |[0]", self.windio_dict)
        if isinstance(mat_props["E"], list):
            E = mat_props["E"][0]
            if any([abs(_E - E) for _E in mat_props["E"]]):
                raise RuntimeError(
                    f"The material for {name} with material name {mat_name} need to be orthopertopric (all values for E need to be the same)"
                )
        else:
            E = mat_props["E"]
        if "G" not in mat_props:
            if "nu" not in mat_props:
                raise RuntimeError(
                    f"Eiter `G` or `nu` need to be specificized for isotropic materials (component: {name}, material name: {mat_name})"
                )
            G = E / (2 * (1 - mat_props["nu"]))
        elif isinstance(mat_props["G"], list):
            G = mat_props["G"][0]
            if any([abs(_G - G) for _G in mat_props["G"]]):
                raise RuntimeError(
                    f"The material for {name} with material name {mat_name} need to be orthopertopric (all values for G need to be the same)"
                )
        else:
            G = mat_props["G"]
        rho = mat_props["rho"]
        return [[self.get_st_circular_body(s, D, t, E, G, rho)]]

    def get_st_circular_body(self, s, D, t, E, G, rho):
        n = len(s)
        Ix = [
            1 / 4 * np.pi * ((_D / 2) ** 4 - (_D / 2 - _t) ** 4) for _t, _D in zip(t, D)
        ]
        I_torsion = [2 * _I for _I in Ix]
        shear_factor = [0.5 + 0.75 * _t / (_D / 2) for _t, _D in zip(t, D)]
        A = [np.pi * _t * _D * (1 - _t / _D) for _t, _D in zip(t, D)]
        md = [rho * _A for _A in A]
        ri = [np.sqrt(_I / _A) for _I, _A in zip(Ix, A)]
        values = [
            s,  # tower station
            md,  # mass/length
            [0.0] * n,  # center of mass, x
            [0.0] * n,  # center of mass, y
            ri,  # radius gyration, x
            ri,  # radius gyration, y
            [0.0] * n,  # shear center, x
            [0.0] * n,  # shear center, y
            [E] * n,  # young's modulus
            [G] * n,  # shear modulus
            Ix,  # area moment of inertia, x
            Ix,  # area moment of inertia, y
            I_torsion,  # torsional stiffness constant
            shear_factor,  # shear reduction, x
            shear_factor,  # shear reduction, y
            A,  # cross-sectional area
            [0.0] * n,  # structural pitch
            [0.0] * n,  # elastic center, x
            [0.0] * n,  # elastic center, y
        ]
        return dict(zip(self.header_classic(), values))


class tower(circular_body):
    """Tower ST-file"""

    grid = apm.copy_param_ref(grids.param.tower_st, "....grids.tower_st")


class monopile(tower):
    """Monopile ST-file"""

    grid = apm.copy_param_ref(grids.param.monopile_st, "....grids.monopile_st")


class floater(circular_body):
    def convert(self):
        allFloaterBodies = {}

        for member_ in self.windio_dict["components"]["floating_platform"]["members"]:

            if member_["hasCircularSection"]:

                reference_axis = member_["reference_axis"]

                D = interp(
                    reference_axis["grid"],
                    member_["outer_shape"]["outer_diameter"]["grid"],
                    member_["outer_shape"]["outer_diameter"]["values"],
                )

                layer = member_["internal_structure"]["layers"][0]
                thickness = interp(
                    reference_axis["grid"],
                    layer["thickness"]["grid"],
                    layer["thickness"]["values"],
                )

                # Find material properties for current member
                material = layer["material"]
                material_properties = jp(
                    f"materials[?name=='{material}'] |[0]", self.windio_dict
                )
                E = material_properties["E"]
                G = material_properties["G"]
                rho = material_properties["rho"]

                member_["s"] = member_["reference_axis"]["grid"] * member_["length"]

                allFloaterBodies[member_["name"]] = [
                    self.get_st_circular_body(member_["s"], D, thickness, E, G, rho)
                ]

            else:
                raise NotImplementedError(
                    "Non-cylindrical floater bodies not implemented yet."
                )

        return allFloaterBodies
