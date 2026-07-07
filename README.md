# VMan3 Data Processing Toolkit

A Python package for processing and quality checking VA data.

## Features
- Automatically marks skipped questions based on relevance expressions
- Comprehensive data cleaning pipeline
- Handles complex ODK relevance expressions
- Case-insensitive variable matching
- Detailed debugging output

## Installation

```bash
pip install vman3
```

## Usage

```bash
import vman3 as vman
import pandas as pd

# Load your data
data_df = pd.read_csv('va_data.csv')
dict_df = pd.read_csv('dictionary.csv')

# Basic cleaning
processed_data = vman.change_null_toskipped(data_df, dict_df, verbose=True)


