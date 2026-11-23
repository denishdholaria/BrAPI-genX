#!/usr/bin/env python3
import runpy, sys
from pathlib import Path
sys.argv[0] = str(Path(__file__).with_name("check_semantic_neighbor_governance.py"))
runpy.run_path(str(Path(__file__).with_name("check_semantic_neighbor_governance.py")), run_name="__main__")
