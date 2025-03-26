import aesoptparam as apm

from ...windio import convert_coordinate_system
from .ae import ae
from .common import (
    base_inipos,
    connector_shaft_ratio,
    dtu_we_controller,
    filenames,
    grids,
    init_blade_pitch,
    init_rotor_speed,
    mbdy_names,
    nbodies,
    shaft_length,
    use_blade_FPM,
    use_constant_rotor_speed,
    windio_to_hawc2_base,
)
from .htc import htc
from .pc import pc
from .st import st


class windio_to_hawc2(windio_to_hawc2_base):
    htc = apm.SubParameterized(htc, precedence=0.20)
    ae = apm.SubParameterized(ae, precedence=0.21)
    pc = apm.SubParameterized(pc, precedence=0.22)
    st = apm.SubParameterized(st, precedence=0.23)
    filenames = apm.SubParameterized(filenames)
    mbdy_names = apm.SubParameterized(mbdy_names)
    grids = apm.SubParameterized(grids)
    nbodies = apm.SubParameterized(nbodies)
    dtu_we_controller = apm.SubParameterized(dtu_we_controller)
    no_warnings = apm.Boolean(
        False, doc="Flag for turning warnings on/off", precedence=1.0
    )
    use_blade_FPM = use_blade_FPM
    use_constant_rotor_speed = use_constant_rotor_speed
    shaft_length = shaft_length
    connector_shaft_ratio = connector_shaft_ratio
    init_blade_pitch = init_blade_pitch
    init_rotor_speed = init_rotor_speed
    base_inipos = base_inipos

    def __init__(self, windio_dict=None, parent_object=None, **params):
        super().__init__(windio_dict, parent_object, **params)
        self.windio_dict = convert_coordinate_system(
            self.windio_dict, cs_transform_name="windio_to_hawc2"
        ).convert()
        if self.has_floater():
            self.preprocessFloatingPlatformBodyMembers()
        if self.has_mooring():
            self.preprocessMooringMembers()
        self.param.trigger("connector_shaft_ratio")

    def convert(self):
        hawc2_dict = dict()
        # Add base files
        hawc2_dict["htc"] = self.htc.convert()
        hawc2_dict["ae"] = self.ae.convert()
        hawc2_dict["pc"] = self.pc.convert()
        hawc2_dict["st"] = self.st.convert()
        hawc2_dict["htc_filename"] = self.filenames.htc
        return hawc2_dict

    @apm.depends("shaft_length", watch=True)
    def update_connector_shaft_ratio(self):
        with apm.discard_events(self):
            self.connector_shaft_ratio = (
                self.shaft_length / self.get_connector_shaft_length()
            )

    @apm.depends("connector_shaft_ratio", watch=True)
    def update_shaft_length(self):
        with apm.discard_events(self):
            self.shaft_length = (
                self.get_connector_shaft_length() * self.connector_shaft_ratio
            )
