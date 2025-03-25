# -*- coding: utf-8-*-

###### MMT IndeX #######
## Version 0.2.0 ##

# Standard library imports
import os
import sys
import time
import re
from itertools import combinations, permutations

# Plotting Libraries
import matplotlib.pyplot as plt

# Data manipulation libraries
import numpy as np
import pandas as pd
from datetime import date

# Statistical Libraries
from scipy.stats import pearsonr, rankdata

# Local application/library specific imports
from causalimpact import CausalImpact
from dtw import *

# Multiprocessing library
import multiprocessing

# Set random seed
np.random.seed(500)

# Progress Bar library
from tqdm import tqdm

# Catch warnings
if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")

##################################
#       MMT class
##################################
class MMT ():

    ########################################
    # constructor
    ########################################
    def __init__ (self) -> None:

        self.work_dir = None
        self.data_dir = None
        self.dma_fName = None
        self.gmm_metric = None
        self.corr_thresh = 0.6
        self.pval_threshold = 0.1
        self.pre_period_start = None
        self.pre_period_end = None
        self.post_period_start = None
        self.post_period_end = None
        self.gmm_rank = 3
        self.gmm_plots = False
        self.initials = None
        self.campaign = None
        self.brand = None
        self.num_processes = 0
        self.parallel_processing = True

        self.df = pd.DataFrame()
        self.data = pd.DataFrame()
        self.data_pairs = pd.DataFrame()
        self.markets_to_be_matched = None
        self.matches = 0
        self.dtw_emphasis = 0
        self.shortest_distances = pd.DataFrame()
        self.pairs = None
        self.results = pd.DataFrame()
        self.df_pairs = pd.DataFrame()

    ########################################
    # read dma file
    ########################################
    def read_data(self, data_dir, dma_fName):
        print("Reading data")
        try:
            df = pd.read_csv(data_dir+"/"+dma_fName).fillna(0)
            return df
        except Exception as e:
            print("Error reading data: ", e)
            return None

    ########################################
    # check_columns_exist
    ########################################
    def check_columns_exist(self, df, required_columns):
        for column in required_columns:
            if column not in df.columns:
                raise ValueError(f"{column} not found in data")

    ########################################
    # check_threshold
    ########################################
    def check_threshold(self, value, variable_name, min_val=0, max_val=1):
        try:
            if not (min_val <= value <= max_val):
                raise ValueError(f"{variable_name} threshold must be between {min_val} and {max_val}")
        except Exception as e:
            print(f"Error checking threshold value {variable_name}: {e}")
            sys.exit(1)

    ########################################
    # check_paths_exist
    ########################################
    def check_paths_exist(self, fPath):
        try:
            if os.path.exists(fPath):
                print(f"{fPath}")
                return True
            else:
                print(f"{fPath} not found...creating directory")
                os.makedirs(fPath)
                return False
        except Exception as e:
            print("Error creating path: ", e)
            sys.exit(1)

    ########################################
    # read_input_parameters
    ########################################
    def read_input_parameters(self, work_dir, dma_fName, gmm_metric):

        try:
            df = self.read_data(work_dir, dma_fName)
            
            required_columns = ['Date', 'DMA']
            required_columns.append(gmm_metric)
            self.check_columns_exist(df, required_columns)
            
            print("Data loaded successfully")

            return df

        except ValueError as e:
            print("Error reading imput parameters: ", e)
            sys.exit(1)

    ########################################
    # read_input_parameters
    ########################################
    def read_test_pairs_file (self, work_dir, file_name):
            ''' Read the csv file '''

            try:
                # read the csv file
                df = pd.read_csv(work_dir+"/"+file_name)

                print("Pair Data loaded successfully")

                return df

            except Exception as e:
                raise e
        

    ########################################
    # check_inputs
    ########################################
    def check_inputs(self, data=None, id=None, matching_variable=None, date_variable=None):
        if data is None:
            raise ValueError("ERROR: No data is provided")
        if id is None:
            raise ValueError("ERROR: No ID is provided")
        if matching_variable is None:
            raise ValueError("ERROR: No matching metric is provided")
        if date_variable is None:
            raise ValueError("ERROR: No date variable is provided")
        if id not in data.columns:
            raise ValueError("ERROR: ID variable not found in input data")
        if date_variable not in data.columns:
            raise ValueError("ERROR: date variable not found in input data")
        if matching_variable not in data.columns:
            raise ValueError("ERROR: matching metric not found in input data")
        if len(data[id].unique()) <= 1:
            raise ValueError("ERROR: Need at least 2 unique markets")
        if data[id].isna().any():
            raise ValueError("ERROR: NAs found in the market column")
        if data[id].isnull().any():
            raise ValueError("ERROR: NULLs found in the market column")
        if '' in data[id].unique():
            raise ValueError("ERROR: Blanks found in the market column")
        if data[matching_variable].isna().any():
            raise ValueError("ERROR: NAs found in the matching variable")
        if not pd.api.types.is_datetime64_any_dtype(data[date_variable]):
            raise ValueError("ERROR: date_variable is not a Date. Check your data frame or use pd.to_datetime().")


    ########################################
    # check_pair_inputs
    ########################################
    def check_pair_inputs(self, data=None):
        if data is None:
            raise ValueError("ERROR: No data is provided")
        if 'Control' not in data.columns:
            raise ValueError("ERROR: Control variable not found in input data")
        if 'Exposed' not in data.columns:
            raise ValueError("ERROR: Exposed variable not found in input data")
        if data['Control'].isna().any():
            raise ValueError("ERROR: NAs found in the Control variable")
        if data['Exposed'].isna().any():
            raise ValueError("ERROR: NAs found in the Exposed variable")
        if data['Control'].isnull().any():
            raise ValueError("ERROR: NULLs found in the Control variable")
        if data['Exposed'].isnull().any():
            raise ValueError("ERROR: NULLs found in the Exposed variable")
        if '' in data['Control'].unique():
            raise ValueError("ERROR: Blanks found in the Control variable")
        if '' in data['Exposed'].unique():
            raise ValueError("ERROR: Blanks found in the Exposed variable")
    


    ########################################
    # process_data program
    ########################################
    def process_data(self, data, id_variable, date_variable, matching_variable, markets_to_be_matched, suggest_market_splits, matches, dtw_emphasis, start_match_period, end_match_period):

        ## Check the start date and end dates
        if start_match_period is None:
            raise ValueError("No start date provided")
        if end_match_period is None:
            raise ValueError("No end date provided")

        # Clean up the emphasis
        if dtw_emphasis is None:
            dtw_emphasis = 0
        elif dtw_emphasis > 1:
            dtw_emphasis = 1
        elif dtw_emphasis < 0:
            dtw_emphasis = 0

        ## check the inputs
        if date_variable not in data.columns:
            raise ValueError("ERROR: date variable not found in input data")

        if len(data[date_variable].dtypes) > 1:
            if "Date" not in data[date_variable].dtypes:
                print("NOTE: Date variable converted to Date using pd.to_datetime()")
                print()
                data[date_variable] = pd.to_datetime(data[date_variable])
        elif data[date_variable].dtype != "datetime64[ns]":
            print("NOTE: Date variable converted to Date using pd.to_datetime()")
            print()
            data[date_variable] = pd.to_datetime(data[date_variable])

        # Trim the date variable
        data[date_variable] = pd.to_datetime(data[date_variable])

        # Check inputs
        self.check_inputs(data=data, id=id_variable, matching_variable=matching_variable, date_variable=date_variable)

        # Create new columns
        data['date_var'] = data[date_variable]
        data['id_var'] = data[id_variable] 
        data['match_var'] = data[matching_variable]

        if markets_to_be_matched is not None and suggest_market_splits:
            print("The suggest_market_splits parameter has been turned off since markets_to_be_matched is not NULL")
            print("Set markets_to_be_matched to NULL if you want optimized pairs")
            print()

        if matches is None:
            if markets_to_be_matched is None and suggest_market_splits:
                matches = len(set(data['id_var']))
            else:
                matches = 5
        else:
            if markets_to_be_matched is None and suggest_market_splits:
                matches = len(set(data['id_var']))
                print("The matches parameter has been overwritten for splitting to conduct a full search for optimized pairs")
                print()

        # check for duplicates
        ddup = data.drop_duplicates(subset=['id_var', 'date_var'])
        if len(ddup) < len(data):
            raise Exception("ERROR: There are date/market duplicates in the input data")
        del ddup

        ## reduce the width of the data.frame
        data = data.sort_values(by=['id_var', 'date_var'])
        data = data[['id_var', 'date_var', 'match_var']]
        data = data.reset_index(drop=True)
        # data.head()

        # Filter rows where date_var is between start_match_period and end_match_period
        data_filtered = data[(data['date_var'] >= start_match_period) & (data['date_var'] <= end_match_period)]
        data_filtered = data_filtered.reset_index(drop=True)

        # Group by id_var and calculate the row number within each group, then get the max row number for each group
        data_filtered['rows'] = data_filtered.groupby('id_var').cumcount()
        data_filtered['max_row'] = data_filtered.groupby('id_var')['rows'].transform('max')

        # Remove the groupby effect
        data_filtered = data_filtered.reset_index(drop=True)

        # Calculate the maximum of 'rows' across the entire DataFrame
        max_rows = data_filtered['rows'].max()

        # Create the 'short' boolean column
        data_filtered['short'] = data_filtered['rows'] < max_rows

        # Select the desired columns (dropping 'rows', 'max_rows', and 'short')
        data = data_filtered.drop(columns=['rows', 'max_row', 'short'])

        # Check if any data is left
        if data.shape[0] == 0:
            raise Exception("ERROR: no data left after filter for dates")

        # Get a vector of all markets that matches are wanted for. Check to ensure markets_to_be_matched exists in the data.
        if markets_to_be_matched is None:
            markets_to_be_matched = data['id_var'].unique()
        else:
            markets_to_be_matched = pd.unique(markets_to_be_matched)
            for k in markets_to_be_matched:
                if k not in data['id_var'].unique():
                    raise Exception(f"test market {k} does not exist")
                
        return data, markets_to_be_matched, matches, dtw_emphasis

    ########################################
    # process_intervention_data program
    ########################################
    def process_intervention_data(self, data, id_variable, date_variable, matching_variable, start_match_period, end_match_period):

        ## Check the start date and end dates
        if start_match_period is None:
            raise ValueError("No start date provided")
        if end_match_period is None:
            raise ValueError("No end date provided")

        ## check the inputs
        if date_variable not in data.columns:
            raise ValueError("ERROR: date variable not found in input data")

        if len(data[date_variable].dtypes) > 1:
            if "Date" not in data[date_variable].dtypes:
                print("NOTE: Date variable converted to Date using pd.to_datetime()")
                print()
                data[date_variable] = pd.to_datetime(data[date_variable])
        elif data[date_variable].dtype != "datetime64[ns]":
            print("NOTE: Date variable converted to Date using pd.to_datetime()")
            print()
            data[date_variable] = pd.to_datetime(data[date_variable])

        # Trim the date variable
        data[date_variable] = pd.to_datetime(data[date_variable])

        # Check inputs
        self.check_inputs(data=data, id=id_variable, matching_variable=matching_variable, date_variable=date_variable)

        # Create new columns
        data['date_var'] = data[date_variable]
        data['id_var'] = data[id_variable] 
        data['match_var'] = data[matching_variable]

        # check for duplicates
        ddup = data.drop_duplicates(subset=['id_var', 'date_var'])
        if len(ddup) < len(data):
            raise Exception("ERROR: There are date/market duplicates in the input data")
        del ddup

        ## reduce the width of the data.frame
        data = data.sort_values(by=['id_var', 'date_var'])
        data = data[['id_var', 'date_var', 'match_var']]
        data = data.reset_index(drop=True)
        # data.head()

        # Filter rows where date_var is between start_match_period and end_match_period
        data_filtered = data[(data['date_var'] >= start_match_period) & (data['date_var'] <= end_match_period)]
        data_filtered = data_filtered.reset_index(drop=True)

        # Group by id_var and calculate the row number within each group, then get the max row number for each group
        data_filtered['rows'] = data_filtered.groupby('id_var').cumcount()
        data_filtered['max_row'] = data_filtered.groupby('id_var')['rows'].transform('max')

        # Remove the groupby effect
        data_filtered = data_filtered.reset_index(drop=True)

        # Calculate the maximum of 'rows' across the entire DataFrame
        max_rows = data_filtered['rows'].max()

        # Create the 'short' boolean column
        data_filtered['short'] = data_filtered['rows'] < max_rows

        # Select the desired columns (dropping 'rows', 'max_rows', and 'short')
        data = data_filtered.drop(columns=['rows', 'max_row', 'short'])

        # Check if any data is left
        if data.shape[0] == 0:
            raise Exception("ERROR: no data left after filter for dates")
                
        return data

    ########################################
    # process_pair_data program
    ########################################
    def process_pair_data(self, data):
        # Check inputs
        self.check_pair_inputs(data=data)
        return data
    
    ########################################
    # create_market_vectors program
    ########################################
    def create_market_vectors(self, data, test_market, ref_markets):
        
        # Select rows for the test market and rename the 'match_var' to 'y'
        test = data.loc[data['id_var'] == test_market, ['date_var', 'match_var']]
        test = test.rename(columns={'match_var': 'y'}).dropna()
        
        # Pivot the data to have a column for each reference market's match_var values
        refs = data.loc[data['id_var'].isin(ref_markets), ['id_var', 'date_var', 'match_var']].dropna()
        refs_pivot = refs.pivot(index='date_var', columns='id_var', values='match_var')
        refs_pivot.columns = [f'x{i+1}' for i in range(len(refs_pivot.columns))]

        # Merge the test and reference data on the date_var
        merged = pd.merge(test, refs_pivot, on='date_var', how='inner')
        
        y = merged['y'].to_numpy()
        x = merged.filter(regex='^x\d+$').to_numpy()
        dates = pd.to_datetime(merged['date_var'])

        return y, x, dates

    ########################################
    # calculate_distances_optimized program
    ########################################
    def calculate_distances_optimized(self, markets_to_be_matched, data, id_column, i, warping_limit, matches, dtw_emphasis):
        ThisMarket = markets_to_be_matched[i]
        unique_markets = data['id_var'].unique()
        
        # Prepare the DataFrame to store distances without appending within a loop.
        distances = []
        
        # Pre-calculate this market vectors once, outside the loop.
        test_y, _, _ = self.create_market_vectors(data, ThisMarket, [ThisMarket])
        test_var = np.var(test_y)
        sum_test = np.sum(test_y)
        
        for ThatMarket in unique_markets:
            # Skip if markets are the same or there's no variance in the test market.
            if ThisMarket == ThatMarket or test_var == 0 or sum_test == 0:
                continue
            
            ref_y, _, _ = self.create_market_vectors(data, ThatMarket, [ThatMarket])
            
            # Skip if there's no variance in the reference market.
            if np.var(ref_y) == 0 or len(ref_y) <= 2 * warping_limit + 1:
                continue
            
            sum_ref = np.sum(ref_y)
            
            # Calculate DTW distance if dtw_emphasis is positive and there is data to compare.
            if dtw_emphasis > 0:
                rawdist = dtw(test_y, ref_y, window_type="sakoechiba", window_args={"window_size": warping_limit}).distance
                relative_dist = rawdist / sum_test if sum_test != 0 else np.nan
            else:
                relative_dist = 0
                rawdist = 0
            
            # Calculate Pearson correlation
            correlation = pearsonr(test_y, ref_y)[0] if len(test_y) > 2 else np.nan
            correlation_logs = pearsonr(np.log1p(test_y), np.log1p(ref_y))[0] if np.max(ref_y) > 0 and np.max(test_y) > 0 else np.nan
            
            distances.append({
                id_column: ThisMarket,
                "BestControl": ThatMarket,
                "RelativeDistance": relative_dist,
                "Correlation": correlation,
                "Length": len(test_y),
                "SUMTEST": sum_test,
                "SUMCNTL": sum_ref,
                "RAWDIST": rawdist,
                "Correlation_of_logs": correlation_logs,
                "populated": 1
            })
        
        if not distances:
            return pd.DataFrame()
        
        distances_df = pd.DataFrame(distances)
        distances_df['matches'] = matches
        distances_df['w'] = dtw_emphasis
        
        # Rank and sort based on combined rank
        distances_df["dist_rank"] = rankdata(distances_df["RelativeDistance"])
        distances_df["corr_rank"] = rankdata(-distances_df["Correlation"])
        distances_df["combined_rank"] = distances_df["w"] * distances_df["dist_rank"] + (1 - distances_df["w"]) * distances_df["corr_rank"]
        distances_df.sort_values("combined_rank", inplace=True)
        
        # Select the top matches based on the sorted combined rank
        top_matches = distances_df.head(matches)
        
        # Calculate normalized distance
        top_matches["NORMDIST"] = 2 * top_matches["RAWDIST"] / (top_matches["SUMTEST"] + top_matches["SUMCNTL"])
        top_matches.replace([np.inf, -np.inf], np.nan, inplace=True)
        
        return top_matches
    

    ########################################
    # calculate_initial_validity program
    ########################################
    def calculate_initial_validity(self, p_value, pval_threshold):

        """
        Null Hypothesis (H0): The intervention (such as a new policy, marketing campaign, event, etc.) 
         has an effect on the outcome metric of interest over the time period being considered.
        
        Compare P-value to Alpha: 
         If the p-value ≤ α: There is sufficient statistical evidence to reject the null hypothesis. 
           This implies that the observed data are unlikely under the assumption that the null 
            hypothesis is true.
         If the p-value > α: There is not enough statistical evidence to reject the null hypothesis. 
           This suggests that the observed data are not sufficiently extreme to consider them 
           unlikely under the null hypothesis.
        """

        # Initially we do not want there to be a significant difference between the two markets
        #   so we want the p-value to be greater than the threshold, which is why if the p_value 
        #   is less than the pval_threshold then to return False

        if p_value <= pval_threshold:
            return False
        else:
            return True
        
    ########################################
    # calculate_post_validity program
    ########################################
    def calculate_post_validity(self, p_value, pval_threshold):

        """
        Null Hypothesis (H0): The intervention (such as a new policy, marketing campaign, event, etc.) 
         has an effect on the outcome metric of interest over the time period being considered.
        
        Compare P-value to Alpha: 
         If the p-value ≤ α: There is sufficient statistical evidence to reject the null hypothesis. 
           This implies that the observed data are unlikely under the assumption that the null 
            hypothesis is true.
         If the p-value > α: There is not enough statistical evidence to reject the null hypothesis. 
           This suggests that the observed data are not sufficiently extreme to consider them 
           unlikely under the null hypothesis.
        """

        # After the test is completed, we want there to be a significant difference between the two markets
        #   so we want the p-value to be less than the threshold, which is why if the p_value 
        #   is greater than the pval_threshold then to return False

        if p_value <= pval_threshold:
            return True
        else:
            return False


    ########################################
    # calculate_distances_for_market program
    ########################################
    def calculate_distances_for_market(self, args):
        # Unpack the arguments
        markets_to_be_matched, data, id_column, i, warping_limit, matches, dtw_emphasis = args
        # Call the calculate_distances_optimized function with the unpacked arguments
        return self.calculate_distances_optimized(markets_to_be_matched, data, id_column, i, warping_limit, matches, dtw_emphasis)


    ########################################
    # process_markets_in_parallel program
    ########################################
    def process_markets_in_parallel(self, markets_to_be_matched, data, id_column, warping_limit, matches, dtw_emphasis, num_processes=None):
        # Determine the number of processes to use
        if num_processes is None:
            num_processes = multiprocessing.cpu_count()
        
        # Prepare arguments for each market
        args_list = [
            (markets_to_be_matched, data, id_column, i, warping_limit, matches, dtw_emphasis)
            for i in range(len(markets_to_be_matched))
        ]

        print("Estimating cycle time...")
        ts0 = time.time()
        _ = self.calculate_distances_for_market(args_list[0])
        ts1 = time.time()
        totalPTime = (ts1-ts0)/60
        totalPTimeCore = (totalPTime*len(args_list))/num_processes

        print(f"Estimated total time per core is {np.round_(totalPTimeCore,2)} min or {np.round_(totalPTimeCore/60,2)} hr")
        
        # Create a Pool of workers and map the function to the arguments
        with multiprocessing.Pool(processes=num_processes) as pool:
            results = list(tqdm(pool.imap(self.calculate_distances_for_market, args_list), total=len(args_list), desc="Processing", ascii=False, ncols=75))
        
        # Concatenate all the DataFrames in the results
        shortest_distances_res = pd.concat(results, ignore_index=True)

        return shortest_distances_res
    

    ########################################
    # calculate_causal_impact_for_pair program
    ########################################
    def calculate_causal_impact_for_pair(self, args):
        # Unpack the arguments
        data, metric, pair, pre_period, post_period, plots, exp_details = args
        # Call the calculate_causal_impact function with the unpacked arguments
        return self.calculate_causal_impact(data, metric, pair, pre_period, post_period, plots, exp_details)


    ########################################
    # process_pairs_in_parallel program
    ########################################
    def process_pairs_in_parallel(self, data, metric, pairs, pre_period, post_period, plots, exp_details, num_processes=None):
        # Determine the number of processes to use
        if num_processes is None:
            num_processes = multiprocessing.cpu_count()

        # Prepare arguments for each pair
        args_list = [
            (data, metric, pairs[i], pre_period, post_period, plots, exp_details)
            for i in range(len(pairs))
        ]

        print("Estimating cycle time...")
        ts0 = time.time()
        _ = self.calculate_causal_impact_for_pair(args_list[0])
        ts1 = time.time()
        totalPTime = (ts1-ts0)/60
        totalPTimeCore = (totalPTime*len(args_list))/num_processes

        print(f"Estimated total time per core is {np.round_(totalPTimeCore,2)} min or {np.round_(totalPTimeCore/60,2)} hr")

        # Create a Pool of workers and map the function to the arguments
        with multiprocessing.Pool(processes=num_processes) as pool:
            results = list(tqdm(pool.imap(self.calculate_causal_impact_for_pair, args_list), total=len(args_list), desc="Processing", ascii=False, ncols=75))
    
        return results

    ########################################
    # calculate_causal_impact program
    ########################################
    def calculate_causal_impact(self, data, metric, pair, pre_period, post_period, plots, exp_details):
        results = []

        # print(f"Backtesting | Pair {j}/{len(pairs_test)} | {pair[0]}-{pair[1]}")
        combs = list(combinations(pair, 2))

        for i in range(len(combs)):

            # Assign the test and control markets
            (dma1, dma2) = combs[i]

            # Create dataframe for the entire date range
            d1 = pd.date_range(start=pre_period[0], end=post_period[1], freq='D')
            dat = pd.DataFrame(d1, columns=['Date'])
            dat['tmp'] = 0
            dat.index = pd.to_datetime(dat['Date'])
            dat = dat.drop(columns=["Date"])

            # Get the data for the first DMA
            x1 = data[data['DMA'] == dma1][['Date', metric]].sort_values(by=['Date']).reset_index(drop=True)
            x1 = x1.rename(columns={metric: 'x1'})
            x1.index = pd.to_datetime(x1['Date'])
            x1 = x1.drop(columns=["Date"])
            len_x1 = x1.shape[0]

            # Get the data for the second DMA
            y = data[data['DMA'] == dma2][['Date', metric]].sort_values(by=['Date']).reset_index(drop=True)
            y = y.rename(columns={metric: 'y'})
            y.index = pd.to_datetime(y['Date'])
            y = y.drop(columns=["Date"])
            len_y = y.shape[0]

            if (len_x1==0) or (len_y==0):
                if exp_details:
                    results = [pair, np.nan, np.nan, np.nan]
                    print(f"Fetch Data Error {dma1}-{dma2}")
                else:
                    results = [pair, np.nan]
                    print(f"Fetch Data Error {dma1}-{dma2}")

            else:
                # Merge the data
                dat1 = dat.join(x1, how='left')
                dat1 = dat1.join(y, how='left')
                dat1 = dat1.drop(columns=['tmp'])
                dat1 = dat1.rename(columns={'x1': 'y', 'y': 'x'})
                dat1 = dat1.sort_index()
                dat1 = dat1.reset_index(drop=False)
                dat1['Date'] = pd.to_datetime(dat1['Date'])
                dat1 = dat1.fillna(0)

                # Plot the results
                if plots:
                    fig, ax = plt.subplots()
                    fig.set_size_inches(30, 8)

                    ax.plot(dat1.Date[1:], dat1['y'][1:], color='black', label=dma1, linewidth=2)
                    ax.plot(dat1.Date[1:], dat1['x'][1:], '--', color='blue', label=dma2, linewidth=2)
                    ax.axvline(pd.to_datetime(pre_period[1]), color='red', linestyle='--', label='Post-Period Start')

                    ax.set_xlabel('Date', fontsize=16)
                    ax.tick_params(axis='x', which='major', labelsize=16)
                    ax.tick_params(axis='y', which='major', labelsize=16)
                    ax.legend(fontsize=12)
                    ax.grid(True)

                    # save the plot
                    fig.savefig(f"{self.work_dir}/Plots/Data_Plot_{dma1}_{dma2}.png", dpi=300)

                    # to avoid plotting the image in the notebook
                    plt.close()

                # Run the causal impact model hmc
                dated_data = dat1.copy()
                dated_data['Date'] = pd.to_datetime(dated_data['Date'])
                dated_data.index = dated_data['Date']
                dated_data = dated_data.drop(columns=['Date'])

                impact_flag = False
                try:
                    impact = CausalImpact(dated_data, pre_period, post_period, model_args={'prior_level_sd':np.std(dated_data['y'].values), 'fit_method': 'vi'})
                    impact_flag = True

                except Exception as e:
                    print(f"Error processing {dma1}-{dma2}: {str(e)}")

                if impact_flag:
                    if exp_details:
                        report_text = impact.summary(output = "report")

                        # Extract the values
                        overall_value, sum_of = self.parse_causal_impact_summary(report_text)

                    # Examine the results
                    res = pd.DataFrame(impact.inferences)
                    res['y'] = impact.data['y']
                    res = res.reset_index(drop=False)

                    # Plot the results
                    if plots:
                        fig, ax = plt.subplots()
                        fig.set_size_inches(30, 8)

                        ax.plot(res['Date'][1:], res['y'][1:], color='black', label='y', linewidth=2)
                        ax.plot(res['Date'][1:], res['preds'][1:], '--', color='blue', label='Predicted', linewidth=2)
                        ax.fill_between(res['Date'][1:], res['preds_lower'][1:], res['preds_upper'][1:], color='blue', alpha=0.3)
                        ax.axvline(pre_period[1], color='red', linestyle='--', label='Post-Period Start')

                        ax.set_xlabel('Date', fontsize=16)
                        ax.tick_params(axis='x', which='major', labelsize=16)
                        ax.tick_params(axis='y', which='major', labelsize=16)
                        ax.legend(fontsize=12)
                        ax.grid(True)

                        # save the plot
                        fig.savefig(f"{self.work_dir}/Plots/CausalImpact_OriginalPlot_{dma1}_{dma2}.png", dpi=300)

                        # to avoid plotting the image in the notebook
                        plt.close()
                    
                    # Plot the results
                    if plots:
                        fig, ax = plt.subplots()
                        fig.set_size_inches(30, 8)

                        ax.plot(res['Date'][1:], res['point_effects'][1:], '--', color='blue', label='Point Effects', linewidth=2)
                        ax.fill_between(res['Date'][1:], res['point_effects_lower'][1:], res['point_effects_upper'][1:], color='blue', alpha=0.3)
                        ax.axhline(0, color='black', linestyle='--')
                        ax.axvline(pre_period[1], color='red', linestyle='--', label='Post-Period Start')


                        ax.set_xlabel('Date', fontsize=16)
                        ax.tick_params(axis='x', which='major', labelsize=16)
                        ax.tick_params(axis='y', which='major', labelsize=16)
                        ax.legend(fontsize=12)
                        ax.grid(True)

                        # save the plot
                        fig.savefig(f"{self.work_dir}/Plots/CausalImpact_PointwisePlot_{dma1}_{dma2}.png", dpi=300)

                        # to avoid plotting the image in the notebook
                        plt.close()

                    # Get the p-value
                    p_value = float(impact.p_value)

                    if exp_details:
                        results = [pair, p_value, overall_value, sum_of]
                    else:
                        results = [pair, p_value]

                else:
                    if exp_details:
                        results = [pair, np.nan, np.nan, np.nan]
                    else:
                        results = [pair, np.nan]
            
        return results
    

    ########################################
    # causal_impact_iter program
    ########################################
    def causal_impact_iter(self, data, metric, pairs_test, pre_period, post_period, plots, exp_details):
        results = []
        for j in tqdm(range(len(pairs_test)), desc="Processing", ascii=False, ncols=75):
            
            pair = pairs_test[j]
            
            tmp_results = self.calculate_causal_impact(data, metric, pair, pre_period, post_period, plots, exp_details)

            results.append(tmp_results)
                
        return results


    ########################################
    # parse causal impact summary
    ########################################
    def parse_causal_impact_summary(self, report):
        # Regular expressions for the desired values, adjusted to avoid trailing non-numeric characters
        overall_value_pattern = r"overall value of ([\d.]+)"
        sum_of_pattern = r"sum of ([\d.]+)"

        # Search for the patterns and extract values
        overall_value_match = re.search(overall_value_pattern, report)
        sum_of_match = re.search(sum_of_pattern, report)

        # Extracting matched values and removing any trailing periods
        overall_value = float(overall_value_match.group(1).rstrip('.')) if overall_value_match else None
        sum_of = float(sum_of_match.group(1).rstrip('.')) if sum_of_match else None

        return overall_value, sum_of



    ########################################
    # get_market_matches program
    ########################################
    def get_market_matches (self, data_dir: str, dma_fName: str, gmm_metric: str, 
                           corr_thresh: float, pval_threshold: float, 
                           pre_period_start: str, pre_period_end: str, 
                           post_period_start: str, post_period_end: str, 
                           gmm_rank: int, initials: str, campaign: str, brand: str,
                           gmm_plots: bool = False, parallel_processing: bool = True):
        '''
        Driver program 
        '''
        try:
            
            # Check if the data directory exists
            if not self.check_paths_exist("./" + data_dir):
                sys.exit(1)

            # Assign the work directory
            self.work_dir = "./" + data_dir

            # Determine the number of cores
            self.num_processes = multiprocessing.cpu_count()

            # Check if the plot directory exists
            if gmm_plots:
                _ = self.check_paths_exist(self.work_dir + "/Plots")

            # Check if the correlation and p-value thresholds are between 0 and 1
            self.check_threshold(corr_thresh, "Correlation", 0, 1)
            self.check_threshold(pval_threshold, "P-value", 0, 1)

            # Ready input data
            self.df = self.read_input_parameters(self.work_dir, dma_fName, gmm_metric)

            # Process Input Data
            self.data, self.markets_to_be_matched, self.matches, self.dtw_emphasis = self.process_data(data = self.df.copy(), 
                                                                            id_variable = "DMA", 
                                                                            date_variable = "Date", 
                                                                            matching_variable = gmm_metric, 
                                                                            markets_to_be_matched = None, 
                                                                            suggest_market_splits = False, 
                                                                            matches = gmm_rank, 
                                                                            dtw_emphasis = 1, 
                                                                            start_match_period = pre_period_start, 
                                                                            end_match_period = pre_period_end)
            
            print("Number of markets to be matched: ", len(self.markets_to_be_matched))

            print("######## Calculate DTW Distances for Market Pairs ########")

            # User chose not to use multiprocessing
            if not parallel_processing:
                
                for i in tqdm(range(len(self.markets_to_be_matched)), desc="Processing", ascii=False, ncols=75):
                    all_distances = self.calculate_distances_optimized(
                        markets_to_be_matched = self.markets_to_be_matched,
                        data = self.data,
                        id_column = "DMA",
                        i = i,
                        warping_limit = 1,
                        matches = self.matches,
                        dtw_emphasis = self.dtw_emphasis,
                    )
                self.shortest_distances = pd.concat([self.shortest_distances, all_distances], ignore_index=True)

            # User chose to use multiprocessing
            if parallel_processing:

                print("Start Multiprocessing")
                p0 = time.time()
                print("Distributing the work to {} cores".format(self.num_processes))
                self.shortest_distances = self.process_markets_in_parallel(markets_to_be_matched = self.markets_to_be_matched, 
                                                                           data = self.data, 
                                                                           id_column = "DMA", 
                                                                           warping_limit = 1, 
                                                                           matches = self.matches, 
                                                                           dtw_emphasis = self.dtw_emphasis, 
                                                                           num_processes=self.num_processes
                                                                           )
                p1 = time.time()
                totalPTime = (p1-p0)/60
                print("Multiprocessing Time {:.2f} min".format(totalPTime))

            print("Filter the results based on the correlation threshold")
            self.shortest_distances = self.shortest_distances[self.shortest_distances['Correlation'] >= corr_thresh].reset_index(drop=True)

            print("Saving results")
            save_path = self.work_dir+"/"+initials+"_"+brand+"_"+campaign+"_Best_Matches_"+str(date.today())+".csv"
            self.shortest_distances.to_csv(save_path)

            #####################################################################################################################################

            # Determine the pairs to be tested based on the resuls of the matching
            self.pairs = [None] * len(self.shortest_distances)
            print("Number of market pairs: ", len(self.pairs))

            for i in range(len(self.pairs)):
                self.pairs[i] = [self.shortest_distances.loc[i, 'DMA'], self.shortest_distances.loc[i, 'BestControl']]

            try:
                if len(self.pairs) >= 5:
                    print("The first five pairs:")
                    for i in range(0,5):
                        print("Pair: ", self.pairs[i])
                else:
                    print(f"The first {len(self.pairs)} pairs:")
                    for i in range(len(self.pairs)):
                        print("Pair: ", self.pairs[i])
            except Exception as e:
                print("Function::Print Pairs failed: %s", e)
                sys.exit(1)

            print("######## Determining Causal Impact ########")

            # User chose not to use multiprocessing
            if not parallel_processing:

                back_test = self.causal_impact_iter(data = self.df.copy(),
                                            metric = gmm_metric, 
                                            pairs_test = self.pairs, 
                                            pre_period = [pre_period_start, pre_period_end], 
                                            post_period = [post_period_start, post_period_end],
                                            plots = gmm_plots,
                                            exp_details = False)
                
                # Create DataFrame for results
                self.results = pd.DataFrame(columns=["DMA1", "DMA2", "Valid", "Train P-value", "Correlation", "Relative Distance"])

                for i in range(len(back_test)):
                    pair = back_test[i][0]
                    p_value = back_test[i][1]
                    corr = self.shortest_distances.loc[i, "Correlation"]
                    dist = self.shortest_distances.loc[i, "RelativeDistance"]
                    self.results.loc[i, "DMA1"] = pair[0]
                    self.results.loc[i, "DMA2"] = pair[1]
                    self.results.loc[i, "Valid"] = self.calculate_initial_validity(p_value, pval_threshold)
                    self.results.loc[i, "Train P-value"] = p_value
                    self.results.loc[i, "Correlation"] = corr
                    self.results.loc[i, "Relative Distance"] = dist


            # User chose to use multiprocessing
            if parallel_processing:
                
                print("Start Multiprocessing")
                p0 = time.time()
                print("Distributing the work to {} cores".format(self.num_processes))
                back_test = self.process_pairs_in_parallel(data = self.df.copy(),
                                                        metric = gmm_metric, 
                                                        pairs = self.pairs, 
                                                        pre_period = [pre_period_start, pre_period_end], 
                                                        post_period = [post_period_start, post_period_end],
                                                        plots = gmm_plots,
                                                        exp_details = False,
                                                        num_processes=self.num_processes)
                p1 = time.time()
                totalPTime = (p1-p0)/60
                print("Multiprocessing Time {:.2f} min".format(totalPTime))

                # Create DataFrame for results
                self.results = pd.DataFrame(columns=["DMA1", "DMA2", "Valid", "Train P-value", "Correlation", "Relative Distance"])

                for i in range(len(back_test)):
                    pair = back_test[i][0]
                    p_value = back_test[i][1]
                    corr = self.shortest_distances.loc[i, "Correlation"]
                    dist = self.shortest_distances.loc[i, "RelativeDistance"]
                    self.results.loc[i, "DMA1"] = pair[0]
                    self.results.loc[i, "DMA2"] = pair[1]
                    self.results.loc[i, "Valid"] = self.calculate_initial_validity(p_value, pval_threshold)
                    self.results.loc[i, "Train P-value"] = p_value
                    self.results.loc[i, "Correlation"] = corr
                    self.results.loc[i, "Relative Distance"] = dist

            print("Saving results")
            save_path = self.work_dir+"/"+initials+"_"+brand+"_"+campaign+"_Market_Pairs_"+str(date.today())+".csv"
            self.results.to_csv(save_path)

            return self.results

        except Exception as e:
            print("Function::Get Market Matches failed: %s", e)
            sys.exit(1)

    ########################################
    # intervention program
    ########################################
    def intervention (self, data_dir: str, dma_fName: str, gmm_metric: str,  
                            gmm_pName: str, pval_threshold: float, 
                           pre_period_start: str, pre_period_end: str, 
                           post_period_start: str, post_period_end: str, 
                           initials: str, campaign: str, brand: str,
                           gmm_plots: bool = False, parallel_processing: bool = True):
        '''
        Driver program 
        '''
        try:
            
            # Check if the data directory exists
            if not self.check_paths_exist("./" + data_dir):
                sys.exit(1)

            # Assign the work directory
            self.work_dir = "./" + data_dir

            # Determine the number of cores
            self.num_processes = multiprocessing.cpu_count()

            # Check if the plot directory exists
            if gmm_plots:
                _ = self.check_paths_exist(self.work_dir + "/Plots")

            # Check if the p-value thresholds are between 0 and 1
            self.check_threshold(pval_threshold, "P-value", 0, 1)

            # Ready input data
            self.df = self.read_input_parameters(self.work_dir, dma_fName, gmm_metric)

            # Process Input Data
            self.data = self.process_intervention_data(data = self.df.copy(), 
                    id_variable = "DMA", 
                    date_variable = "Date", 
                    matching_variable = gmm_metric, 
                    start_match_period = pre_period_start, 
                    end_match_period = pre_period_end)

            # Ready pair input data
            self.df_pairs = self.read_test_pairs_file(self.work_dir, gmm_pName)

            # Process Pair Input Data
            self.data_pairs = self.process_pair_data(data = self.df_pairs.copy())

            # Determine the pairs to be tested based on the resuls of the matching
            self.pairs = [None] * len(self.data_pairs)
            print("Number of market pairs: ", len(self.pairs))

            for i in range(len(self.pairs)):
                self.pairs[i] = [self.data_pairs.loc[i, 'Exposed'], self.data_pairs.loc[i, 'Control']]

            try:
                if len(self.pairs) >= 5:
                    print("The first five pairs:")
                    for i in range(0,5):
                        print("Pair: ", self.pairs[i])
                else:
                    print(f"The first {len(self.pairs)} pairs:")
                    for i in range(len(self.pairs)):
                        print("Pair: ", self.pairs[i])
            except Exception as e:
                print("Function::Print Pairs failed: %s", e)
                sys.exit(1)

            print("######## Determining Causal Impact ########")

            # User chose not to use multiprocessing
            if not parallel_processing:

                back_test = self.causal_impact_iter(data = self.df.copy(),
                                            metric = gmm_metric, 
                                            pairs_test = self.pairs, 
                                            pre_period = [pre_period_start, pre_period_end], 
                                            post_period = [post_period_start, post_period_end],
                                            plots = gmm_plots,
                                            exp_details = True)
                
                # Create DataFrame for results
                self.results = pd.DataFrame(columns=["Control", "Exposed", "Actual", "Predicted", "Test P-value", "Valid"])

                for i in range(len(back_test)):
                    pair = back_test[i][0]
                    p_value = back_test[i][1]
                    overall_value = back_test[i][2]
                    sum_of = back_test[i][3]
                    self.results.loc[i, "Control"] = pair[1]
                    self.results.loc[i, "Exposed"] = pair[0]
                    self.results.loc[i, "Actual"] = overall_value
                    self.results.loc[i, "Predicted"] = sum_of
                    self.results.loc[i, "Test P-value"] = p_value
                    self.results.loc[i, "Valid"] = self.calculate_post_validity(p_value, pval_threshold)


            # User chose to use multiprocessing
            if parallel_processing:
                
                print("Start Multiprocessing")
                p0 = time.time()
                print("Distributing the work to {} cores".format(self.num_processes))
                back_test = self.process_pairs_in_parallel(data = self.df.copy(),
                                                        metric = gmm_metric, 
                                                        pairs = self.pairs, 
                                                        pre_period = [pre_period_start, pre_period_end], 
                                                        post_period = [post_period_start, post_period_end],
                                                        plots = gmm_plots,
                                                        exp_details = True,
                                                        num_processes=self.num_processes)
                p1 = time.time()
                totalPTime = (p1-p0)/60
                print("Multiprocessing Time {:.2f} min".format(totalPTime))

                # Create DataFrame for results
                self.results = pd.DataFrame(columns=["Control", "Exposed", "Actual", "Predicted", "Test P-value", "Valid"])

                for i in range(len(back_test)):
                    pair = back_test[i][0]
                    p_value = back_test[i][1]
                    overall_value = back_test[i][2]
                    sum_of = back_test[i][3]
                    self.results.loc[i, "Control"] = pair[1]
                    self.results.loc[i, "Exposed"] = pair[0]
                    self.results.loc[i, "Actual"] = overall_value
                    self.results.loc[i, "Predicted"] = sum_of
                    self.results.loc[i, "Test P-value"] = p_value
                    self.results.loc[i, "Valid"] = self.calculate_post_validity(p_value, pval_threshold)

            print("Saving results")
            save_path = self.work_dir+"/"+initials+"_"+brand+"_"+campaign+"_Test_Market_Pairs_"+str(date.today())+".csv"
            self.results.to_csv(save_path)

            return self.results

        except Exception as e:
            print("Function::Get Market Matches failed: %s", e)
            sys.exit(1)