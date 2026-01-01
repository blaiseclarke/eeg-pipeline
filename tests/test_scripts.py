#!/usr/bin/env python3
from bin.convert_to_fif import standardize_channel_names
from bin.utils import EVENT_ID_MAP


def test_channel_name_standardization():
    """
    Tests if channel names with periods are correctly cleaned.
    """
    test_names = ['EEG Fp1.', 'EEG Fp2', 'Another.Name.']
    expected_mapping = {'EEG Fp1.': 'EEG Fp1', 'EEG Fp2': 'EEG Fp2', 'Another.Name.': 'AnotherName'}

    result = standardize_channel_names(test_names)

    assert result == expected_mapping


def test_event_id_map():
    """
    Tests if the shared event ID map is correct.
    """
    assert EVENT_ID_MAP == {"T0": 0, "T1": 1, "T2": 2}