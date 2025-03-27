import aesoptparam as apm
import numpy as np

from ....utils import (
    Nx6x6_to_Nx21,
    Nx21_to_Nx6x6,
    Transform6x6,
    compute_curve_length,
    interp,
    jp,
    rad2deg,
    warn,
)
from ..common import grids, use_blade_FPM
from .common import st_base


class structural_pitch(apm.AESOptParameterized):
    grid = apm.AESOptArray(doc="Grid for input structural pitch")
    values = apm.AESOptArray(doc="Values for input structural pitch")


class blade(st_base):
    grid = apm.copy_param_ref(grids.param.blade_st, "....grids.blade_st")
    use_blade_FPM = apm.copy_param_ref(use_blade_FPM, "....use_blade_FPM")
    structural_pitch = apm.SubParameterized(structural_pitch)

    def convert(self):
        if self.use_blade_FPM:
            return self.FPM()
        return self.classic()

    def FPM(self):
        # create FPM blade data; need to be fixed
        # User can use st_blade_no_FPM() function
        # warn("st_blade", self.get_no_warnings())
        warn(
            "st_blade",
            self.get_no_warnings(),
            "Create FPM blade data! Wrong implementation!"
            + "Need to be fixed! Use st_blade_no_FPM() function.",
        )
        elmb = self.windio_dict["components"]["blade"]["elastic_properties_mb"][
            "six_x_six"
        ]
        # Grid
        grid = self.grid

        # Twist of the input axis (assuming it is the structual local coordinate system)
        twist = [-_val for _val in interp(grid, *jp("twist.[grid, values]", elmb))]

        # C2-def axis
        x_c2, y_c2, z_c2, twist_c2 = self.get_blade_c2def(grid)
        s = compute_curve_length(x_c2, y_c2, z_c2)
        # Change to windio
        twist_c2 = [-_val for _val in twist_c2]

        # Interpolate structual pitch if passed as an argument
        st_pitch = None
        if (self.structural_pitch.grid is not None) and (
            self.structural_pitch.values is not None
        ):
            st_pitch = interp(
                grid, self.structural_pitch.grid, self.structural_pitch.values
            )

        # Interpolate beam probs to grid
        K = np.empty((len(grid), 21))
        M = np.empty((len(grid), 21))
        _K = np.array(elmb["stiff_matrix"]["values"])
        _M = np.array(elmb["inertia_matrix"]["values"])
        for j in range(21):
            K[:, j] = interp(grid, elmb["stiff_matrix"]["grid"], _K[:, j])
            M[:, j] = interp(grid, elmb["inertia_matrix"]["grid"], _M[:, j])

        # Convert to Nx6x6 matrix
        K6x6 = Nx21_to_Nx6x6(K)
        M6x6 = Nx21_to_Nx6x6(M)

        # Initialize data
        xe = np.empty((len(grid)))
        ye = np.empty_like(xe)
        xm = np.empty_like(xe)
        ym = np.empty_like(xe)
        pitch = np.empty_like(xe)

        # Loop over each section (following: https://gitlab.windenergy.dtu.dk/becaspp/BECASpp/-/wikis/Cross-section-properties)
        for i, (_K, _M, _twist, _x_c2, _twist_c2) in enumerate(
            zip(K6x6, M6x6, twist, x_c2, twist_c2)
        ):
            # Change to hawc2 coordinate system
            # TODO: Should twist be corrected here? (kenloen)
            _K = Transform6x6(_K, 0, 0, np.pi / 2 - (_twist - _twist_c2))
            _M = Transform6x6(_M, 0, 0, np.pi / 2 - (_twist - _twist_c2))
            # Compute compliance matrix (K^-1)
            F = np.linalg.inv(_K)
            # Compute elastic center
            _xe = -(-F[3, 3] * F[4, 2] + F[3, 4] * F[3, 2]) / (
                F[3, 3] * F[4, 4] - F[3, 4] ** 2
            )
            _ye = -(F[3, 2] * F[4, 4] - F[3, 4] * F[4, 2]) / (
                F[3, 3] * F[4, 4] - F[3, 4] ** 2
            )
            # Compute center of mass (mean of both entries, from: https://github.com/OpenFAST/python-toolbox/blob/main/pyFAST/converters/beam.py)
            _xm = (_M[1, 5] - _M[2, 4]) / (2 * _M[0, 0])
            _ym = (-_M[0, 5] + _M[2, 3]) / (2 * _M[0, 0])
            # Compute/get structural pitch
            if st_pitch is None:
                _, vec = np.linalg.eig(_K[3:5, 3:5])
                angs = np.array(
                    [np.arctan2(vec[1, 0], vec[0, 0]), np.arctan2(vec[1, 1], vec[0, 1])]
                )
                pitch[i] = angs[np.argmin(np.abs(angs))]
            else:
                pitch[i] = st_pitch[i]
            # Translate 6x6 to elastic center
            _K = Transform6x6(_K, _xe, _ye, pitch[i])
            _M = Transform6x6(_M, _xe, _ye, pitch[i])
            # Set it back to the Nx6x6 matrix
            K6x6[i] = _K
            M6x6[i] = _M
            # Set elastic center and center of mass
            xe[i] = _xe - _x_c2
            ye[i] = _ye
            xm[i] = _xm - _x_c2
            ym[i] = _ym

        # Transform Nx6x6 to Nx21
        K = Nx6x6_to_Nx21(K6x6)

        # Compute radius of gyration (rx = sqrt(Ixx/m), ry = sqrt(Iyy/m))
        rx = np.sqrt(M6x6[:, 3, 3] / M6x6[:, 0, 0])
        ry = np.sqrt(M6x6[:, 4, 4] / M6x6[:, 0, 0])

        # Setting data in dict
        out = dict(
            s=s,
            m=M6x6[:, 0, 0].tolist(),
            x_cg=xm.tolist(),
            y_cg=ym.tolist(),
            ri_x=rx.tolist(),
            ri_y=ry.tolist(),
            pitch=rad2deg(pitch),
            xe=xe.tolist(),
            ye=ye.tolist(),
        )
        # Adding beam properties
        for i, j in zip(*np.triu_indices(6)):
            out[f"K{i+1}{j+1}"] = K6x6[:, i, j].tolist()

        return [[out]]

    def classic(self):
        # Inspired by the conversion of the windIO 6x6 matrices to DNV Bladed 4.x format, here:
        # https://dnvgldocs.azureedge.net/BladedManual/4_16/workflow/preProcessingTools/WindIOtoBladed.html#mjx-eqn%3Aeq%3Aelasticcentre
        # There was some errors in the DNV bladed converter.
        # The errors are fixed within this implementation

        warn(
            "classic(): ",
            self.get_no_warnings(),
            "The classic beam inputs (no FPM) is used to create htc-file!",
        )
        elmb = self.windio_dict["components"]["blade"]["elastic_properties_mb"][
            "six_x_six"
        ]
        # get Grid:
        # use the grid in the six_x_six.reference_axis structural matrices (K and M) read from the windIO file
        grid = self.grid

        # Compute c2_def coordinates (x,y,z) based on the grid used by 6x6 structural matrices (K and M)
        # get_blade_c2def() return the twist angle in degree
        x_c2, y_c2, z_c2, twist_c2 = self.get_blade_c2def(grid)
        # change the units to rads and change the sign as required in c2_def section
        twist_c2 = [np.deg2rad(-_val) for _val in twist_c2]
        # compute the curved length distance between cross-sections
        s = compute_curve_length(x_c2, y_c2, z_c2)

        # outer shape bem data in windIO
        osb_data = dict(
            x_ref=interp(grid, *jp("reference_axis.x.[grid, values]", elmb)),
            y_ref=interp(grid, *jp("reference_axis.y.[grid, values]", elmb)),
            z_ref=interp(grid, *jp("reference_axis.z.[grid, values]", elmb)),
        )

        # Interpolate structual pitch if passed as an argument
        st_pitch = None
        if self.structural_pitch.grid is not None and (
            self.structural_pitch.values is not None
        ):
            st_pitch = interp(
                grid, self.structural_pitch.grid, self.structural_pitch.values
            )
            warn(
                "st_blade_no_FPM",
                self.get_no_warnings(),
                "Using user defined pitch axis values!",
            )

        # Interpolate beam probs to grid
        K = np.empty((len(grid), 21))
        M = np.empty((len(grid), 21))
        _K = np.array(elmb["stiff_matrix"]["values"])
        _M = np.array(elmb["inertia_matrix"]["values"])
        for j in range(21):
            K[:, j] = interp(grid, elmb["stiff_matrix"]["grid"], _K[:, j])
            M[:, j] = interp(grid, elmb["inertia_matrix"]["grid"], _M[:, j])

        # Convert to Nx6x6 matrix
        K6x6 = Nx21_to_Nx6x6(K)
        M6x6 = Nx21_to_Nx6x6(M)

        # Initialize data
        xe = np.empty((len(grid)))
        ye = np.empty_like(xe)
        xm = np.empty_like(xe)
        ym = np.empty_like(xe)
        xs = np.empty_like(xe)
        ys = np.empty_like(xe)
        rx = np.empty_like(xe)
        ry = np.empty_like(xe)
        pitch = np.empty_like(xe)

        # Initialize data
        pec_c2 = np.empty((4, 1))
        psc_c2 = np.empty((4, 1))
        pmc_c2 = np.empty((4, 1))
        O_ref_f = np.empty((3, 1))
        O_ref_h = np.empty((3, 1))

        # Transformation matrix that translates from the reference axes location to elastic center location
        _Te = np.empty((3, 3))
        # Transformation matrix that translates from the reference axes location to shear center location
        _Ts = np.empty((3, 3))
        # Transformation matrix (6x6) that translates from the reference axes location to mass center location
        _Tm = np.empty((6, 6))
        # Rotation matrix from HAWC2 blade root: "h"-frame to windIO reference: "r"-frame
        T_hr = np.empty((4, 4))
        # Rotation matrix that rotates from the reference axes orientation to principal elastic axes orientation
        _Re = np.empty((3, 3))
        # Rotation matrix that rotates from the reference axes orientation to principal shear axes orientation
        _Rs = np.empty((3, 3))
        # Rotation matrix that rotates from the reference axes orientation to principal mass axes orientation
        _Rm = np.empty((6, 6))

        # Fully populated 3x3 stiffness matrix associated with axial force and bending moment
        # defined at reference axes location and orientation
        _Ke_rr = np.empty_like(_Te)
        # The 3x3 stiffness matrix associated with elastic center, in the reference axes orientation
        _Ke_er = np.empty_like(_Te)
        # The 3x3 stiffness matrix associated with elastic center, in the elastic axes orientation
        _Ke_ee = np.empty_like(_Te)
        # The 3x3 stiffness matrix associated with elastic center, in the elastic axes orientation
        _Ke_ee = np.empty_like(_Te)
        # The 3x3 axial and bending stiffness matrix associated with the elastic axes orientation
        # represented in c2_def axis at elastic center
        Ke_ee = np.empty_like(_Te)

        # Fully populated 3x3 stiffness matrix associated with shear force and torsional moment
        # defined at reference axes location and orientation
        _Ks_rr = np.empty_like(_Te)
        # The 3x3 stiffness matrix associated with shear center, in the reference axes orientation
        _Ks_sr = np.empty_like(_Te)
        # The 3x3 stiffness matrix associated with shear center, in the elastic axes orientation
        _Ks_se = np.empty_like(_Te)
        # The 3x3 torsion and shear stiffness matrix associated with the elastic axes orientation
        # represented in c2_def axis at elastic center
        Ks_se = np.empty_like(_Te)

        # Fully populated 6x6 mass matrix associated with reference axes location and orientation
        _M_rr = np.empty((6, 6))
        # The 6x6 mass matrix associated with mass center in reference axes orientation
        _M_mr = np.empty((6, 6))
        # The 6x6 mass matrix associated with mass center in principal inertia axes orientation
        # represented in windIO reference: "r"-frame
        _M_mm = np.empty((6, 6))
        # The 6x6 mass matrix associated with mass center in principal inertia axes orientation
        # represented in hawc2 blade root reference: "h"-frame
        M_mm = np.empty((6, 6))

        # Loop over each section/grid location:
        for i, (_K, _M, _x_c2, _y_c2, _z_c2, _twist_c2) in enumerate(
            zip(K6x6, M6x6, x_c2, y_c2, z_c2, twist_c2)
        ):
            #
            # Performing computations on stiffness matrix associated with
            # axial force and bending moments.
            #
            # Compute elastic center in reference axis along x-and y-direction
            # specified by .yaml file.  Equation (4)
            _xe = -(_K[2, 4] / _K[2, 2])
            _ye = _K[2, 3] / _K[2, 2]

            # Compute transformation matrix, Equation (5).
            _Te = np.array([[1, 0, 0], [-_ye, 1, 0], [_xe, 0, 1]])
            # Fully populated 3x3 stiffness matrix associated with axial
            # force and bending moment defined at reference axes location
            # and orientation.
            _Ke_rr = _K[2:5, 2:5]
            # Compute 3x3 stiffness matrix _Ke_er, Equation (6).
            _Ke_er = np.matmul(_Te, np.matmul(_Ke_rr, np.transpose(_Te)))

            # Compute angle between elastic axes orientation and the reference
            # axes orientation.
            _, eigen_vec = np.linalg.eig(_Ke_er[1:3, 1:3])
            # theta_e = np.arctan(eigen_vec[0,1]/eigen_vec[0,0])
            # In reference axes system of windIO, the value is negative
            # if there is a clockwise rotation.
            theta_e = np.arctan2(eigen_vec[1, 0], eigen_vec[0, 0])

            # Compute the rotation matrix that rotates from the reference
            # axes to elastic axes.
            _Re = np.array(
                [
                    [1.0, 0.0, 0.0],
                    [0.0, np.cos(theta_e), -np.sin(theta_e)],
                    [0.0, np.sin(theta_e), np.cos(theta_e)],
                ]
            )

            # Compute 3x3 stiffness matrix _Ke_ee, Equation (10).
            # Note: Eq. 10 is wrong!
            # The correct equation is as: Ke_ee = (Re)^T*Ke_er*(Re)
            _Ke_ee = np.matmul(np.transpose(_Re), np.matmul(_Ke_er, _Re))
            #
            # Performing computations on stiffness matrix associated with
            # shear forces and torsional moment.
            #
            # Extracting the necessary elements from full 6x6 stiffness
            # matrix at current grid point.
            elements = [
                _K[0, 0],
                _K[0, 1],
                _K[0, 5],  # Elements from the 1st row
                _K[1, 0],
                _K[1, 1],
                _K[1, 5],  # Elements from the 2nd row
                _K[5, 0],
                _K[5, 1],
                _K[5, 5],  # Elements from the 6th row
            ]
            _Ks_rr = np.array(elements).reshape((3, 3))

            # Compute shear center in reference axes along
            # x- and y-direction. Equation (13)
            _xs = (_K[0, 0] * _K[5, 1] - _K[0, 1] * _K[5, 0]) / (
                _K[0, 0] * _K[1, 1] - _K[0, 1] * _K[0, 1]
            )
            _ys = -(-_K[0, 1] * _K[5, 1] + _K[1, 1] * _K[5, 0]) / (
                _K[0, 0] * _K[1, 1] - _K[0, 1] * _K[0, 1]
            )

            # Compute transformation matrix, Equation (14)
            _Ts = np.array([[1, 0, 0], [0, 1, 0], [_ys, -_xs, 1]])

            # Compute 3x3 stiffness matrix _Ks_sr, Equation (15)
            _Ks_sr = np.matmul(_Ts, np.matmul(_Ks_rr, np.transpose(_Ts)))

            # Compute the rotation matrix that rotates from the reference axes
            # orientation to elastic axes orientation.
            # HAWC2 requires shear stiffness terms (Kx,Ky) in principal
            # elastic axes orientation.
            _Rs = np.array(
                [
                    [np.cos(theta_e), -np.sin(theta_e), 0.0],
                    [np.sin(theta_e), np.cos(theta_e), 0.0],
                    [0.0, 0.0, 1.0],
                ]
            )

            # Compute 3x3 stiffness matrix _Ks_se, Equation (16).
            # Note: Eq. 16 is wrong!
            # The correct equation is as: Ks_se = (Rs)^T*Ks_sr*(Rs)
            _Ks_se = np.matmul(np.transpose(_Rs), np.matmul(_Ks_sr, _Rs))
            #
            # Performing computation on the mass properties
            #
            # Compute center of mass in reference axes along x-and y-direction.
            # Equation (20)
            _xm = (_M[1, 5]) / (_M[0, 0])
            _ym = (_M[2, 3]) / (_M[0, 0])

            # Fully populated 6x6 mass matrix associated with reference axes
            # location and orientation.
            _M_rr = _M

            # Compute transformation matrix, Equation (21)
            _Tm = np.array(
                [
                    [1, 0, 0, 0, 0, 0],
                    [0, 1, 0, 0, 0, 0],
                    [0, 0, 1, 0, 0, 0],
                    [0, 0, -_ym, 1, 0, 0],
                    [0, 0, _xm, 0, 1, 0],
                    [_ym, -_xm, 0, 0, 0, 1],
                ]
            )

            # Transform the 6x6 mass matrix from reference axes location to
            # mass center location (_M_mr), Equation (23)
            _M_mr = np.matmul(_Tm, np.matmul(_M_rr, np.transpose(_Tm)))

            # Compute angle between principal inertia axes orientation
            # and the reference axes orientation
            _, eigen_vec = np.linalg.eig(_M_mr[3:5, 3:5])
            # theta_m = np.arctan(eigen_vec[0,1]/eigen_vec[0,0])
            theta_m = np.arctan2(eigen_vec[0, 1], eigen_vec[0, 0])

            # Compute the rotation matrix, Equation (24)
            _Rm = np.array(
                [
                    [1, 0, 0, 0, 0, 0],
                    [0, 1, 0, 0, 0, 0],
                    [0, 0, 1, 0, 0, 0],
                    [0, 0, 0, np.cos(theta_m), -np.sin(theta_m), 0.0],
                    [0, 0, 0, np.sin(theta_m), np.cos(theta_m), 0.0],
                    [0, 0, 0, 0.0, 0.0, 1.0],
                ]
            )

            # Rotate the 6x6 mass matrix from reference axes orientation
            # to principal inertia orientation (_M_mm), Equation (26)
            # Note eq. 26 is wrong!!
            # The correct equation is as: _M_mm = (_Rm)^T*_M_mr*(_Rm)
            _M_mm = np.matmul(np.transpose(_Rm), np.matmul(_M_mr, _Rm))

            # ----------------------------------------------------- #
            # Compute HAWC2 classical beam input parameters (no FPM)
            # ----------------------------------------------------- #

            # Compute the angle for the rotation from reference axes
            # orientation to HAWC2 c2_def orientation
            theta_r2c2 = -(
                -_twist_c2 + np.pi / 2.0
            )  # _twist_c2 value is negative (this is checked and correct)

            # compute the offset of c2_def system in reference axes system
            # setup rotation matrix from HAWC2 blade root:
            # "h"-frame to windIO blade root: "f"-frame
            theta_h2f = np.pi / 2
            R_hf = np.array(
                [
                    [np.cos(theta_h2f), -np.sin(theta_h2f), 0.0],
                    [np.sin(theta_h2f), np.cos(theta_h2f), 0.0],
                    [0.0, 0.0, 1.0],
                ]
            )

            # position of the origin of reference axis in windIO ('f'-frame)
            O_ref_f = np.array(
                [osb_data["x_ref"][i], osb_data["y_ref"][i], osb_data["y_ref"][i]]
            ).reshape(3, 1)

            # position of the origin of windIO reference axis represented
            # in HAWC2 blade root "h"-frame
            O_ref_h = np.matmul((R_hf), O_ref_f)

            # setup transformation matrix from HAWC2 blade root:
            # "h"-frame to windIO reference: "r"-frame
            T_hr = np.array(
                [
                    [np.cos(theta_h2f), -np.sin(theta_h2f), 0.0, O_ref_h[0, 0]],
                    [np.sin(theta_h2f), np.cos(theta_h2f), 0.0, O_ref_h[1, 0]],
                    [0.0, 0.0, 1.0, O_ref_h[2, 0]],
                    [0.0, 0.0, 0.0, 1.0],
                ]
            )

            # create homogenious coordinates for the position of the origin
            # of windIO reference axis ("r"-frame) represented in "h"-frame
            PO_ref_h = np.array(
                [O_ref_h[0, 0], O_ref_h[1, 0], O_ref_h[2, 0], 1.0]
            ).reshape(4, 1)
            # compute the original of hawc2 c2_def represented in "r"-frame
            PO_c2_r = np.matmul(np.linalg.inv(T_hr), PO_ref_h)

            # setup transformation matrix from from windIO reference axis
            # ("r"-frame) to c2_def ("c2"-frame)
            T_rc2 = np.array(
                [
                    [np.cos(theta_r2c2), -np.sin(theta_r2c2), 0.0, PO_c2_r[0, 0]],
                    [np.sin(theta_r2c2), np.cos(theta_r2c2), 0.0, PO_c2_r[1, 0]],
                    [0.0, 0.0, 1.0, PO_c2_r[2, 0]],
                    [0.0, 0.0, 0.0, 1.0],
                ]
            )

            # set elastic center in windIO reference axis ("r"-frame)
            pec_r = np.array([_xe, _ye, 0.0, 1.0]).reshape(
                4, 1
            )  # homogenious coordinates: z-coordinate is dummy,
            # compute elastic center in HAWC2 c2_def axes
            pec_c2 = np.matmul(np.linalg.inv(T_rc2), pec_r)

            # set shear center in windIO reference axis ("r"-frame)
            psc_r = np.array([_xs, _ys, 0.0, 1.0]).reshape(
                4, 1
            )  # homogenious coordinates: z-coordinate is dummy,
            # compute shear center in HAWC2 c2_def axes
            psc_c2 = np.matmul(np.linalg.inv(T_rc2), psc_r)

            # set mass center in windIO reference axis ("r"-frame)
            pmc_r = np.array([_xm, _ym, 0.0, 1.0]).reshape(
                4, 1
            )  # homogenious coordinates: z-coordinate is dummy,
            # compute mass center in HAWC2 c2_def axes
            pmc_c2 = np.matmul(np.linalg.inv(T_rc2), pmc_r)

            # Transform the stiffness and mass related to the principal
            # elastic axis orientation from windIO reference axis system
            # to the HAWC2 blade root system
            # Rotation matrix for stiffness matrix
            R_rh = np.array(
                [
                    [1.0, 0.0, 0.0],
                    [0.0, np.cos(-theta_h2f), -np.sin(-theta_h2f)],
                    [0.0, np.sin(-theta_h2f), np.cos(-theta_h2f)],
                ]
            )

            # Rotation matrix for mass matrix
            Rm_rh = np.array(
                [
                    [1, 0, 0, 0, 0, 0],
                    [0, 1, 0, 0, 0, 0],
                    [0, 0, 1, 0, 0, 0],
                    [0, 0, 0, np.cos(-theta_h2f), -np.sin(-theta_h2f), 0.0],
                    [0, 0, 0, np.sin(-theta_h2f), np.cos(-theta_h2f), 0.0],
                    [0, 0, 0, 0.0, 0.0, 1.0],
                ]
            )

            Ke_ee = np.matmul(np.transpose(R_rh), np.matmul(_Ke_ee, R_rh))
            Ks_se = np.matmul(np.transpose(R_rh), np.matmul(_Ks_se, R_rh))

            # transform mass matrix
            M_mm = np.matmul(np.transpose(Rm_rh), np.matmul(_M_mm, Rm_rh))

            # Compute structural pitch or get it from user input value
            if st_pitch is None:
                # Compute structural pitch
                pitch[i] = -(np.abs(theta_e) - np.abs(_twist_c2))
            else:
                # get structural pitch
                pitch[i] = np.array(st_pitch[i])
                warn(
                    "st_blade_no_FPM",
                    self.get_no_warnings(),
                    "Using user input structure pitch angles",
                )

            # compute the structure pitch angle
            # pitch[i] = -(np.abs(theta_e) - np.abs(_twist_c2))

            # assemble the Nx6x6 matrix in this loop using the cross-sectional
            # stiffness and mass matrices
            K6x6[i, 2:5, 2:5] = Ke_ee
            K6x6[i, 0:2, 0:2] = Ks_se[:2, :2]
            K6x6[i, 5, 3:6] = Ks_se[2, :]
            K6x6[i, 3:6, 5] = Ks_se[:, 2]
            M6x6[i] = M_mm

            # Set elastic center, center of mass and shear center
            xe[i] = pec_c2[0, 0]
            ye[i] = pec_c2[1, 0]
            xm[i] = pmc_c2[0, 0]
            ym[i] = pmc_c2[1, 0]
            xs[i] = psc_c2[0, 0]
            ys[i] = psc_c2[1, 0]
            # compute radius of gyration (rx = sqrt(Ixx/m), ry = sqrt(Iyy/m))
            rx[i] = np.sqrt(M_mm[3, 3] / M_mm[0, 0])
            ry[i] = np.sqrt(M_mm[4, 4] / M_mm[0, 0])

        # Transform Nx6x6 to Nx21
        K = Nx6x6_to_Nx21(K6x6)
        # first store data in a list
        # the number of sections
        n = len(s)
        A = [1.0] * n  # choose a value for sectional area
        E = [_K6x6[2, 2] / _A for _K6x6, _A in zip(K6x6, A)]
        Ix = [_K6x6[3, 3] / _E for _K6x6, _E in zip(K6x6, E)]
        Iy = [_K6x6[4, 4] / _E for _K6x6, _E in zip(K6x6, E)]
        G = [1.0e10] * n  # choose a value for shear modulus
        I_torsion = [_K6x6[5, 5] / _G for _K6x6, _G in zip(K6x6, G)]
        kx = [_K6x6[0, 0] / (_G * _A) for _K6x6, _G, _A in zip(K6x6, G, A)]
        ky = [_K6x6[1, 1] / (_G * _A) for _K6x6, _G, _A in zip(K6x6, G, A)]

        values = [
            s,  # tower station
            M6x6[:, 0, 0].tolist(),  # mass/length
            xm.tolist(),  # center of mass, x
            ym.tolist(),  # center of mass, y
            rx.tolist(),  # radius gyration, x
            ry.tolist(),  # radius gyration, y
            xs.tolist(),  # shear center, x
            ys.tolist(),  # shear center, y
            E,  # young's modulus
            G,  # shear modulus
            Ix,  # area moment of inertia, x
            Iy,  # area moment of inertia, y
            I_torsion,  # torsional stiffness constant
            kx,  # shear reduction, x
            ky,  # shear reduction, y
            A,  # cross-sectional area
            rad2deg(pitch.tolist()),  # structural pitch
            xe.tolist(),  # elastic center, x
            ye.tolist(),  # elastic center, y
        ]
        # Setting data in dict
        out = dict(zip(self.header_classic(), values))
        # Output the data as numpy array format if required
        return [[out]]
