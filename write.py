"""Write a stream of close approaches to CSV or to JSON.

This module exports two functions: `write_to_csv` and `write_to_json`, each of
which accept an `results` stream of close approaches and a path to which to
write the data.

These functions are invoked by the main module with the output of the `limit`
function and the filename supplied by the user at the command line. The file's
extension determines which of these functions is used.

You'll edit this file in Part 4.
"""
import csv
import json


def write_to_csv(results, filename):
    """Write an iterable of `CloseApproach` objects to a CSV file.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    fieldnames = (
        'datetime_utc', 'distance_au', 'velocity_km_s',
        'designation', 'name', 'diameter_km', 'potentially_hazardous'
    )
    
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        
        for approach in results:
            neo = approach.neo
            neo_name = neo.name if neo.name else ''
            neo_diameter = getattr(neo, 'diameter_km', 'nan')  # Use getattr for diameter
            neo_hazardous = getattr(neo, 'potentially_hazardous', 'False')  # Use getattr for potentially_hazardous

            row = {
                'datetime_utc': approach.time.strftime("%Y-%m-%d %H:%M"),
                'distance_au': approach.distance,
                'velocity_km_s': approach.velocity,
                'designation': neo.designation,
                'name': neo_name,
                'diameter_km': neo_diameter,
                'potentially_hazardous': str(neo_hazardous)
            }
            
            writer.writerow(row)



def write_to_json(results, filename):
    """
    Write an iterable of `CloseApproach` objects to a JSON file.
    
    Each `CloseApproach` entry in the JSON output will contain the approach's details
    as well as the associated NEO's details under the 'neo' key.
    
    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    # Construct a list to hold all serialized CloseApproach data
    data_to_write = []
    
    for approach in results:
        # Serialize the CloseApproach object
        approach_data = approach.serialize()
        
        # Serialize the associated NearEarthObject and add it under the 'neo' key
        approach_data['neo'] = approach.neo.serialize()
        
        # Append the serialized data to the list
        data_to_write.append(approach_data)
    
    # Open the file in write mode and use json.dump to write the list of data
    with open(filename, 'w') as outfile:
        json.dump(data_to_write, outfile, ensure_ascii=False, indent=4)


