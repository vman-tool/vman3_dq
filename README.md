# VMan3 Data Quality Toolkit

A Python package for processing and quality checking VMan3 data.

## Features
Automatically marks skipped questions based on relevance expression
Handles complex ODK relevance expressions
Case-insensitive variable matching
Detailed debugging output

## Installation

```bash
pip install vman3-dq
```

## Usage

```bash
import pandas as pd
from vman3_dq import change_null_toskipped

# Load your data
data_df = pd.read_csv('va_data.csv')
dict_df = pd.read_csv('dictionary.csv')

# Process the data
processed_data = change_null_toskipped(data_df, dict_df, verbose=True)
