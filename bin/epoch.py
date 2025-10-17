#!/usr/bin/env python3
import mne
import argparse
import sys


def create_epochs(input_path: str, output_path: str):
    print(f"Loading filtered data from {input_path}...")
    raw = mne.io.read_raw_fif(input_path, preload=True, verbose=False)

    print("Extracting all available events (T0, T1, T2)...")
    annotation_map = {"T0": 0, "T1": 1, "T2": 2}

    try:
        events, event_id = mne.events_from_annotations(raw, event_id=annotation_map)
    except ValueError:
        print(f"No valid T0, T1, or T2 annotations found in {input_path}. Skipping.")
        sys.exit(0)

    if events.shape[0] == 0:
        print(
            "Annotations were present, but no T0, T1, or T2 events were found. Skipping."
        )
        sys.exit(0)

    print(f"Found {len(events)} events. Event IDs found: {list(event_id.keys())}")
    print("Building epochs...")
    tmin, tmax = -1.0, 4.0
    epochs = mne.Epochs(
        raw,
        events,
        event_id,
        tmin,
        tmax,
        proj=True,
        baseline=(None, 0),
        preload=True,
        verbose=False,
    )

    if len(epochs) == 0:
        print(
            f"No valid epochs were created from the events found in {input_path}. Skipping file save."
        )
        sys.exit(0)

    print(f"Saving {len(epochs)} epochs to {output_path}...")
    epochs.save(output_path, overwrite=True, verbose=False)
    print("Epoch creation done.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Create epochs for available T0, T1, or T2 events."
    )
    parser.add_argument("--input", type=str, required=True)
    parser.add_argument("--output", type=str, required=True)
    args = parser.parse_args()
    create_epochs(args.input, args.output)
