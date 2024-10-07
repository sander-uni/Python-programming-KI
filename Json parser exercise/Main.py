#  Functions below taken from one of my other projects in lua
#  Translated from lua to python with transpiler tool
#  Used for purposes of quality controlling json parser

from pathlib import Path
import os
import re
import time
import json_parser as json
import tests

tests.test_json_performance()
