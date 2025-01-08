import numpy as np
import time
import math

def compute_displacement(accel, time_delay=0.1, scale_factor=100):
    """
    Compute the displacement from acceleration in g's to pixels.
    
    Parameters:
    accel_x_g (np.array): Acceleration in the x direction (in g's).
    accel_y_g (np.array): Acceleration in the y direction (in g's).
    time_delay (float): Time delay between samples (in seconds).
    scale_factor (float): Number of pixels per meter for conversion. Default is 100 pixels/meter.
    
    Returns:
    displacement_x_pixels (np.array): Displacement in pixels along x-axis.
    displacement_y_pixels (np.array): Displacement in pixels along y-axis.
    """
    
    # Convert g's to m/s²
    g = 9.81
    accel = accel * g
    
    # Integrating acceleration to get velocity (numerical integration)
    velocity = np.cumsum(accel) * time_delay  # velocity = sum(acceleration * dt)

    # Integrating velocity to get displacement (numerical integration)
    displacement = np.cumsum(velocity) * time_delay  # displacement = sum(velocity * dt)

    # Convert displacement from meters to pixels
    displacement_pixels = displacement * scale_factor

    return displacement_pixels

def getGrav(pitch, roll, yaw)->list:
    return (math.cos(pitch), math.cos(roll), math.cos(yaw))
def getAngles()->list:pass

# def compute_displacement(accel_x_g, accel_y_g, time_delay, scale_factor=100):
#     """
#     Compute the displacement from acceleration in g's to pixels.
    
#     Parameters:
#     accel_x_g (np.array): Acceleration in the x direction (in g's).
#     accel_y_g (np.array): Acceleration in the y direction (in g's).
#     time_delay (float): Time delay between samples (in seconds).
#     scale_factor (float): Number of pixels per meter for conversion. Default is 100 pixels/meter.
    
#     Returns:
#     displacement_x_pixels (np.array): Displacement in pixels along x-axis.
#     displacement_y_pixels (np.array): Displacement in pixels along y-axis.
#     """
    
#     # Convert g's to m/s²
#     g = 9.81
#     accel_x = accel_x_g * g
#     accel_y = accel_y_g * g

#     # Integrating acceleration to get velocity (numerical integration)
#     velocity_x = np.cumsum(accel_x) * time_delay  # velocity = sum(acceleration * dt)
#     velocity_y = np.cumsum(accel_y) * time_delay  # velocity = sum(acceleration * dt)

#     # Integrating velocity to get displacement (numerical integration)
#     displacement_x = np.cumsum(velocity_x) * time_delay  # displacement = sum(velocity * dt)
#     displacement_y = np.cumsum(velocity_y) * time_delay  # displacement = sum(velocity * dt)

#     # Convert displacement from meters to pixels
#     displacement_x_pixels = displacement_x * scale_factor
#     displacement_y_pixels = displacement_y * scale_factor

#     return displacement_x_pixels, displacement_y_pixels
