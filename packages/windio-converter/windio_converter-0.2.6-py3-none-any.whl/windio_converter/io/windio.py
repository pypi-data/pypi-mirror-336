import numpy as np
from scipy.interpolate import PchipInterpolator

from .aesopt import AESOpt_dict, AESOpt_list


class WindIO_dict(AESOpt_dict):
    """WindIO dict type to interact with WindIO data structure. Inherits from AESOpt_dict - see that for documentation of all methods."""

    def interp(self, grid=None, extrapolate=True, inplace=False):
        """Interpolate grid-value pair for a given new grid, using `scipy.interpolation.PchipInterpolator`.

        It only works for objects with grid and value fields.

        Parameters
        ----------
        grid : ndarray,list,int,None, optional
            None -> returns the "value" elements
            int -> return interpolated value for linspaced values in the range for grid
            ndarray,list -> iter with grid values to interpolate for
        extrapolate : bool, optional
            Flag for doing extrapolation (see `scipy.interpolation.PchipInterpolator` for more), by default True
        inplace : bool, optional
            Flag, `True` means the `grid` and value is overwritten, by default False

        Returns
        -------
        ndarray
            interpolated values

        Raises
        ------
        AttributeError
            If the current location do not contain `grid`, `values` keys.
        """
        if not ("grid" in self and "values" in self):
            raise AttributeError(
                "The object do not contain grid and values and the interp can not be used"
            )
        if grid is None:
            return self["values"]
        if isinstance(grid, int):
            grid = np.linspace(self["grid"][0], self["grid"][-1], grid)
        if extrapolate:
            vals = PchipInterpolator(self["grid"], self["values"])(grid)
        else:
            vals = PchipInterpolator(self["grid"], self["values"], extrapolate=False)(
                grid
            )
            ix = np.argwhere(np.isnan(vals) == False).flatten()
            grid = np.asarray(grid)[ix]
            vals = vals[ix]
        if inplace:
            self.update(grid=grid, values=vals)
        return vals


class WindIO_list(AESOpt_list):
    """WindIO list type to interact with WindIO data structure. Inherits from AESOpt_list - see that for documentation of all methods."""

    pass
