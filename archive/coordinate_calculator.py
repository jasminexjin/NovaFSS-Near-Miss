import pandas as pd
import csv

radius = 5

file_path = 'NoVA_NM_data_to_23_July_2023.csv'

data = []

with open(file_path, 'r') as csv_file:
    csv_reader = csv.reader(csv_file)


