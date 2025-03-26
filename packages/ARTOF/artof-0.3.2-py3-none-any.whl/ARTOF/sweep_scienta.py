# calculation of sweet parameters based on the code of VG Scienta. This is querky and should be replaced in acquisition script by proper implementation (see sweep.py)
from .data_read import Metadata
import math

def get_sweep_parameters(spectrum_begin_energy: float, spectrum_end_energy: float, step_size: float, lens_k: float):
    """
    Extract sweep parameters (sweep start and end energy, channel width, steps number) based on implementation of VG Scienta.

    Args:
        spectrum_begin_energy: Begin energy of the spectrum.
        spectrum_end_energy: End energy of the spectrum.
        step_size: Width of the channel.
        lens_k: Lens configuration indicating the energy window width per measurement.

    Returns:
        4 sweep parameters (sweep start energy, sweep end energy, channel width, steps number).

    """
    # calculate adjusted channel width
    adjusted_channel_width = step_size / (1- lens_k/2)

    # calculate lower edge of first measurement (equals sweep start energy)
    spectrum_begin_upper_energy = spectrum_begin_energy / (1- lens_k/2) # caclulate upper edge of first measurement    
    lower_edge_e = (1 - lens_k) * spectrum_begin_upper_energy # calculate lower edge of first measurement
    channel_count = math.floor((spectrum_begin_upper_energy - lower_edge_e) / adjusted_channel_width) # calculate number of channels
    rest_e  = spectrum_begin_upper_energy - lower_edge_e - channel_count * adjusted_channel_width # calculate rest energy not convered by a full channel
    lower_edge_e += + rest_e - 1.5 * adjusted_channel_width # calculate new lower edge assuring each energy is hit by entire channel
    # continuesly increase lower edge until upper edge is below spectrum begin
    upper_edge_e = (lower_edge_e / (1 - lens_k/2)) * (1+ lens_k/2)
    while upper_edge_e <= spectrum_begin_upper_energy:
        lower_edge_e += adjusted_channel_width
        upper_edge_e = (lower_edge_e / (1 - lens_k/2)) * (1+ lens_k/2)
        noOfChannels = math.floor((upper_edge_e - lower_edge_e) / adjusted_channel_width)
        upper_edge_e = lower_edge_e + noOfChannels * adjusted_channel_width
    sweep_start_energy = lower_edge_e

    # calculate upper sweep end energy
    sweep_end_energy = spectrum_end_energy/(1 - lens_k/2)

    # calculate number of steps
    sweep_steps = math.floor((sweep_end_energy - sweep_start_energy) / adjusted_channel_width) + 1

    return sweep_start_energy, sweep_end_energy, adjusted_channel_width, sweep_steps, lens_k
    