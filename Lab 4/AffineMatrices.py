import numpy as np


def get_rotation_mat(theta, l, m, n):
    cos_theta = np.cos(theta)
    sin_theta = np.sin(theta)
    return np.array([
        [l ** 2 + cos_theta * (1 - l ** 2), l * (1 - cos_theta) * m + n * sin_theta,
         l * (1 - cos_theta) * n - m * sin_theta, 0],
        [l * (1 - cos_theta) * m - n * sin_theta, m ** 2 + cos_theta * (1 - m ** 2),
         m * (1 - cos_theta) * n + l * sin_theta, 0],
        [l * (1 - cos_theta) * n + m * sin_theta, m * (1 - cos_theta) * n - l * sin_theta,
         n ** 2 + cos_theta * (1 - n ** 2), 0],
        [0, 0, 0, 1]
    ])

def get_isometry_mat(alpha, beta):
    rotate_mat_x = get_x_rotation_mat(alpha)
    rotate_mat_y = get_y_rotation_mat(beta)
    return np.dot(rotate_mat_x, rotate_mat_y)

def get_x_rotation_mat(theta):
    cos_theta = np.cos(theta)
    sin_theta = np.sin(theta)
    rotation_matrix = np.array([
        [1, 0, 0, 0],
        [0, cos_theta, sin_theta, 0],
        [0, -sin_theta, cos_theta, 0],
        [0, 0, 0, 1]
    ])
    return rotation_matrix


def get_y_rotation_mat(theta):
    cos_theta = np.cos(theta)
    sin_theta = np.sin(theta)
    rotation_matrix = np.array([
        [cos_theta, 0, -sin_theta, 0],
        [0, 1, 0, 0],
        [sin_theta, 0, cos_theta, 0],
        [0, 0, 0, 1]
    ])
    return rotation_matrix


def get_z_rotation_mat(theta):
    cos_theta = np.cos(theta)
    sin_theta = np.sin(theta)
    rotation_matrix = np.array([
        [cos_theta, sin_theta, 0, 0],
        [-sin_theta, cos_theta, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])
    return rotation_matrix


def get_translation_mat(dx, dy, dz):
    return np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [dx, dy, dz, 1]
    ])


def get_scale_mat(mx, my, mz):
    return np.array([
        [mx, 0, 0, 0],
        [0, my, 0, 0],
        [0, 0, mz, 0],
        [0, 0, 0, 1]
    ])


def get_yoz_mat():
    return np.array([
        [-1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])


def get_zox_mat():
    return np.array([
        [1, 0, 0, 0],
        [0, -1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])


def get_xoy_mat():
    return np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, -1, 0],
        [0, 0, 0, 1]
    ])

