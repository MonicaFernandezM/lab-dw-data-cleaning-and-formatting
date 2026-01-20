#data_cleaning.py

import pandas as pd

# -------------------------
# Function to load data
# -------------------------
def load_data(file_path: str) -> pd.DataFrame:
    """
    Load CSV file into a DataFrame.
    """
    df = pd.read_csv(file_path)
    return df


# -------------------------
# Function to standardize column names
# -------------------------
def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize column names: lowercase, replace spaces with '_', 'st' -> 'state'.
    """
    df.columns = (
        df.columns.str.lower()
        .str.replace(' ', '_')
        .str.replace('st', 'state')
    )
    return df


# -------------------------
# Function to clean categorical values
# -------------------------
def clean_categorical(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize gender, education, state, vehicle_class, and customer_lifetime_value.
    """
    # Gender
    df['gender'] = df['gender'].replace({
        'Female': 'F', 'female': 'F', 'Femal': 'F',
        'Male': 'M', 'male': 'M', 'M': 'M'
    })
    
    # Education
    df['education'] = df['education'].replace({'Bachelors': 'Bachelor'})
    
    # State
    df['state'] = df['state'].replace({'AZ': 'Arizona', 'Cali': 'California', 'WA': 'Washington'})
    
    # Vehicle class
    df['vehicle_class'] = df['vehicle_class'].replace({
        'Sports Car': 'Luxury', 'Luxury SUV': 'Luxury', 'Luxury Car': 'Luxury'
    })
    
    # Remove % from customer lifetime value and convert to float
    if 'customer_lifetime_value' in df.columns:
        df['customer_lifetime_value'] = (
            df['customer_lifetime_value'].astype(str).str.replace('%', '')
        ).astype(float)
    
    return df


# -------------------------
# Function to handle numeric columns and nans
# -------------------------
def fill_numeric_nans(df: pd.DataFrame, numeric_columns: list) -> pd.DataFrame:
    """
    Fill numeric NaNs with the median of the column.
    """
    for col in numeric_columns:
        if col in df.columns:
            median_value = df[col].median()
            df[col] = df[col].fillna(median_value)
    return df


# -------------------------
# Function to clean duplicates
# -------------------------
def remove_duplicates(df: pd.DataFrame, subset_columns: list = None) -> pd.DataFrame:
    """
    Remove duplicate rows. Optionally, specify a subset of columns to consider.
    """
    df = df.drop_duplicates(subset=subset_columns, keep='first')
    df = df.reset_index(drop=True)
    return df


# -------------------------
# Main cleaning function
# -------------------------
def main(file_path: str) -> pd.DataFrame:
    """
    Load and clean the dataset.
    """
    df = load_data(file_path)
    df = clean_column_names(df)
    df = clean_categorical(df)
    
    # Fill numeric nans
    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    df = fill_numeric_nans(df, numeric_cols)
    
    # Remove duplicates
    df = remove_duplicates(df)
    
    return df


# Example usage (uncomment to test inside this file):
# if __name__ == '__main__':
#     cleaned_df = main("customer_data.csv")
#     print(cleaned_df.head())

'''
# Enable autoreload to automatically reload changes in data_cleaning.py
%load_ext autoreload
%autoreload 2

# Import the module
import data_cleaning as dc

# Run the main cleaning function
file_path = "customer_data.csv"
df_clean = dc.main(file_path)

# Check result
df_clean.head()
'''