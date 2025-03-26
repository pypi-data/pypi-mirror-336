import numpy as np
from scipy.interpolate import RectBivariateSpline
from .data_read import Metadata
from .default_bin_config import get_default_xyr_config, get_default_t_config, get_default_phi_config, get_default_E_config, get_default_theta_config

class ARTOFTransformer:
    """Class to transform raw artof data"""

    def __init__(self, metadata: Metadata, x0: int, y0: int, t0: int):
        """
        Initializer ARTOFTransform class

        Args:
            metadata: Metadata class containing all metadata for current measurement.
            x0: x offset in ticks.
            y0: y offset in ticks.
            t0: t offset in ticks.
        """
        self.tdc_res = metadata.detector.tdcResolution
        self.e_kin_ref = metadata.lensmode.eKinRef
        self.lens_k = metadata.lensmode.lensK
        # create transformations
        self.x_transform, self.y_transform, self.t_transform = self.__ticks_to_SI_transform(metadata, x0, y0, t0)                
        self.E_transform, self.theta_transform = self.__tr_to_Etheta_transform(metadata)       
        # save t0 in tacks, t_min, and t_max in SI (at reference energy)
        self.t0 = metadata.detector.t0 if t0 is None else t0
        self.t_min, self.t_max = metadata.lensmode.tofVector[0], metadata.lensmode.tofVector[-1]
                    

    def transform(self, raw_data: list, load_as: str, center_energy: float = None) -> list:
        """
        Transform raw data to desired representation.

        Args:
            raw_data: 2D list of raw data points (x, y, t ticks).
            load_as: Desired representation to transform to (options: 'raw', 'raw_SI', 'cylindrical', 'spherical').
            center_energy: Center energy in eV (required for spherical transformation).

        Returns:
            Three 2D list of transformed data, list of variable names, and list of default bin edges for given transformation.
        """

        match load_as:
            case 'raw':
                data = raw_data
            case 'raw_SI':
                x, y, t = self.__raw_to_SI(raw_data)
                data = np.stack([x, y, t], -1)
            case 'cylindrical':
                r, phi, t = self.__raw_to_cylindrical(raw_data)
                data = np.stack([r, phi, t], -1)
            case 'spherical':           
                if center_energy is None:
                    raise ValueError('Center energy is required for spherical transformation.')             
                E, phi, theta = self.__raw_to_spherical(raw_data, center_energy)
                data = np.stack([E, phi, theta],-1)
            case _:
                print(f'Did not recognize transformation of type {load_as}. Using raw data')
                data = raw_data
        return data
    
    def __raw_to_spherical(self, raw_data: list, center_energy: float) -> list:
        """
        Transform raw data to spherical coordinates.

        Args:
            raw_data: 2D list of raw data points (x, y, t ticks).
            center_energy: Center energy in eV.
        
        Returns:
            3 lists containing E, phi, and theta values
        """
        energy_scaler = center_energy / self.e_kin_ref

        raw_data = self.__clip_t(raw_data, energy_scaler)
        r, phi, t = self.__raw_to_cylindrical(raw_data)
        t *= np.sqrt(energy_scaler)
        E = self.E_transform.ev(r, t) * energy_scaler
        theta = self.theta_transform.ev(r, t)
        E, phi, theta = self.__clip_E(E, phi, theta, center_energy)
        return E, phi, theta
    
    def __clip_t(self, raw_data: list, energy_scaler: float):    
        """
        Clip raw data to t_min and t_max in SI units.

        Args:
            raw_data: 2D list of raw data points (x, y, t ticks).
            energy_scaler: Energy scaler to scale energy and time.

        Returns:
            Clipped raw data.
        """    
        t_min_raw = self.t_min * self.tdc_res / np.sqrt(energy_scaler) + self.t0
        t_max_raw = self.t_max * self.tdc_res / np.sqrt(energy_scaler) + self.t0
        return raw_data[(raw_data[:,2] >= t_min_raw) & (raw_data[:,2] <= t_max_raw)]
    
    def __clip_E(self, E, phi, theta, center_energy):
        """
        Clip (E, phi, and theta) point values to be within lensK window.

        Args:
            E: Energy in eV.
            phi: Phi in radians.
            theta: Theta in radians.

        Returns:
            Clipped E, phi, and theta.
        """
        E_min = center_energy *  (1 - self.lens_k/2)
        E_max = center_energy *  (1 + self.lens_k/2)
        return E[(E >= E_min) & (E <= E_max)], phi[(E >= E_min) & (E <= E_max)], theta[(E >= E_min) & (E <= E_max)]
    
    def __raw_to_cylindrical(self, raw_data: list) -> list:
        """
        Transform raw data to cylindrical coordinates.

        Args:
            raw_data: 2D list of raw data points (x, y, t ticks).

        Returns:
            Three lists containing r, phi, and t values.
        """
        x, y, t = self.__raw_to_SI(raw_data)
        r, phi = self.__xy_to_polar(x,y)
        return r, phi, t

    def __raw_to_SI(self, raw_data: list) -> list:
        """
        Transform raw data to SI units.

        Args:
            raw_data: 2D list of raw data points (x, y, t ticks).

        Returns:
            Three lists containing x, y, and t values in SI units.
        """
        x = self.x_transform.ev(raw_data[:,1], raw_data[:,0])
        y = self.y_transform.ev(raw_data[:,1], raw_data[:,0])
        t = self.t_transform(raw_data[:,2])
        return x,y,t


    def get_axis_and_bins(self, load_as: str, metadata: Metadata) -> tuple:
        """
        Get axis names and default bin edges for given transformation.

        Args:
            load_as: Desired representation to transform to (options: 'raw', 'raw_SI', 'cylindrical', 'spherical').
            metadata: Metadata class containing all metadata for current measurement.
            t_0: Time offset in ticks.
        """
        match load_as:
            case 'raw':
                x_bin_conf = get_default_xyr_config(metadata.detector.spatialDiameter)
                y_bin_conf = get_default_xyr_config(metadata.detector.spatialDiameter)
                t_bin_conf = get_default_t_config(metadata.lensmode.tofVector, metadata.lensmode.energyMatrix, metadata.lensmode.eKinRef, 
                                                  metadata.detector.tdcResolution, metadata.general.spectrumBeginEnergy, metadata.general.spectrumEndEnergy,
                                                  metadata.detector.t0Tolerance, self.t0)

                return ['x_ticks', 'y_ticks', 't_ticks'], [x_bin_conf, y_bin_conf, t_bin_conf]
            case 'raw_SI':
                spatial_diameter = metadata.detector.spatialDiameter
                # implemented based on Igor ARTOFLoader, TODO check if correct
                x_vec_max = metadata.detector.transformXVector[-1]
                x_matrix_max = max([max(row) for row in metadata.detector.transformXMatrix])
                x_scaling = x_matrix_max / x_vec_max
                y_vec_max = metadata.detector.transformYVector[-1]            
                y_matrix_max = max([max(row) for row in metadata.detector.transformYMatrix])
                y_scaling = y_matrix_max / y_vec_max
                x_bin_conf = get_default_xyr_config(spatial_diameter, scaling_factor=x_scaling)
                y_bin_conf = get_default_xyr_config(spatial_diameter, scaling_factor=y_scaling)
                t_bin_conf = get_default_t_config(metadata.lensmode.tofVector, metadata.lensmode.energyMatrix, metadata.lensmode.eKinRef, 
                                                  metadata.detector.tdcResolution, metadata.general.spectrumBeginEnergy, metadata.general.spectrumEndEnergy,
                                                  metadata.detector.t0Tolerance, self.t0, si=True)
                return ['x_m', 'y_m', 't_s'], [x_bin_conf, y_bin_conf, t_bin_conf]
            case 'cylindrical':
                spatial_diameter = metadata.detector.spatialDiameter
                # implemented based on Ugor ARTOFLoader, TODO check if correct
                x_vec_max = metadata.detector.transformXVector[-1]
                x_matrix_max = max([max(row) for row in metadata.detector.transformXMatrix])
                x_scaling = x_matrix_max / x_vec_max
                y_vec_max = metadata.detector.transformYVector[-1]            
                y_matrix_max = max([max(row) for row in metadata.detector.transformYMatrix])
                y_scaling = y_matrix_max / y_vec_max
                r_bin_conf = get_default_xyr_config(spatial_diameter, scaling_factor=max(x_scaling,y_scaling), radius=True)
                phi_bin_conf = get_default_phi_config()
                t_bin_conf = get_default_t_config(metadata.lensmode.tofVector, metadata.lensmode.energyMatrix, metadata.lensmode.eKinRef,
                                                    metadata.detector.tdcResolution, metadata.general.spectrumBeginEnergy, metadata.general.spectrumEndEnergy,
                                                    metadata.detector.t0Tolerance, self.t0, si=True)
                return ['r_m', 'phi_rad', 't_s'], [r_bin_conf, phi_bin_conf, t_bin_conf]
            case 'spherical':
                E_min = metadata.general.spectrumBeginEnergy
                E_max = metadata.general.spectrumEndEnergy
                E_step_size = metadata.general.lensLowEdgeEnergyStep if metadata.general.acquisitionMode == 'sweep' else None
                E_bin_conf = get_default_E_config(E_min, E_max, E_step_size=E_step_size)
                phi_bin_conf = get_default_phi_config()
                theta_bin_conf = get_default_theta_config(metadata.lensmode.maxTheta)
                return ['E_eV', 'phi_rad', 'theta_rad'], [E_bin_conf, phi_bin_conf, theta_bin_conf] 
            case _:
                raise ValueError(f'Did not recognize transformation of type {load_as}.')

    def __ticks_to_SI_transform(self, metadata: Metadata, x0: int = None, y0: int = None, t0: int = None) -> tuple:
        """
        Transform x, y, and t from ticks to SI units using transformation matrices and tdcResolution from acquisition.cfg file.

        Args:
            metadata: Metadata class containing all metadata for current measurement.
            x0: x offset in ticks (default: from the acquisition.cfg file).
            t0: y offset in ticks (default: from the acquisition.cfg file).
            t0: t offset in ticks (default: from the acquisition.cfg file).

        Returns:
            Three lists containing x, y, and t values in SI units.
        """
        # convert x and y ticks to radius in m and phi in radians
        detector = metadata.detector
        x0 = detector.x0 if x0 is None else x0
        y0 = detector.y0 if y0 is None else y0
        x_transform = self.__create_matrix_transform(x0, y0, detector.transformXVector, detector.transformYVector, detector.transformXMatrix)
        y_transform = self.__create_matrix_transform(x0, y0, detector.transformXVector, detector.transformYVector, detector.transformYMatrix)

        # transform time ticks to time in seconds
        t_transform = lambda t:  self.__transform_time(t, self.t0, detector.tdcResolution)

        return x_transform, y_transform, t_transform


    def __xy_to_polar(self, x: float, y: float) -> tuple:    
        """
        Transform x and y in SI units to polar coordinates. The function arctan2(y, x) is used.

        Args:
            x: x value in meters (SI).
            y: y value in meters (SI).

        Returns:
            r in meters and phi in radians.
        """
        r = np.sqrt(x**2 + y**2)
        phi = np.arctan2(y, x)
        return r, phi


    def __tr_to_Etheta_transform(self, metadata: Metadata) -> tuple:
        """
        Transform t and r in SI units to E and theta. The transformation matrices from the acquisition.cfg file are used. Warning: Scaling has to be done when evaluting using factor centerEnergy/eKinRef.

        Args:
            metadata: Metadata class containing all metadata for current measurement.

        Returns:
            E in eV and theta in radians.
        """
        lensmode = metadata.lensmode
        t_vector = lensmode.tofVector
        r_vector = lensmode.radiusVector
        energy_matrix = lensmode.energyMatrix
        theta_matrix = lensmode.thetaMatrix

        E = self.__create_matrix_transform(0, 0, t_vector, r_vector, energy_matrix)
        theta = self.__create_matrix_transform(0, 0, t_vector, r_vector, theta_matrix)
        return E, theta


    def __transform_time(self, t_raw: int, t0: int, tdcResolution: float) -> float:
        """
        Transform time from ticks to seconds.

        Args:
            t_ticks: Time in ticks.
            t0: Time offset in ticks.
            tdcResolution: Resolutions of time to digital converter (tdc); number of events per second.

        Returns:
            Time in seconds.
        """
        return (t_raw - t0) * 1 / tdcResolution 


    def __create_matrix_transform(self, p1_0: int, p2_0: int, p1_vec: list, p2_vec: list, trans_mat: list) -> RectBivariateSpline:
        """
        Transform 2D data point using a given matrix using interpolation through a bivariate spline.

        Args:
            p1_0: Offset of p1.
            p2_0: Offset of p2.
            p1_vec: Vector corresponding to p1 and the columns of the matrix.
            p2_vec: Vector corresponding to p2 and the rows of the matrix.
            trans_mat: 2D list representing the transformation matrix.

        Returns:
            RectBivariateSpline interpolation for given matrix.
        """
        interp = RectBivariateSpline(p2_vec+p2_0, p1_vec+p1_0, trans_mat)
        return interp