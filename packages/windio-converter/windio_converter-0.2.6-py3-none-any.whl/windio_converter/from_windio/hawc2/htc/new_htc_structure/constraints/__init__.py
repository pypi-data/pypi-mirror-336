import aesoptparam as apm

from ..common import new_htc_structure_base
from .bearing import bearing1, bearing2, bearing3
from .fix import fix0, fix1
from .mooring import mooring


class constraints(new_htc_structure_base):
    fix0 = apm.SubParameterized(fix0)
    fix1 = apm.SubParameterized(fix1)
    bearing1 = apm.SubParameterized(bearing1)
    bearing2 = apm.SubParameterized(bearing2)
    bearing3 = apm.SubParameterized(bearing3)
    mooring = apm.SubParameterized(mooring)

    def convert(self):
        constraintsDict = dict(
            fix0=self.fix0.convert(),
            fix1=self.fix1.convert(),
            bearing1=self.bearing1.convert(),
            bearing2=self.bearing2.convert(),
            bearing3=self.bearing3.convert(),
        )

        if self.has_mooring():
            constraintsDict["dll"] = self.mooring.convert()

        # Remove empty constraint types
        constraintsDict = {k: v for k, v in constraintsDict.items() if v}

        return constraintsDict
