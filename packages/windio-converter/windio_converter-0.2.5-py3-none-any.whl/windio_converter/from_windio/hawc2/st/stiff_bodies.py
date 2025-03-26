import aesoptparam as apm
import numpy as np

from ..common import shaft_length
from .common import st_base


class stiff_body(st_base):
    def convert(self):
        out = dict()
        # Assuming rigid body has cylinder shape and is massless in this
        # new implementation
        s_len = self.get_body_length()
        mass = 1.0
        r = 1.0  # assuming cylinder radius is one
        for name in self.header_classic():
            if name in ["x_cg", "y_cg", "x_sh", "y_sh", "xe", "ye", "pitch"]:
                out[name] = [0.0] * 2
            elif name in ["ri_y", "ri_x"]:
                Ix = 1.0 / 12.0 * mass * (3.0 * r**2 + s_len**2)
                rx = np.sqrt(
                    Ix / mass
                )  # Should this be sqrt(Ix/A)? and not sqrt(Ix/m)?!
                out[name] = [rx] * 2
            elif name in ["E", "G"]:
                out[name] = [1e17] * 2
            elif name in ["m"]:  # Assuming total mass is 1 kg
                out[name] = [1.0 / s_len] * 2
            elif name in ["s"]:
                out[name] = [0, s_len]
            else:
                out[name] = [1.0] * 2

        return [[out]]

    def get_body_length(self):
        raise NotImplementedError(
            f"{type(self).__name__} body length is not implemented"
        )


class towertop(stiff_body):
    def get_body_length(self):
        return self.get_towertop_length()


class connector(stiff_body):
    shaft_length = apm.copy_param_ref(shaft_length, "....shaft_length")

    def get_body_length(self):
        return self.get_connector_shaft_length() - self.shaft_length


class shaft(stiff_body):
    shaft_length = apm.copy_param_ref(shaft_length, "....shaft_length")

    def get_body_length(self):
        return self.shaft_length


class hub(stiff_body):
    def get_body_length(self):
        return self.windio_dict["components"]["hub"]["diameter"] / 2
