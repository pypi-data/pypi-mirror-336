import aesoptparam as apm

from ......utils import rad2deg
from ....common import filenames, grids, mbdy_names, nbodies, use_blade_FPM
from .common import main_body_base


class blade(main_body_base):
    grid = apm.copy_param_ref(grids.param.blade, "........grids.blade")
    filename = apm.copy_param_ref(filenames.param.blade, "........filenames.blade")
    mbdy_name = apm.copy_param_ref(mbdy_names.param.blade, "........mbdy_names.blade")
    nbodies = apm.copy_param_ref(nbodies.param.blade, "........nbodies.blade")
    use_blade_FPM = apm.copy_param_ref(use_blade_FPM, "........use_blade_FPM")

    def convert(self):
        # c2_def
        # Change coordinate system
        x_h2, y_h2, z_h2, twist_deg = self.get_blade_c2def(self.grid)
        nsec = len(x_h2)
        sec = [None] * nsec
        for i, (x, y, z, twist) in enumerate(zip(x_h2, y_h2, z_h2, twist_deg)):
            sec[i] = [i + 1, x, y, z, -twist]

        bmbdy = self.get_mbdy_base(1)
        bmbdy["c2_def"]["nsec"] = nsec
        bmbdy["c2_def"]["sec"] = sec
        if self.use_blade_FPM:
            bmbdy["timoschenko_input"]["fpm"] = 1
        else:
            bmbdy["timoschenko_input"]["fpm"] = 0
        return bmbdy
