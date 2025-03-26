import aesoptparam as apm

from ....common import dtu_we_controller as dtu_we_controller_options
from ....common import windio_to_hawc2_child
from .dtu_we_controller import dtu_we_controller


class type2_dll(windio_to_hawc2_child):
    dtu_we_controller = apm.SubParameterized(dtu_we_controller, precedence=0.20)
    add_controller_block = apm.utils.copy_param_ref(
        dtu_we_controller_options.param.add_controller_block,
        "......dtu_we_controller.add_controller_block",
    )

    def convert(self):
        type2_dll = []
        if self.add_controller_block:
            type2_dll.append(self.dtu_we_controller.convert())
        return type2_dll
