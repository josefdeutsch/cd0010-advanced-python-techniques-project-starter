"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.

You'll edit this file in Task 1.
"""


import math
from helpers import cd_to_datetime, datetime_to_str


class NearEarthObject:
    """Represent a near-Earth object (NEO).

    This class encapsulates semantic and physical parameters about the NEO,
    such as its primary designation (required, unique), IAU name (optional),
    diameter in kilometers (optional, sometimes unknown), and a flag indicating
    if it is potentially hazardous.

    Attributes:
        designation (str): The primary designation for the NEO.
        name (str or None): The IAU name of the NEO, if available.
        diameter (float): The diameter of the NEO in kilometers.
        hazardous (bool): True if the NEO is potentially hazardous, otherwise False.
        approaches (list): A list of close approaches related to this NEO.
    """

    def __init__(self, designation="Unknown", name=None, diameter=float('nan'), hazardous=False):
        
        """
        Initializes a new NearEarthObject instance with the given properties.

        Parameters:
            designation (str): The designation of the NEO. Defaults to "Unknown".
            name (str, optional): The name of the NEO. Defaults to None.
            diameter (float): The diameter of the NEO. Non-numeric values default to NaN.
            hazardous (bool): Indicates if the NEO is potentially hazardous. Defaults to False.

        Raises:
            ValueError: If the provided diameter cannot be converted to a float and is not a numeric value.
            TypeError: If the input types are incorrect for the designated parameters.
        """

        self.designation = designation
        self.name = str(name) if name else None  
        try:
            self.diameter = float(diameter) if float(diameter) > 0 else float('nan')
        except (ValueError, TypeError):
            self.diameter = float('nan')
        self.hazardous = bool(hazardous)
        self.approaches = []


    @property
    def fullname(self):
        """Return the full name of this NEO, combining designation and name."""
        return f"{self.designation} ({self.name})" if self.name else self.designation

    def __str__(self):
        """Return a human-readable string representation of this NEO."""
        hazardous_text = "Yes" if self.hazardous else "No"
        name_text = self.name if self.name else "N/A"
        diameter_text = f"{self.diameter:.3f}" if not math.isnan(self.diameter) else "Unknown"
        
        return (f"A NearEarthObject with designation {self.designation}, "
                f"name {name_text}, diameter {diameter_text} km, "
                f"and potentially hazardous: {hazardous_text}.")

    def __repr__(self):
        """Return a computer-readable string representation of this NEO."""
        return (f"NearEarthObject(designation={self.designation!r}, name={self.name!r}, "
                f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r})")


    def serialize(self):
        """Serialize this NearEarthObject into a dictionary suitable for JSON serialization."""
        return {
            'designation': self.designation,
            'name': self.name if self.name else "",  # Default to an empty string if name is None
            'diameter_km': self.diameter if not math.isnan(self.diameter) else float('nan'),  # Preserve NaN for JSON
            'potentially_hazardous': self.hazardous
        }

class CloseApproach:
    """Represent a close approach to Earth by an NEO.

    Attributes:
        designation (str): The NEO's designation this approach is associated with.
        time (datetime.datetime): The date and time of the close approach.
        distance (float): The nominal approach distance in astronomical units.
        velocity (float): The relative approach velocity in kilometers per second.
        neo (NearEarthObject or None): The NEO this approach is associated with.
    """

    def __init__(self, designation="Unknown", time=None, distance=float('nan'), velocity=float('nan'), neo=None):
        """Initialize a new CloseApproach.

        Args:
            designation (str): The designation of the NEO associated with this approach.
            time (str): The date and time of the close approach as a string, to be converted.
            distance (float): The nominal distance of the approach in astronomical units.
            velocity (float): The relative velocity of the approach in kilometers per second.
            neo (NearEarthObject, optional): The NearEarthObject associated with this approach.
        """
        self.designation = designation if designation else "Unknown"
        self.time = cd_to_datetime(time) if time else None
        self.distance = distance
        self.velocity = velocity
        self.neo = neo

    @property
    def time_str(self):
        """Return a formatted string representation of the approach time."""
        return datetime_to_str(self.time) if self.time else "Unknown time"

    def __str__(self):
        """Return a human-readable string representation of this close approach."""
        distance_str = f"{self.distance:.2f}" if not math.isnan(self.distance) else "N/A"
        velocity_str = f"{self.velocity:.2f}" if not math.isnan(self.velocity) else "N/A"
        return (f"A CloseApproach on {self.time_str}, at a distance of {distance_str} au, "
                f"and a velocity of {velocity_str} km/s.")

    def __repr__(self):
        """Return a computer-readable string representation of this close approach."""
        time_repr = datetime_to_str(self.time) if self.time else "None"
        return (f"CloseApproach(designation={self.designation!r}, time={time_repr!r}, "
                f"distance={self.distance:.2f}, velocity={self.velocity:.2f}, neo={self.neo!r})")
    
    def serialize(self):
        """Serialize this CloseApproach into a dictionary suitable for JSON serialization."""
        return {
            'datetime_utc': datetime_to_str(self.time),
            'distance_au': self.distance,
            'velocity_km_s': self.velocity
        }