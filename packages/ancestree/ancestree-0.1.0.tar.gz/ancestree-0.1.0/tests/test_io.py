"""
Tests for the IO module
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import tempfile
import os

from gwas_toolkit.io import load_data, save_data


def test_load_data_csv():
    """Test loading data from a CSV file"""
    # Create a temporary CSV file
    with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as tmp:
        # Write some test data
        test_data = pd.DataFrame({
            'CHR': [1, 1, 2, 2, 3],
            'POS': [100, 200, 300, 400, 500],
            'SNP': ['rs1', 'rs2', 'rs3', 'rs4', 'rs5'],
            'A1': ['A', 'C', 'G', 'T', 'A'],
            'A2': ['G', 'T', 'C', 'A', 'G'],
            'MAF': [0.1, 0.2, 0.3, 0.4, 0.5],
            'P': [0.001, 0.01, 0.05, 0.5, 0.9]
        })
        test_data.to_csv(tmp.name, index=False)
        tmp_path = tmp.name
    
    try:
        # Load the data
        loaded_data = load_data(tmp_path)
        
        # Check that the data was loaded correctly
        assert isinstance(loaded_data, pd.DataFrame)
        assert loaded_data.shape == test_data.shape
        assert list(loaded_data.columns) == list(test_data.columns)
        assert loaded_data['SNP'].tolist() == test_data['SNP'].tolist()
    finally:
        # Clean up
        os.remove(tmp_path)


def test_save_and_load_data():
    """Test saving and loading data"""
    # Create test data
    test_data = pd.DataFrame({
        'CHR': [1, 1, 2, 2, 3],
        'POS': [100, 200, 300, 400, 500],
        'SNP': ['rs1', 'rs2', 'rs3', 'rs4', 'rs5'],
        'A1': ['A', 'C', 'G', 'T', 'A'],
        'A2': ['G', 'T', 'C', 'A', 'G'],
        'MAF': [0.1, 0.2, 0.3, 0.4, 0.5],
        'P': [0.001, 0.01, 0.05, 0.5, 0.9]
    })
    
    # Save to a temporary file
    with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as tmp:
        tmp_path = tmp.name
    
    try:
        # Save the data
        save_data(test_data, tmp_path, delimiter='\t')
        
        # Load the data back
        loaded_data = load_data(tmp_path)
        
        # Check that the data was loaded correctly
        assert isinstance(loaded_data, pd.DataFrame)
        assert loaded_data.shape == test_data.shape
        assert list(loaded_data.columns) == list(test_data.columns)
        assert loaded_data['SNP'].tolist() == test_data['SNP'].tolist()
    finally:
        # Clean up
        os.remove(tmp_path)


def test_format_inference():
    """Test format inference from file extension"""
    # Create test data
    test_data = pd.DataFrame({
        'CHR': [1, 2, 3],
        'POS': [100, 200, 300],
        'SNP': ['rs1', 'rs2', 'rs3'],
        'P': [0.001, 0.01, 0.05]
    })
    
    # Test different file extensions
    extensions = ['.csv', '.txt', '.tsv']
    
    for ext in extensions:
        with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            # Save the data
            if ext == '.csv':
                test_data.to_csv(tmp_path, index=False)
            else:
                test_data.to_csv(tmp_path, sep='\t', index=False)
            
            # Load the data back
            loaded_data = load_data(tmp_path)
            
            # Check that the data was loaded correctly
            assert isinstance(loaded_data, pd.DataFrame)
            assert loaded_data.shape == test_data.shape
            assert loaded_data['SNP'].tolist() == test_data['SNP'].tolist()
        finally:
            # Clean up
            os.remove(tmp_path) 