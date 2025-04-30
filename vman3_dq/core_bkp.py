import re
import pandas as pd
import argparse
import chardet
import numpy as np
from typing import Tuple, Dict

import os
from importlib.resources import files, as_file
from typing import Optional
def parse_odk_relevance_to_mask(data_df: pd.DataFrame, relevance_expr: str, verbose: bool = False) -> pd.Series:
    # Ensure we're working with a clean copy of the DataFrame
    eval_df = data_df.copy()
    
    # Convert all columns to string type for safer evaluation
    for col in eval_df.columns:
        if pd.api.types.is_object_dtype(eval_df[col]):
            eval_df[col] = eval_df[col].astype(str)
    
    col_case_mapping = {col.lower(): col for col in eval_df.columns}
    expr = str(relevance_expr).strip()
    
    # Normalize whitespace
    expr = ' '.join(expr.split())

    # Handle selected()
    def convert_selected(match):
        var = match.group(1).strip().lower()
        value = match.group(2).strip()
        actual_col = col_case_mapping.get(var, 'False')
        return f"({actual_col} == '{value}')"  # Always treat as string comparison
    
    expr = re.sub(r"selected\(\s*\$\{?([^}]+)\}?\s*,\s*'([^']+)'\s*\)", convert_selected, expr, flags=re.IGNORECASE)

    # Replace variables
    def replace_var(match):
        var = match.group(1).lower()
        return col_case_mapping.get(var, 'False')
    
    expr = re.sub(r'\$\{(\w+)\}', replace_var, expr)

    # Fix operators
    expr = re.sub(r'>\s*==', '>=', expr)
    expr = re.sub(r'!\s*==', '!=', expr)
    expr = re.sub(r'(?<!=)=(?!=)', '==', expr)
    expr = re.sub(r'(?>!=)=(?!=)', '==', expr)
    expr = (expr
            .replace(" and ", " & ")
            .replace(" or ", " | ")
            .replace("not(", "~(")
            .replace("! =", " != ")
            .replace(">==", " >= ")
            .replace("<==", " <= ")
            )

    # Handle string-length()
    expr = re.sub(r'string-length\(\s*([^)]+)\s*\)\s*==\s*0', r'(\1 == "")', expr)
    expr = re.sub(r'string-length\(\s*([^)]+)\s*\)\s*>=\s*1', r'(\1 != "")', expr)

    # Validate parentheses
    if expr.count("(") != expr.count(")"):
        return pd.Series(False, index=eval_df.index)

    try:
        # Use locals() to ensure all columns are available in evaluation context
        return eval_df.eval(expr, engine='python', local_dict={col: eval_df[col] for col in eval_df.columns})
    except Exception as e:
        print(f"Error evaluating expression: {expr}\nError: {str(e)}")
        return pd.Series(False, index=eval_df.index)

def change_null_toskipped(
        data_df: pd.DataFrame, 
        dictionary_df: Optional[pd.DataFrame] = None, 
        verbose: bool = False
) -> pd.DataFrame:
    """
    Populates NaN/NULL with 'skipped' in variables that were conditionally not shown.

    Parameters:
    - data_df: DataFrame containing the raw VA data
    - dictionary_df: DataFrame containing the xForm-style dictionary
    - verbose: Print debugging info if True

    Returns:
    - Updated DataFrame with 'skipped' in hidden-but-null fields
    """

    # drop all colums with sufix _check. These do not provide any relevant informaton
    data_df = data_df.drop(columns=[col for col in data_df.columns if "_check" in col])

    # Load default dictionary if none provided
    if dictionary_df is None:
        try:
            # Using importlib.resources for modern Python package resource handling
            from importlib.resources import files, as_file
            ref = files('vman3_dq.data').joinpath('dictionary.csv')
            with as_file(ref) as dict_path:
                dictionary_df = pd.read_csv(dict_path)
                if verbose:
                    print("Loaded default dictionary from package data")
        except Exception as e:
            raise ValueError("Could not load default dictionary from package") from e
        
    # if verbose:
    #     print("\n[DEBUG check_input] Processing Start")
    #     print(f"[DEBUG check_input] List of variables: {list(data_df.columns)}")

    # Create case mapping for DataFrame columns
    col_case_mapping = {col.lower(): col for col in data_df.columns}
    
    # Clean column names in dictionary
    #dictionary_df['name'] = dictionary_df['name'].astype(str).str.strip()
    dictionary_df['name'] = dictionary_df['name'].str.lower().str.strip()
    
    # Only apply logic to select_one/text questions with a relevance rule
    target_vars = dictionary_df[
        dictionary_df['type'].str.contains('select_one|text', na=False) &
        dictionary_df['relevant'].notna()
    ][['name', 'relevant']]
    
    for _, row in target_vars.iterrows():
        dict_var_name = row['name'].strip()
        relevance = str(row['relevant']).strip()
        
        # Find matching column (case-insensitive)
        df_var_name = col_case_mapping.get(dict_var_name.lower())
        
        # if verbose:
        #     print(f"[DEBUG] Processing Variable: {dict_var_name}")
            
        if df_var_name is None:
            if verbose:
                print(f"Skipping {dict_var_name}: not found in dataset.")
            continue
        
        try:
            # Get the mask for when the question should be shown
            should_show = parse_odk_relevance_to_mask(data_df, relevance, verbose=verbose)
        
            # if verbose and isinstance(should_show, pd.Series):
            #     print(f"[DEBUG] Number of rows to be updated:\n{should_show.value_counts()}")
            
            if isinstance(should_show, pd.Series):
                # Mark as 'skipped' when:
                # 1. The question should NOT be shown (not should_show)
                # 2. The value is currently null/NA
                mask = (~should_show) & (
                    data_df[df_var_name].isna() | 
                    (data_df[df_var_name].astype(str).str.strip().str.upper().isin(["NULL", "NA", ""]))
                )
                data_df.loc[mask, df_var_name] = 'skipped'
                # if verbose:
                #     print(f"[DEBUG] Processed {dict_var_name} (matched to {df_var_name}): set {mask.sum()} values to 'skipped'")
        except Exception as e:
            if verbose:
                print(f"Error processing '{dict_var_name}' with relevance '{relevance}': {str(e)}")
    
    # Update ageInYears with ageInYears2 if ageInYears is NULL
    # Reduce the number of NUll in the ageInYears column
    # if verbose:
    #     print("\nUpdating ageInYears column")
    #     print(data_df.columns)

    # Create case-insensitive column name mapping
    col_case_mapping = {col.lower(): col for col in data_df.columns}

    # Get the actual column names with case preserved
    age_col = col_case_mapping.get('ageinyears')
    age_col2 = col_case_mapping.get('ageinyears2')
    neonatal_col = col_case_mapping.get('isneonatal')
    age_adult_col = col_case_mapping.get('age_adult')  # Note: underscore remains important

    if age_col and age_col2 in data_df.columns:
        data_df[age_col] = data_df[age_col].fillna(data_df[age_col2])
        if verbose:
            print(f"Updated {age_col} with values from {age_col2}")

    if age_col and neonatal_col in data_df.columns:
        data_df.loc[data_df[age_col].isna() & (data_df[neonatal_col] == 1), age_col] = 0
        if verbose:
            print(f"Set {age_col} to 0 for neonatal cases")

    if age_col and age_adult_col in data_df.columns:
        data_df[age_col] = data_df[age_col].fillna(
            data_df[age_adult_col].where(
                (data_df[age_adult_col].notna()) & 
                (data_df[age_adult_col] != 999) & 
                (data_df[age_adult_col] <= 120)
            )
        )
        if verbose:
            print(f"Updated {age_col} adults if NULL with valid values from {age_adult_col}")

    if verbose:
        print("\n[DEBUG check_input] Processing Complete")

    return data_df

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, required=True, help="Path to input CSV")
    parser.add_argument("--verbose", type=bool, required=False, help="Print output to terminal")
    args = parser.parse_args()
    
    with open(args.input, 'rb') as file:
        result = chardet.detect(file.read())
        encoding = result['encoding']

    # Read file with detected encoding
    print("\n Reading the input file")
    df = pd.read_csv(args.input,encoding = encoding,low_memory = False)
    #change_null_toskipped(df)
    change_null_toskipped(df, verbose=args.verbose)