import aesoptparam as apm

from .common import new_htc_structure_base
from .constraints import constraints
from .ext_sys import ext_sys
from .main_body import main_body
from .orientation import orientation


class new_htc_structure(new_htc_structure_base):
    main_body = apm.SubParameterized(main_body, precedence=0.20)
    orientation = apm.SubParameterized(orientation, precedence=0.21)
    constraints = apm.SubParameterized(constraints, precedence=0.22)
    ext_sys = apm.SubParameterized(ext_sys, precedence=0.23)

    def convert(self):
        nhs = dict()
        nhs["main_body"] = self.main_body.convert()
        nhs["orientation"] = self.orientation.convert()
        nhs["constraint"] = self.constraints.convert()
        if self.has_mooring():
            nhs["ext_sys"] = self.ext_sys.convert()
        return nhs
