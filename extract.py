"""Extract data on near-Earth objects and close approaches from CSV and JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided at the command
line, and uses the resulting collections to build an `NEODatabase`.

You'll edit this file in Task 2.
"""
import csv
import json

from models import NearEarthObject, CloseApproach


def load_neos(neo_csv_path):
    """Read and process NEO data from a CSV file.

    This function reads a CSV file containing data about near Earth objects,
    and creates a list of NearEarthObject instances for each valid record.

    Args:
        filename (str): The path to the CSV file containing NEO data.

    Returns:
        list of NearEarthObject: A list of NearEarthObject instances.
    """

    neos = []
    with open(neo_csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['pdes'] and row['name'] and row['pha'] and row['diameter']:
                neo = NearEarthObject(
                    designation=row['pdes'],
                    name=row['name'],
                    diameter=row['diameter'],
                    hazardous=row['pha']
                )
                neos.append(neo)
    return neos

    
#neos = load_neos('/Users/Joseph/Documents/capstone/cd0010-advanced-python-techniques-project-starter/data/neos.csv')
#print(neos)  # to see the output



def load_approaches(cad_json_path):
    
    """
    Load and process JSON data into a list of CloseApproach objects.

    Args:
    filepath (str): The path to the JSON file containing close approach data.

    Returns:
    list: A list of CloseApproach objects initialized with data from the file.
    """

    with open(cad_json_path, 'r') as file:
        data = json.load(file)

    # Extract data items
    close_approaches = []
    for entry in data['data']:
        des = entry[0]
        cd = entry[3]
        dist = float(entry[4])
        v_rel = float(entry[7])

        # Create a CloseApproach object and append it to the list
        approach = CloseApproach(designation=des, time=cd, distance=dist, velocity=v_rel)
        close_approaches.append(approach)

    return close_approaches

#close_approaches = load_approaches('/Users/Joseph/Documents/capstone/cd0010-advanced-python-techniques-project-starter/data/cad.json')
#print(close_approaches)