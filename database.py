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
from helpers import Helper

class NEODatabase:
    """A database of near-Earth objects and their close approaches.

    A `NEODatabase` contains a collection of NEOs and a collection of close
    approaches. It additionally maintains a few auxiliary data structures to
    help fetch NEOs by primary designation or by name and to help speed up
    querying for close approaches that match criteria.
    """
    def __init__(self, neos, approaches):

        """
        Initialize and link NEOs and their close approaches.

        This method initializes NEO and approach attributes of the class.
        It also creates a dictionary mapping each NEO's designation to the NEO instance.
        The method links each close approach with a corresponding NEO instance.
        If a matching NEO is not found, it assigns the first NEO in the list as a default.
        Additionally, it ensures that each NEO has an 'approaches' attribute and appends
        each close approach to this list.

        Args:
            neos (list): A list of NearEarthObject instances.
            approaches (list): A list of CloseApproach instances.
        """

        self._neos = neos
        self._approaches = approaches

        self.neo_dict = {neo.designation: neo for neo in neos}
        self.default_neo = self._neos[0]
        for approach in approaches:
        # Use the default Neo instance if no match is found
            neo = self.neo_dict.get(approach.designation)
            approach.neo = neo  # Linking NEO to CloseApproach
            if not hasattr(neo, 'approaches'):
                neo.approaches = []
            neo.approaches.append(approach)
        
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
       if (designation := Helper.validate_input(designation)) is None:
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
        if (name := Helper.validate_input(name)) is None:
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
            if all(f(approach) for f in filters):
                yield approach