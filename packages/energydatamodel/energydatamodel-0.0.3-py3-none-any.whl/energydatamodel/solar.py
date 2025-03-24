from dataclasses import dataclass, field
from typing import List, Optional, Union
import pandas as pd
from shapely.geometry import Point
import pytz
from uuid import uuid4
import json
import pvlib

from energydatamodel import EnergyAsset, GeoPolygon, GeoMultiPolygon


@dataclass
class FixedMount:
    surface_tilt: float = 0.0
    surface_azimuth: float = 0.0


@dataclass
class SingleAxisTrackerMount: 
    axis_tilt: float = 0.0
    axis_azimuth: float = 0.0 
    max_angle: Union[float, tuple] = 90.0 
    backtrack: bool = True 
    gcr: float = 0.2857142857142857 
    cross_axis_tilt: float = 0.0 
    racking_model: Optional[str] = None
    module_height: Optional[float] = None


@dataclass(repr=False)
class PVArray(EnergyAsset):
    capacity: Optional[float] = None 
    surface_azimuth: Optional[float] = None 
    surface_tilt: Optional[float] = None 
    surface_area: Optional[float] = None        # Area in square meters
    efficiency: Optional[float] = None  # Efficiency in percentage
    module: Optional[str] = None
    module_type: str = "glass_polymer"
    module_parameters: Union[dict, pd.Series] = None
    temperature_model_parameters: Union[dict, pd.Series] = None

    def get_timeseries(self):
        return self.timeseries_df[self.column_df]

@dataclass(repr=False)
class PVSystem(EnergyAsset):
    """
    The PVSystem class defines a standard set of PV system attributes
    and modeling functions. This class describes the collection and
    interactions of PV system components rather than an installed system
    on the ground. It is typically used in combination with
    :py:class:`~pvlib.location.Location` and
    :py:class:`~pvlib.modelchain.ModelChain`
    objects.

    """

    pv_arrays: List[PVArray] = field(default_factory=list)
    capacity: float = None
    surface_azimuth: float = None
    surface_tilt: float = None
    albedo: Optional[float] = None
    surface_type: Optional[str] = None
    module_parameters: Optional[dict] = None
    inverter_parameters: Optional[dict] = None
    module_type: str = "glass_polymer"
    racking_model: str = "open_rack"

    def __post_init__(self):
        super().__post_init__()

        # If no PVArray list is provided, but capacity, azimuth, and tilt are,
        # create a PVArray and add it to the list.
        if not self.pv_arrays and all([self.capacity, self.surface_azimuth, self.surface_tilt]):
            self.pv_arrays.append(PVArray(capacity=self.capacity, surface_azimuth=self.surface_azimuth, surface_tilt=self.surface_tilt))

    """

    The class supports basic system topologies consisting of:

        * `N` total modules arranged in series
          (`modules_per_string=N`, `strings_per_inverter=1`).
        * `M` total modules arranged in parallel
          (`modules_per_string=1`, `strings_per_inverter=M`).
        * `NxM` total modules arranged in `M` strings of `N` modules each
          (`modules_per_string=N`, `strings_per_inverter=M`).

    The class is complementary to the module-level functions.

    The attributes should generally be things that don't change about
    the system, such the type of module and the inverter. The instance
    methods accept arguments for things that do change, such as
    irradiance and temperature.

    Parameters
    ----------
    arrays : Array or iterable of Array, optional
        An Array or list of arrays that are part of the system. If not
        specified a single array is created from the other parameters (e.g.
        `surface_tilt`, `surface_azimuth`). If specified as a list, the list
        must contain at least one Array;
        if length of arrays is 0 a ValueError is raised. If `arrays` is
        specified the following PVSystem parameters are ignored:

        - `surface_tilt`
        - `surface_azimuth`
        - `albedo`
        - `surface_type`
        - `module`
        - `module_type`
        - `module_parameters`
        - `temperature_model_parameters`
        - `modules_per_string`
        - `strings_per_inverter`

    surface_tilt: float or array-like, default 0
        Surface tilt angles in decimal degrees.
        The tilt angle is defined as degrees from horizontal
        (e.g. surface facing up = 0, surface facing horizon = 90)

    surface_azimuth: float or array-like, default 180
        Azimuth angle of the module surface.
        North=0, East=90, South=180, West=270.

    albedo : float, optional
        Ground surface albedo. If not supplied, then ``surface_type`` is used
        to look up a value in ``irradiance.SURFACE_ALBEDOS``.
        If ``surface_type`` is also not supplied then a ground surface albedo
        of 0.25 is used.

    surface_type : string, optional
        The ground surface type. See ``irradiance.SURFACE_ALBEDOS`` for
        valid values.

    module : string, optional
        The model name of the modules.
        May be used to look up the module_parameters dictionary
        via some other method.

    module_type : string, default 'glass_polymer'
         Describes the module's construction. Valid strings are 'glass_polymer'
         and 'glass_glass'. Used for cell and module temperature calculations.

    module_parameters : dict or Series, optional
        Module parameters as defined by the SAPM, CEC, or other.

    temperature_model_parameters : dict or Series, optional
        Temperature model parameters as required by one of the models in
        pvlib.temperature (excluding poa_global, temp_air and wind_speed).

    modules_per_string: int or float, default 1
        See system topology discussion above.

    strings_per_inverter: int or float, default 1
        See system topology discussion above.

    inverter : string, optional
        The model name of the inverters.
        May be used to look up the inverter_parameters dictionary
        via some other method.

    inverter_parameters : dict or Series, optional
        Inverter parameters as defined by the SAPM, CEC, or other.

    racking_model : string, default 'open_rack'
        Valid strings are 'open_rack', 'close_mount', and 'insulated_back'.
        Used to identify a parameter set for the SAPM cell temperature model.

    losses_parameters : dict or Series, optional
        Losses parameters as defined by PVWatts or other.

    name : string, optional

    **kwargs
        Arbitrary keyword arguments.
        Included for compatibility, but not used.

    Raises
    ------
    ValueError
        If `arrays` is not None and has length 0.

    See also
    --------
    pvlib.location.Location

    """

    def to_pvlib(self, **kwargs):
        # TODO This one is a bit tricky. 
        # When creating pvlib object I want to be able to add missing parameters
        # But still use the ones that are already set on the edm.PVSystem object. 
        if self.module_parameters is None:
            self.module_parameters = {"pdc0": self.capacity}
#            self.module_parameters.update({"pdc0": self.capacity})
        if "pdc0" not in self.module_parameters.keys():
            self.module_parameters["pdc0"] = self.capacity

        if self.inverter_parameters is None:
            self.inverter_parameters = {"pdc0": self.capacity}
        if "pdc0" not in self.inverter_parameters.keys():
            self.inverter_parameters["pdc0"] = self.capacity

        return pvlib.pvsystem.PVSystem(name=self.name,
                                surface_tilt=self.surface_tilt, 
                                surface_azimuth=self.surface_azimuth, 
                                albedo=self.albedo, 
                                surface_type=self.surface_type,
                                module_parameters=self.module_parameters,
                                inverter_parameters=self.inverter_parameters,
                                module_type=self.module_type,
                                racking_model=self.racking_model,
                                **kwargs) 


@dataclass(repr=False)
class SolarPowerArea(EnergyAsset): 
    capacity: Union[float, pd.DataFrame] = None
    geopolygon: Union[GeoPolygon, GeoMultiPolygon] = None

    def to_geojson(self):
        return json.loads(json.dumps(self.geopolygon.multipolygon.__geo_interface__))

    @property
    def geojson(self):
        return self.to_geojson()