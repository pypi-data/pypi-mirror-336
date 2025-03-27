import aesoptparam as apm

from ..common import windio_to_hawc2_child
from .aero_hydro import aero, aerodrag, hydro
from .dll import dll
from .new_htc_structure import new_htc_structure


class htc(windio_to_hawc2_child):
    """Settings for the HTC-file conversion"""

    new_htc_structure = apm.SubParameterized(new_htc_structure, precedence=0.20)
    aero = apm.SubParameterized(aero, precedence=0.21)
    aerodrag = apm.SubParameterized(aerodrag, precedence=0.22)
    hydro = apm.SubParameterized(hydro, precedence=0.23)
    dll = apm.SubParameterized(dll, precedence=0.24)

    def convert(self):
        htc_data = dict()
        htc_data["new_htc_structure"] = self.new_htc_structure.convert()
        htc_data["aero"] = self.aero.convert()
        htc_data["aerodrag"] = self.aerodrag.convert()
        if self.has_floater() or self.has_monopile():
            htc_data["hydro"] = self.hydro.convert()
            if not htc_data["hydro"]:
                htc_data.pop("hydro")
        if self.dll.add_dll():
            htc_data["dll"] = self.dll.convert()
        return htc_data
