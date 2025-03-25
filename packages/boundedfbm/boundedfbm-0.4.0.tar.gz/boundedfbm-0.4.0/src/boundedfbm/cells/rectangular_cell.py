from dataclasses import dataclass
from typing import Tuple

import numpy as np
import pyvista as pv

from .base_cell import BASE_TOLERANCE, BaseCell


@dataclass
class RectangularCell(BaseCell):
    """
    Represents a rectangular cell in 3D space.

    Attributes:
        bounds (np.ndarray):
            [[xmin,xmax],[ymin,ymax],[zmin,zmax]]
    """

    bounds: np.ndarray

    def contains_point_fallback(
        self, x: float, y: float, z: float, tolerance: float = BASE_TOLERANCE
    ) -> bool:
        """
        Determines if a point (x, y, z) is inside the rectangular cell.

        Args:
            x (float): X-coordinate of the point
            y (float): Y-coordinate of the point
            z (float): Z-coordinate of the point

        Returns:
            bool: True if the point is inside the ovoid, False otherwise
        """
        # Convert single values to a point vector
        point = np.array([x, y, z])
        for i in range(len(point)):
            if (point[i] < self.bounds[i]) or (point[i] > self.bounds[i + 1]):
                return False
        return True

    def reflecting_point(
        self,
        x1: float,
        y1: float,
        z1: float,
        x2: float,
        y2: float,
        z2: float,
        max_iterations: int = 5,
    ) -> Tuple[float, float, float]:
        """
        Calculate the final position of a ray after reflections in a 3D rectangular box.

        Args:
            x1, y1, z1: Coordinates of the starting point
            x2, y2, z2: Coordinates of the initial direction point
            max_iterations: Maximum number of reflections to calculate

        Returns:
            Tuple[float, float, float]: The final position after reflections
        """
        if self.contains_point_fallback(x2, y2, z2) and self.contains_point_fallback(
            x1, y1, z1
        ):
            return (x2, y2, z2)
        # Current position
        candidate_pos = [x2, y2, z2]

        # Extract bounds
        mins = [self.bounds[0], self.bounds[2], self.bounds[4]]  # x_min, y_min, z_min
        maxs = [self.bounds[1], self.bounds[3], self.bounds[5]]  # x_max, y_max, z_max

        for dim in range(3):
            while (candidate_pos[dim] > maxs[dim]) or (candidate_pos[dim] < mins[dim]):
                if candidate_pos[dim] > maxs[dim]:
                    candidate_pos[dim] = 2 * maxs[dim] - candidate_pos[dim]
                elif candidate_pos[dim] < mins[dim]:
                    candidate_pos[dim] = 2 * mins[dim] - candidate_pos[dim]
        return (candidate_pos[0], candidate_pos[1], candidate_pos[2])


def make_RectangularCell(bounds: np.ndarray) -> RectangularCell:
    """
    Parameters:
    -----------
    bounds (np.ndarray):
        [[xmin,xmax],[ymin,ymax],[zmin,zmax]]

    Returns:
    --------
    RectangularCell object
    """

    pv_bounds = np.asarray(bounds).flatten()
    rec = pv.Box(bounds=pv_bounds)
    return RectangularCell(mesh=rec, bounds=bounds)


@dataclass
class RectangularCellParams:
    bounds: np.ndarray

    @classmethod
    def validate_bounds(cls, value):
        if not isinstance(value, (list, tuple, np.ndarray)):
            raise ValueError("bounds must be an array-like object")

        # Convert to numpy array if needed
        if not isinstance(value, np.ndarray):
            value = np.array(value)

        # Check shape
        if value.shape != (3, 2):
            raise ValueError("bounds must be a 3x2 array (min and max points)")

        # Check min < max
        for i in range(3):
            if value[i, 0] >= value[i, 1]:
                raise ValueError(
                    f"Min bound must be less than max bound for dimension {i}"
                )
