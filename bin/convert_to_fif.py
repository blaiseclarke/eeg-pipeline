#!/usr/bin/env python3
import mne
import argparse


def standardize_channel_names(ch_names):
    return {name: name.replace(".", "") for name in ch_names}


def convert_edf_to_fif(input_path: str, output_path: str):
    print(f"Reading {input_path}...")
    raw = mne.io.read_raw_edf(input_path, preload=True)

    print("Standardizing channel names...")
    channel_mapping = standardize_channel_names(raw.ch_names)
    raw.rename_channels(channel_mapping)

    print(f"Writing clean FIF file to {output_path}...")
    raw.save(output_path, overwrite=True)

    print("Conversion complete.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--input", type=str, required=True, help="Path to the input EDF file"
    )
    parser.add_argument(
        "--output", type=str, required=True, help="Path to the output FIF file"
    )
    args = parser.parse_args()
    convert_edf_to_fif(args.input, args.output)
