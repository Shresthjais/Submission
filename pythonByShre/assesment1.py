import pandas as pd
import numpy as np


def generate_car_matrix(df)->pd.DataFrame:
    """
    Creates a DataFrame  for id combinations.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Matrix generated with 'car' values, 
                          where 'id_1' and 'id_2' are used as indices and columns respectively.
    """

    # ANS1
    matrix_df = df.pivot(index='id_1', columns='id_2', values='car').fillna(0)

    # Set the diagonal values to 0
    for index in matrix_df.index:
        matrix_df.at[index, index] = 0

    return matrix_df

#ANS2
def get_type_count(df)->dict:
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    conditions = [
        (df['car'] <= 15),
        (df['car'] > 15) & (df['car'] <= 25),
        (df['car'] > 25)
    ]

    choices = ['low', 'medium', 'high']
    df['car_type'] = np.select(conditions, choices, default='Unknown')

    # Calculate the count of occurrences for each 'car_type' category
    type_count = df['car_type'].value_counts().to_dict()

    
    type_count_sorted = {k: v for k, v in sorted(type_count.items())}

    return type_count_sorted

#Ans3
def get_bus_indexes(df)->list:
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """

    mean_bus_value = df['bus'].mean()
    bus_indexes = df[df['bus'] > 2 * mean_bus_value].index.tolist()
    bus_indexes.sort()

    return bus_indexes

#Ans4
def filter_routes(df)->list:
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    
    route_avg_truck = df.groupby('route')['truck'].mean()
    selected_routes = route_avg_truck[route_avg_truck > 7].index.tolist()
    selected_routes.sort()

    return selected_routes


#Ans5
def multiply_matrix(matrix)->pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    modified_df = matrix.copy()
    modified_df = modified_df.applymap(lambda x: x * 0.75 if x > 20 else x * 1.25)
    modified_df = modified_df.round(1)

    return modified_df


#Ans6
def time_check(df)->pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """

    df['start_timestamp'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'],errors='coerce')
    df['end_timestamp'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'],errors='coerce')
    df['day_of_week'] = df['start_timestamp'].dt.day_name()

    # Check if the timestamp spans all 7 days and covers a full 24-hour period
    completeness_check = (
        (df.groupby(['id', 'id_2'])['start_timestamp'].min().dt.day_name() == 'Monday') &
        (df.groupby(['id', 'id_2'])['end_timestamp'].max().dt.day_name() == 'Sunday') &
        (df.groupby(['id', 'id_2'])['start_timestamp'].min().dt.time == pd.to_datetime('00:00:00').time()) &
        (df.groupby(['id', 'id_2'])['end_timestamp'].max().dt.time == pd.to_datetime('23:59:59').time())
    )

    return completeness_check



file_path1 = (r'C:\Users\HOT_SINAX066\pythonByShre\dataset-1.csv')
file_path2 = (r'C:\Users\HOT_SINAX066\pythonByShre\dataset-2.csv')
df1 = pd.read_csv(file_path1)

df2 = pd.read_csv(file_path2,encoding = 'ISO-8859-1')



result_matrix = generate_car_matrix(df1)
result_type_count = get_type_count(df1)
result_bus_indexes = get_bus_indexes(df1)
result_routes = filter_routes(df1)
modified_car_matrix = multiply_matrix(result_matrix)
completeness_series = time_check(df2)

print(result_matrix)
print(result_type_count)
print(result_bus_indexes)
print(result_routes)
print(modified_car_matrix)
print(completeness_series)
