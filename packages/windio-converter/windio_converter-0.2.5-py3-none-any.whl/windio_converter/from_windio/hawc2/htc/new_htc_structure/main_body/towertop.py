import aesoptparam as apm
import numpy as np

from ......utils import mat3x3_to_vec6, vec6_to_mat3x3
from ....common import filenames, mbdy_names, nbodies
from .common import main_body_base


class towertop(main_body_base):
    filename = apm.copy_param_ref(
        filenames.param.towertop, "........filenames.towertop"
    )
    mbdy_name = apm.copy_param_ref(
        mbdy_names.param.towertop, "........mbdy_names.towertop"
    )
    nbodies = apm.copy_param_ref(nbodies.param.towertop, "........nbodies.towertop")

    def convert(self):
        tt = self.get_mbdy_base()

        # Get towertop length
        tt_len = self.get_towertop_length()

        # Add sec and nsec to c2_def
        tt["c2_def"]["nsec"] = 2
        tt["c2_def"]["sec"] = [[1, 0.0, 0.0, 0.0, 0.0], [2, 0.0, 0.0, -tt_len, 0.0]]

        # Navigate to elastic_properties_mb key
        tt_mass = self.windio_dict["components"]["nacelle"]["drivetrain"][
            "elastic_properties_mb"
        ]
        nacelle_MoI = np.array(tt_mass["system_inertia"])
        if len(nacelle_MoI) < 6:
            nacelle_MoI = np.append(nacelle_MoI, [0.0, 0.0, 0.0])
        nacelle_CoM = np.array(tt_mass["system_center_mass"])
        nacelle_mass = np.array(tt_mass["system_mass"])
        yaw_mass = np.array(tt_mass["yaw_mass"])

        # Setup the rotation matrix from OpenFAST tower top to HAWC2 tower top
        # rotation pi/2 radians around the z
        R_F2Fp = np.array(
            [
                [np.cos(np.pi / 2.0), -np.sin(np.pi / 2.0), 0.0],
                [np.sin(np.pi / 2.0), np.cos(np.pi / 2.0), 0.0],
                [0.0, 0.0, 1.0],
            ]
        )
        # rotation pi radians around the new x
        R_Fp2H = np.array(
            [
                [1.0, 0.0, 0.0],
                [0.0, np.cos(np.pi), -np.sin(np.pi)],
                [0.0, np.sin(np.pi), np.cos(np.pi)],
            ]
        )
        # compute the total rotation matrix from OpenFAST tt to HAWC2 tt
        R_Ftt2Htt = np.matmul(R_F2Fp, R_Fp2H)

        # Transform the CoM of Nacelle to HAWC2 coordinate system
        CoM_F = nacelle_CoM
        CoM_H = np.matmul(np.transpose(R_Ftt2Htt), CoM_F)
        nacelle_CoM = CoM_H

        # Transform the moment of inertia (MoI) of Nacelle around its CoM
        # represented in windIO reference system to HAWC2 reference system.

        # Convert the inertia 6x1 vector to the order: Ixx,Ixy,Ixz,Iyy,Iyz,Izz
        # to represent the upper-triangle of a 3x3 matrix
        i_3x3_utri = [0, 3, 4, 1, 5, 2]
        nac_MoI_vec6 = nacelle_MoI[i_3x3_utri]
        # make the 3x3 MoI matrix
        nac_MoI_tensor_F = vec6_to_mat3x3(nac_MoI_vec6)
        # Transform the MoI of Nacelle to HAWC2 coordinate system
        nac_MoI_tensor_H = np.matmul(
            np.transpose(R_Ftt2Htt), np.matmul(nac_MoI_tensor_F, R_Ftt2Htt)
        )
        # Convert to the vec(6) which represents the upper-triangle part of
        # a 3x3 matrix
        nac_MoI_vec6 = mat3x3_to_vec6(nac_MoI_tensor_H)
        # Convert the 6x1 inertia vector to the order: Ixx,Iyy,Izz,Ixy,Ixz,Iyz
        i_vec6 = [0, 3, 5, 1, 2, 4]
        nacelle_MoI = nac_MoI_vec6[i_vec6]

        # Now Add yaw and nacelle mass as concentrated_mass to htc-file
        tt["concentrated_mass"] = [
            [1, 0.0, 0.0, 0.0, yaw_mass.tolist(), 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # yaw
            [1]
            + nacelle_CoM.tolist()  # nacelle center of mass
            + [nacelle_mass.tolist()]  # total nacelle mass
            + nacelle_MoI.tolist(),  # nacelle moment of inertia
        ]
        return tt
