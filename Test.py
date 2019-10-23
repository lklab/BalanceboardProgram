#!/usr/bin/env python3

from BalanceModules.Outfit import *
from BalanceModules.ServerInterface import *

outfit = Outfit()
requestId(outfit)
updateStatus(outfit)
fetchCommand(outfit)
print("command: " + str(outfit.command))
