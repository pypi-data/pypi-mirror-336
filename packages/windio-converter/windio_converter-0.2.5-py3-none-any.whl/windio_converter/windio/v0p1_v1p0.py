from copy import deepcopy

hub_osb_names = dict(
    diameter="diameter", cone_angle="cone_angle", drag_coefficient="drag_coefficient"
)
nac_osb_names = dict(
    uptilt_angle="uptilt",
    distance_tt_hub="distance_tt_hub",
    overhang="overhang",
    drag_coefficient="drag_coefficient",
)
nac_epm_names = dict(
    above_yaw_mass="system_mass",
    center_mass="system_center_mass",
    inertia="system_inertia",
)


class v0p1_to_v1p0:
    def __init__(self, wio_dict, **kwargs) -> None:
        self.wio_dict = wio_dict

    def convert(self):
        # Copy the input windio dict
        wio_out = deepcopy(self.wio_dict)
        # WindIO version string
        wio_out["windio_version"] = 1.0
        # Update hub
        for old_name, new_name in hub_osb_names.items():
            if old_name in wio_out["components"]["hub"]["outer_shape_bem"]:
                wio_out["components"]["hub"][new_name] = wio_out["components"]["hub"][
                    "outer_shape_bem"
                ].pop(old_name)
        if wio_out["components"]["hub"]["outer_shape_bem"]:
            raise RuntimeError(
                f"Unknown elements in `hub.outer_shape_bem`: {wio_out['components']['hub']['outer_shape_bem']}"
            )
        else:
            wio_out["components"]["hub"].pop("outer_shape_bem")
        # Update nacelle outer_shape_bem
        wio_out["components"]["nacelle"].setdefault("drivetrain", {})
        for old_name, new_name in nac_osb_names.items():
            if old_name in wio_out["components"]["nacelle"]["outer_shape_bem"]:
                wio_out["components"]["nacelle"]["drivetrain"][new_name] = wio_out[
                    "components"
                ]["nacelle"]["outer_shape_bem"].pop(old_name)
        if wio_out["components"]["nacelle"]["outer_shape_bem"]:
            raise RuntimeError(
                f"Unknown elements in `nacelle.outer_shape_bem`: {wio_out['components']['nacelle']['outer_shape_bem']}"
            )
        else:
            wio_out["components"]["nacelle"].pop("outer_shape_bem")
        # Update nacelle elastic_properties_mb
        if "elastic_properties_mb" in wio_out["components"]["nacelle"]:
            wio_out["components"]["nacelle"]["drivetrain"]["elastic_properties_mb"] = (
                wio_out["components"]["nacelle"].pop("elastic_properties_mb")
            )
            nac_epm = wio_out["components"]["nacelle"]["drivetrain"][
                "elastic_properties_mb"
            ]
            for old_name, new_name in nac_epm_names.items():
                if old_name in nac_epm:
                    nac_epm[new_name] = nac_epm.pop(old_name)
        return wio_out


class v1p0_to_v0p1:
    def __init__(self, wio_dict, **kwargs) -> None:
        self.wio_dict = wio_dict

    def convert(self):
        # Copy the input windio dict
        wio_out = deepcopy(self.wio_dict)
        # WindIO version string
        wio_out["windio_version"] = 0.1
        # hub
        hub_osb = dict()
        for old_name, new_name in hub_osb_names.items():
            if new_name in wio_out["components"]["hub"]:
                hub_osb[old_name] = wio_out["components"]["hub"].pop(new_name)
        if hub_osb:
            wio_out["components"]["hub"]["outer_shape_bem"] = hub_osb
        # nacelle
        nacelle_osb = dict()
        for old_name, new_name in nac_osb_names.items():
            if new_name in wio_out["components"]["nacelle"]["drivetrain"]:
                nacelle_osb[old_name] = wio_out["components"]["nacelle"][
                    "drivetrain"
                ].pop(new_name)
        if nacelle_osb:
            wio_out["components"]["nacelle"]["outer_shape_bem"] = nacelle_osb
        # Update nacelle elastic_properties_mb
        if "elastic_properties_mb" in wio_out["components"]["nacelle"]["drivetrain"]:
            wio_out["components"]["nacelle"]["elastic_properties_mb"] = wio_out[
                "components"
            ]["nacelle"]["drivetrain"].pop("elastic_properties_mb")
            nac_epm = wio_out["components"]["nacelle"]["elastic_properties_mb"]
            for new_name, old_name in nac_epm_names.items():
                if old_name in nac_epm:
                    nac_epm[new_name] = nac_epm.pop(old_name)
        return wio_out
