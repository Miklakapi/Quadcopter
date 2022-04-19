#!/usr/bin/env python

"""Adds a path for importing between directories to work"""

import sys
from pathlib import Path

here = Path(__file__).resolve()

sys.path.insert(1, str(here.parent.parent.absolute()))
sys.path.insert(1, str(here.parent.parent.absolute()) + '/src')
