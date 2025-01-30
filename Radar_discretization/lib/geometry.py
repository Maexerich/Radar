import numpy as np

def from_gt_to_doppler(gt, radar_params, angle_unit="degrees"):
    """
    This function projects the ground truth velocity (gt, given in np array with columns [vx, vy, vz]) 
    onto the sampled radar point (radar_params, a numpy array with coumns [range, elevation, azimuth]).
    In addition, the sign of the projection is flipped.
    (Doppler is the relative velocity of objects onto me, not my velocity.)

    Params:
    - gt: Ground-truth velocity as numpy array in cartesian coordinates, where columns are [vx, vy, vz].
    - radar_params: Radar point as numpy array in spherical coordinates, where columns are [range, elevation, azimuth].
    - angle_unit: 'radians' or 'degrees'. The unit of the angles in the input array. 'degrees' is default

    Returns:
    - numpy array with columns [range, azimuth, elevation, doppler] with angle_unit as specified.
    """
    radar_points_cartesian = spherical_to_cartesian(radar_params, angle_unit=angle_unit, convention='TI')

    # Project ground-truth velocity vectors onto vectors pointing to radar points
    projected_velocities = project_vectors(radar_points_cartesian, gt)
    doppler_velocities = -projected_velocities[:, 0]

    return np.hstack((radar_params, doppler_velocities.reshape(-1, 1)))

def spherical_to_cartesian(radar_coords, angle_unit='degrees', convention='TI'):
    """
    Convert spherical coordinates to cartesian coordinates.

    Params:
    - radar_coords: Numpy array with shape (N, 3) where each row is [range, elevation, azimuth].
    - angle_unit: 'radians' or 'degrees'. The unit of the angles in the input array. 'degrees' is default

    Returns:
    - Numpy array with shape (N, 3) where each row is [x, y, z].
    """
    if convention != 'TI':
        raise ValueError("Currently only TI-convetion is supported. It differs from common spherical coordinates.")
    else:
        print(f"ATTENTION: Using {convention}-convention for [range, elevation, azimuth] -> [x, y, z].")

    coordinates = radar_coords.copy() # Ensures no in-place operations effect the passed argument
    # Ensure angles are in radians
    if angle_unit == 'degrees':
        for i in range(2):
            coordinates[:, i+1] = np.deg2rad(coordinates[:, i+1])
    elif angle_unit != 'radians':
        raise ValueError("Invalid angle unit. Expected 'radians' or 'degrees'.")

    # Assert that no angle is greater than 2 in magnitude (not a strictly correct assertion, but should be triggered
    # if angles are in wrong units)
    if np.all(np.abs(coordinates[:, 1:3]) >= 2):
        print("WARNING: Azimuth and elevation angles are in the range [-2, 2].")
    assert np.all(np.abs(coordinates[:, 1:3]) <= 2), f"Azimuth and elevation angles must be in the range [-2, 2]. {coordinates}"
    
    cartesian_coords = np.zeros_like(coordinates)
    # X Coordinate = range * cos(elevation) * sin(azimuth)
    cartesian_coords[:, 0] = coordinates[:, 0] * np.cos(coordinates[:, 1]) * np.sin(coordinates[:, 2])

    # Y Coordinate = range * cos(elevation) * cos(azimuth)
    cartesian_coords[:, 1] = coordinates[:, 0] * np.cos(coordinates[:, 1]) * np.cos(coordinates[:, 2])

    # Z Coordinate = range * sin(elevation)
    cartesian_coords[:, 2] = coordinates[:, 0] * np.sin(coordinates[:, 1])

    return cartesian_coords

def cartesian_to_spherical(radar_coords: np.array, angle_unit='degrees', convention='TI'):
    """
    Converts cartesian coordinates to spherical coordinates according to the specified convention.
    
    TI-Convention:
    - Range: Euclidean norm of the vector.
    - Elevation: arctan2(z, sqrt(x^2 + y^2))
    - Azimuth: arctan2(x, y)
    
    Params:
    - radar_coords: Numpy array with shape (N, 3) where each row is [x, y, z].
    - angle_unit: 'radians' or 'degrees'. The unit of the angles in the output array. 'degrees' is default.
    - convention: String specifying the convention.
    
    Returns:
    - np.array with shape (N, 3) according to convention."""
    coordinates_spherical = np.zeros_like(radar_coords)
    # Calculate range
    coordinates_spherical[:, 0] = np.linalg.norm(radar_coords, axis=1)
    # Need to fix nan's appearing here!!!

    # Calculate elevation
    # elevation = arctan2(z, sqrt(x^2 + y^2))
    coordinates_spherical[:, 1] = np.arctan2(radar_coords[:, 2], np.linalg.norm(radar_coords[:, :2], axis=1))
    coordinates_spherical[:, 1] = np.round(coordinates_spherical[:, 1], 3)

    # Calculate azimuth
    # azimuth = arctan2(x, y)
    coordinates_spherical[:, 2] = np.arctan2(radar_coords[:, 0], radar_coords[:, 1])
    coordinates_spherical[:, 2] = np.round(coordinates_spherical[:, 2], 3)

    if angle_unit == 'degrees':
        for i in range(1, 3):
            coordinates_spherical[:, i] = np.rad2deg(coordinates_spherical[:, i])
    elif angle_unit != 'radians':
        raise ValueError("Invalid angle unit. Expected 'radians' or 'degrees'.")
    
    # Assert no nan values in the output
    if np.any(np.isnan(coordinates_spherical)):
        print("WARNING: Conversion to spherical coordinates resulted in NaN values.")
    assert np.all(~np.isnan(coordinates_spherical)), "Conversion to spherical coordinates resulted in NaN values."
    
    return coordinates_spherical


def normalize_vectors(vectors):
    """
    Normalize each vector in the array to have unit length.

    Params:
    - vectors: Numpy array with shape (N, 3) where each row is a vector [x, y, z].

    Returns:
    - Numpy array with shape (N, 3) where each row is a normalized vector.
    """
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    assert np.all(norms != 0), "Cannot normalize a vector with zero length."
    return vectors / norms

def project_vectors(direction, vector):
    """
    Project each row of 'vector' onto the corresponding row of 'direction'.
    Formula for projection of vector 'a' onto vector 'b' is dot(a, b/||b||).

    Params:
    - direction: Numpy array with shape (N, 3) where each row is a direction vector [x, y, z].
    - vector: Numpy array with shape (N, 3) where each row is a vector to be projected [x, y, z].

    Returns:
    - Numpy array with shape (N, 4) where the first three columns are the projected vectors and the last column is the norm of the projected vector.
    """
    # Normalize the direction vectors
    direction_normalized = normalize_vectors(direction)

    # Calculate the dot product of each vector with the corresponding direction vector
    # (Dot product of two matricies includes element-wise multiplication and then summing across axis 1)
    dot_products = np.sum(vector * direction_normalized, axis=1, keepdims=True)

    # Assert that every dot product is not nan
    assert np.all(~np.isnan(dot_products)), "Dot product calculation resulted in NaN values"

    # Calculate the norms of the projected vectors
    norms = np.linalg.norm(dot_products, axis=1, keepdims=True)

    # Combine the projections and their norms into a single array
    result = np.hstack((dot_products, norms))

    return result