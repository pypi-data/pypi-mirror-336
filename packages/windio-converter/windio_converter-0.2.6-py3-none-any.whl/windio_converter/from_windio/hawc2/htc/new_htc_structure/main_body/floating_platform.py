import aesoptparam as apm
import numpy as np

from ......utils import interp
from ....common import filenames, floater_mooring_base
from .common import main_body_base


class floating_platform(main_body_base, floater_mooring_base):
    filename = apm.copy_param_ref(filenames.param.floater, "........filenames.floater")

    def convert(self):
        floaterMultibodies = []

        for member_ in self.windio_dict["components"]["floating_platform"]["members"]:
            mono_axis = member_["reference_axis"]
            grid = mono_axis["grid"]

            # Coordinate in local coordinate system
            z_val = mono_axis["values"]
            z_val = [z - z_val[0] for z in z_val]
            z_loc = interp(grid, mono_axis["grid"], z_val)

            # Initial offset
            x0 = member_["jointObjRef"][0]["xyz"]

            # Coordinates in global system
            coord_abs = x0 + np.outer(z_loc, member_["unit_axial_vector"])

            # Rotate to Hawc2 coordinate system
            coord_abs_hawc = np.zeros_like(coord_abs)
            coord_abs_hawc[:, 0] = coord_abs[:, 1]
            coord_abs_hawc[:, 1] = coord_abs[:, 0]
            coord_abs_hawc[:, 2] = -coord_abs[:, 2]

            nsec = len(grid)
            memberBase = self.get_mbdy_base(member_["name"], nbodies=1)

            if member_["jointObjRef"][0].get("transition", False):
                nsecTransition = 1
            elif member_["jointObjRef"][-1].get("transition", False):
                nsecTransition = len(grid)
            else:
                nsecTransition = None

            if nsecTransition is not None:
                memberBase["concentrated_mass"] = [
                    [
                        nsecTransition,
                        0.0,
                        0.0,
                        0.0,
                        self.windio_dict["components"]["floating_platform"][
                            "transition_piece_mass"
                        ],
                        0.0,
                        0.0,
                        0.0,
                    ]
                ]

            # Add sec and nsec
            sec = [None] * nsec
            for i, (x, y, z) in enumerate(coord_abs_hawc):
                sec[i] = [i + 1, x, y, z, 0.0]
            memberBase["c2_def"]["nsec"] = nsec
            memberBase["c2_def"]["sec"] = sec

            floaterMultibodies.append(memberBase)

        if self.has_mooring():
            self.preprocessMooringMembers()

        return floaterMultibodies

    def get_mbdy_base(self, mbdy_name, imbdy=None, nbodies=1):
        name = self.get_full_mbdy_name(mbdy_name, imbdy)
        return dict(
            name=name,
            type="timoschenko",
            nbodies=nbodies,
            node_distribution="c2_def",
            timoschenko_input=dict(filename=self.filename, set=[1, 1]),
            c2_def=dict(),
        )
