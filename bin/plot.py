#!/usr/bin/env python3
import argparse
import mne
import matplotlib.pyplot as plt
import numpy as np
try:
    import utils
except ImportError:
    from bin import utils


def generate_psd_plot(input_path: str, output_path: str, pick: str):
    print(f"Loading epochs from {input_path}...")
    epochs = mne.read_epochs(input_path, verbose=False)

    epochs.event_id = utils.EVENT_ID_MAP

    # Plotting logic
    fig, ax = plt.subplots()
    plot_generated = False
    freqs = None

    # Check for and plot resting state (T0)
    if "T0" in epochs.event_id:
        print("Found T0 event. Plotting resting state...")
        psd_rest = epochs["T0"].compute_psd(fmin=1.0, fmax=40.0)
        rest_psd_data, freqs = psd_rest.get_data(picks=[pick], return_freqs=True)
        avg_rest_psd = 10 * np.log10(rest_psd_data.mean(axis=0).squeeze())
        ax.plot(
            freqs,
            avg_rest_psd,
            color="green",
            linestyle="--",
            alpha=0.7,
            label="Rest (T0)",
        )
        plot_generated = True

    # Check for and plot left fist (T1)
    if "T1" in epochs.event_id:
        print("Found T1 event. Plotting left fist...")
        psd_left = epochs["T1"].compute_psd(fmin=1.0, fmax=40.0)
        left_psd_data, freqs_t1 = psd_left.get_data(picks=[pick], return_freqs=True)
        if freqs is None:
            freqs = freqs_t1  # Set freqs if not already set
        avg_left_psd = 10 * np.log10(left_psd_data.mean(axis=0).squeeze())
        ax.plot(freqs, avg_left_psd, color="blue", alpha=0.8, label="Left Fist (T1)")
        plot_generated = True

    # Check for and plot right fist (T2)
    if "T2" in epochs.event_id:
        print("Found T2 event. Plotting right fist...")
        psd_right = epochs["T2"].compute_psd(fmin=1.0, fmax=40.0)
        right_psd_data, freqs_t2 = psd_right.get_data(picks=[pick], return_freqs=True)
        if freqs is None:
            freqs = freqs_t2  # Set freqs if not already set
        avg_right_psd = 10 * np.log10(right_psd_data.mean(axis=0).squeeze())
        ax.plot(freqs, avg_right_psd, color="red", alpha=0.8, label="Right Fist (T2)")
        plot_generated = True

    # Finalize and save plot
    if plot_generated:
        ax.set_title(f"PSD Analysis at Channel {pick}")
        ax.set_xlabel("Frequency (Hz)")
        ax.set_ylabel("Power Spectral Density (dB)")
        ax.grid(True, alpha=0.3)
        ax.legend()
        print(f"Saving plot to {output_path}...")
        plt.savefig(output_path)
        print("Plot generation complete.")
    else:
        print(f"No T0, T1, or T2 events found for plotting in {input_path}. Skipping.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, required=True)
    parser.add_argument("--output", type=str, required=True)
    parser.add_argument("--pick", type=str, default="C3")
    args = parser.parse_args()
    generate_psd_plot(args.input, args.output, pick=args.pick)
