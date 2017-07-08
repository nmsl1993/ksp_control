import math
import numpy as np
import time
import krpc
import IPython

conn = krpc.connect(name='Interactive IPython KRPC')
vessel = conn.space_center.active_vessel
IPython.embed()
