#!/usr/bin/env python3

from BalanceModules.Outfit import *
from BalanceModules.ServerInterface import *

outfit = Outfit()
requestId(outfit)
updateStatus(outfit)
fetchCommand(outfit)
result = submitResult(outfit, "this is data to save in the file")
print("result is: " + str(result))
