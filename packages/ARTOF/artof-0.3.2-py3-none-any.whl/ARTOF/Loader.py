import numpy as np
import pandas as pd
import os 
import time
from io import TextIOWrapper
from IPython.display import display
import plotly.graph_objects as go

# internal
from .data_read import read_metadata, load_file, get_metadata_df
from .data_process import get_bin_edges, project_data, get_axis_values
from .Transformer import ARTOFTransformer
from .sweep_scienta import get_sweep_parameters
from .normalize import get_norm_scaling_factor, norm_sweep
from .artof_utils import get_next_step, next_file_exists
from .threading_utils import PropagatingThread

# convert name of datatype to actual type
data_type_dict = {'int32': np.int32, 'float64': np.float64}


class ARTOFLoader:
    """Class to load ARTOF data."""

    def __init__(self):
        """Initialize ARTOFLoader class"""
        self.data = None
        self.binned_data = None
        self.bin_edges = list()
        self.format = None
        self.axes = None
        self.metadata = None
        self.transformer = None

    def load_run(self, path: str, format: str, x0: int = None, y0: int = None, t0: int = None, iter_interval: tuple = None, sweep_type: str = 'Sienta', multithreading=True):
        """
        Load ARTOF data for run in directory and transform into desired format.

        Args:
            path: Path to run directory.
            format: Load parameters in given format ('raw', 'raw_SI', 'cylindrical', 'spherical').
                `raw`: Load raw data in ticks (x,y,t).
                `raw_SI`: Load raw data in SI units (x,y,t).
                `cylindrical`: Load data in cylindrical coordinates (r, phi, t).
                `spherical`: Load data in spherical coordinates and associated energy (E, theta, phi).
            x0: Offset for x ticks, optional (default extracted from acquisition.cfg).
            y0: Offset for y ticks, optional (default extracted from acquisition.cfg).
            t0: Offset for t ticks, optional (default extracted from acquisition.cfg).
            iter_interval: Tuple of start (including) and stop (excluding) lens iteration to load (default None, load all).
            sweep_type: Type of sweep analysis ('Sienta' or 'normal'), optional (default 'Sienta')
            multithreading: Use multithreading for data loading (default True).
        """     

        self.__init_run(path, format, x0, y0, t0, sweep_type)

        # setup range of iterations to load
        if iter_interval is None:
            iter_range = range(self.metadata.general.lensIterations)
        else:
            if iter_interval[1] > self.metadata.general.lensIterations or iter_interval[0] < 0:
                raise ValueError(f'Given range of iterations is not within range of available iterations (0 to {self.metadata.general.lensIterations-1}).')
            iter_range = range(iter_interval[0], iter_interval[1])
        # save number of iterations
        self.iterations = len(iter_range)
        # setup progress information                
        self.progress_info = {'current': 0, 'total': self.iterations * self.lens_steps}
        self.__print_progress()
        # transform data to desired format via multithreading if desired
        data_pieces = []
        if multithreading:
            threads = []
            for iter in iter_range:
                for step in range(self.lens_steps):                    
                    thread = PropagatingThread(target=self.__process_data, args=(path, iter, step, data_pieces, format))
                    threads.append(thread)
                    thread.start()
            for thread in threads:
                thread.join()
        else:
            for iter in range(self.metadata.general.lensIterations):
                for step in range(self.lens_steps):
                    self.__process_data(path, iter, step, data_pieces, format)
        self.data = np.concatenate(data_pieces, axis=0)

        # print information about loaded data
        print() # need to stop overwriting of progress bar
        print(f'Loaded and transformed {self.data.shape[0]} data points to formats {self.axes}.')

    def __init_run(self, path: str, format: str, x0: int, y0: int, t0: int , sweep_type: str):
        """
        Initialize ARTOFLoader class for run in directory.

        Args:
            path: Path to run directory.
            format: Load parameters in given format ('raw', 'raw_SI', 'cylindrical', 'spherical').
                `raw`: Load raw data in ticks (x,y,t).
                `raw_SI`: Load raw data in SI units (x,y,t).
                `cylindrical`: Load data in cylindrical coordinates (r, phi, t).
                `spherical`: Load data in spherical coordinates and associated energy (E, theta, phi).
            x0: Offset for x ticks
            y0: Offset for y ticks
            t0: Offset for t ticks
            sweep_type: Type of sweep analysis ('Sienta' or 'normal')
        """
        
        # save format 
        self.format = format
        # aquire metadata
        self.metadata = read_metadata(path)
        # setup everything need for sweep analysis
        self.acquisitionMode = self.metadata.general.acquisitionMode
        if self.acquisitionMode == 'sweep':
            if sweep_type == 'Sienta':
                general = self.metadata.general
                self.sweep_start_energy, self.sweep_end_energy, self.adjusted_channel_width, self.lens_steps, self.lens_k = get_sweep_parameters(general.spectrumBeginEnergy,
                    general.spectrumEndEnergy, general.lensLowEdgeEnergyStep, self.metadata.lensmode.lensK)
            else:
                raise Exception('Normal sweep analysis not implemented yet.')
        else: 
            self.lens_steps = 1
        # create transformer based on metadata and transformation parameters        
        self.x0 = self.metadata.detector.x0 if x0 is None else x0
        self.y0 = self.metadata.detector.y0 if y0 is None else y0
        self.t0 = self.metadata.detector.t0 if t0 is None else t0
        self.transformer = ARTOFTransformer(self.metadata, self.x0, self.y0, self.t0)
        # save axes and set returned bin configurations as default
        self.axes, self.default_bin_confs = self.transformer.get_axis_and_bins(format, self.metadata)
        # check if lens iterations and steps are available
        if self.metadata.general.lensIterations == 0 or self.metadata.general.lensSteps == 0:
            raise ValueError('No lens iterations or steps found in metadata.')

    def log_metadata(self, pars: list = ['analyzer.lensMode', 'analyzer.elementSet', 'analyzer.passEnergy', 'general.acquisitionStarted', 'general.acquisitionMode', 'general.xytFormat', 'general.lensIterations', 'general.lensDwellTime', 'general.spectrumBeginEnergy', 'general.spectrumEndEnergy', 'general.centerEnergy', 'detector.t0', 'detector.t0Tolerance']) -> pd.DataFrame:
        """
        Get metadata of loaded data.

        Args:
            pars: List of keys to be extracted from metadata (when 'None' all metadata will be returned), optional.                

        Returns:
            Dataframe conisting of metadata of loaded data.
        """

        return get_metadata_df(self.metadata, pars)


    def save_transformed_data(self, path: str):
        """
        Save transformed data to binary file (path + '.bin') and save addional info file (path + '_info.txt')

        Args:
            path: Path to file where transformed data should be stored.
        """    

        self.data.tofile(f'{path}.bin') 
        with open(f'{path}_info.txt', 'w') as f:
            self.__write_par(f, type(self.data[0,0]).__name__)
            self.__write_par(f, self.format)
            self.__write_par(f, f'{self.x0}, {self.y0}, {self.t0}')
            self.__write_par(f, self.acquisitionMode)
            if self.acquisitionMode == 'sweep':
                self.__write_par(f, f'{self.sweep_start_energy},{self.sweep_end_energy},{self.adjusted_channel_width},{self.lens_steps},{self.lens_k}')
            self.__write_par(f, ",".join(self.axes))
            self.__write_par(f, ";".join(map(str, self.default_bin_confs)))

        print(f'Saved transformed data as binary file to {path}_{self.format}.bin and additional information to {path}_{self.format}_info.txt')


    def __write_par(self, file: TextIOWrapper, par):
        """
        Write parameter to file with new line at the end.

        Args:
            file: File to write to.
            par: Parameter to write.
        
        """

        file.write(par)
        file.write('\n')

    def load_transformed_data(self, data_path: str, info_path: str):
        """
        Load transformed data from file.

        Args:
            data_path: Path to file where transformed data is stored.
            info_path: Path to file where information about the transformed data is stored.
        """

        with open(info_path) as f:
            data_type = data_type_dict[next(f).strip()]
            self.format = next(f).strip()
            self.x0, self.y0, self.t0 = map(int, next(f).strip().split(','))
            self.acquisitionMode = next(f).strip()
            if self.acquisitionMode == 'sweep':
                self.sweep_start_energy, self.sweep_end_energy, self.adjusted_channel_width, self.lens_steps, self.lens_k = map(float, next(f).strip().split(','))
                self.lens_steps = int(self.lens_steps)
            self.axes = next(f).strip().split(',')
            self.default_bin_confs = [eval(bin_conf) for bin_conf in next(f).strip().split(';')]
        self.data = np.fromfile(data_path, dtype=data_type).reshape(-1,3)


    def bin_data(self, cust_bin_confs: list = [None, None, None], norm_modes: list = None):
        """
        Bin loaded data into 3D histogram.

        Args:        
            bin_confs: List of 3 custom binning configurations for the 3 parameters [min, max, points], optional. F.e.: [[-1500, 1500, 101], [-1500, 1500, 101],[12000, 18000, 201]]  
            norm_mode: Normalization mode for binned data ('iterations', 'dwell_time', 'sweep'). Default is None.
                `iterations`: Normalize data by number of iterations.
                `dwell_time`: Normalize data by dwell time.
                `sweep`: Normalize data by changing window size of sweep data.

        Raises:
            Exception: If data is not loaded before binning.
        """

        if self.data is None:
            raise Exception('Load the data before binning the data.')
        
        # use either passed or default bin configurations
        bin_confs = self.__get_bin_confs(cust_bin_confs)

        self.bin_edges = self.__get_bin_edges(bin_confs)
        
        self.binned_data = self.__bin_data(self.data, self.bin_edges, norm_modes)

    def __get_bin_confs(self, cust_bin_confs: list):
        """
        Set bin configurations for 3 parameters.

        Args:
            cust_bin_confs: List of 3 custom binning configurations for the 3 parameters [min, max, points], optional. F.e.: [[-1500, 1500, 101], [-1500, 1500, 101],[12000, 18000, 201]]        
        """

        bin_confs = []
        for i, bin_conf in enumerate(cust_bin_confs):
            if bin_conf is None:
                print(f'Using default bin configuration for {self.axes[i]}: {self.default_bin_confs[i]}')
                bin_confs.append(self.default_bin_confs[i])
            else:
                bin_confs.append(bin_conf)
        return bin_confs
    
    def __get_bin_edges(self, bin_confs: list):
        
        
        # create bin edges based on the passed bin configs
        bin_edges = []
        for i in range(3):
            bin_edges.append(get_bin_edges(bin_confs[i], data_id=self.axes[i]))

        return bin_edges


    def __bin_data(self, data: np.ndarray, bin_edges: list, norm_modes: list):
        """
        Bin loaded data into 3D histogram.

        Args:
            data: Data to be binned.        
            bin_edges: List of bin edges for each axis.
            norm_mode: Normalization mode for binned data ('iterations', 'dwell_time', 'sweep').
                `iterations`: Normalize data by number of iterations.
                `dwell_time`: Normalize data by dwell time.
                `sweep`: Normalize data by changing window size of sweep data.
        """

        # bin data in 3D histogram
        binned_data, _ = np.histogramdd(data, bins=self.bin_edges) 

        # normalize data if desired        
        if norm_modes is not None:
            scaling_factor = get_norm_scaling_factor(norm_modes, self.iterations, self.metadata.general.lensDwellTime)
            binned_data *= scaling_factor
            # normalize data by sweep acceptance if desired and in sweep mode
            if 'sweep' in norm_modes: 
                if self.acquisitionMode != 'sweep' or self.format != 'spherical':
                    raise Exception('Sweep normalization only possible for sweep data in spherical format.')
                binned_data = norm_sweep(binned_data, self.bin_edges[0], self.sweep_start_energy,
                                              self.adjusted_channel_width, self.lens_steps, self.lens_k)
                
            # print all non-recognized norm modes
            for mode in norm_modes:
                if mode not in ['iterations', 'dwell_time', 'sweep']:
                    print(f'Normalization mode "{mode}" not recognized.')
        
        return binned_data
            
            
    def __process_data(self, path: str, iter: int, step: int, data_pieces: list, load_as: str):            
        """
        Load and transform single data file in given format (needed for multithreading).

        Args:
            path: Path where data files are located.
            iter: Index of the lens iteration to be loaded.
            step: Index of the lens step to be loaded.
            data_pieces: List of transformed data pieces to which the newly transformed data should be appended.
            load_as: Desired transformation format.

        Raises:
            FileNotFoundError: If file (and next file) is not found.
        
        """

        # relevant for live plotting
        try:
            raw_data = load_file(path, iter, step)
        except FileNotFoundError:
            if next_file_exists(path, iter, step, self.lens_steps, self.iterations):
                print(f'Skipping file {path}/{iter}_{step} as it is missing.')
                self.progress_info['current'] += 1
                self.__print_progress()
                return
            else: 
                raise FileNotFoundError(f'File {path}/{iter}_{step} not found (more than 2 files missing).')
        except PermissionError:
            print(f'File {path}/{iter}_{step} does not allow reading yet. Trying again in 0.5 seconds.')
            # if file does not allow reading yet, try again after 0.5 seconds
            time.sleep(0.5)
            raw_data = load_file(path, iter, step)
        data_pieces.append(self.__transform_data(raw_data, iter, step, load_as))
        self.progress_info['current'] += 1
        self.__print_progress()

    def __transform_data(self, raw_data: np.ndarray, iter: int, step: int, load_as: str):        
        """
        Load and transform single data file in given format (needed for multithreading).

        Args:
            raw_data: Raw data to be transformed.
            iter: Index of the lens iteration to be loaded.
            step: Index of the lens step to be loaded.
            data_pieces: List of transformed data pieces to which the newly transformed data should be appended.
            load_as: Desired transformation format.
        """

        if self.acquisitionMode == 'sweep':
            center_energy = self.sweep_start_energy + step * self.adjusted_channel_width
            return self.transformer.transform(raw_data, load_as, center_energy=center_energy)
        else:
            center_energy = self.metadata.general.centerEnergy
            return self.transformer.transform(raw_data, load_as, center_energy=center_energy)


    def __print_progress(self):
        """
        Print progress information.
        """
        current = self.progress_info['current']
        total = self.progress_info['total']
        print('\r', end='')
        print(f'Progress: [{"="*int(current*20/total):<20}] {current}/{total}', end='\r')


    def plot(self, axes: list, ranges: list = [None, None, None], norm_step_size: bool = False, photon_energy: float = None, width: int = 600, height: int = 600):
        """
        Plot loaded data as projection onto given axes. Projections are possible onto 1 or 2 axes.

        Args:
            axes: List containing all axes onto which the projection is performed, e.g., [0,1].
            ranges: List containing ranges for axes (e.g., [[50, 101], [0,50], None]), if None entire range of axes is used (default entire range of each axis).
            norm_step_size: Normalize data with step size before plotting (default False).
            photon_energy: Photon energy to plot in binding energy, optional (default None).
            width: Width of plot (default 600).
            height: Height of plot (default 600).
        """
        
        axes_values = get_axis_values(self.bin_edges, axes, photon_energy)
        proj_data = project_data(self.binned_data, self.bin_edges, axes, ranges, norm_step_size)

        self.fig = go.FigureWidget(layout=go.Layout(width=width, height=height))
        # TODO find better way to display plot        
        display(self.fig)
        if len(axes) == 2: # plot data in 2D as image
            # setup extent for image
            dx = self.bin_edges[axes[0]][1]-self.bin_edges[axes[0]][0]
            x0 = self.bin_edges[axes[0]][0] + dx/2
            dy = self.bin_edges[axes[1]][1]-self.bin_edges[axes[1]][0]
            y0 = self.bin_edges[axes[1]][0] + dy/2
            # invert energy axis if displayed in binding energy
            if photon_energy is not None and 0 in axes:
                energy_idx = axes.index(0)
                if energy_idx == 0:
                    x0 = np.abs(x0-photon_energy)
                    dx = -dx
                    self.fig.update_xaxes(autorange="reversed")
                else:
                    y0 = np.abs(y0-photon_energy)
                    dy = -dy
                    self.fig.update_yaxes(autorange="reversed")
            # Electric, Viridis, Blackbody, Jet
            self.fig.add_heatmap(colorscale='Viridis', z=proj_data, x0=x0, dx=dx, y0=y0, dy=dy)
            self.fig.update_layout(xaxis_title=self.__axis_label(self.axes[axes[0]]), yaxis_title=self.__axis_label(self.axes[axes[1]]))
        elif len(axes) == 1: # plot data in 1D as line
            x_data = axes_values[0]
            self.fig.add_scatter(x=x_data, y=proj_data)
            self.fig.update_layout(xaxis_title=self.__axis_label(self.axes[axes[0]]), yaxis_title='Counts')
            if photon_energy is not None and 0 in axes:
                self.fig.update_xaxes(autorange="reversed")
                self.fig.update_xaxes(title_text='Binding Energy [eV]')
        else:
            raise Exception(f'A projection along {len(axes)} axes is not possible.')
        
    def export_to_csv(self, path: str, axes: list, ranges: list = [None, None, None], norm_step_size: bool = False, delimiter: str = ','):
        """
        Export loaded data as projection onto given axes. Projections are possible onto 1 or 2 axes.

        Args:
            path: Path including file name to which the data is saved.
            axes: List containing all axes onto which the projection is performed, e.g., [0,1].
            ranges: List containing ranges for axes (e.g., [[50, 101], [0,50], None]), if None entire range of axes is used (default entire range of each axis).
            norm_step_size: Normalize data with step size before plotting (default False).
            delimiter: Delimiter by which the data is separated (default ',').
        """  

        axes_values = get_axis_values(self.bin_edges, axes)
        proj_data = project_data(self.binned_data, self.bin_edges, axes, ranges, norm_step_size)        
        # save t0, x0 ad y0 to header        
        header = f'# x0: {self.x0}, y0: {self.y0}, t0: {self.t0}'
        # add axis to header
        for i, ax in enumerate(axes):
            ax_values = ', '.join(map(str, axes_values[i]))
            header += f'\n# {self.axes[ax]}: {ax_values}'
        np.savetxt(path, proj_data, delimiter=delimiter, header=header, comments='')
        # df = pd.DataFrame(axes_values + proj_data).T
        # df.to_csv(path, index=False, header=False, sep=delimiter)

    def __axis_label(self, axis: str) -> str:
        """
        Build string for matplotlib axis label including Greek characters.

        Args:
            axis: String containing the axis label and unit separated by '_'.

        Returns:
            Formatted string for matplotlib.
        """

        name, unit = axis.split('_')
        match name:
            case 'phi':
                name = '&#966;'
            case 'theta':
                name = '&#977;'
        return f'{name} [{unit}]'
    

    def live_plot(self, path: str, format: str,  axes: list, x0: int = None, y0: int = None, t0: int = None, iter_interval: tuple = None, sweep_type: str = 'Sienta', cust_bin_confs: list = [None, None, None], norm_modes: list = None, ranges: list = [None, None, None], norm_step_size: bool = False, photon_energy: float = None, width: int = 600, height: int = 600, update_intervall: int = 10, multithreading = True, timeout: float = 30):  
        """
        Load, bin and plot data in one step.
        
        Args:
            path: Path to run directory.
            format: Load parameters in given format ('raw', 'raw_SI', 'cylindrical', 'spherical').
                `raw`: Load raw data in ticks (x,y,t).
                `raw_SI`: Load raw data in SI units (x,y,t).
                `cylindrical`: Load data in cylindrical coordinates (r, phi, t).
                `spherical`: Load data in spherical coordinates and associated energy (E, theta, phi).
            axes: List containing all axes onto which the projection is performed, e.g., [0,1].
            x0: Offset for x ticks, optional (default extracted from acquisition.cfg).
            y0: Offset for y ticks, optional (default extracted from acquisition.cfg).
            t0: Offset for t ticks, optional (default extracted from acquisition.cfg).
            iter_interval: Tuple of start (including) and stop (excluding) lens iteration to load (default None, load all).
            sweep_type: Type of sweep analysis ('Sienta' or 'normal'), optional (default 'Sienta')
            cust_bin_confs: List of 3 custom binning configurations for the 3 parameters [min, max, points], optional. F.e.: [[-1500, 1500, 101], [-1500, 1500, 101],[12000, 18000, 201]]
            norm_modes: Normalization mode for binned data ('iterations', 'dwell_time', 'sweep'). Default is None.
                `iterations`: Normalize data by number of iterations.
                `dwell_time`: Normalize data by dwell time.
                `sweep`: Normalize data by changing window size of sweep data.
            ranges: List containing ranges for axes (e.g., [[50, 101], [0,50], None]), if None entire range of axes is used (default entire range of each axis).
            norm_step_size: Normalize data with step size before plotting (default False).
            photon_energy: Photon energy to plot in binding energy, optional (default None).
            width: Width of plot (default 600).
            height: Height of plot (default 600).
            update_interval: Iteration interval in which the plot is updated (default 10).
            multithreading: Use multithreading for data loading (default False).
            timeout: Time in seconds to wait for file to be available (default)
        """  
             
        # if self.fig is None:
        #     raise Exception('Create figure for live plotting first with show_live_plot().')
        self.fig = go.FigureWidget(layout=go.Layout(width=width, height=height))
        display(self.fig)


        self.__init_run(path, format, x0, y0, t0, sweep_type)

        # get bin configurations
        bin_confs = self.__get_bin_confs(cust_bin_confs)
        # get bin edges
        self.bin_edges = self.__get_bin_edges(bin_confs)

        # setup range of iterations to load
        if iter_interval is None:
            iter_range = range(self.metadata.general.lensIterations)
        else:
            if iter_interval[1] > self.metadata.general.lensIterations or iter_interval[0] < 0:
                raise ValueError(f'Given range of iterations is not within range of available iterations (0 to {self.metadata.general.lensIterations-1}).')
            iter_range = range(iter_interval[0], iter_interval[1])
        # save number of iterations
        self.iterations = len(iter_range)

        # setup progress information
        self.progress_info = {'current': 0, 'total': self.iterations *self.lens_steps}
        self.__print_progress()

        # # create empty binned data with dimensions of binning configuration
        # self.binned_data = np.zeros(np.array(bin_confs)[:,2].astype(int))



        
        if len(axes) == 2: # plot data in 2D as image
            proj_data = np.zeros((len(self.bin_edges[axes[1]])-1, len(self.bin_edges[axes[0]])-1))
            # setup extent for image
            dx = self.bin_edges[axes[0]][1]-self.bin_edges[axes[0]][0]
            x0 = self.bin_edges[axes[0]][0] + dx/2
            dy = self.bin_edges[axes[1]][1]-self.bin_edges[axes[1]][0]
            y0 = self.bin_edges[axes[1]][0] + dy/2
            # invert energy axis if displayed in binding energy
            if photon_energy is not None and 0 in axes:
                energy_idx = axes.index(0)
                if energy_idx == 0:
                    x0 = np.abs(x0-photon_energy)
                    dx = -dx
                    self.fig.update_xaxes(autorange="reversed")
                else:
                    y0 = np.abs(y0-photon_energy)
                    dy = -dy
                    self.fig.update_yaxes(autorange="reversed")
            # Electric, Viridis, Blackbody, Jet
            self.fig.add_heatmap(colorscale='Viridis', z=proj_data, x0=x0, dx=dx, y0=y0, dy=dy)
            self.fig.update_layout(xaxis_title=self.__axis_label(self.axes[axes[0]]), yaxis_title=self.__axis_label(self.axes[axes[1]]))
        elif len(axes) == 1: # plot data in 1D as line
            x_data = np.array(get_axis_values(self.bin_edges, axes, photon_energy=photon_energy)[0])
            proj_data = np.zeros(len(x_data))

            self.fig.add_scatter(x=x_data, y=proj_data)
            self.fig.update_layout(xaxis_title=self.__axis_label(self.axes[axes[0]]), yaxis_title='Counts')
            if photon_energy is not None and 0 in axes:
                self.fig.update_xaxes(autorange="reversed")
                self.fig.update_xaxes(title_text='Binding Energy [eV]')



        try:
            steps_to_load = [(iter_range.start,0)]*2

            iter = iter_range.start
            step = 0
            while steps_to_load[0] != (iter_range.stop, 0):
                # wait for at least one file to become available
                time_waited = 0
                while not os.path.exists(f'{path}/{iter}_{step}'):
                    if next_file_exists(path, iter, step, self.lens_steps, self.iterations):
                        break
                    time.sleep(0.5)
                    time_waited += 0.5
                    if time_waited >= timeout:
                        raise TimeoutError(f'File {path}/{iter}_{step} not available after {timeout} seconds.')
                iter, step = get_next_step(iter, step, self.lens_steps)
                

                # add additional steps to load
                while os.path.exists(f'{path}/{iter}_{step}') and (iter, step) != (iter_range.stop, 0):
                    steps_to_load[1] = (iter, step)
                    iter, step = get_next_step(iter, step, self.lens_steps)

                # transform data
                data_pieces = []
                if multithreading:
                    threads = []
                    for cur_iter in range(steps_to_load[0][0], steps_to_load[1][0]+1):
                        for cur_step in range(steps_to_load[0][1], steps_to_load[1][1]+1):
                            thread = PropagatingThread(target=self.__process_data, args=(path, cur_iter, cur_step, data_pieces, format))
                            threads.append(thread)
                            thread.start()

                    for thread in threads:
                        thread.join()
                else:
                    for cur_iter in range(steps_to_load[0][0], steps_to_load[1][0]+1):
                        for cur_step in range(steps_to_load[0][1], steps_to_load[1][1]+1):
                            self.__process_data(path, cur_iter, cur_step, data_pieces, format)

                # bin data 
                if len(data_pieces) > 0: # only bin data if data is available
                    data = np.concatenate(data_pieces, axis=0)
                    binned_data = self.__bin_data(data, self.bin_edges, norm_modes)

                    # project data onto axes
                    proj_data += project_data(binned_data, self.bin_edges, axes, ranges, norm_step_size)

                    # update plot
                    if len(axes) == 2:
                        self.fig.data[0].z = proj_data
                    elif len(axes) == 1:
                        self.fig.data[0].y = proj_data

                # update steps to load
                steps_to_load[0] = steps_to_load[1] = (iter, step)
        except KeyboardInterrupt:
            print()
            print('Stopping live plotting.')
            if multithreading:
                for thread in threads:
                    thread.join()
            