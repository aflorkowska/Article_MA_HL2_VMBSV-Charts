
def preprocess_data_from_csv(input_data_csv, marker_sizes, column_name, mean = str('_mean'), median = str('_median'), std = str('_std')):
    output = {}

    for size in marker_sizes:
        mean = input_data_csv[str(column_name) + str(size) + str(mean)].dropna().tolist()
        median = input_data_csv[str(column_name) + str(size) + str(median)].dropna().tolist()
        std = input_data_csv[str(column_name) + str(size) + str(std)].dropna().tolist()
        output[size] = [ [i,j,k] for i, j, k in zip(mean, median, std)]

    return output

def get_distances_as_list_from_csv(input_data_csv):
    return input_data_csv['distance'].tolist()