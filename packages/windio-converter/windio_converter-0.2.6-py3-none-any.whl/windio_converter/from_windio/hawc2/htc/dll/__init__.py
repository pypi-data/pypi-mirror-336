import aesoptparam as apm

from ...common import dtu_we_controller as dtu_we_controller_options
from ...common import windio_to_hawc2_child
from .type2_dll import type2_dll


class dll(windio_to_hawc2_child):
    type2_dll = apm.SubParameterized(type2_dll, precedence=0.20)
    add_controller_block = apm.utils.copy_param_ref(
        dtu_we_controller_options.param.add_controller_block,
        "....dtu_we_controller.add_controller_block",
    )

    def convert(self):
        dlls = dict()
        dlls["type2_dll"] = self.type2_dll.convert()
        return dlls

    def add_dll(self):
        """Method to compute if the DLL block should be added"""
        return self.add_controller_block
