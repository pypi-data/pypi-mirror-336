import aesoptparam as apm
import numpy as np

from ....common import copy_param
from ....utils import interp
from ..common import filenames, grids, mbdy_names, shaft_length, windio_to_hawc2_child


class aero(windio_to_hawc2_child):
    shaft_mbdy_name = apm.copy_param_ref(mbdy_names.param.shaft, "....mbdy_names.shaft")
    blade_mbdy_name = apm.copy_param_ref(mbdy_names.param.blade, "....mbdy_names.blade")
    ae_filename = apm.copy_param_ref(filenames.param.ae, "....filenames.ae")
    pc_filename = apm.copy_param_ref(filenames.param.pc, "....filenames.pc")

    def convert(self):
        NB = self.windio_dict["assembly"]["number_of_blades"]
        aero = dict(
            nblades=NB,
            hub_vec=[self.shaft_mbdy_name, -3],
            link=[
                [i, "mbdy_c2_def", self.get_full_mbdy_name(self.blade_mbdy_name, i)]
                for i in range(1, NB + 1)
            ],
            ae_filename=self.ae_filename,
            pc_filename=self.pc_filename,
            ae_sets=[1] * NB,
            aero_distribution=["ae_file", 1],
            aerocalc_method=1,
            induction_method=1,
            tiploss_method=1,
            dynstall_method=2,
        )
        return aero


class sections(apm.AESOptParameterized):
    """Number of aero dynamic section to use"""

    tower = apm.Integer(10, doc="Aerodynamic sections for the tower")
    connector = apm.Integer(2, doc="Aerodynamic sections for the connector")
    shaft = apm.Integer(2, doc="Aerodynamic sections for the shaft")


class aerodrag(windio_to_hawc2_child):
    sections = apm.SubParameterized(sections)
    tower_drag_grid = apm.copy_param_ref(grids.param.tower_drag, "....grids.tower_drag")
    tower_grid = apm.copy_param_ref(grids.param.tower, "....grids.tower")
    tower_mbdy_name = apm.copy_param_ref(mbdy_names.param.tower, "....mbdy_names.tower")
    connector_drag_grid = apm.copy_param_ref(
        grids.param.connector_drag, "....grids.connector_drag"
    )
    connector_mbdy_name = apm.copy_param_ref(
        mbdy_names.param.connector, "....mbdy_names.connector"
    )
    shaft_drag_grid = apm.copy_param_ref(grids.param.shaft_drag, "....grids.shaft_drag")
    shaft_mbdy_name = apm.copy_param_ref(mbdy_names.param.shaft, "....mbdy_names.shaft")
    shaft_length = apm.copy_param_ref(shaft_length, "....shaft_length")

    def convert(self):
        return dict(
            aerodrag_element=self.elements(),
        )

    def elements(self):
        # Tower
        tower = self.windio_dict["components"]["tower"]["outer_shape_bem"]
        grid = self.tower_drag_grid
        tower_grid = self.tower_grid
        s = interp(grid, tower_grid, self.get_curve_length("tower", tower_grid))
        D = interp(
            grid, tower["outer_diameter"]["grid"], tower["outer_diameter"]["values"]
        )
        cd = interp(
            grid, tower["drag_coefficient"]["grid"], tower["drag_coefficient"]["values"]
        )
        tower_drag = dict(
            mbdy_name=self.tower_mbdy_name,
            aerodrag_sections=["uniform", self.sections.tower],
            nsec=len(s),
            sec=[[_s, _D, _cd] for _s, _D, _cd in zip(s, D, cd)],
        )

        # Nacelle (converting from 3D drag to 2D drag)
        # Assuming nacelle height is h=2*distance_tt_hub
        h = (
            2
            * self.windio_dict["components"]["nacelle"]["drivetrain"]["distance_tt_hub"]
        )
        CD = self.windio_dict["components"]["nacelle"]["drivetrain"]["drag_coefficient"]
        # Connector
        grid = self.connector_drag_grid
        con_len = self.get_connector_shaft_length() - self.shaft_length
        connector_drag = dict(
            mbdy_name=self.connector_mbdy_name,
            aerodrag_sections=["uniform", self.sections.connector],
            nsec=len(grid),
            sec=[[_s * con_len, CD, h] for _s in grid],
        )
        # Shaft
        grid = self.shaft_drag_grid
        shaft_len = self.shaft_length
        shaft_drag = dict(
            mbdy_name=self.shaft_mbdy_name,
            aerodrag_sections=["uniform", self.sections.shaft],
            nsec=len(grid),
            sec=[[_s * shaft_len, CD, h] for _s in grid],
        )
        return [tower_drag, connector_drag, shaft_drag]


class hydro(windio_to_hawc2_child):
    def convert(self):

        hydro = dict()

        hydro["water_properties"] = self.water_properties()
        hydro["hydro_element"] = self.hydro_elements()

        return hydro

    def water_properties(self):
        return dict(
            rho=self.windio_dict["environment"]["water_density"],
            mwl=0.0,
            mudlevel=self.windio_dict["environment"]["water_depth"],
        )

    def hydro_elements(self):

        # NOTE: the implementation assumes the structure either has a floater or a monopile.
        if self.has_floater():
            return self.assemble_floater_hydro_elements()
        elif self.has_monopile():
            return self.assemble_monopile_hydro_elements()

    def assemble_floater_hydro_elements(self):
        hydro_elements = []
        for member_ in self.windio_dict["components"]["floating_platform"]["members"]:
            if member_["hasCircularSection"]:

                reference_axis = member_["reference_axis"]
                D = np.array(
                    interp(
                        reference_axis["grid"],
                        member_["outer_shape"]["outer_diameter"]["grid"],
                        member_["outer_shape"]["outer_diameter"]["values"],
                    )
                )
                A = 0.25 * D**2 * np.pi
                drdz = np.gradient(0.5 * D, reference_axis["values"])
                nsec = len(A)
                hydro_element = dict(
                    mbdy_name=member_["name"],
                    hydrosections="uniform 10",
                    buoyancy=1,
                    nsec=nsec,
                    sec=[
                        [
                            z_,
                            member_["Ca"],
                            member_["Cd"],
                            A_,
                            A_,
                            D_,
                            drdz_,
                            0.0,
                            0.0,
                            0.0,
                            0.0,
                            0.0,
                            0.0,
                        ]
                        for z_, A_, D_, drdz_ in zip(reference_axis["grid"], A, D, drdz)
                    ],
                )

                hydro_elements.append(hydro_element)

            else:
                thisMemberName = member_["name"]
                raise NotImplementedError(
                    f"Non-circular floater members are not supported yet. Error in member {thisMemberName}"
                )

        return hydro_elements

    def assemble_monopile_hydro_elements(self):
        hydro_elements = []

        # Store a reference to monopile inside member_ to make subsequent calls shorter
        member_ = self.windio_dict["components"]["monopile"]
        outer_shape = member_["outer_shape_bem"]

        # NOTE: assumes that "z" is the reference axis
        reference_axis = outer_shape["reference_axis"]["z"]

        D = np.array(
            interp(
                reference_axis["grid"],
                outer_shape["outer_diameter"]["grid"],
                outer_shape["outer_diameter"]["values"],
            )
        )

        Cd = np.array(
            interp(
                reference_axis["grid"],
                outer_shape["drag_coefficient"]["grid"],
                outer_shape["drag_coefficient"]["values"],
            )
        )

        # FIXME: Ca is now hardcoded and it assumed the monopile has a circular section
        Ca = 1.0

        A = 0.25 * D**2 * np.pi
        drdz = np.gradient(0.5 * D, reference_axis["values"])
        nsec = len(A)
        hydro_element = dict(
            mbdy_name="monopile",
            hydrosections="uniform 10",
            buoyancy=1,
            nsec=nsec,
            sec=[
                [
                    z_,
                    Ca,
                    Cd_,
                    A_,
                    A_,
                    D_,
                    drdz_,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                ]
                for z_, A_, D_, drdz_, Cd_ in zip(
                    reference_axis["grid"], A, D, drdz, Cd
                )
            ],
        )

        hydro_elements.append(hydro_element)

        return hydro_elements
