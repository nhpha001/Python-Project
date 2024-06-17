import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

def load_clean_data():
    # 1. Load data
    directory_path = "/Users/mia/Desktop/Minh/Electives/Basic in Python/Project_Dataset"

    # Use "glob" to get all ".csv" files in the directory
    all_csv_files = glob.glob(os.path.join(directory_path, "*.csv"))
    """os.path.join() joins the directory path with the file extension *.csv
        glob.glob() returns a list of all .csv files in the directory"""

    # Load all ".csv" files into a list of "DataFrames"
    dfs = [pd.read_csv(file, skiprows=1) for file in all_csv_files]
    """pd.read_csv() reads the .csv file into a DataFrame
        skiprows=1 skips the first row of the .csv file"""

    # 2. Clean data
    # Remove missing values and duplicates from each "DataFrame" in the list
# (?)   cleaned_dfs = [df.dropna().drop_duplicates() for df in dfs]
    """dropna() removes rows with missing values
        drop_duplicates() removes duplicate rows in each DataFrame"""
    
    # Concatenate all "DataFrames" in the list into a single "DataFrame"
# (?)   df = pd.concat(cleaned_dfs, ignore_index=True)
    df = pd.concat(dfs, ignore_index=True)

    # Save the concatenated "DataFrame" to a new ".csv" file
    df.to_csv("concatenated_data.csv", index=False)
    """to_csv() saves the DataFrame to a new .csv file
        index=False prevents the DataFrame index from being saved to the file"""
    
    return df

def filter_data_by_date(df):
    date = input("Please specify the date you want to filter (DD/MM/YYYY), e.g. 01/07/2023:\n")
    return df[df["Date"] == date]

def plot_demand_supply(df):
    hour = 1
    sell = "Sell"
    purchase = "Purchase"
    supply = df[(df["Sale/Purchase"] == sell) & (df["Hour"] == hour)]
    demand = df[(df["Sale/Purchase"] == purchase) & (df["Hour"] == hour)]

    plt.figure(figsize=(10, 6))
    for row in range(1, 5):
        for colume in range(1, 7):
            plt.subplot(4, 6, hour)
            plt.plot(supply["Volume"], supply["Price"], label="Supply Curve", color="red")
            plt.plot(demand["Volume"], demand["Price"], label="Demand Curve", color="blue")
            plt.grid(True)
            plt.title(f"Hour {hour}")
            hour += 1
    plt.suptitle("Aggregated Supply and Demand Curves", fontweight="bold")
    plt.xlabel("Volume (MWh)", loc = "center")
    plt.ylabel("Price ($/MWh)", loc = "center")
    plt.legend(loc = "upper right")
    plt.show()

def plot_initial_altered_supply(initial_df, altered_df):
    hour = 1
    sell = "Sell"
    initial_supply = initial_df[(initial_df["Sale/Purchase"] == sell) & (initial_df["Hour"] == hour)]
    altered_supply = altered_df[(altered_df["Sale/Purchase"] == sell) & (altered_df["Hour"] == hour)]

    plt.figure(figsize=(10, 6))
    plt.plot(initial_supply["Volume"], initial_supply["Price"], label="Initial Supply Curve", color="red")
    plt.plot(altered_supply["Volume"], altered_supply["Price"], label="Altered Supply Curve", color="blue")
    plt.grid(True)
    plt.title(f"Initial and Altered Supply Curves")
    plt.xlabel("Volume (MWh)", loc = "center")
    plt.ylabel("Price ($/MWh)", loc = "center")
    plt.legend(loc = "upper right")
    plt.show()
    

def adjust_price(df):
    lower = float(input("Please specify the lower price limit, e.g. 10000:\n"))
    upper = float(input("Please specify the upper price limit, e.g. 10000:\n"))
    add_supply_percent = float(input("Please specify the percent of energy should be added to the supply, e.g. 10:\n"))

    # Filter data by price range and "Sell"
    sell = "Sell"
    filtered_price_df = df[(df["Price"] >= lower) & (df["Price"] <= upper) & (df["Sale/Purchase"] == sell)].copy()

    # Adjust supply
    filtered_price_df["Volume"] *= (1 + add_supply_percent / 100)

    return print(filtered_price_df)


def main():
    # Check if the concatenated data file already exists
    if os.path.isfile("concatenated_data.csv"):
        df = pd.read_csv("concatenated_data.csv")
    else:
        df = load_clean_data()
    print(df.head())

    # Filter data by date
    filtered_date_df = filter_data_by_date(df)

    # Plot supply and demand curve
#    plot_demand_supply(filtered_date_df)

    # Adjust price
    adjusted_price_df = adjust_price(filtered_date_df)

    # Plot initial and altered supply curve
    plot_initial_altered_supply(filtered_date_df, adjusted_price_df)

if __name__ == "__main__":
    main()