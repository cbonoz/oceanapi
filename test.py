import os
import time

from squid_py import (
    Ocean,
    ConfigProvider,
    Config,
    Metadata,
    Account
)

# PUBLISHER
# Let's start by registering an asset in the Ocean network
metadata = Metadata.get_example()

print('metadata', metadata)