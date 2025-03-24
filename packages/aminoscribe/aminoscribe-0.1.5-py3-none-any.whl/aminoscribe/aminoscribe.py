import pandas as pd
import random
import numpy as np
import pickle
import scipy.signal as scipy_signal
from scipy.interpolate import interp1d
from Bio import SeqIO
import importlib
import aminoscribe.generate_template as generate_template

FREQ = 3012

_step_sizes_df = None
_step_durations_df = None
_amplitude_noise_df = None
_human_proteome_dict = None


def load_data():
    global _step_sizes_df, _step_durations_df, _amplitude_noise_df, _human_proteome_dict

    data_dir = importlib.resources.files("aminoscribe.data")

    _step_sizes_df = pd.read_csv(data_dir.joinpath("step_sizes_in_aa.csv"))
    _step_durations_df = pd.read_csv(
        data_dir.joinpath("step_durations_in_ms.csv"))
    _amplitude_noise_df = pd.read_csv(data_dir.joinpath("amplitude_noise.csv"))

    with open(data_dir.joinpath("sequences.pickle"), "rb") as f:
        _human_proteome_dict = pickle.load(f)
            

def _verify_data_loaded():
    if (_step_sizes_df is None or
        _step_durations_df is None or
        _amplitude_noise_df is None or
        _human_proteome_dict is None):
        load_data()


def add_timewarp(template):
    _verify_data_loaded()
    # Choose an array of step sizes from the (weighted) options
    step_sizes = random.choices(
        _step_sizes_df['step_size'],
        weights=_step_sizes_df['count'],
        k=len(template)  # We can take at most len(template) steps
    )

    # Step durations are binned, we use the middle value of each bin
    bin_size = _step_durations_df['bin_end'][0] - \
        _step_durations_df['bin_start'][0]
    options = _step_durations_df['bin_start'] + bin_size / 2
    durations = random.choices(
        options,
        weights=_step_durations_df['count'],
        k=len(template)  # We can take at most len(template) steps
    )

    # Use the step size and duration options that we picked out to build the timewarped squiggle
    i = -1
    timewarped_squiggle = []
    for step_size, step_duration in zip(step_sizes, durations):
        i += int(step_size)
        if i >= len(template):
            break

        # Add this step to the timewarped_squiggle
        # step duration is in ms
        step = [template[i]] * int(step_duration * FREQ / 1000)
        timewarped_squiggle.extend(step)

    return np.array(timewarped_squiggle)


def add_noise(timewarped_template):
    _verify_data_loaded()
    # Noise values are binned, we use the middle value of each bin
    bin_size = _amplitude_noise_df['bin_end'][0] - \
        _amplitude_noise_df['bin_start'][0]
    noise_values = _amplitude_noise_df['bin_start'] + bin_size / 2
    noise = random.choices(
        noise_values,
        weights=_amplitude_noise_df['count'],
        k=len(timewarped_template)
    )
    return timewarped_template + noise


def timewarp_and_noise(template, seed=None):
    _verify_data_loaded()
    random.seed(seed)
    return add_noise(add_timewarp(template))


def get_protein_seq(protein_id):
    _verify_data_loaded()
    # Use UniProt Accession Number as a safe id (without weird characters for filenames)
    protein_id = protein_id.split("|")[1] if "|" in protein_id else protein_id
    return _human_proteome_dict[protein_id]


def gen_template(sequence, cterm, nterm):
    if cterm:
        sequence = sequence + cterm
    if nterm:
        sequence = nterm + sequence
    return generate_template.template_from_sequence(sequence)


def generate_squiggle(sequence: str = None,
                      protein_id: str = None,
                      base_template=None,
                      seed=None,
                      template_only: bool = False,
                      cterm: str = None,
                      nterm: str = None,
                      filter_noise: bool = False,
                      bessel_N: int = 8,
                      bessel_Wn: float = 100/(0.5 * 3012),  # A 100Hz cutoff
                      normalize: bool = False,
                      norm_cutoff: int = None,
                      downsample: bool = False,
                      downsample_factor: float = 10):
    """
    Generates a simulated squiggle signal from an amino acid sequence.

    This function converts an amino acid sequence into a simulated nanopore squiggle. It can optionally apply noise filtering, min-max normalization, and downsampling. 
    The sequence can be provided directly or retrieved using a protein ID.

    Args:
        sequence (str, optional): Amino acid sequence. Required if neither `protein_id` or 'base_template' are provided.
        protein_id (str, optional): Protein ID to fetch the sequence. Ignored if `sequence` is given.
        base_template (optional): Base template (signal) on which to apply time and amplitude domain noise. Ignored if `sequence` of 'protein_id' are given.
        seed (optional): Random seed for reproducibility of the generated squiggle.
        template_only (bool, optional): If True, returns an idealized template for this sequence's nanopore squiggle. There is one datapoint for every reading window (20 amino acids) in the sequence.
        cterm (str, optional): Additional sequence to append to the C-terminal end.
        nterm (str, optional): Additional sequence to prepend to the N-terminal end.
        filter_noise (bool, optional): If True, applies a low-pass Bessel filter to reduce noise.
        bessel_N (int, optional): Order of the Bessel filter. Defaults to 8.
        bessel_Wn (float, optional): Normalized cutoff frequency for the Bessel filter. Defaults to 100Hz at 3012Hz sampling rate.
        normalize (bool, optional): If True, applies min-max normalization to the squiggle signal.
        norm_cutoff (int, optional): Number of initial elements to consider when finding min and max values for normalization. This is done prior to any downsampling.
        downsample (bool, optional): If True, applies linear downsampling to the squiggle signal.
        downsample_factor (float, optional): Factor by which the signal length is reduced. Defaults to 10.

    Returns:
        list: Processed squiggle signal as a list of float values.

    Raises:
        ValueError: If both `sequence` and `protein_id` are missing.

    Example:
        >>> signal = amino_scribe(sequence="MKTLLDLGYTMKTLLLTLVVTMKTLLDLGYTMKTLLLTLVVLLTLVVVTIVCLDLGYTLGYT", normalize=True, downsample=True, downsample_factor=5)
        >>> print(signal[:5])  # First few values of the processed signal
    """
    _verify_data_loaded()

    if sequence:
        template = gen_template(sequence, cterm, nterm)
    elif protein_id:
        sequence = get_protein_seq(protein_id)
        if not sequence:
            raise ValueError("Unable to recognize protein id '{protein_id}'")
        template = gen_template(sequence, cterm, nterm)
    elif base_template is not None:
        template = base_template
    else:
        raise ValueError(
            "Either 'sequence', 'protein_id', or 'base_template' must be provided.")

    if template_only:
        if normalize:
            cutoff = norm_cutoff if norm_cutoff else len(template)
            min_val = min(template[:cutoff])
            max_val = max(template[:cutoff])
            template = [(x - min_val) / (max_val - min_val)
                        for x in template]
        return template
    squiggle = timewarp_and_noise(template, seed)
    if filter_noise:
        b, a = scipy_signal.bessel(bessel_N, bessel_Wn, btype='low')
        squiggle = scipy_signal.filtfilt(b, a, squiggle)
    if normalize:
        cutoff = norm_cutoff if norm_cutoff else len(squiggle)
        min_val = min(squiggle[:cutoff])
        max_val = max(squiggle[:cutoff])
        squiggle = [(x - min_val) / (max_val - min_val)
                    for x in squiggle]
    if downsample:
        x_original = np.linspace(0, len(squiggle), len(squiggle))
        x_new = np.linspace(0, len(squiggle), int(
            len(squiggle)/downsample_factor))
        f_linear = interp1d(x_original, squiggle, kind='linear')
        squiggle = f_linear(x_new)
    return squiggle
