import aesoptparam as apm

from ..common import new_htc_structure_base
from .base import base
from .relative import relative


class orientation(new_htc_structure_base):
    base = apm.SubParameterized(base, precedence=0.20)
    relative = apm.SubParameterized(relative, precedence=0.21)

    def convert(self):
        ori = dict()
        # Base
        ori["base"] = self.base.convert()
        # Relative
        ori["relative"] = self.relative.convert()
        return ori
