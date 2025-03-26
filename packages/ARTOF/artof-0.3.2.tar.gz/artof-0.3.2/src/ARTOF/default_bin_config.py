import numpy as np

XYR_POINTS = 101

def get_default_xyr_config(spatial_diameter: int, scaling_factor: float = 1, radius: bool = False) -> list:
    """
    Extract the default x, y or r binning configuration.

    Args:
        spacial_diameter: Spacial diameter of the detector.
        scaling_factor: The scaling factor of the x, y r binning (default is 1). Important for x and y in SI units.
        radius: Wether the binning should be in radius or not.
    
    Returns:
        The default configuration for x, y or r binning configs.
    """
    xyr_min = 0 if radius else (-spatial_diameter/2)*scaling_factor
    xyr_max = (spatial_diameter/2)*scaling_factor
    return [xyr_min, xyr_max, XYR_POINTS]


T_UPSCALE_FACTOR = 10
T_MAX_POINTS = 201

def get_default_t_config(tof_vector: list, energy_matrix: list, e_ref: float, tdc_res: int, E_begin: float, E_end: float, t_0_tol: int, t0: int, si: bool = False) -> list:
    """
    Extract the default t binning configuration.

    Args:
        tof_vector: The time of flight vector from the acquisition.cfg.
        energy_matrix: The energy matrix from the acquisition.cfg.
        e_ref: The reference energy from the acquisition.cfg.
        tdc_res: The time to digital converter resolution from the acquisition.cfg.
        E_begin: The start energy from the acquisition.cfg.
        E_end: The end energy from the acquisition.cfg.
        t_0_tol: The tolerance for t_0 from the acquisition.cfg.
        t0: The t offset.
        si: Wether bin conf should be given in SI units (s).

    Returns:
        The default configuration for t binning configs.
    """
    ## calculate t0 for reference energy from energy matrix at theta=0
    # interpolate for higher precision
    t = np.linspace(tof_vector[0], tof_vector[-1], T_UPSCALE_FACTOR*len(tof_vector))
    E = np.interp(t, tof_vector, energy_matrix[0])
    # find crossing of reference energy and calculate t_0 in ticks
    crossing_idx = next(i for i,x in enumerate(E) if x < e_ref)
    t_0_ref = t[crossing_idx] * tdc_res
    # determin t_0 at spectrum start and end energy
    t_0_end = int(t_0_ref * np.sqrt(e_ref / E_begin ))
    t_0_begin = int(t_0_ref * np.sqrt(e_ref / E_end ))
    # calculate t_min und t_max based on t_0_tol
    t_min = (t_0_begin - t_0_tol + t0)
    t_max = (t_0_end + t_0_tol + t0)
    # calulate number of points
    t_points = min(T_MAX_POINTS, t_max - t_min)

    # if desired transform into seconds (si)
    if si:
        t_min /= tdc_res
        t_max /= tdc_res

    return [t_min, t_max, t_points]


PHI_MIN = -np.pi
PHI_MAX = np.pi
PHI_POINTS = 201

def get_default_phi_config() -> list:
    """
    Extract the default phi binning configuration.

    Returns:
        The default configuration for phi binning configs.
    """
    return [PHI_MIN, PHI_MAX, PHI_POINTS]

E_POINTS = 101

def get_default_E_config(E_min: float, E_max: float, E_step_size:float = None) -> list:
    """
    Extract the default E binning configuration.

    Args:
        E_min: The minimum value of the E binninge from aquisition.cfg.
        E_max: The maximum value of the E binninge from aquisition.cfg.
        E_step_size: The step size of the E binning e from aquisition.cfg for sweep mode. Default is None and there for E_POINTS will be used.

    Returns:
        The default configuration for E binning configs.
    """
    e_points = E_POINTS if E_step_size is None else int((E_max - E_min) / E_step_size) + 1

    return [E_min, E_max, e_points]

THETA_MIN = 0
THETA_POINTS = 201

def get_default_theta_config(theta_max: float) -> list:
    """
    Extract the default theta binning configuration.

    Args:
        theta_max: The maximum theta value from aquisition.cfg.

    Returns:
        The default configuration for theta binning configs.
    """
    return [THETA_MIN, theta_max, THETA_POINTS]