import pandas as pd

#ANS1
def calculate_distance_matrix(df)->pd.DataFrame():
    """
    Calculate a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Distance matrix
    """
    distance_matrix = df.pivot(index='id_start', columns='id_end', values='distance')
    distance_matrix = distance_matrix.fillna(0)
    distance_matrix = distance_matrix + distance_matrix.T
    distance_matrix = distance_matrix.cumsum(axis=1)

    # Set diagonal values to 0
    distance_matrix.values[[range(distance_matrix.shape[0])]*2] = 0

    return distance_matrix


#Ans2
def unroll_distance_matrix(df)->pd.DataFrame():
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
    distance_matrix_copy = df.copy()
    if 'id_start' in distance_matrix_copy.index.names:
        # print('a')
        distance_matrix_copy.reset_index(inplace=True)
    print(distance_matrix_copy)
    unrolled_df = pd.melt(distance_matrix_copy, id_vars='id_start', var_name='id_end', value_name='distance')
    unrolled_df = unrolled_df[unrolled_df['id_start'] != unrolled_df['id_end']]
    unrolled_df.reset_index(drop=True, inplace=True)

    return unrolled_df


#Ans3
def find_ids_within_ten_percentage_threshold(df, reference_id)->pd.DataFrame():
    """
    Find all IDs whose average distance lies within 10% of the average distance of the reference ID.

    Args:
        df (pandas.DataFrame)
        reference_id (int)

    Returns:
        pandas.DataFrame: DataFrame with IDs whose average distance is within the specified percentage threshold
                          of the reference ID's average distance.
    """
    reference_rows = df[df['id_start'] == reference_value]
    reference_avg_distance = reference_rows['distance'].mean()
    threshold_range = 0.1 * reference_avg_distance
    within_threshold_rows = df[
        (df['distance'] >= reference_avg_distance - threshold_range) &
        (df['distance'] <= reference_avg_distance + threshold_range)
    ]

    # Get unique values from the id_start column and sort them
    result_ids = within_threshold_rows['id_start'].unique()
    result_ids.sort()

    return result_ids


#Ans4
def calculate_toll_rate(df)->pd.DataFrame():
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    rate_coefficients = {
        'moto': 0.8,
        'car': 1.2,
        'rv': 1.5,
        'bus': 2.2,
        'truck': 3.6
    }

    for vehicle_type, rate_coefficient in rate_coefficients.items():
        column_name = f'{vehicle_type}_rate'
        df[column_name] = df['distance'] * rate_coefficient

    return df



file_path3 = (r'C:\Users\HOT_SINAX066\pythonByShre\dataset-3.csv')
df1 = pd.read_csv(file_path3)

result_matrix = calculate_distance_matrix(df1)
result_unrolled = unroll_distance_matrix(result_matrix)
result_ids_within_threshold = find_ids_within_ten_percentage_threshold(result_matrix, 1001434)
result_with_toll_rates = calculate_toll_rate(result_unrolled)


# Display the resulting DataFrame
print(result_matrix)
print(result_unrolled)
print(result_ids_within_threshold)

