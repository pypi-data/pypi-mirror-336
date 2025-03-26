import numpy as np
from typing import List, Sequence
from scipy.spatial import ConvexHull
from colav_unsafe_set.objects import DynamicObstacleWithMetrics

def gen_uIoI_convhull(uIoI: List[DynamicObstacleWithMetrics]) -> List[int]:
    """
    Generate the convex hull indices of the union of safety regions from a list of dynamic obstacles.
    
    Each dynamic obstacle's safety region is approximated as a circle (using _generate_circle_vertices). 
    The union of all vertices from these circles is then used to compute the convex hull, and the function 
    returns the indices of the hull's vertices.
    
    Args:
        uIoI (List[DynamicObstacleWithMetrics]): A list of dynamic obstacles with associated metrics.
    
    Returns:
        List[int]: A list of indices representing the convex hull vertices. If no vertices are generated, returns an empty list.
    """
    unsafe_set_vertices: List[List[float]] = [
        vertex
        for dynamic_obstacle in uIoI
        for vertex in _generate_circle_vertices(
            centroid=[
                dynamic_obstacle.dynamic_obstacle.position[0],
                dynamic_obstacle.dynamic_obstacle.position[1]
            ],
            radius=dynamic_obstacle.dynamic_obstacle.safety_radius
        )
    ]
    
    if not unsafe_set_vertices:
        return []
    
    unsafe_set_vertices = np.array(unsafe_set_vertices, dtype=np.float64)  # Ensure float type
    hull_indices = ConvexHull(unsafe_set_vertices).vertices
    hull_points = unsafe_set_vertices[hull_indices].tolist()  # Convert back to a list of lists

    return hull_points  # Returns actual coordinates, not indices

def _generate_circle_vertices(centroid: Sequence[float], radius: float, num_points: int = 10) -> List[List[float]]:
    """
    Generate vertices approximating a circle in the XY plane.
    
    The circle is defined by its centroid and radius, and is approximated by 'num_points' evenly spaced vertices.
    
    Args:
        centroid (Sequence[float]): The (x, y) coordinates of the circle's center.
        radius (float): The radius of the circle.
        num_points (int): The number of vertices to generate (default is 10).
        
    Returns:
        List[List[float]]: A list of [x, y] vertices representing the circle.
    """
    x_c, y_c = centroid
    theta = np.linspace(0, 2 * np.pi, num_points, endpoint=False)
    x = x_c + radius * np.cos(theta)
    y = y_c + radius * np.sin(theta)
    circle_vertices = np.column_stack((x, y))
    return circle_vertices.tolist()
