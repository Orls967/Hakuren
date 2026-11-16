#!/usr/bin/env python3
"""Wrapper: runs hakuren_audit check(s) 'schemas'. See tools/README.md."""
import sys
from hakuren_audit import main
sys.exit(main(default="schemas"))
