"""A database encapsulating collections of near-Earth objects and their close approaches.

A `NEODatabase` holds an interconnected data set of NEOs and close approaches.
It provides methods to fetch an NEO by primary designation or by name, as well
as a method to query the set of close approaches that match a collection of
user-specified criteria.

Under normal circumstances, the main module creates one NEODatabase from the
data on NEOs and close approaches extracted by `extract.load_neos` and
`extract.load_approaches`.

You'll edit this file in Tasks 2 and 3.
"""


class NEODatabase:
    """A database of near-Earth objects and their close approaches.

    A `NEODatabase` contains a collection of NEOs and a collection of close
    approaches. It additionally maintains a few auxiliary data structures to
    help fetch NEOs by primary designation or by name and to help speed up
    querying for close approaches that match criteria.
    """
    def __init__(self, neos, approaches):
        """Create a new `NEODatabase`.

        As a precondition, this constructor assumes that the collections of NEOs
        and close approaches haven't yet been linked - that is, the
        `.approaches` attribute of each `NearEarthObject` resolves to an empty
        collection, and the `.neo` attribute of each `CloseApproach` is None.

        However, each `CloseApproach` has an attribute (`._designation`) that
        matches the `.designation` attribute of the corresponding NEO. This
        constructor modifies the supplied NEOs and close approaches to link them
        together - after it's done, the `.approaches` attribute of each NEO has
        a collection of that NEO's close approaches, and the `.neo` attribute of
        each close approach references the appropriate NEO.

        :param neos: A collection of `NearEarthObject`s.
        :param approaches: A collection of `CloseApproach`es.
        """
        self._neos = neos
        self._approaches = approaches

        self.neo_dict = {neo.designation: neo for neo in neos}
        for approach in approaches:
            neo = self.neo_dict.get(approach.designation)
            if neo:
                approach.neo = neo  # Linking NEO to CloseApproach
                if hasattr(neo, 'approaches'):
                   neo.approaches.append(approach)
                else:
                    neo.approaches = [approach]
        
        
        
    def display_data(self):
         for key, value in self.neo_dict.items():
            print(f"Key: {key}, Value: {value}") 

    def get_neo_by_designation(self, designation):
      
       """Retrieve a NEO by its designation.

        Validates that the designation is a non-empty string and attempts to retrieve
        the NEO associated with that designation from the dictionary. If the NEO
        is not found, an error message is printed.

        Args:
            designation (str): The designation of the NEO to retrieve.

        Returns:
            dict or None: The NEO details if found, None otherwise.
        """
       
       if not isinstance(designation, str):
            print("Input error: Designation must be a string.")
            return None
       if designation == "":
            print("Input error: Designation cannot be empty.")
            return None

       neo = self.neo_dict.get(designation)
       if neo is not None:
            return neo

        # If no matching NEO is found, report the error
       print(f"Search error: NEO with designation '{designation}' not found.")
       return None
    

    def get_neo_by_name(self, name):
        """
        Search for a Near Earth Object (NEO) by its name in the dictionary.
        
        Args:
        name (str): The name of the NEO to search for.
        
        Returns:
        object: Returns the NEO object if found, otherwise None.
        """
        # Validate input
        if not isinstance(name, str):
            print("Input error: Name must be a string.")
            return None
        if name == "":
            print("Input error: Name cannot be empty.")
            return None

        # Search for the NEO by name
        for neo in self.neo_dict.values():
            if neo.name == name:
                return self.neo_dict[neo.designation]

        # If no matching NEO is found, report the error
        print(f"Search error: NEO with name '{name}' not found.")
        return None
    
    



    def query(self, filters=()):
        """Query close approaches to generate those that match a collection of filters.

        This generates a stream of `CloseApproach` objects that match all of the
        provided filters.

        If no arguments are provided, generate all known close approaches.

        The `CloseApproach` objects are generated in internal order, which isn't
        guaranteed to be sorted meaningfully, although is often sorted by time.

        :param filters: A collection of filters capturing user-specified criteria.
        :return: A stream of matching `CloseApproach` objects.
        """
        # TODO: Generate `CloseApproach` objects that match all of the filters.
        for approach in self._approaches:
            yield approach
