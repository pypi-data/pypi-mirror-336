from dataclasses import dataclass, field
from datetime import datetime
import numpy as np
import pandas as pd

datetime_format = '%Y-%m-%d, %H:%M:%S'

# define metadata classes
@dataclass
class General:   
    version: str = ''
    acquisitionStarted: datetime = datetime(1, 1, 1, 0, 0, 0)
    spectrumBeginEnergy: float = 0.0
    spectrumEndEnergy: float = 0.0
    spectrumChannelWidthEnergy: float = 0.0
    lensLowEdgeEnergyStep: float = 0.0
    lensDwellType: str = ''
    lensDwellTime: int = 0
    lensIterations: int = 0
    lensSteps: int = 0
    userSpectrumEndEnergy: float = 0.0
    userLensLowEdgeEnergyStep: float = 0.0
    acquisitionMode: str = ''
    centerEnergy: float = 0.0
    xytFormat: str = ''
    conversionLibraryName: str = ''
    conversionLibraryVersion= str = ''

@dataclass
class Lensmode:
    lensK: float = 0.0
    vectorSize: int = 0
    maxTheta: float = 0.0
    eKinRef: int = 0
    tofVector: np.ndarray = field(default_factory= lambda: np.array([], dtype=float)) # 1D
    radiusVector: np.ndarray = field(default_factory= lambda: np.array([], dtype=float)) # 1D
    energyMatrix: np.ndarray = field(default_factory= lambda: np.array([], dtype=float)) # 2D
    thetaMatrix: np.ndarray = field(default_factory= lambda: np.array([], dtype=float)) # 2D

@dataclass
class Detector:
    transformVectorSize: int = 0
    transformMaxY: int = 0
    transformXRef: int = 0
    transformXVector: np.ndarray = field(default_factory= lambda: np.array([], dtype=float)) # 1D
    transformYVector: np.ndarray = field(default_factory= lambda: np.array([], dtype=float)) # 1D
    transformXMatrix: np.ndarray = field(default_factory= lambda: np.array([], dtype=float)) # 2D
    transformYMatrix: np.ndarray = field(default_factory= lambda: np.array([], dtype=float)) # 2D
    x0: int = 0
    y0: int = 0
    t0: int = 0
    t0Tolerance: int = 0
    tdcResolution: float = 0.0
    spatialResolution: int = 0
    spatialDiameter: int = 0
    xDelayTimeMin: int = 0
    xDelayTimeMax: int = 0
    yDelayTimeMin: int = 0
    yDelayTimeMax: int = 0
    zDelayTimeMin: int = 0
    zDelayTimeMax: int = 0

@dataclass
class Analyzer:
    elementSet: str = ''
    lensMode: str = ''
    passEnergy: int = 0  

@dataclass
class Metadata:
    """
    Metadata class containing all metadata for current measurement.
    """
    general: General = field(default_factory=lambda: General())
    lensmode: Lensmode = field(default_factory=lambda: Lensmode())
    detector: Detector = field(default_factory=lambda: Detector())
    analyzer: Analyzer = field(default_factory=lambda: Analyzer())

    
 
def read_metadata(dir: str) -> Metadata:
    """
    Read metadata for given run from acquisition.cfg file.

    Args:
        dir: Path to run directory.

    Returns:
        Metadata object containing all info from acquisition.cfg file.
    """
    # create empty metadata object
    metadata = Metadata()

    # read acquisition.cfg file
    with open(f'{dir}/acquisition.cfg') as f:
        cur_section = None
        while line := f.readline():
            # strip line of linebreaks
            line = line.rstrip()
            # set current section
            if line.startswith('['):
                cur_section = line[1:-1]
            else:             
                # retrieve parameter name and value
                par_name, value = line.split('=')         
                # set current dataclass depending on section
                cur_dataclass = None                          
                match cur_section:
                    case 'general':
                        cur_dataclass = metadata.general
                    case 'lensmode':
                        cur_dataclass = metadata.lensmode
                    case 'detector':
                        cur_dataclass = metadata.detector
                    case 'analyzer':
                        cur_dataclass = metadata.analyzer
                    case _:
                        print('Value either has no section or an unknown section. Skipping value.')
                        continue
                # set attribute in current dataclass
                setattr(cur_dataclass, par_name, parse_type(cur_dataclass, par_name, value))

    return metadata
        
def parse_type(dclass: 'dataclass', par_name: str, value: any) -> any:
    """
    Parse string read from file to given type. Possible non-trivial conversions are int, float, datetime, list.

    Args:
        dclass: Dataclass containing the given parameter.
        par_name: Name of parameter.
        value: Value to be set for parameter.

    Returns:
        Parsed parameter.
    """
    data_type = type(getattr(dclass, par_name)).__name__
    match data_type:
        case 'str':
            return value
        case 'int':
            return int(value)
        case 'float':
            return float(value)
        case 'datetime':
            return datetime.strptime(value, datetime_format)
        case 'ndarray':
            data = np.array(list(map(float, value.strip('[]').split(' '))))
            if par_name in ['energyMatrix', 'thetaMatrix']: # reorganize theta and enregy matrices from 1D list to 2D list
                data = np.reshape(data, (-1, dclass.vectorSize))
            elif par_name in ['transformXMatrix', 'transformYMatrix']: # reorganize transformation matrices from 1D list to 2D list
                data = np.reshape(data, (-1, dclass.transformVectorSize))
            return data
        case _:
            print(f'Did not find data type {data_type} for {par_name}, saving it as string.')
            return value
        
def get_metadata_df(metadata: Metadata, pars: list, run_name: str = None) -> pd.DataFrame:
    """
    Get selected keys from metadata as pandas DataFrame.

    Args:
        metadata: Metadata object containing all metadata.
        pars: List of keys to be extracted from metadata (when 'None' all metadata will be returned)
        run_name: Name of current run to be displayed in first column, optional.

    Returns:
        DataFrame containing all requested metadata.
    """
    # create dict from metadata object (and for all its sub-objects (2 levels))
    metadata_dict =  metadata.__dict__.copy()
    for key in metadata_dict.keys():
        metadata_dict[key] = metadata_dict[key].__dict__

    # create empty DataFrame
    df = pd.DataFrame()    
    # add run name if given
    if run_name is not None:
        df['run'] = [run_name]

    # extract selected keys from metadata
    if pars is None: # add all items
        for key, sub_dict in metadata_dict.items():
            for sub_key, value in sub_dict.items():
                df[f'{key}.{sub_key}'] = [value]
    else:
        for par in pars:
            key, sub_key = par.split('.')
            try:
                df[par] = [metadata_dict[key][sub_key]]
            except KeyError:
                print(f'Key {par} not found in metadata. Skipping it.')

    return df
    

def load_file(path: str, iter: int, step: int) -> np.ndarray:
    """
    Load raw data from file and transform into data points with 3 values.

    Args:
        path: Path to run directory.
        iter: Current lens iteration.
        step: Current lens step.

    Returns:
        2D list containing three int32 values per row.
    """
    filepath = f'{path}/{iter}_{step}'
    raw_data = np.fromfile(filepath, dtype=np.int32)        
    # reshape long array into 2D array with 3 values per entry
    return np.reshape(raw_data, (-1, 3))