import os
import sys
import numpy as np
import pytest

# Ensure the directory that contains the `foamify` package is on sys.path
CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", "..", ".."))
if PROJECT_ROOT not in sys.path:
	sys.path.insert(0, PROJECT_ROOT)

from foamify.src.draw.draw import draw_line


def test_draw_line_point_and_triangle_counts():
	points = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [2.0, 1.0, 0.0]]
	radius = 0.1
	draw_points, draw_tris = draw_line(points, radius=radius)

	# Implementation creates 3 vertices for each input point
	expected_points = 3 * len(points)
	expected_tris = 6 * (len(points) - 1)
	assert len(draw_points) == expected_points
	assert len(draw_tris) == expected_tris

	# Triangles index into the flattened vertex list; verify index ranges
	max_index = 3 * len(points) - 1
	for tri in draw_tris:
		for idx in tri:
			assert 0 <= idx <= max_index


def test_draw_line_vertices_are_radius_from_centers():
	points = [[0.0, 0.0, 0.0], [1.0, 1.0, 0.0]]
	radius = 0.2
	draw_points, _ = draw_line(points, radius=radius)
	# First 3 points correspond to first center
	center0 = np.array(points[0])
	p0_0, p0_1, p0_2 = [np.array(p) for p in draw_points[0:3]]
	for p in (p0_0, p0_1, p0_2):
		assert np.isclose(np.linalg.norm(p - center0), radius)


def test_draw_line_vertical_segment_no_zero_division():
	# Segment aligned with z; function perturbs to avoid degenerate cross product
	points = [[0.0, 0.0, 0.0], [0.0, 0.0, 1.0]]
	draw_points, draw_tris = draw_line(points, radius=0.05)
	assert len(draw_points) == 6  # 3 per input point
	assert len(draw_tris) == 6 * (len(points) - 1)  # one segment -> 6 tris


def test_draw_line_base_point_offset_affects_indices():
	points = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0]]
	base_point = 5
	_, draw_tris = draw_line(points, radius=0.05, base_point=base_point)
	# All indices are offset by base_point*3 in the triangle list generation
	min_idx = min(min(tri) for tri in draw_tris)
	assert min_idx == 3 * base_point


def test_draw_line_with_custom_edge_org():
	points = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0]]
	edge_org = [0.0, 0.0, -2.0]
	radius = 0.15
	draw_points, _ = draw_line(points, radius=radius, edge_org=edge_org)
	# Still should lie on a circle of given radius around first point
	center0 = np.array(points[0])
	p0_0, p0_1, p0_2 = [np.array(p) for p in draw_points[0:3]]
	for p in (p0_0, p0_1, p0_2):
		assert np.isclose(np.linalg.norm(p - center0), radius)
