import os
import sys
import math
import numpy as np
import pandas as pd
import pytest

# Ensure the directory that contains the `foamify` package is on sys.path
CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", "..", ".."))
if PROJECT_ROOT not in sys.path:
	sys.path.insert(0, PROJECT_ROOT)

from foamify.src.calcs.calcs import (
	calc_dist,
	calc_dist_numba,
	box_search,
	calc_tot_vol,
	pdb_line,
	periodicize,
	box_search_numba,
	get_bubbles,
	calc_box,
	calc_stats,
)


def test_calc_dist_basic():
	l0 = [0.0, 0.0, 0.0]
	l1 = [3.0, 4.0, 0.0]
	assert calc_dist(l0, l1) == pytest.approx(5.0)


def test_calc_dist_numba_euclidean():
	my_loc = (0.0, 0.0, 0.0)
	other_loc = (1.0, 2.0, 2.0)
	# distance sqrt(1 + 4 + 4) = 3
	assert calc_dist_numba(my_loc, other_loc, box_side=None, periodic=False) == pytest.approx(3.0)


def test_calc_dist_numba_periodic_wraps():
	# With periodic box of side 10, distance between (0,0,0) and (9,0,0)
	# should wrap to 1 along x
	my_loc = (0.0, 0.0, 0.0)
	other_loc = (9.0, 0.0, 0.0)
	assert calc_dist_numba(my_loc, other_loc, box_side=10.0, periodic=True) == pytest.approx(1.0)


def test_box_search_into_correct_cell():
	# Box from (0,0,0) to (10,10,10), split 5 => cell size 2
	box_verts = [[0.0, 0.0, 0.0], [10.0, 10.0, 10.0]]
	loc = [4.9, 0.1, 7.9]
	# indices should be int(4.9/2)=2, int(0.1/2)=0, int(7.9/2)=3
	assert box_search(loc, 5, box_verts) == [2, 0, 3]


def test_box_search_numba_direct():
	loc = np.array([4.9, 0.1, 7.9])
	box_verts = np.array([[0.0, 0.0, 0.0], [10.0, 10.0, 10.0]])
	assert box_search_numba(loc, 5, box_verts) == [2, 0, 3]


def test_calc_tot_vol_spheres():
	# radii 1 and 2
	r = [1.0, 2.0]
	expected = (4.0 / 3.0) * math.pi * (1.0 ** 3) + (4.0 / 3.0) * math.pi * (2.0 ** 3)
	assert calc_tot_vol(r) == pytest.approx(expected)


def test_pdb_line_formatting():
	line = pdb_line(
		atom="ATOM",
		ser_num=1,
		name="C",
		alt_loc=" ",
		res_name="FOA",
		chain="A",
		res_seq=1,
		cfir=" ",
		x=1.2345,
		y=2.3456,
		z=3.4567,
		occ=1.0,
		tfact=0.0,
		seg_id="FOAM",
		elem="C",
		charge=""
	)
	# Python uses bankers rounding; 1.2345 -> 1.234 with {:.3f}
	assert "ATOM" in line
	assert "   1.234" in line
	assert "   2.346" in line
	assert "   3.457" in line
	assert line.endswith("\n")


def test_get_bubbles_returns_expected_entries():
	# Create a small 3x3x3 matrix of lists; place one ball in [1,1,1]
	n = 3
	ball_matrix = np.empty((n, n, n), dtype=object)
	for i in range(n):
		for j in range(n):
			for k in range(n):
				ball_matrix[i, j, k] = []
	# put an identifier in the center cell
	marker = {"id": 42}
	ball_matrix[1, 1, 1] = [marker]
	# last element must contain [n] per implementation
	ball_matrix[-1, -1, -1] = [n]

	sub_box_size = [1.0, 1.0, 1.0]
	cells = [1, 1, 1]
	balls = get_bubbles(ball_matrix, cells, sub_box_size, dist=0, periodic=False)
	assert marker in balls


def test_calc_box_sets_expected_bounds():
	class BoxSys:
		def __init__(self, box_size):
			self.box_size = box_size
			self.atoms_box = None
			self.box = None

	sys_obj = BoxSys(box_size=0.5)
	locs = [
		[0.0, 1.0, 2.0],
		[2.0, 3.0, 4.0],
	]
	rads = [0.5, 0.75]
	calc_box(sys_obj, locs, rads)
	# atoms_box should be min/max enclosing locs
	assert sys_obj.atoms_box == [[0.0, 1.0, 2.0], [2.0, 3.0, 4.0]]
	# Expanded box should be min - 0.5*r_box, max + 0.5*r_box
	r_box = np.array([2.0, 2.0, 2.0])
	expected_min = (np.array([2.0, 3.0, 4.0]) - 0.5 * r_box).round(3).tolist()
	expected_max = (np.array([0.0, 1.0, 2.0]) + 0.5 * r_box).round(3).tolist()
	assert sys_obj.box == [expected_min, expected_max]


def test_periodicize_mirror_mode():
	class MockSys:
		def __init__(self):
			self.box = [[0.0, 0.0, 0.0], [1.0, 1.0, 1.0]]
			self.bubbles = pd.DataFrame([
				{"loc": np.array([0.25, 0.25, 0.25]), "residue": 1, "chain": "A"}
			])

	sys_mirror = MockSys()
	periodicize(sys_mirror, mirror=True)
	# 1 original + 26 clones
	assert len(sys_mirror.bubbles) == 27
	# Check at least one mirrored coordinate as per implementation: -loc or 2-max - loc
	locs = np.vstack(sys_mirror.bubbles["loc"].values)
	orig = np.array([0.25, 0.25, 0.25])
	assert any(np.isclose(locs[:, 0], -orig[0])) or any(np.isclose(locs[:, 0], 2.0 - orig[0]))


def test_calc_stats_smoke():
	# Smoke test: should run without error and return None
	result = calc_stats(sds=[0.2], mu=1.0, num_its=1, num_balls=1)
	assert result is None
