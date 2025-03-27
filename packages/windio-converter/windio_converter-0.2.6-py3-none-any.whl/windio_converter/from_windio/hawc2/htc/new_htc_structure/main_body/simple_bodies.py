import aesoptparam as apm

from ....common import filenames, mbdy_names, nbodies, shaft_length
from .common import main_body_base


class connector(main_body_base):
    filename = apm.copy_param_ref(
        filenames.param.connector, "........filenames.connector"
    )
    shaft_length = apm.copy_param_ref(shaft_length, "........shaft_length")
    mbdy_name = apm.copy_param_ref(
        mbdy_names.param.connector, "........mbdy_names.connector"
    )
    nbodies = apm.copy_param_ref(nbodies.param.connector, "........nbodies.connector")

    def convert(self):
        con = self.get_mbdy_base()
        # Get connector length
        con_len = self.get_connector_shaft_length() - self.shaft_length

        # Add sec and nsec
        con["c2_def"]["nsec"] = 2
        con["c2_def"]["sec"] = [[1, 0.0, 0.0, 0.0, 0.0], [2, 0.0, 0.0, con_len, 0.0]]
        return con


class hub(main_body_base):
    filename = apm.copy_param_ref(filenames.param.hub, "........filenames.hub")
    mbdy_name = apm.copy_param_ref(mbdy_names.param.hub, "........mbdy_names.hub")
    nbodies = apm.copy_param_ref(nbodies.param.hub, "........nbodies.hub")

    def convert(self):
        hub = self.get_mbdy_base(1)
        # Get connector length
        hub_len = self.windio_dict["components"]["hub"]["diameter"] / 2

        # Add sec and nsec
        hub["c2_def"]["nsec"] = 2
        hub["c2_def"]["sec"] = [[1, 0.0, 0.0, 0.0, 0.0], [2, 0.0, 0.0, hub_len, 0.0]]
        return hub
