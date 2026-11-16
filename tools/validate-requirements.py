#!/usr/bin/env python3
"""Wrapper: runs hakuren_audit check(s) 'ids,requirements'. See tools/README.md."""
import sys
from hakuren_audit import main
sys.exit(main(default="ids,requirements"))
