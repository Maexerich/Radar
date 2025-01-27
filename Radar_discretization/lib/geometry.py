import numpy as np

def from_gt_to_doppler(gt, radar_params):
    """
    This function projects the ground truth velocity (gt, given in np array with columns [vx, vy, vz]) 
    onto the sampled radar point (radar_params, a numpy array with coumns [azimuth, elevation, range]).
    In addition, the sign of the projection is flipped.
    (Doppler is the relative velocity of objects onto me, not my velocity.)

    Params:
    - gt: Ground-truth velocity as numpy array in cartesian coordinates, where columns are [vx, vy, vz].
    - radar_params: Radar point as numpy array in spherical coordinates, where columns are [azimuth, elevation, range].

    Returns:
    - numpy array with columns [azimuth, elevation, range, doppler]
    """
    radar_points_cartesian = spherical_to_cartesian(radar_params)

    # Project ground-truth velocity vectors onto vectors pointing to radar points
    projected_velocities = project_vectors(radar_points_cartesian, gt)
    doppler_velocities = -projected_velocities[:, 0]

    return np.hstack((radar_params, doppler_velocities.reshape(-1, 1)))

def spherical_to_cartesian(spherical_coords):
    """
    Convert spherical coordinates to cartesian coordinates.

    Params:
    - spherical_coords: Numpy array with shape (N, 3) where each row is [azimuth, elevation, range].

    Returns:
    - Numpy array with shape (N, 3) where each row is [x, y, z].
    """
    cartesian_coords = np.zeros_like(spherical_coords)
    # X Coordinate = range * cos(azimuth) * sin(elevation)
    cartesian_coords[:, 0] = spherical_coords[:, 2] * np.cos(spherical_coords[:, 0]) * np.sin(spherical_coords[:, 1])

    # Y Coordinate = range * sin(azimuth) * sin(elevation)
    cartesian_coords[:, 1] = spherical_coords[:, 2] * np.sin(spherical_coords[:, 0]) * np.sin(spherical_coords[:, 1])

    # Z Coordinate = range * cos(elevation)
    cartesian_coords[:, 2] = spherical_coords[:, 2] * np.cos(spherical_coords[:, 1])

    return cartesian_coords

def normalize_vectors(vectors):
    """
    Normalize each vector in the array to have unit length.

    Params:
    - vectors: Numpy array with shape (N, 3) where each row is a vector [x, y, z].

    Returns:
    - Numpy array with shape (N, 3) where each row is a normalized vector.
    """
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
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

    # Calculate the norms of the projected vectors
    norms = np.linalg.norm(dot_products, axis=1, keepdims=True)

    # Combine the projections and their norms into a single array
    result = np.hstack((dot_products, norms))

    return result