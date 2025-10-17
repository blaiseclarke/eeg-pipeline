#!/usr/bin/env python3
import argparse
import mne


def filter_data(input_path: str, output_path: str, low_freq: float, high_freq: float):
    print(f"Loading {input_path}...")
    raw = mne.io.read_raw_fif(input_path, preload=True)

    print(f"Filtering ({low_freq}, {high_freq})...")
    raw.filter(l_freq=low_freq, h_freq=high_freq, fir_design="firwin")

    print(f"Saving filtered data to {output_path}...")
    raw.save(output_path, overwrite=True)
    print(f"Done.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Apply bandpass filter")

    parser.add_argument(
        "--input", type=str, required=True, help="Path to the input FIF file"
    )
    parser.add_argument(
        "--output", type=str, required=True, help="Path to the filtered FIF file"
    )
    parser.add_argument(
        "--low_freq",
        type=float,
        default=1.0,
        required=True,
        help="Lower frequency of the bandpass filter",
    )
    parser.add_argument(
        "--high_freq",
        type=float,
        default=40.0,
        required=True,
        help="Higher frequency of the bandpass filter",
    )

    args = parser.parse_args()

    filter_data(args.input, args.output, args.low_freq, args.high_freq)
