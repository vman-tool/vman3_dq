import pandas as pd
import vman3 as vman
import csv  # Needed for quoting options
from importlib.resources import files

def test_functions():
    # Sample data
    data_path = files("vman3.data").joinpath("sample_data2.csv")
    data = pd.read_csv(data_path)

    # Test change_null_toskipped
    cleaned_data = vman.change_null_toskipped(data, verbose=True)
    cleaned_data.to_csv(files("vman3.data").joinpath("cleaned_data.csv"),index=False,encoding='utf-8',quoting=csv.QUOTE_NONNUMERIC)

    # Print summary of changes
    print(f"Input data dimensions: {data.shape[0]} rows × {data.shape[1]} columns")
    print(f"Output data dimensions: {cleaned_data.shape[0]} rows × {cleaned_data.shape[1]} columns")
    print(f"Number of NULLs before cleaning: {data.isna().sum().sum():,}")
    print(f"Number of NULLs after cleaning: {cleaned_data.isna().sum().sum():,}")
    print(f"Number of columns with 'Skipped': {(cleaned_data == 'skipped').sum().sum():,}")
    
if __name__ == "__main__":
    test_functions()