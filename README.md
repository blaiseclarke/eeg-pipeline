# Automated EEG Power Spectral Density Pipeline

## Description

This project implements an automated, multi-stage pipeline to process raw EEG data from the [EEG Motor Movement/Imagery Dataset](https://physionet.org/content/eegmmidb/1.0.0/). The pipeline converts `.edf` files, filters the data, creates epochs based on event annotations (T0, T1, T2), calculates the Power Spectral Density (PSD), then generates summary plots and an HTML report. The entire pipeline is run using Nextflow and containerized with Docker.

## Key Features

* **Automated processing:** Handles multiple `.edf` files automatically.
* **Standard EEG workflow:** Includes filtering and epoching steps using the MNE-Python library.
* **Conditional PSD plotting:** Generates plots showing PSD for resting state (T0) and/or comparison plots for motor tasks (T1 vs. T2), depending on the events present in each file.
* **Channel selection:** Allows the user to choose the EEG channel for PSD analysis via a command-line parameter.
* **Reproducible environment:** Uses Docker to package the pipeline, Python environment, Nextflow, and all dependencies.
* **Workflow:** Uses Nextflow for execution and management of the multi-step process.
* **HTML report:** Generates an HTML file summarizing the run and visualizing all PSD plots for easy viewing.
* **Unit tested:** Includes unit tests using `pytest` to verify core code components.

## Tech Stack

* **Workflow:** Nextflow
* **Containerization:** Docker
* **Language:** Python 3.12.5
* **Core libraries:** MNE-Python, Matplotlib, NumPy
* **Testing:** Pytest

## Setup

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/blaiseclarke/eeg-pipeline.git](https://github.com/blaiseclarke/eeg-pipeline.git)
    cd eeg-pipeline
    ```

2.  **Build the Docker image:** Ensure you have Docker Desktop installed and running.
    ```bash
    docker build -t eeg-pipeline .
    ```

## Usage

1.  **Prepare input data:** Place your raw `.edf` files inside the `data/` directory within the project folder.
2.  **Create output directory:** Ensure an empty directory named `results/` exists in the project folder.
3.  **Run the pipeline:** Execute the following command from your project's root directory in your terminal:

    ```bash
    docker run \
      -v "$(pwd)/data:/app/data" \
      -v "$(pwd)/results:/app/results" \
      eeg-pipeline --input_dir /app/data --output_dir /app/results
    ```

    * This command mounts your local `data` folder to `/app/data` inside the container and your local `results` folder to `/app/results`.
    * The pipeline reads `.edf` files from `/app/data` and writes all outputs (intermediate `.fif` files, `.png` plots, and `report.html`) to `/app/results`.

4.  **Optional parameters:**
    * To analyze a different channel (ex. C4):
        ```bash
        docker run \
          -v "$(pwd)/data:/app/data" \
          -v "$(pwd)/results:/app/results" \
          eeg-pipeline --input_dir /app/data --output_dir /app/results --pick_channel C4
        ```
    * Other parameters (like `low_freq`, `high_freq`) can be changed in the `nextflow.config` file before building the Docker image.

## Project Structure
eeg-pipeline/
├── bin/ # Python scripts
│ ├── convert_to_fif.py
│ ├── epoch.py
│ ├── filter.py
│ ├── make_report.py
│ └── plot.py
├── data/ # Input EDF files go here
├── results/ # Output files will be saved here
├── tests/ # Pytest unit tests
│ └── test_scripts.py
├── .gitignore
├── Dockerfile
├── main.nf # Nextflow workflow script
├── nextflow.config # Nextflow parameters
├── pytest.ini # Pytest configuration
├── README.md
└── requirements.txt
