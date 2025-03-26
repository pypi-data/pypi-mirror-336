from copy import deepcopy

import numpy as np
from jmespath import search
from scipy.integrate import quad
from scipy.interpolate import PchipInterpolator, griddata
from scipy.spatial.transform import Rotation


def warn(method, no_warnings, message=None):
    import warnings

    if not no_warnings and message is None:
        warnings.warn(method + " is not implemented")

    if not no_warnings and message is not None:
        if not isinstance(message, str):
            raise TypeError("message should be a string")
        warnings.warn(method + " " + message)


def change_pitch_axis(x, y, z, chord, twist_rad, pitch_axis_in, pitch_axis_out):
    twist_rad = np.asarray(twist_rad)
    chord = np.asarray(chord)
    pitch_axis_in = np.asarray(pitch_axis_in)
    pitch_axis_out = np.asarray(pitch_axis_out)
    # Compute curve length
    s = compute_curve_length(x, y, z)

    # Create interpolation objects
    xi = PchipInterpolator(s, x)
    yi = PchipInterpolator(s, y)
    zi = PchipInterpolator(s, z)

    # Compute unit-vectors without twist
    tan_unit_vec = np.array([xi(s, 1), yi(s, 1), zi(s, 1)])
    tan_unit_vec /= np.linalg.norm(tan_unit_vec, axis=0)
    chord_unit_vec = np.array([np.zeros_like(x), -zi(s, 1), yi(s, 1)])
    chord_unit_vec /= np.linalg.norm(chord_unit_vec, axis=0)

    # Apply twist to unit-vectors
    chord_unit_vec = Rotation.from_rotvec(
        twist_rad.reshape((-1, 1)) * tan_unit_vec.T
    ).apply(chord_unit_vec.T)

    # Update x, y, z for new pitch axis
    return (
        x + chord_unit_vec[:, 0] * chord * (pitch_axis_in - pitch_axis_out),
        y + chord_unit_vec[:, 1] * chord * (pitch_axis_in - pitch_axis_out),
        z + chord_unit_vec[:, 2] * chord * (pitch_axis_in - pitch_axis_out),
    )


def compute_curve_length(x, y, z):
    st = np.zeros_like(x)
    st[1:] = np.cumsum(np.sqrt(np.diff(x) ** 2 + np.diff(y) ** 2 + np.diff(z) ** 2))
    xi = PchipInterpolator(st, x)
    yi = PchipInterpolator(st, y)
    zi = PchipInterpolator(st, z)

    def grad_mag(s):
        return np.sqrt(xi(s, 1) ** 2 + yi(s, 1) ** 2 + zi(s, 1) ** 2)

    s = np.zeros_like(x)
    for i, (st1, st2) in enumerate(zip(st[:-1], st[1:]), 1):
        s[i] = quad(grad_mag, st1, st2)[0] + s[i - 1]
    return s


def change_coord_sys(ref_axis, coordinate_transform):
    out = dict()
    for _name in ["x", "y", "z"]:
        sign = -1 if coordinate_transform[_name][0] == "-" else 1
        name = coordinate_transform[_name].replace("-", "")
        out[_name] = dict(
            grid=ref_axis[name]["grid"],
            values=(sign * np.asarray(ref_axis[name]["values"])).tolist(),
        )
    return out


def interp(x, x_in, y_in):
    return PchipInterpolator(x_in, y_in)(x).tolist()


def rad2deg(angle):
    return np.rad2deg(angle).tolist()


def deg2rad(angle):
    return np.deg2rad(angle).tolist()


def hz2rads(rot_speed):
    return 2 * np.pi * rot_speed


def rads2hz(rot_speed):
    return rot_speed / (2 * np.pi)


def degs2rads(rot_speed):
    return deg2rad(rot_speed)


def rads2degs(rot_speed):
    return rad2deg(rot_speed)


def rads2rpm(rot_speed):
    return rot_speed * 30 / np.pi


def rpm2rads(rot_speed):
    return rot_speed / rads2rpm(1.0)


def trapz(y, x):
    return np.trapezoid(y, x)


def TransformMatrix6x6(x, y, angle_rad):
    """Transform 6x6 beam inertia and stiffness matrix

        Example: (Transform away from elastic center)
        >>> R = Transform6x6(0., 0., -spitch) # Rotation
        >>> T = Transform6x6(-xe, -ye, 0.) # Translation
        >>> TR = T @ R # Combining Translation and Rotation
        >>> Kref = TR @ Kec @ TR.T # Applying the transformation for Kec

    Parameters
    ----------
    x : float
        Translation in x
    y : float
        Translation in y
    angle_rad : float
        rotation around current axis

    Returns
    -------
    ndarray
        Transformation matrix (translation and rotation) (shape=(6,6))
    """
    # First translation to (x,y) then rotation
    s = np.sin(angle_rad)
    c = np.cos(angle_rad)
    return np.array(
        [
            [c, s, 0.0, 0.0, 0.0, 0.0],
            [-s, c, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, x * s - y * c, c, s, 0.0],
            [0.0, 0.0, x * c + y * s, -s, c, 0.0],
            [y, -x, 0.0, 0.0, 0.0, 1.0],
        ]
    )


def Transform6x6(X, x, y, angle_rad):
    TR = TransformMatrix6x6(x, y, angle_rad)
    return TR @ X @ TR.T


def Nx21_to_Nx6x6(X):
    out = np.zeros((len(X), 6, 6))
    i_tri, j_tri = np.triu_indices(6)
    # i_triu, j_triu = np.triu_indices(6, 1)
    # i_tril, j_tril  = np.tril_indices(6, -1)
    for i, row in enumerate(X):
        out[i, i_tri, j_tri] = row
        out[i, j_tri, i_tri] = row
        # out[i, i_tril, j_tril] = out[i, i_triu, j_triu]
    return out


def Nx6x6_to_Nx21(X):
    out = np.zeros((len(X), 21))
    i_tri, j_tri = np.triu_indices(6)
    for i, mat in enumerate(X):
        out[i] = mat[i_tri, j_tri]
    return out


def TransformNx6x6(X, x, y, angle_rad):
    out = np.empty_like(X)
    for i, (mat, _x, _y, _ang) in enumerate(zip(X, x, y, angle_rad)):
        TR = TransformMatrix6x6(_x, _y, _ang)
        out[i] = TR @ mat @ TR.T
    return out


def TransformNx21(X, x, y, angle_rad):
    X6x6 = Nx21_to_Nx6x6(X)
    X6x6_trans = TransformNx6x6(X6x6, x, y, angle_rad)
    return Nx6x6_to_Nx21(X6x6_trans)


def vec6_to_mat3x3(X):
    out = np.zeros((3, 3))
    i_tri, j_tri = np.triu_indices(3)
    out[i_tri, j_tri] = X
    out[j_tri, i_tri] = X
    return out


def mat3x3_to_vec6(X):
    out = np.zeros((6))
    i_tri, j_tri = np.triu_indices(3)
    out = X[i_tri, j_tri]
    return out


def airfoils2polars(airfoils, aoa_rad=None, polar_index=None, kwargs_griddata=None):
    """Convert WindIO-airfoils to a set of polars. It is able to perform multi-dimensional interpolation for each airfoil

    Parameters
    ----------
    airfoils : list of dict
        Each list element is a WindIO airfoil dict
    aoa_rad : list or ndarray or dict or None, optional
        For list or ndarray of floats it will interpolate all polars to the same grid.
        For dict the grid control can be set for each airfoil while preserving the default.
            By name: aoa_rad={"FFA-W3-241":aoa_grid, ...} (Set a specific grid the airfoil with {"name": "FFA-W3-241", ...})
            By index: aoa_rad={1:aoa_grid, ...} (Set a specific grid the airfoil with index 1)
            Set default: aoa_rad={"default": aoa_grid, ...} (Set aoa_grid for all airfoils that are not set by the previous keys)
        For None (the default) the grid for the first c_l polar is used (aoa_grid=polars[0]["c_l"]["grid"])
    polar_index : int or str or dict or None, optional
        For int it will select the polar with the given index for all airfoils (polar_index=1 -> will select polar 1 for all airfoils)
        For str it will select the polar a given configurations name (polar_index="Triped" -> will select the polar with the "Triped" configuration for all airfoils)
        For dict the polars can be selected or interpolated for all or only a given subset. Using int or str for the value has a similar effect as above.
            By name: polar_index={"FFA-W3-241":2, ...} (For airfoil with name "FFA-W3-241" select polar 2)
            By index: polar_index={2:2, ...} (For airfoil 2 select polar 2)
            Set default: polar_index={"default": 2, ...} (For all airfoils not set otherwise select polar 2)
            Interpolation in re: polar_index={"default": {"re": 3e6}, ...} (Will interpolate airfoil polars for re=3e6 - interpolation requires that re is within range)
            Interpolation for configuration: polar_index={"default": {"configuration": {"Clean": 1, "Triped": 0}, "configuration_value": 0.5, ...} (Assigning values for each configuration (0 and 1) and interpolates to 0.5)
        For None (the default) the first polar is selected (equivalent to polar_index=0)
    kwargs_griddata : dict, optional
        Options parsed to scipy.interpolation.griddata. Can be used to select the interpolation method and set rescaling, by default None -> kwargs_griddata={"rescale"=True}

    Returns
    -------
    list
        Similar to WindIO-airfoils but with "polars" replaced with "polar".
        "polar" keywords:
            re: float, Reynolds Number
            configuration: dict, with name:value ({"Clean": 1, "Triped": 0})
            configuration_value: float, value for the configuration
            aoa_rad: ndarray or list, AoA in radians
            aoa_deg: ndarray or list, AoA in degrees
            c_l: ndarray or list, Lift coefficient
            c_d: ndarray or list, Drag coefficient
            c_m: ndarray or list, Moment coefficient
    """
    if kwargs_griddata is None:
        kwargs_griddata = dict(rescale=True)
    out = deepcopy(airfoils)
    # Sort airfoils by relative thickness
    iair_sorted = np.argsort([airfoil["relative_thickness"] for airfoil in airfoils])

    for iair in iair_sorted:
        # Get current airfoil
        airfoil = airfoils[iair].copy()
        out[iair].pop("polars")

        # Get indices for polars
        if polar_index is None:
            ipols = 0
        elif isinstance(polar_index, int):
            ipols = polar_index
        elif isinstance(polar_index, dict):
            if airfoil["name"] in polar_index:
                ipols = polar_index[airfoil["name"]]
            elif iair in polar_index:
                ipols = polar_index[iair]
            elif "default" in polar_index:
                ipols = polar_index["default"]
            else:
                ipols = 0
        else:
            ipols = polar_index

        if isinstance(ipols, str):
            ipols = [pol["configuration"] for pol in airfoil["polars"]].index(ipols)

        # Getting AoA
        if aoa_rad is None:
            # If not added using the same grid as c_l
            ipol = ipols if isinstance(ipols, int) else 0
            aoa_grid = airfoil["polars"][ipol]["c_l"]["grid"]
        else:
            if isinstance(aoa_rad, dict):
                if airfoil["name"] in aoa_rad:
                    aoa_grid = aoa_rad[airfoil["name"]]
                elif iair in aoa_rad:
                    # If aoa_grid_rad is a dict extract wrt. to index
                    aoa_grid = aoa_rad[iair]
                elif "default" in aoa_rad:
                    aoa_grid = aoa_rad["default"]
                else:
                    ipol = ipols if isinstance(ipols, int) else 0
                    aoa_grid = airfoil["polars"][ipol]["c_l"]["grid"]
            else:
                # Otherwise assume that aoa_grid_rad is a list/array
                aoa_grid = aoa_rad

        # Interpolate cl, cd, cm
        polar = dict()
        polar["aoa_rad"] = aoa_grid
        polar["aoa_deg"] = rad2deg(aoa_grid)

        if isinstance(ipols, int):
            polar.update(deepcopy(airfoil["polars"][ipols]))
            polar["configuration_value"] = polar["configuration"]
            for coef in ["c_l", "c_d", "c_m"]:
                polar[coef] = interp(
                    aoa_grid,
                    airfoil["polars"][ipols][coef]["grid"],
                    airfoil["polars"][ipols][coef]["values"],
                )
        else:
            if "configuration" in ipols:
                for con_key, con_value in ipols["configuration"].items():
                    for ipol, pol in enumerate(airfoil["polars"]):
                        if pol["configuration"] == con_key:
                            pol["configuration_value"] = con_value
                        elif isinstance(con_key, int) and con_key == ipol:
                            pol["configuration_value"] = con_value

            for coef in ["c_l", "c_d", "c_m"]:
                points = [
                    np.concatenate([pol[coef]["grid"] for pol in airfoil["polars"]])
                ]
                values = np.concatenate(
                    [pol[coef]["values"] for pol in airfoil["polars"]]
                )
                xi = [np.asarray(aoa_grid)]
                for key, value in ipols.items():
                    if "configuration" == key:
                        continue
                    points.append(
                        np.concatenate(
                            [
                                [pol[key]] * len(pol[coef]["grid"])
                                for pol in airfoil["polars"]
                            ]
                        )
                    )
                    xi.append(value)
                polar[coef] = griddata(
                    tuple(points), values, tuple(xi), **kwargs_griddata
                )
            polar["configuration"] = ipols.get(
                "configuration",
                {pol["configuration"]: None for pol in airfoil["polars"]},
            )
            polar["configuration_value"] = ipols.get("configuration_value", None)
            polar["re"] = ipols.get("re", [pol["re"] for pol in airfoil["polars"]])

        out[iair]["polar"] = polar

        # Interpolate airfoil coordinates
        if False:
            # From internal_structure
            x = af["coordinates"]["x"]
            y = af["coordinates"]["y"]
            if np.abs(y[0] - y[-1]) < 1.0e-12:
                y[0] += 0.002
                y[-1] -= 0.002
                print("opening base airfoil TE", label)
            dx = np.zeros_like(x)
            dy = np.zeros_like(x)
            dx[1:] = np.diff(x)
            dy[1:] = np.diff(y)
            ds = (dx**2 + dy**2) ** 0.5
            if np.any(ds[1:] == 0.0):
                raise ValueError("WARNING, non-unique points in airfoil", label)
            s = np.cumsum(ds)
            s /= s[-1]
            afn = np.zeros((snew.shape[0], 2))
            afn[:, 0] = PchipInterpolator(s, x)(snew)
            afn[:, 1] = PchipInterpolator(s, y)(snew)
            base_airfoils.append(afn)
            # Add to list
            out[iair]["polar"] = polar
    return out


def get_s_airfoils(wio_dict, airfoil_values=None):
    """Extracts the grid (along the span) and values for the airfoils from a WindIO dictionary.
    It will default to using the the relative thickness if available and unique.

    Parameters
    ----------
    wio_dict : dict
        WindIO dictionary
    airfoil_values : dict, optional
        Dictionary with keys for the airfoil names and corresponding numerical value, by default None (only used if relative_thickness is not unique for the airfoils used)

    Returns
    -------
    grid : list or ndarray
        Span grid where the s_airfoil values are located
    s_airfoils : list or ndarray
        Numerical values for the airfoils related to grid. Defaults to the relative thickness of the airfoils if they are unique.

    Raises
    ------
    Exception
        If not relative_thickness is unique and airfoil_values are not provided it will raise an exception
    """

    # Return rthick by default if present
    if "rthick" in wio_dict["components"]["blade"]["outer_shape_bem"]:
        return (
            wio_dict["components"]["blade"]["outer_shape_bem"]["rthick"]["grid"],
            wio_dict["components"]["blade"]["outer_shape_bem"]["rthick"]["values"],
        )

    # Use airfoil locations if relative_thickness is unique
    rthick_airfoils = {
        air["name"]: air["relative_thickness"] for air in wio_dict["airfoils"]
    }
    airfoils_used_unique = list(
        set(
            wio_dict["components"]["blade"]["outer_shape_bem"]["airfoil_position"][
                "labels"
            ]
        )
    )
    rthick_used_unique = set([rthick_airfoils[name] for name in airfoils_used_unique])
    if len(airfoils_used_unique) == len(rthick_used_unique):
        rthick = [
            rthick_airfoils[name]
            for name in wio_dict["components"]["blade"]["outer_shape_bem"][
                "airfoil_position"
            ]["labels"]
        ]
        return (
            wio_dict["components"]["blade"]["outer_shape_bem"]["airfoil_position"][
                "grid"
            ],
            rthick,
        )

    # Use airfoils values if not having unique relative_thickness
    if airfoil_values is None:
        raise Exception(
            "WindIO dict do not have rthick or a unique relative_thickness for the airfoils. It therefore need airfoil_values need to be provided to create s_airfoils"
        )
    return wio_dict["components"]["blade"]["outer_shape_bem"]["airfoil_position"][
        "grid"
    ], [
        airfoil_values[name]
        for name in wio_dict["components"]["blade"]["outer_shape_bem"][
            "airfoil_position"
        ]["labels"]
    ]


def jp(expression, data, options=None, return_value=True):
    out = search(expression, data, options)
    if return_value and out is None:
        raise ValueError(
            f"JMESPath did not return any data with expression {expression} for data {data}. Set `allow_none` to suppress this error."
        )
    return out
