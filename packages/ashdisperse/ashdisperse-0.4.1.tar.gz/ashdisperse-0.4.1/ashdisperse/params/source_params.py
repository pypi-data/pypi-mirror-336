from collections import OrderedDict

import numpy as np
from numba import float64, int64, optional
from numba.experimental import jitclass
from numba.types import unicode_type

source_spec = OrderedDict()
source_spec["latitude"] = float64  # latitude of source
source_spec["longitude"] = float64  # longitude of source
source_spec["utmcode"] = int64  # EPSG utm code of source
source_spec["radius"] = float64  # radius of the source
source_spec["PlumeHeight"] = float64  # height of the source plume
source_spec["MER"] = float64  # mass eruption rate
source_spec["duration"] = float64  # duration of eruption
source_spec["name"] = unicode_type  # name of source


@jitclass(source_spec)
class SourceParameters:
    def __init__(
        self,
        lat,
        lon,
        utmcode,
        radius=10e3,
        PlumeHeight=10e3,
        MER=1e6,
        duration=18000,
        name="",
    ):

        self.latitude = np.float64(lat)
        self.longitude = np.float64(lon)
        self.utmcode = utmcode

        if radius < 0:
            raise ValueError("In SourceParameters, radius must be positive")
        self.radius = np.float64(radius)

        if PlumeHeight < 0:
            raise ValueError("In SourceParameters, PlumeHeight must be positive")
        self.PlumeHeight = np.float64(PlumeHeight)

        if MER < 0:
            raise ValueError("In SourceParameters, MER must be positive")
        self.MER = np.float64(MER)

        if duration < 0:
            raise ValueError("In SourceParameters, duration must be positive")
        self.duration = np.float64(duration)

        self.name = name

    def describe(self):
        print("Source parameters for AshDisperse")
        print("  Mass eruption rate MER = ", self.MER, " kg/s")
        print("  Eruption duration = ", self.duration, " s")
        print("  Plume height H = ", self.PlumeHeight, " m")
        print("  Gaussian source radius = ", self.radius, " m")
        print("********************")

# pylint: disable=E1101
SourceParameters_type = SourceParameters.class_type.instance_type

def _source_dict(p):
    return {
        "name": p.name,
        "latitude": p.latitude,
        "longitude": p.longitude,
        "utmcode": p.utmcode,
        "radius": p.radius,
        "PlumeHeight": p.PlumeHeight,
        "MER": p.MER,
        "duration": p.duration,
    }