import os
import sys
import pytest

# Ensure the directory that contains the `foamify` package is on sys.path
CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", "..", ".."))
if PROJECT_ROOT not in sys.path:
	sys.path.insert(0, PROJECT_ROOT)

from foamify.src.make_foam.atomic import find_closest_key, standardize_radii_to_atomic, element_radii


def test_find_closest_key_exact_match():
	# Simple sorted mapping
	mapping = {1.0: "A", 2.0: "B", 3.0: "C"}
	key, value = find_closest_key(2.0, mapping)
	assert key == 2.0 and value == "B"


def test_find_closest_key_selects_nearest():
	mapping = {1.0: "A", 2.0: "B", 3.0: "C"}
	# 1.6 is closer to 2.0
	key, value = find_closest_key(1.6, mapping)
	assert key == 2.0 and value == "B"
	# 2.6 is closer to 3.0
	key, value = find_closest_key(2.6, mapping)
	assert key == 3.0 and value == "C"


def test_standardize_radii_to_atomic_basic_rounding():
	# Choose values that are unambiguous nearest to existing element radii
	# 1.31 -> 1.30 (H); 1.495 -> 1.50 (O); 0.77 -> 0.76 (LI)
	input_radii = [1.31, 1.495, 0.77]
	new_radii, new_atoms = standardize_radii_to_atomic(input_radii)
	assert new_radii[0] == pytest.approx(1.30, rel=0, abs=1e-9)
	assert new_radii[1] == pytest.approx(1.50, rel=0, abs=1e-9)
	assert new_radii[2] == pytest.approx(0.76, rel=0, abs=1e-9)
	# Returned atoms correspond to keys having those radii
	radius_to_atom = {v: k for k, v in element_radii.items()}
	assert new_atoms[0] == radius_to_atom[new_radii[0]]
	assert new_atoms[1] == radius_to_atom[new_radii[1]]
	assert new_atoms[2] == radius_to_atom[new_radii[2]]
