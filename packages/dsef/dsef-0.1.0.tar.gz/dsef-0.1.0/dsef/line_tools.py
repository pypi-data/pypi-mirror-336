"""
line_tools.py

Line calculations util functions 
"""

import numpy as np

from typing import List, Tuple

__all__ = ('normalized',
           'normalvector',
           'calc_heading_vector',
           'calc_heading',
           'RunningExponentialVectorAverage')

def normalized(v: List[float]) -> np.ndarray:
    """
    Normalize a 2D vector.

    Parameters:
        v (List[float]): A 2D vector represented as a list of two float values [x, y].

    Returns:
        np.ndarray: The normalized vector with a magnitude of 1.
    """
    norm = (v[0]**2 + v[1]**2)**0.5
    return np.array([v[0]/norm, v[1]/norm])

def normalvector(v: List[float], CC: bool = True, NORMALIZE: bool = True) -> np.ndarray:
    """
    Compute the normal vector of a 2D vector.

    Parameters:
        v (List[float]): A 2D vector represented as a list of two float values [x, y].
        CC (bool): If True, compute the counter-clockwise normal vector. 
                   If False, compute the clockwise normal vector. Default is True.
        NORMALIZE (bool): If True, normalize the resulting vector. Default is True.

    Returns:
        np.ndarray: The computed normal vector.
    """
    vx = [v[1], -v[0]] if CC else [-v[1], v[0]]
    if NORMALIZE:        
        return normalized(vx)
    else:
        return vx

def calc_heading_vector(heading_deg: float, dtype=np.float64) -> np.ndarray:
    """
    Calculate a 2D heading vector from a compass heading in degrees.

    Parameters:
        heading_deg (float): Compass heading in degrees, where 0 = North, 90 = East, etc.
        dtype (data-type): The desired data type of the output array.

    Returns:
        np.ndarray: The 2D heading vector [x, y].
    """
    t = np.radians(heading_deg)
    return np.array([np.sin(t), np.cos(t)], dtype)

def calc_heading(heading_vec: Tuple[float]) -> float:
    """
    Calculate the compass heading in degrees from a 2D heading vector.

    Parameters:
        heading_vec (Tuple[float]): A 2D heading vector (x, y).

    Returns:
        float: The compass heading in degrees, ranging from 0° to 360°.
    """
    if len(heading_vec) != 2:
        raise TypeError("heading_vec is not a Tuple of len 2")
    ve, vn = heading_vec    
    return (np.degrees(np.arctan2(ve, vn)) + 360) % 360.0

class RunningExponentialVectorAverage:
    """
    Calculates a running exponential vector average (REVA).

    Attributes:
        mu (np.ndarray): The current mean vector.
        var (np.ndarray): The current variance vector.
        rho (float): The smoothing factor (0 < rho <= 1).
    """
    def __init__(self, mu: np.ndarray = np.array([0, 0]), var: np.ndarray = np.array([0, 0]), rho: float = 0.1):
        self.mu, self.var, self.rho = mu, var, rho

    def push(self, v: float) -> None:
        """
        Add a new vector to update the mean and variance.

        Parameters:
            v (np.ndarray): A 2D vector to include in the running average.
        """
        self.mu = self.rho*v + (1 - self.rho)*self.mu
        d        = abs(v - self.mu)
        self.var = (d**2)*self.rho + (1 - self.rho)*self.var

    def __repr__(self) -> str:
        return("REWA: mu = [%0.1f, %0.1f], var = [%0.1f, %0.1f], rho = %0.1f" % (self.mu[0], self.mu[1], self.var[0], self.var[1], self.rho))
