import aesoptparam as apm


class windio_converter_base(apm.AESOptParameterized):
    windio_dict = apm.SubParameterized(
        dict,
        default=lambda self: self.get_windio_dict(),
        doc="windIO data structure",
        precedence=0.0,
    )

    def __init__(self, windio_dict=None, parent_object=None, **params):
        super().__init__(parent_object=parent_object)
        if not windio_dict is None:
            self._param__private.values["windio_dict"] = windio_dict
        self.from_dict(params)

    def convert(self):
        raise RuntimeError("`.convert` is not implemented")

    def get_windio_dict(self):
        if callable(self._param__private.values["windio_dict"]):
            if self.has_parent():
                return self.parent_object.get_windio_dict()
            return None
        return self._param__private.values["windio_dict"]


def copy_param(param, exclude=None, update=None):
    if exclude is None:
        exclude = []
    if update is None:
        update = dict()
    kwargs = dict()
    for name in param._slot_defaults:
        if (
            name == "allow_none"
        ):  # Should be fixed in aesoptparam (remove afterwards, kenloen)
            name = "allow_None"
        val = getattr(param, name)
        if not name in exclude and val is not None:
            kwargs[name] = val
    for name, val in update.items():
        kwargs[name] = val

    return type(param)(**kwargs)
