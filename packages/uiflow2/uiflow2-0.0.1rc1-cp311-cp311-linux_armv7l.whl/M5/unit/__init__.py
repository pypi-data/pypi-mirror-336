# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

_attrs = {
    "ENVPROUnit": "envpro",
    "TMOSUnit": "tmos",
    "GPSV11Unit": "gps_v11",
    "IMUUnit": "imu",
    "IMUProUnit": "imu_pro",
    "PAHUBUnit": "pahub",
}

import sys
def __getattr__(attr):
    mod = _attrs.get(attr, None)
    if mod is None:
        raise AttributeError(attr)
    if sys.platform == "linux": # for linux
        value = getattr(__import__(mod, globals(), None, [attr], 1), attr)  # python
    else:
        value = getattr(__import__(mod, None, None, True, 1), attr)
    globals()[attr] = value
    return value
