import csv
# Extract the data from csv file
def extract_data(input_file):
    with open(input_file, 'r') as file:
        reader = csv.DictReader(file)
        data = [row for row in reader]
    return data