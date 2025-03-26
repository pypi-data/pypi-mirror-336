import aesoptparam as apm
import numpy as np

from ......utils import mat3x3_to_vec6, vec6_to_mat3x3
from ....common import filenames, mbdy_names, nbodies, shaft_length
from .common import main_body_base


class shaft(main_body_base):
    shaft_length = apm.copy_param_ref(shaft_length, "........shaft_length")
    filename = apm.copy_param_ref(filenames.param.shaft, "........filenames.shaft")
    mbdy_name = apm.copy_param_ref(mbdy_names.param.shaft, "........mbdy_names.shaft")
    nbodies = apm.copy_param_ref(nbodies.param.shaft, "........nbodies.shaft")

    def convert(self):
        shaft = self.get_mbdy_base()
        # Get shaft length
        shaft_len = self.shaft_length

        # Add sec and nsec
        shaft["c2_def"]["nsec"] = 2
        shaft["c2_def"]["sec"] = [
            [1, 0.0, 0.0, 0.0, 0.0],
            [2, 0.0, 0.0, shaft_len, 0.0],
        ]

        # Add hub mass
        hub_epmb = self.windio_dict["components"]["hub"]["elastic_properties_mb"]
        if "system_center_mass" in hub_epmb:
            CoM_F = np.array(hub_epmb["system_center_mass"])
        else:
            CoM_F = np.array([0.0, 0.0, 0.0])
        MoI_F = np.array(hub_epmb["system_inertia"])
        if len(MoI_F) < 6:
            MoI_F = np.append(MoI_F, [0.0, 0.0, 0.0])

        # Setup the rotation matrix from OpenFAST hub-align to HAWC2 shaft.
        # rotation pi/2 radians around the z
        R_F2Fp = np.array(
            [
                [np.cos(np.pi / 2.0), -np.sin(np.pi / 2.0), 0.0],
                [np.sin(np.pi / 2.0), np.cos(np.pi / 2.0), 0.0],
                [0.0, 0.0, 1.0],
            ]
        )
        # rotation -(pi/2) radians around the new x
        R_Fp2H = np.array(
            [
                [1.0, 0.0, 0.0],
                [0.0, np.cos(-np.pi / 2.0), -np.sin(-np.pi / 2.0)],
                [0.0, np.sin(-np.pi / 2.0), np.cos(-np.pi / 2.0)],
            ]
        )
        # compute the total rotation matrix from OpenFAST hub to HAWC2 shaft.
        R_Fhub2Hsh = np.matmul(R_F2Fp, R_Fp2H)
        # Transform the CoM of hub to HAWC2 coordinate system
        CoM_H = np.matmul(np.transpose(R_Fhub2Hsh), CoM_F)

        # Transform the moment of inertia (MoI) of hub around its CoM to HAWC2
        # shaft.

        # Convert the vec(6) inertia vector to represent the upper-triangle of
        # a 3x3 matrix row by row.
        # Convert the inertia vector to the order: Ixx,Ixy,Ixz,Iyy,Iyz,Izz
        i_3x3_utri = [0, 3, 4, 1, 5, 2]
        MoI_vec6 = MoI_F[i_3x3_utri]
        # make the 3x3 MoI matrix
        MoI_tensor_F = vec6_to_mat3x3(MoI_vec6)
        # Transform the MoI of hub to HAWC2 coordinate system
        MoI_tensor_H = np.matmul(
            np.transpose(R_Fhub2Hsh), np.matmul(MoI_tensor_F, R_Fhub2Hsh)
        )
        # Convert to the vec(6) which represents the upper-triangle part of
        # a 3x3 matrix
        MoI_vec6 = mat3x3_to_vec6(MoI_tensor_H)
        # Convert the 6x1 vector to the order: Ixx,Iyy,Izz,Ixy,Ixz,Iyz
        i_vec6 = [0, 3, 5, 1, 2, 4]
        MoI_H = MoI_vec6[i_vec6]

        # the coordinate system of moment of inertia needs to be checked and
        # fixed
        shaft["concentrated_mass"] = [
            [2]
            + CoM_H.tolist()  # represent hub center of mass
            + [hub_epmb["system_mass"]]  # represent total hub mass
            + MoI_H.tolist(),  # represent moment of inertia
        ]
        return shaft
