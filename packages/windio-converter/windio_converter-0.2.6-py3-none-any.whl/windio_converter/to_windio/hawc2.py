import numpy as np

from ..utils import (
    Nx6x6_to_Nx21,
    Transform6x6,
    TransformNx6x6,
    compute_curve_length,
    deg2rad,
    degs2rads,
    hz2rads,
    interp,
    jp,
    trapz,
    warn,
)
from ..windio.coordinate_system import convert_coordinate_system


class hawc2_to_windio:
    _windio_version = "1.0"
    _hawc2_version = "12.9"

    def __init__(self, hawc2_dict, **kwargs) -> None:
        self.hawc2_dict = hawc2_dict
        self.no_warnings = kwargs.get("no_warnings", False)
        self.pitch_axis = kwargs.get("pitch_axis", None)
        self.concentrated_mass = kwargs.get("concentrated_mass", {})
        self.pitch_axis = kwargs.get("pitch_axis", None)
        self.grids = kwargs.get("grids", {})
        self.mbdy_names = kwargs.get("mbdy_names", {})
        self.airfoil_names = kwargs.get("airfoil_names", None)
        self.cone_location = kwargs.get("cone_location", {})
        self.cone_location.setdefault("mbdy2", "hub1")
        self.cone_location.setdefault("eulerang_index", -1)
        self.cone_location.setdefault("element_index", 0)
        self.tilt_location = kwargs.get("tilt_location", {})
        self.tilt_location.setdefault("mbdy2", "shaft")
        self.tilt_location.setdefault("eulerang_index", -1)
        self.tilt_location.setdefault("element_index", 0)
        self.shaft_bodies = kwargs.get("shaft_bodies", ["connector", "shaft"])
        self.towertop_bodies = kwargs.get("towertop_bodies", ["towertop"])
        self.drag = kwargs.get("drag", {})
        self.drag.setdefault("tower", "tower")
        self.drag.setdefault("nacelle", "shaft")
        self.control_actuators_parameters = kwargs.get(
            "control_actuators_parameters", {}
        )
        self.control_actuators_parameters.setdefault(
            "rated_power", ["dtu_we_controller", 1]
        )
        self.control_actuators_parameters.setdefault(
            "VS_minspd", ["dtu_we_controller", 2]
        )
        self.control_actuators_parameters.setdefault(
            "max_gen_speed", ["dtu_we_controller", 3]
        )
        self.control_actuators_parameters.setdefault(
            "min_pitch", ["dtu_we_controller", 5]
        )
        self.control_actuators_parameters.setdefault(
            "max_pitch", ["dtu_we_controller", 6]
        )
        self.control_actuators_parameters.setdefault(
            "max_pitch_rate", ["dtu_we_controller", 7]
        )
        self.control_actuators_parameters.setdefault(
            "PC_zeta", ["servo_with_limits", 2]
        )
        self.control_actuators_parameters.setdefault(
            "PC_omega", ["servo_with_limits", 3]
        )
        self.control_actuators_parameters.setdefault("VS_omega", ["generator_servo", 1])
        self.control_actuators_parameters.setdefault("VS_zeta", ["generator_servo", 2])
        self.control_actuators_parameters.setdefault("tsr", ["dtu_we_controller", 49])
        self.control_actuators_parameters.setdefault(
            "hss_brake_duration", ["mech_brake", 4]
        )
        self.control_actuators_parameters.setdefault(
            "hss_brake_torque", ["mech_brake", 1]
        )
        self.control_actuators_parameters.setdefault(
            "hss_brake_start_time", ["mech_brake", 3]
        )
        self.materials_inp = kwargs.get("materials", {})
        self.materials_inp.setdefault("tower", {})
        self.materials_inp["tower"].setdefault("name", "steel")
        self.materials_inp.setdefault("monopile", {})
        self.materials_inp["monopile"].setdefault("name", "steel")

    def __call__(self):
        return convert_coordinate_system(
            self.root(), cs_transform_name="hawc2_to_windio"
        ).convert()

    def root(self):
        return dict(
            windio_version=float(self._windio_version),
            assembly=self.assembly(),
            components=self.components(),
            airfoils=self.airfoils(),
            materials=self.materials(),
            control=self.control(),
            actuators=self.actuators(),
        )

    def assembly(self):
        return dict(number_of_blades=self.hawc2_dict["htc"]["aero"]["nblades"])

    def components(self):
        comp = dict(
            blade=self.components_blade(),
            hub=self.components_hub(),
            nacelle=self.components_nacelle(),
            tower=self.components_tower(),
        )
        if self.has_monopile():
            comp["monopile"] = self.components_monopile()
        return comp

    def components_blade(self):
        return dict(
            outer_shape_bem=self.components_blade_osb(),
            elastic_properties_mb=self.components_blade_epb(),
        )

    def components_blade_osb(self):
        return dict(
            airfoil_position=self.components_blade_airfoil_position(),
            reference_axis=self.components_blade_reference_axis(),
            chord=self.components_blade_chord(),
            twist=self.components_to_blade_twist(),
            pitch_axis=self.components_blade_pitch_axis(),
            rthick=self.components_blade_rthick(),
        )

    def components_blade_airfoil_position(self):
        s, tcs = (np.array(arr) for arr in self.get_blade_grid_and_tc())
        air_names, air_names_tc = (np.array(arr) for arr in self.get_airfoil_names())
        grid = []
        air_pos = []
        # Stepping though s vs t/c and find when airfoil is changed
        for s1, tc1, s2, tc2 in zip(s[:-1], tcs[:-1], s[1:], tcs[1:]):
            dtc_sign = -np.sign(tc2 - tc1)
            loc = (dtc_sign * tc1 >= dtc_sign * air_names_tc) & (
                dtc_sign * air_names_tc > dtc_sign * tc2
            )
            for tc in air_names_tc[loc]:
                # Computing grid value
                s = (tc - tc1) / (tc2 - tc1) * (s2 - s1) + s1
                grid.append(s)
                # Adding airfoil name
                iair = list(air_names_tc).index(tc)
                air_pos.append(air_names[iair])
        return dict(grid=list(grid), labels=list(air_pos))

    def components_blade_reference_axis(self):
        grid_in, x, y, z = self.get_c2def_grid_and_axis("blade", imbdy=1)

        xg = self.get_blade_grid("blade_x")
        yg = self.get_blade_grid("blade_y")
        zg = self.get_blade_grid("blade_z")
        return dict(
            x=dict(grid=xg, values=interp(xg, grid_in, x)),
            y=dict(grid=yg, values=interp(xg, grid_in, y)),
            z=dict(grid=zg, values=interp(xg, grid_in, z)),
            desc="-y,x,z (windio to hawc2 blade)",
            coordinate_system="hawc2 blade",
        )

    def components_blade_chord(self):
        grid = self.get_blade_grid(
            "chord",
        )
        grid_in, chord = self.get_blade_grid_and_chord()
        return dict(grid=grid, values=interp(grid, grid_in, chord))

    def components_to_blade_twist(self):
        grid = self.get_blade_grid(
            "twist",
        )
        grid_in, twist = self.get_blade_grid_and_twist()
        return dict(grid=grid, values=interp(grid, grid_in, -np.array(deg2rad(twist))))

    def components_blade_pitch_axis(self):
        grid = self.get_blade_grid("pitch_axis")
        return dict(
            grid=grid, values=interp(grid, *self.get_blade_grid_and_pitch_axis())
        )

    def components_blade_rthick(self):
        grid_in, tc = self.get_blade_grid_and_tc()
        grid = self.get_blade_grid(
            "rthick",
        )
        return dict(
            grid=grid, values=(np.array(interp(grid, grid_in, tc)) / 100).tolist()
        )

    def components_blade_epb(self):
        warn("components_blade_epb", self.no_warnings)
        # Getting ST data
        st_data = self.get_st_data("blade", 1)
        if not "K11" in st_data:
            # Converting to FPM if classic is given
            st_data = self.convert_st_classic_to_FPM(st_data)

        # ST-grid
        grid_st = [el / st_data["s"][-1] for el in st_data["s"]]

        # Create 6x6 in H2 coordinate system (at elastic center)
        # Stiffness matrix
        K = np.empty((len(grid_st), 6, 6))
        for i, j in zip(*np.triu_indices(6)):
            K[:, i, j] = st_data[f"K{i+1}{j+1}"]
            K[:, j, i] = st_data[f"K{i+1}{j+1}"]
        # Mass matrix
        M = np.zeros((len(grid_st), 6, 6))
        M[:, 0, 0] = M[:, 1, 1] = M[:, 2, 2] = st_data["m"]
        M[:, 0, 5] = M[:, 5, 0] = [
            -m * Ycm for m, Ycm in zip(st_data["m"], st_data["y_cg"])
        ]
        M[:, 1, 5] = M[:, 5, 1] = [
            m * Xcm for m, Xcm in zip(st_data["m"], st_data["x_cg"])
        ]
        M[:, 2, 3] = M[:, 3, 2] = [
            m * Ycm for m, Ycm in zip(st_data["m"], st_data["y_cg"])
        ]
        M[:, 2, 4] = M[:, 4, 2] = [
            -m * Xcm for m, Xcm in zip(st_data["m"], st_data["x_cg"])
        ]
        Ixx = [m * ri_x**2 for m, ri_x in zip(st_data["m"], st_data["ri_x"])]
        M[:, 3, 3] = Ixx
        Iyy = [m * ri_y**2 for m, ri_y in zip(st_data["m"], st_data["ri_y"])]
        M[:, 4, 4] = Iyy
        # TODO: Ixy is implicitly assumed to be 0 - but can in be computed?! (kenloen)
        M[:, 5, 5] = [ixx + iyy for ixx, iyy in zip(Ixx, Iyy)]

        # Remove pitch and translate to C2def axis
        K = TransformNx6x6(
            K,
            -np.array(st_data["xe"]),
            -np.array(st_data["ye"]),
            deg2rad(-np.array(st_data["pitch"])),
        )
        M = TransformNx6x6(
            M,
            -np.array(st_data["xe"]),
            -np.array(st_data["ye"]),
            deg2rad(-np.array(st_data["pitch"])),
        )

        # Rotate to WindIO coordinate system
        for i in range(len(grid_st)):
            K[i] = Transform6x6(K[i], 0, 0, -np.pi / 2)
            M[i] = Transform6x6(M[i], 0, 0, -np.pi / 2)

        # Convert to Nx21
        K_Nx21 = Nx6x6_to_Nx21(K).tolist()
        M_Nx21 = Nx6x6_to_Nx21(M).tolist()
        return dict(
            six_x_six=dict(
                reference_axis=self.components_blade_reference_axis(),
                twist=self.components_to_blade_twist(),
                stiff_matrix=dict(grid=grid_st, values=K_Nx21),
                inertia_matrix=dict(grid=grid_st, values=M_Nx21),
            )
        )

    def components_hub(self):
        mbdy_name = self.get_hawc2_mbdy_name("hub", 1)
        # Diameter
        hub_start = jp(
            f"htc.new_htc_structure.main_body[?name=='{mbdy_name}'] | [0].c2_def.sec[0][1:4]",
            self.hawc2_dict,
        )
        hub_end = jp(
            f"htc.new_htc_structure.main_body[?name=='{mbdy_name}'] | [0].c2_def.sec[-1][1:4]",
            self.hawc2_dict,
        )
        diameter = 2 * sum([(e - s) ** 2 for s, e in zip(hub_start, hub_end)]) ** 0.5
        return dict(
            diameter=diameter,
            cone_angle=deg2rad(self.get_rotor_cone_deg()),
            elastic_properties_mb=self.components_hub_epb(),
        )

    def components_hub_epb(self):
        # From ST-file
        mass, [Ix, Iy, _] = self.get_st_net_mass_inertia("hub", 1)
        nblades = self.hawc2_dict["htc"]["aero"]["nblades"]
        mass *= nblades
        Ix *= nblades
        Iy *= nblades
        Iz = Iy
        if "hub" in self.concentrated_mass:
            cm = self.get_concentrated_mass(**self.concentrated_mass["hub"])
            mass += cm[4]
            Ix += cm[7]
            Iy += cm[5]
            Iz += cm[6]
        # Moment of inertia (Inertia of the hub system, on the hub reference system, which has the x aligned with the rotor axis, and y and z perpendicular to it)
        return dict(system_mass=mass, system_inertia=[Ix, Iy, Iz])

    def components_nacelle(self):
        return dict(drivetrain=self.components_nacelle_drivetrain())

    def components_nacelle_drivetrain(self):
        # Tilt angle
        mbdy2 = self.tilt_location["mbdy2"]
        ieu = self.tilt_location["eulerang_index"]
        iel = self.tilt_location["element_index"]
        tilt_deg = jp(
            f"htc.new_htc_structure.orientation.relative[?mbdy2[0]=='{mbdy2}'] | [0].mbdy2_eulerang[{ieu}][{iel}]",
            self.hawc2_dict,
        )
        tilt_rad = deg2rad(tilt_deg)
        # Computing length from tower center to hub (including tilt)
        L_shaft = 0
        for name in self.shaft_bodies:
            # Only using start and end node
            mbdy_name = self.get_hawc2_mbdy_name(name)
            b_start = jp(
                f"htc.new_htc_structure.main_body[?name=='{mbdy_name}'] | [0].c2_def.sec[0][1:4]",
                self.hawc2_dict,
            )
            b_end = jp(
                f"htc.new_htc_structure.main_body[?name=='{mbdy_name}'] | [0].c2_def.sec[-1][1:4]",
                self.hawc2_dict,
            )
            L_shaft += sum([(e - s) ** 2 for s, e in zip(b_start, b_end)]) ** 0.5
        # Computing length of towertop
        L_towertop = 0
        for name in self.towertop_bodies:
            # Only using start and end node
            mbdy_name = self.get_hawc2_mbdy_name(name)
            b_start = jp(
                f"htc.new_htc_structure.main_body[?name=='{mbdy_name}'] | [0].c2_def.sec[0][1:4]",
                self.hawc2_dict,
            )
            b_end = jp(
                f"htc.new_htc_structure.main_body[?name=='{mbdy_name}'] | [0].c2_def.sec[-1][1:4]",
                self.hawc2_dict,
            )
            L_towertop += sum([(e - s) ** 2 for s, e in zip(b_start, b_end)]) ** 0.5

        # Nacelle drag
        mbdy_name = self.get_hawc2_mbdy_name(self.drag["nacelle"])
        nac_drag_data = jp(
            f"htc.aerodrag.aerodrag_element[?mbdy_name=='{mbdy_name}'] | [0].sec",
            self.hawc2_dict,
        )
        z = [el[0] for el in nac_drag_data]  # z
        w = [el[2] for el in nac_drag_data]  # w
        cdw = [el[1] * el[2] for el in nac_drag_data]  # cd*w
        CD = trapz(cdw, z) / trapz(w, z)
        return dict(
            uptilt=deg2rad(tilt_deg),
            distance_tt_hub=L_shaft * np.sin(tilt_rad) + L_towertop,
            overhang=L_shaft * np.cos(tilt_rad),
            drag_coefficient=CD,
            elastic_properties_mb=self.components_nacelle_epb(),
        )

    def components_nacelle_epb(self):
        out = dict()
        if "nacelle" in self.concentrated_mass:
            if not self.concentrated_mass["nacelle"] is None:
                cm = self.get_concentrated_mass(**self.concentrated_mass["nacelle"])
                out["system_mass"] = cm[4]
                out["system_inertia"] = cm[5:]
                # Center of mass
                name = self.concentrated_mass["nacelle"]["name"]
                xyz = self.get_c2def_axis(name)
                mass_center = [xyz[0][cm[0] - 1], xyz[1][cm[0] - 1], xyz[2][cm[0] - 1]]
                mass_center[0] += cm[1]
                mass_center[1] += cm[2]
                mass_center[2] += cm[3]
                out["system_center_mass"] = [
                    mass_center[0],
                    mass_center[1],
                    -mass_center[2],
                ]
        else:
            raise KeyError("nacelle need to be added to concentrated_mass")
        if "yaw" in self.concentrated_mass:
            if not self.concentrated_mass["nacelle"] is None:
                cm = self.get_concentrated_mass(**self.concentrated_mass["yaw"])
                out["yaw_mass"] = cm[4]
        else:
            raise KeyError("yaw need to be added to concentrated_mass")
        return out

    def components_tower(self):
        return dict(
            outer_shape_bem=self.components_tower_osb(),
            internal_structure_2d_fem=self.components_tower_is2df(),
        )

    def components_tower_osb(self):
        return dict(
            reference_axis=self.components_tower_reference_axis(),
            outer_diameter=self.components_tower_outer_diameter(),
            drag_coefficient=self.components_tower_drag_coefficient(),
        )

    def components_tower_reference_axis(self):
        out = self.get_circular_body_data(
            "tower",
        )
        return dict(
            x=dict(grid=out["grid_ref"], values=out["x"]),
            y=dict(grid=out["grid_ref"], values=out["y"]),
            z=dict(grid=out["grid_ref"], values=out["z"]),
            desc="-y,x,z (windio to hawc2 base)",
            coordinate_system="hawc2 base",
        )

    def components_tower_outer_diameter(self):
        out = self.get_circular_body_data(
            "tower",
        )
        return dict(grid=out["grid_D_t"], values=out["D"])

    def components_tower_drag_coefficient(self):
        mbdy_name = self.get_hawc2_mbdy_name(self.drag["tower"])
        nac_drag_data = jp(
            f"htc.aerodrag.aerodrag_element[?mbdy_name=='{mbdy_name}'] | [0].sec",
            self.hawc2_dict,
        )
        grid = [el[0] / nac_drag_data[-1][0] for el in nac_drag_data]  # z
        cd = [el[1] for el in nac_drag_data]  # cd
        return dict(grid=grid, values=cd)

    def components_tower_is2df(self):
        return dict(
            reference_axis=self.components_tower_reference_axis(),
            layers=self.components_tower_layers(),
        )

    def components_tower_layers(self):
        out = self.get_circular_body_data(
            "tower",
        )
        return [
            dict(
                name="tower_wall",
                material=self.materials_inp["tower"]["name"],
                thickness=dict(grid=out["grid_D_t"], values=out["t"]),
            )
        ]

    def components_monopile(self):
        mono = dict(
            outer_shape_bem=self.components_monopile_osb(),
            internal_structure_2d_fem=self.components_monopile_is2df(),
        )
        if "monopile_tower_transition" in self.concentrated_mass:
            mono["transition_piece_mass"] = (
                self.components_monopile_transition_piece_mass()
            )
        return mono

    def components_monopile_osb(self):
        return dict(
            reference_axis=self.components_monopile_reference_axis(),
            outer_diameter=self.components_monopile_outer_diameter(),
        )

    def components_monopile_reference_axis(self):
        out = self.get_circular_body_data(
            "monopile",
        )
        return dict(
            x=dict(grid=out["grid_ref"], values=out["x"]),
            y=dict(grid=out["grid_ref"], values=out["y"]),
            z=dict(grid=out["grid_ref"], values=out["z"]),
            desc="-y,x,z (windio to hawc2 base)",
            coordinate_system="hawc2 base",
        )

    def components_monopile_outer_diameter(self):
        out = self.get_circular_body_data(
            "monopile",
        )
        return dict(grid=out["grid_D_t"], values=out["D"])

    def components_monopile_is2df(self):
        return dict(
            reference_axis=self.components_monopile_reference_axis(),
            layers=self.components_monopile_layers(),
        )

    def components_monopile_layers(self):
        out = self.get_circular_body_data(
            "monopile",
        )
        return [
            dict(
                name="monopile_wall",
                material=self.materials_inp["monopile"]["name"],
                thickness=dict(grid=out["grid_D_t"], values=out["t"]),
            )
        ]

    def components_monopile_transition_piece_mass(self):
        trans_data = self.concentrated_mass["monopile_tower_transition"]
        # Get concentrated mass data
        cm = self.get_concentrated_mass(**trans_data)
        return cm[4]

    def airfoils(self):
        air_names, air_names_tc = self.get_airfoil_names()
        pc_set = self.get_pc_set()
        airs = []
        for name, rthick, pol_dat in zip(
            air_names, air_names_tc, self.hawc2_dict["pc"][pc_set - 1]
        ):
            out = dict(
                name=name,
                relative_thickness=rthick / 100,
                polars=[
                    dict(
                        c_l=dict(grid=deg2rad(pol_dat["aoa"]), values=pol_dat["c_l"]),
                        c_d=dict(grid=deg2rad(pol_dat["aoa"]), values=pol_dat["c_d"]),
                        c_m=dict(grid=deg2rad(pol_dat["aoa"]), values=pol_dat["c_m"]),
                    )
                ],
            )
            airs.append(out)
        return airs

    def materials(self):
        mat = [self.get_material_steel("tower")]
        if self.has_monopile():
            if (
                self.materials_inp.get("monopile", dict(name=mat[0]["name"]))["name"]
                != mat[0]["name"]
            ):
                mat.append(self.get_material_steel("monopile"))
        return mat

    def control(self):
        return dict(
            supervisory=self.control_supervisory(),
            pitch=self.control_pitch(),
            torque=self.control_torque(),
        )

    def control_supervisory(self):
        max_gen_speed = self.get_control_actuators_value(
            *self.control_actuators_parameters["max_gen_speed"]
        )
        rotor_radius = self.get_rotor_radius()
        return dict(maxTS=max_gen_speed * rotor_radius)

    def control_pitch(self):
        return dict(
            PC_omega=hz2rads(
                self.get_control_actuators_value(
                    *self.control_actuators_parameters["PC_omega"]
                )
            ),
            PC_zeta=self.get_control_actuators_value(
                *self.control_actuators_parameters["PC_zeta"]
            ),
        )

    def control_torque(self):
        return dict(
            tsr=self.get_control_actuators_value(
                *self.control_actuators_parameters["tsr"]
            ),
            VS_zeta=self.get_control_actuators_value(
                *self.control_actuators_parameters["VS_zeta"]
            ),
            VS_omega=hz2rads(
                self.get_control_actuators_value(
                    *self.control_actuators_parameters["VS_omega"]
                )
            ),
            VS_minspd=self.get_control_actuators_value(
                *self.control_actuators_parameters["VS_minspd"]
            ),
            VS_maxspd=self.get_control_actuators_value(
                *self.control_actuators_parameters["max_gen_speed"]
            ),
        )

    def actuators(self):
        return dict(
            generator=self.actuators_generator(),
            pitch=self.actuators_pitch(),
            hss_brake=self.actuators_hss_brake(),
        )

    def actuators_generator(self):
        return dict(
            rated_power=self.get_control_actuators_value(
                *self.control_actuators_parameters["rated_power"]
            )
            * 1e3,  # Converting from kW to W
            max_gen_speed=self.get_control_actuators_value(
                *self.control_actuators_parameters["max_gen_speed"]
            ),
        )

    def actuators_pitch(self):
        out = dict(
            max_pitch_rate=degs2rads(
                self.get_control_actuators_value(
                    *self.control_actuators_parameters["max_pitch_rate"]
                )
            ),
            max_pitch=deg2rad(
                self.get_control_actuators_value(
                    *self.control_actuators_parameters["max_pitch"]
                )
            ),
        )
        min_pitch = self.get_control_actuators_value(
            *self.control_actuators_parameters["min_pitch"]
        )
        if min_pitch < 90:
            out["min_pitch"] = deg2rad(min_pitch)
        return out

    def actuators_hss_brake(self):
        return dict(
            duration=self.get_control_actuators_value(
                *self.control_actuators_parameters["hss_brake_duration"]
            ),
            torque=self.get_control_actuators_value(
                *self.control_actuators_parameters["hss_brake_torque"]
            ),
            start_time=self.get_control_actuators_value(
                *self.control_actuators_parameters["hss_brake_start_time"]
            ),
        )

    def get_airfoil_names(self):
        if self.airfoil_names is None:
            raise KeyError("airfoil_names need to be given to convert profile data")
        pc_set = self.get_pc_set()
        tcs = jp(f"[*].tc", self.hawc2_dict["pc"][pc_set - 1])
        if tcs is None:
            raise KeyError(f"Did not find airfoil set of {pc_set}")
        return self.airfoil_names, tcs

    def get_blade_grid_and_chord(self):
        ae_set = self.get_ae_set()
        grid = np.asarray(self.hawc2_dict["ae"][ae_set - 1]["s"])
        grid /= grid[-1]
        return grid, self.hawc2_dict["ae"][ae_set - 1]["chord"]

    def get_blade_grid_and_twist(self):
        grid = self.get_c2def_grid("blade", 1)
        mbdy_name = self.get_hawc2_mbdy_name("blade", 1)
        twist = jp(
            "htc.new_htc_structure.main_body[?name=='"
            + mbdy_name
            + "'] | [0].c2_def.sec[*][4]",
            self.hawc2_dict,
        )
        return grid, twist

    def get_blade_grid_and_pitch_axis(self):
        grid_in = self.get_c2def_grid("blade", 1)
        if not self.pitch_axis is None:
            pa = interp(grid_in, self.pitch_axis["grid"], self.pitch_axis["values"])
        else:
            pa = np.full_like(grid_in, 0.5)
        return grid_in, pa

    def get_blade_grid_and_tc(self):
        ae_set = self.get_ae_set() - 1
        grid = np.array(self.hawc2_dict["ae"][ae_set]["s"])
        grid /= grid[-1]
        return grid, self.hawc2_dict["ae"][ae_set]["tc"]

    def get_blade_grid(self, name):
        grid = self.grids.get("blade", None)
        if grid is None:
            grid = self.grids.get(name, None)
        if grid is None:
            if name in [
                "blade_x",
                "blade_y",
                "blade_z",
                "twist",
                "pitch_axis",
            ]:  # c2def grid
                return self.get_c2def_grid("blade", 1)
            elif name in ["chord", "rthick"]:  # AE-grid
                ae_set = self.get_ae_set()
                grid = np.array(self.hawc2_dict["ae"][ae_set - 1]["s"])
                grid /= grid[-1]
                return grid.tolist()

    def get_ae_set(self):
        ae_sets = self.hawc2_dict["htc"]["aero"]["ae_sets"]
        if not (
            len(ae_sets) > 1 and all([ae_sets[0] == _ae_set for _ae_set in ae_sets[1:]])
        ):
            raise ValueError(
                f"All ae_sets need to be the same in aero.ae_sets (found: {ae_sets}"
            )
        return ae_sets[0]

    def get_pc_set(self):
        ae_set = self.get_ae_set() - 1
        pc_sets = self.hawc2_dict["ae"][ae_set]["pc_set"]
        if not (
            len(pc_sets) > 1 and all([pc_sets[0] == _ae_set for _ae_set in pc_sets[1:]])
        ):
            raise ValueError(
                f"All pc_sets in ae-file need to be the same (found: {pc_sets}"
            )
        return int(pc_sets[0])

    def get_c2def_grid_and_axis(self, name, imbdy=None):
        x, y, z = self.get_c2def_axis(name, imbdy)
        s = compute_curve_length(x, y, z)
        s /= s[-1]
        return s.tolist(), x, y, z

    def get_c2def_axis(self, name, imbdy=None):
        mbdy_name = self.get_hawc2_mbdy_name(name, imbdy)
        xyz = np.array(
            jp(
                "htc.new_htc_structure.main_body[?name=='"
                + mbdy_name
                + "'] | [0].c2_def.sec[*][1:4]",
                self.hawc2_dict,
            )
        ).T
        if len(xyz) == 0:
            raise KeyError(f"{mbdy_name} is not new_htc_structure.main_body[*]")
        return xyz[0].tolist(), xyz[1].tolist(), xyz[2].tolist()

    def get_c2def_grid(self, name, imbdy=None):
        return self.get_c2def_grid_and_axis(name, imbdy)[0]

    def get_st_data(self, name, imbdy=None):
        mbdy_name = self.get_hawc2_mbdy_name(name, imbdy)
        # Get filename and set
        fname_set = jp(
            f"htc.new_htc_structure.main_body[?name=='{mbdy_name}'].timoschenko_input",
            self.hawc2_dict,
        )[0]
        return self.hawc2_dict["st"][mbdy_name][fname_set["set"][0] - 1][
            fname_set["set"][1] - 1
        ]

    def get_circular_body_data(self, name):
        # Ref axis
        grid_ref, x, y, z = self.get_c2def_grid_and_axis(name)
        z = np.abs(z).tolist()
        # Test that x and y are zero
        np.testing.assert_almost_equal(x, 0.0, 10)
        np.testing.assert_almost_equal(y, 0.0, 10)
        # Diameter and wall thickness
        st_data = self.get_st_data(
            name,
        )
        grid_D_t = np.array(st_data["s"])
        grid_D_t /= grid_D_t[-1]
        A = np.array(st_data["A"])
        Ix = np.asarray(st_data["Ix"])
        D = np.sqrt(8 * Ix / A + 2 * A / np.pi)
        t = D / 2 - np.sqrt((D / 2) ** 2 - A / np.pi)
        return dict(
            grid_ref=grid_ref,
            x=x,
            y=y,
            z=z,
            grid_D_t=grid_D_t.tolist(),
            D=D.tolist(),
            t=t.tolist(),
        )

    def has_monopile(self):
        return self.get_hawc2_mbdy_name("monopile") in jp(
            "htc.new_htc_structure.main_body[*].name", self.hawc2_dict
        )

    def get_hawc2_mbdy_name(self, default_name, imbdy=None):
        out = self.mbdy_names.get(default_name, default_name)
        if not imbdy is None:
            out += str(imbdy)
        return out

    def get_concentrated_mass(self, name, index, imbdy=None):
        mbdy_name = self.get_hawc2_mbdy_name(name, imbdy)
        cm = jp(
            f"htc.new_htc_structure.main_body[?name=='{mbdy_name}'].concentrated_mass",
            self.hawc2_dict,
        )[0]
        if isinstance(cm[0], list):
            return cm[index]
        elif index > 0:
            raise ValueError(
                f"Index for concentrated mass can not be more than one for a body with only one (given: {cm})"
            )
        return cm

    def get_material_steel(self, name):
        st_data = self.get_st_data(name)
        out = dict()
        out.update(self.materials_inp.get(name, {}))
        if not "rho" in out:
            rhos = np.array(st_data["m"]) / np.array(st_data["A"])
            rho = np.mean(rhos)
            if any([abs(_rho - rho) > 1e-4 for _rho in rhos]):
                raise RuntimeError(
                    f"Could not estimate the {name} material density, please provide it (materials.{name}.rho)"
                )
            out["rho"] = rho
        if not "E" in out:
            if any([abs(_E - st_data["E"][0]) > 1e-10 for _E in st_data["E"]]):
                raise RuntimeError(
                    f"Could not estimate the {name} material Youngs Modulus, please provide it (materials.{name}.E)"
                )
            out["E"] = st_data["E"][:3]
        if not "G" in out:
            if any([abs(_E - st_data["E"][0]) > 1e-10 for _E in st_data["E"]]):
                raise RuntimeError(
                    f"Could not estimate the {name} material Youngs Modulus, please provide it (materials.{name}.E)"
                )
            out["G"] = st_data["G"][:3]
        if not "orth" in out:
            out["orth"] = 0
        return out

    def get_st_net_mass_inertia(self, name, imbdy=None):
        # Assuming z as the main axis
        st_data = self.get_st_data(name, imbdy)
        s = np.array(st_data["s"])
        md = np.array(st_data["m"])
        mass = np.trapezoid(md, s)
        L = s[-1] - s[0]
        inertia_xy = mass * L**2 / 3
        inertia_z = np.trapezoid(st_data["Ix"] + st_data["Iy"], s) / 2
        return mass, [inertia_xy, inertia_xy, inertia_z]

    def convert_st_classic_to_FPM(self, st_classic):
        """This function converts an HAWC2 isotropic input file to the corresponding anisotropic input"""
        # From: https://gitlab.windenergy.dtu.dk/HAWC2Public/modelling/beam-corotational/-/blob/main/Models/TimoBeam.py#L220
        from windio_converter.io.hawc2 import ST_list

        def vec_mat(axis, angle):
            """
            Axis angle to rotation matrix
            input = axis, angle
            output = 3x3 rotation matrix
            """
            if float(angle) == 0.0 or np.linalg.norm(axis) < 10e-9:
                matrix = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]])
            else:
                # equaiton 3.32 from S.Krenk
                axis = np.asarray(axis)
                axis = axis / np.linalg.norm(axis)
                matrix = (
                    np.cos(angle) * np.eye(3)
                    + np.sin(angle) * skew_sym(axis)
                    + (1 - np.cos(angle)) * np.outer(axis, axis.T)
                )
            return matrix

        def skew_sym(n):
            """
            It gives the skew symmetric matrix of a vector for matrix multipication
            input = n
            output = 3x3 matrix
            """
            n_tilde = np.array([[0, -n[2], n[1]], [n[2], 0, -n[0]], [-n[1], n[0], 0]])
            return n_tilde

        def rot_mat_2_vec(v1, v2):
            """
            Returns the rotation matrix which rotates unit vector v1 to unit vector v2
            v2 = Rv1
            Parameters
            ----------
            v1 : unit vector
            v2 : unit vector

            Returns
            -------
            Rotation matrix R

            """
            v1 = v1 / np.linalg.norm(v1)
            v2 = v2 / np.linalg.norm(v2)
            #
            c = np.dot(v1, v2)
            v = np.matmul(skew_sym(v1), v2)
            #
            R = (
                np.eye(3)
                + skew_sym(v)
                + np.matmul(skew_sym(v), skew_sym(v)) * 1 / (1 + c)
            )
            return R

        def get_tsb(v1, v2, angle):
            """Returns the rotation matrix which rotates a vector q_elem defined in the element coorinate system (x',y',v2),
            to a vector q_global in a standard coordinate sytem ([1,0,0]',[0,1,0]',[0,0,1]'), thus
            q_global = tsb q_elem
            """
            if v1[0] != 0 or v1[1] != 0 or v1[2] != 1:
                print("****** ERROR in get_tsb - v1 has to be a [0,0,1] vector ******")

            # normalize to unit vectors
            v2 = v2 / np.linalg.norm(v2)
            v1 = v1 / np.linalg.norm(v1)
            # Compute tsb without rotation around v2 (twist)
            cond1 = abs(v2[0]) > 1e-6 and abs(v2[1]) > 1e-6
            cond2 = abs(v2[0]) < 1e-6 and abs(v2[1]) < 1e-6 and v2[2] < 0

            if cond1 or cond2:  # If v2 is not in the xz or yz plane or v2 = [0,0,-1]
                tsb_no_twist = np.zeros((3, 3))
                tsb_no_twist[:, -1] = v2.copy()
                tsb_no_twist[0, 1] = 0.0
                tsb_no_twist[1, 1] = tsb_no_twist[2, 2] / np.linalg.norm(
                    tsb_no_twist[1:, -1]
                )
                tsb_no_twist[2, 1] = -tsb_no_twist[1, 2] / np.linalg.norm(
                    tsb_no_twist[1:, -1]
                )
                tsb_no_twist[:, 0] = np.cross(tsb_no_twist[:, 1], tsb_no_twist[:, 2])
            else:  # if v2 is in the xz or yz plane
                tsb_no_twist = rot_mat_2_vec(v1, v2)

            # Flip y-axis if negative (following HAWC2 formulation)
            if tsb_no_twist[1, 1] < 0.0:
                tsb_no_twist[1:, 1] = -tsb_no_twist[1:, 1]
                tsb_no_twist[:, 0] = np.cross(tsb_no_twist[:, 1], tsb_no_twist[:, 2])

            # Compute rotation around v2 (twist)
            tsb = tsb_no_twist.copy()
            tsb[:, :2] = np.matmul(vec_mat(v2, angle), tsb_no_twist[:, :2])
            return tsb

        # Properties names
        names_FPM = ST_list.header_FPM()
        names_classic = ST_list.header_classic()
        st_FPM = dict()
        # Standard parameters
        for i, name in enumerate(names_FPM):
            if i < 8:
                st_FPM[name] = st_classic[name]
            else:
                st_FPM[name] = np.zeros_like(st_classic["s"])

        # Internal variables
        v1 = np.array([0.0, 0.0, 1.0])

        # Assemble cross sectional stiffness matrix
        for i in range(len(st_FPM["s"])):
            # Rotation matrix from c2 to elastic coordinates
            t_mat = get_tsb(v1, v1, np.deg2rad(st_FPM[names_FPM[6]][i]))
            svec = t_mat.T @ np.array(
                [st_classic[names_classic[6]][i], st_classic[names_classic[7]][i], 0]
            )
            evec = t_mat.T @ np.array(
                [st_classic[names_classic[17]][i], st_classic[names_classic[18]][i], 0]
            )

            # Cross sectional stiffness matrix
            st_FPM[names_FPM[9]][i] = (
                st_classic[names_classic[13]][i]
                * st_classic[names_classic[15]][i]
                * st_classic[names_classic[9]][i]
            )
            st_FPM[names_FPM[14]][i] = -st_FPM[names_FPM[9]][i] * (svec[1] - evec[1])
            st_FPM[names_FPM[15]][i] = (
                st_classic[names_classic[14]][i]
                * st_classic[names_classic[15]][i]
                * st_classic[names_classic[9]][i]
            )
            st_FPM[names_FPM[19]][i] = st_FPM[names_FPM[15]][i] * (svec[0] - evec[0])
            st_FPM[names_FPM[20]][i] = (
                st_classic[names_classic[8]][i] * st_classic[names_classic[15]][i]
            )
            st_FPM[names_FPM[24]][i] = (
                st_classic[names_classic[8]][i] * st_classic[names_classic[10]][i]
            )
            st_FPM[names_FPM[27]][i] = (
                st_classic[names_classic[8]][i] * st_classic[names_classic[11]][i]
            )
            st_FPM[names_FPM[29]][i] = (
                st_classic[names_classic[9]][i] * st_classic[names_classic[12]][i]
                + st_FPM[names_FPM[19]][i] * (svec[0] - evec[0])
                - st_FPM[names_FPM[14]][i] * (svec[1] - evec[1])
            )

        return st_FPM

    """
    def transform_blade_6x6_to_windio(self, six_by_six, st_data):
        # ST-grid
        grid_st = [el/st_data["s"][-1] for el in st_data["s"]]

        # for pitch-axis change
        x_out = None
        twist_rad = -np.asarray(deg2rad(self.get_blade_grid_and_twist()[1]))
        if not self.pitch_axis is None:
            grid_in, x_h2, y_h2, z_h2 = self.get_c2def_grid_and_axis("blade", imbdy=1)
            x_in, y_in, z_in = change_coord_sys(x_h2, y_h2, z_h2, "hawc2_to_windio")
            pa = self.get_blade_grid_and_pitch_axis()[1]
            chord = interp(grid_in, *self.get_blade_grid_and_chord())
            pa_in = np.full_like(grid_in, 0.5)
            x_out, y_out, z_out = change_pitch_axis(x_in, y_in, z_in, chord, twist_rad, pa_in, pa)
            for pfix in ["_in", "_out"]:
                for name in ["x", "y"]:
                    exec(f"{name}{pfix} = interp(grid_st, grid_in, {name}{pfix})")
        twist_rad = interp(grid_st, grid_in, twist_rad)

        # Transform 6x6
        for i, (xe, ye, pitch) in enumerate(zip(st_data["xe"], st_data["ye"], st_data["pitch"])):
            trans_mat = TransformMatrix6x6(0, 0, -pitch) # Remove structural pitch
            trans_mat = TransformMatrix6x6(-xe, -ye, 0) @ trans_mat # Move to c2_def from el-center
            trans_mat = TransformMatrix6x6(0, 0, np.pi/2) @ trans_mat # Change to WIO coord sys
            if not x_out is None:
                trans_mat = TransformMatrix6x6(x_out[i]-x_in[i], y_out[i]-y_in[i], 0) @ trans_mat # Change for pitch-axis
            trans_mat = TransformMatrix6x6(0, 0, twist_rad[i]) @ trans_mat # Apply twist
            six_by_six[i] = trans_mat @ six_by_six[i] @ trans_mat.T
        
        # Flatten 6x6
        indices = np.triu_indices(6)
        out = np.zeros((len(six_by_six), 21))
        for k, (i, j) in enumerate(zip(*indices)):
            out[:, k] = six_by_six[:, i, j]
        return out
    """

    def get_control_actuators_value(self, name, index):
        return jp(
            f"htc.dll.type2_dll[?name == '{name}'] | [0].init.constant[?[0] == `{index}`] | [0][1]",
            self.hawc2_dict,
        )

    def get_rotor_radius(self):
        blade_c2def = self.get_c2def_axis("blade", 1)
        hub_c2def = self.get_c2def_axis("hub", 1)
        cone_rad = deg2rad(self.get_rotor_cone_deg())
        # Get hub and blade tip y-z (with out cone)
        hub_l = hub_c2def[1][-1] + 1j * hub_c2def[2][-1]
        blade_l = blade_c2def[1][-1] + 1j * blade_c2def[2][-1]
        rotor_l = hub_l + blade_l
        # Apply cone to length
        rotor = rotor_l * np.exp(1j * cone_rad)
        return np.imag(rotor)  # imag for only projected area

    def get_rotor_cone_deg(self):
        mbdy2 = self.cone_location["mbdy2"]
        ieu = self.cone_location["eulerang_index"]
        iel = self.cone_location["element_index"]
        return jp(
            f"htc.new_htc_structure.orientation.relative[?mbdy2[0]=='{mbdy2}'] | [0].mbdy2_eulerang[{ieu}][{iel}]",
            self.hawc2_dict,
        )
