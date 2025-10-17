#!/usr/bin/env python3
from bin.convert_to_fif import standardize_channel_names

def test_channel_name_standardization():
    """
    Tests if channel names with periods are correctly cleaned.
    """
    test_names = ['EEG Fp1.', 'EEG Fp2', 'Another.Name.']
    expected_mapping = {'EEG Fp1.': 'EEG Fp1', 'EEG Fp2': 'EEG Fp2', 'Another.Name.': 'AnotherName'}

    result = standardize_channel_names(test_names)

    assert result == expected_mapping