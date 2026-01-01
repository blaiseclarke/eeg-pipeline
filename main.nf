#!/usr/bin/env nextflow

nextflow.enable.dsl = 2

workflow {
    ch_input_edf = Channel.fromPath("${params.input_dir}/*.edf")

    CONVERT_TO_FIF(ch_input_edf)
    FILTER_DATA(CONVERT_TO_FIF.out)
    EPOCH_DATA(FILTER_DATA.out)
    PLOT_PSD(EPOCH_DATA.out)
    MAKE_REPORT(PLOT_PSD.out.collect())
}

// Define processes
process CONVERT_TO_FIF {
    publishDir "${params.output_dir}/converted_fifs", mode: 'copy'

    input:
    path edf_file

    output:
    path "${edf_file.baseName}.fif"

    script:
    """
    convert_to_fif.py --input ${edf_file} --output "${edf_file.baseName}.fif"
    """
}

process FILTER_DATA {
    publishDir "${params.output_dir}/filtered_fifs", mode: 'copy'

    input:
    path raw_fif_file

    output:
    path "${raw_fif_file.baseName}_filtered.fif"

    script:
    """
    filter.py --input ${raw_fif_file} --output "${raw_fif_file.baseName}_filtered.fif" --low_freq ${params.low_freq} --high_freq ${params.high_freq}
    """
}

process EPOCH_DATA {
    publishDir "${params.output_dir}/epoched_fifs", mode: 'copy'

    input:
    path filtered_fif_file

    output:
    path "${filtered_fif_file.baseName}-epo.fif", optional: true

    script:
    """
    epoch.py --input ${filtered_fif_file} --output "${filtered_fif_file.baseName}-epo.fif"
    """
}

process PLOT_PSD {
    publishDir "${params.output_dir}/psd_images", mode: 'copy'

    input:
    path epochs_file

    output:
    path "${epochs_file.baseName}_psd.png", optional: true

    script:
    """
    plot.py --input ${epochs_file} --output "${epochs_file.baseName}_psd.png" --pick ${params.pick_channel}
    """
}

process MAKE_REPORT {
    publishDir params.output_dir, mode: 'copy'

    input:
    path images

    output:
    path "report.html"

    script:
    """
    make_report.py --images ${images.join(' ')} --output report.html
    """
}