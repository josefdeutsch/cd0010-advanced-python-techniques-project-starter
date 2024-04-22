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
from helpers import Helper
from typing import List

def load_neos(neo_csv_path=str) -> List[NearEarthObject]: 

    """
    Load a list of NearEarthObject instances from a CSV file.

    This function opens a CSV file specified by the path `neo_csv_path`,
    reads its content, and populates a list with NearEarthObject instances
    based on the data found in the file. It specifically checks for a
    primary designation ('pdes') for each NEO in the file and constructs
    a NearEarthObject instance only if the designation exists.

    Args:
        neo_csv_path (str): The path to the CSV file containing NEO data.

    Returns:
        List[NearEarthObject]: A list of NearEarthObject instances
        constructed from the data in the CSV file.

    """

    neos = []
    with open(neo_csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['pdes']:  # Check for primary designation
                hazardous = Helper.parse_hazardous(row.get('pha'))
                neo = NearEarthObject(
                    designation=row['pdes'],
                    name=row.get('name'),
                    diameter=row.get('diameter'),
                    hazardous=hazardous
                )
                neos.append(neo)
    return neos
   
def load_approaches(cad_json_path: str) -> List[CloseApproach]:
    
    """
    Load a list of CloseApproach instances from a JSON file.

    This function opens a JSON file specified by the path `cad_json_path`,
    reads its contents, and populates a list with CloseApproach instances
    based on the data found in the file. The function extracts necessary
    details like designation, time of close approach, distance, and relative
    velocity from each entry in the JSON file to construct CloseApproach
    instances.

    Args:
        cad_json_path (str): The path to the JSON file containing close
        approach data of NEOs.

    Returns:
        List[CloseApproach]: A list of CloseApproach instances constructed
        from the data in the JSON file.

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

