import numpy as np


def draw_line(points, radius=0.02, edge_org=None, base_point=0):
    """
    Draws a line from point to points
    :param base_point:
    :param points: two points
    :param radius: Radius for the line to be drawn
    :param edge_org: Vector for the edge orientation
    :return: points and tris for drawing
    """
    if edge_org is None:
        edge_org = [0, 0, -1]
    # Initiate the draw attributes
    draw_points, draw_tris = [], []
    r = None
    # Go through the points
    for i in range(len(points)):
        # If we are at the end of the points list, use the previous point for calibration
        p0 = np.array(points[i])
        if i < len(points) - 1:
            p1 = np.array(points[i + 1])
            r = p1 - p0
        # Find the vector and its normal between the two points
        rn = r / np.linalg.norm(r)
        # In the case that the vector between the points is in the z direction only, move it
        if rn[0] == 0 and rn[1] == 0:
            r = r + np.array([0.001, 0.001, 0])
            rn = r / np.linalg.norm(r)
        # Take the cross product with the +z direction and normalize it
        v0_0x = np.cross(rn, np.array(p0 - edge_org))
        v0_0n = v0_0x / np.linalg.norm(v0_0x)
        # Calculate the location of the first point
        p0_0 = v0_0n * radius + p0
        # Take the cross product of the edge vector and the vector to the first point and normalize it
        v0_1x = np.cross(rn, v0_0n)
        v0_1nx = v0_1x / np.linalg.norm(v0_1x)
        # Find the vectors for the other two points (30/60/90 triangle)
        v0_1 = - 0.5 * radius * v0_0n + 0.5 * np.sqrt(3) * radius * v0_1nx
        v0_2 = - 0.5 * radius * v0_0n - 0.5 * np.sqrt(3) * radius * v0_1nx
        # Get the points and add them to the list of draw points
        p0_1, p0_2 = v0_1 + p0, v0_2 + p0
        draw_points += [p0_0, p0_1, p0_2]
    # Go through the points
    for i in range(base_point, base_point + len(points) - 1):
        # List the points
        p0_0, p0_1, p0_2, p1_0, p1_1, p1_2 = range(3 * i, 3 * (i + 2))
        # Create the triangles
        draw_tris += [[p0_0, p0_1, p1_0], [p1_0, p1_1, p0_1],
                           [p0_1, p0_2, p1_1], [p1_1, p1_2, p0_2],
                           [p0_2, p0_0, p1_2], [p1_2, p1_0, p0_0]]
    # Return the points and triangles
    return draw_points, draw_tris
