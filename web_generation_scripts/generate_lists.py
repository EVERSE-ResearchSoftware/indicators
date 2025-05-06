import os
import json

indicators_dir = './indicators/'
dimensions_dir = './dimensions/'

indicators_list_file = './website/utils/indicators_list.json'
dimensions_list_file = './website/utils/dimensions_list.json'

def generate_lists():
    print('Generating lists...')
    
    print(f'Accessing {indicators_dir} ...')
    indicators = sorted([f for f in os.listdir(indicators_dir) if f.endswith('.json')])
    
    print(f'Accessing {dimensions_dir} ...')
    dimensions = sorted([f for f in os.listdir(dimensions_dir) if f.endswith('.json')])

    print(f'Checking {indicators_list_file} ...')
    if os.path.exists(indicators_list_file):
        os.remove(indicators_list_file)

    print(f'Checking {dimensions_list_file} ...')
    if os.path.exists(dimensions_list_file):
        os.remove(dimensions_list_file)

    print('Dumping lists into files...')
    with open(indicators_list_file, 'w') as outfile:
        json.dump(indicators, outfile, indent=4)
        
    with open(dimensions_list_file, 'w') as outfile:
        json.dump(dimensions, outfile, indent=4)

if __name__ == '__main__':
    generate_lists()
