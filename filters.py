"""Provide filters for querying close approaches and limit the generated results.

The `create_filters` function produces a collection of objects that is used by
the `query` method to generate a stream of `CloseApproach` objects that match
all of the desired criteria. The arguments to `create_filters` are provided by
the main module and originate from the user's command-line options.

This function can be thought to return a collection of instances of subclasses
of `AttributeFilter` - a 1-argument callable (on a `CloseApproach`) constructed
from a comparator (from the `operator` module), a reference value, and a class
method `get` that subclasses can override to fetch an attribute of interest from
the supplied `CloseApproach`.

The `limit` function simply limits the maximum number of values produced by an
iterator.

You'll edit this file in Tasks 3a and 3c.
"""
import operator
from datetime import date

class UnsupportedCriterionError(NotImplementedError):
    """Exception raised for unsupported filter criteria."""
    pass

class AttributeFilter:
    """
    Abstract base class for filters that compare attributes of close approaches.

    Attributes:
        op (callable): A comparison operator from the operator module.
        value (various): The value to compare against the attribute.
    """

    def __init__(self, op, value):
        """
        Initialize an AttributeFilter with an operator and a target value.

        Args:
            op (callable): A comparison operator function.
            value (various): The value to compare the attribute against.
        """
        self.op = op
        self.value = value

    def __call__(self, approach):
        """
        Evaluate the filter on a single close approach record.

        Args:
            approach (CloseApproach): A close approach data record.

        Returns:
            bool: The result of applying the operator to the attribute and value.
        """
        return self.op(self.get(approach), self.value)

    @classmethod
    def get(cls, approach):
        """
        Retrieve the attribute of interest from a close approach object.

        This method must be overridden by subclasses.

        Args:
            approach (CloseApproach): A close approach data record.

        Raises:
            UnsupportedCriterionError: If the filter criterion is unsupported.
        """
        raise UnsupportedCriterionError("Filter criterion is unsupported.")

class DateFilter(AttributeFilter):
    """Filter close approaches by their approach date."""

    @classmethod
    def get(cls, approach):
        """Return the date of the close approach."""
        return approach.time.date()

class DistanceFilter(AttributeFilter):
    """Filter close approaches by their approach distance."""

    @classmethod
    def get(cls, approach):
        """Return the distance of the close approach."""
        return approach.distance

class VelocityFilter(AttributeFilter):
    """Filter close approaches by their relative velocity."""

    @classmethod
    def get(cls, approach):
        """Return the velocity of the close approach."""
        return approach.velocity

class DiameterFilter(AttributeFilter):
    """Filter close approaches by the diameter of the NEO."""

    @classmethod
    def get(cls, approach):
        """Return the diameter of the NEO involved in the close approach."""
        return approach.neo.diameter

class HazardousFilter(AttributeFilter):
    """Filter close approaches by whether the NEO is potentially hazardous."""

    @classmethod
    def get(cls, approach):
        """Return whether the NEO is potentially hazardous."""
        return approach.neo.hazardous

def create_filters(date=None, start_date=None, end_date=None,
                   distance_min=None, distance_max=None,
                   velocity_min=None, velocity_max=None,
                   diameter_min=None, diameter_max=None,
                   hazardous=None):
    """
    Create a list of filters from provided criteria.

    Args:
        date (date, optional): Specific date to filter.
        start_date (date, optional): Starting date for a date range filter.
        end_date (date, optional): Ending date for a date range filter.
        distance_min (float, optional): Minimum distance of the approach.
        distance_max (float, optional): Maximum distance of the approach.
        velocity_min (float, optional): Minimum velocity of the approach.
        velocity_max (float, optional): Maximum velocity of the approach.
        diameter_min (float, optional): Minimum diameter of the NEO.
        diameter_max (float, optional): Maximum diameter of the NEO.
        hazardous (bool, optional): Filter for potentially hazardous NEO.

    Returns:
        list of AttributeFilter: The list of initialized filter objects.
    """
    filters = []
    if date:
        filters.append(DateFilter(operator.eq, date))
    if start_date:
        filters.append(DateFilter(operator.ge, start_date))
    if end_date:
        filters.append(DateFilter(operator.le, end_date))
    if distance_min:
        filters.append(DistanceFilter(operator.ge, distance_min))
    if distance_max:
        filters.append(DistanceFilter(operator.le, distance_max))
    if velocity_min:
        filters.append(VelocityFilter(operator.ge, velocity_min))
    if velocity_max:
        filters.append(VelocityFilter(operator.le, velocity_max))
    if diameter_min:
        filters.append(DiameterFilter(operator.ge, diameter_min))
    if diameter_max:
        filters.append(DiameterFilter(operator.le, diameter_max))
    if hazardous is not None:
        filters.append(HazardousFilter(operator.eq, hazardous))

    return filters


def limit(iterator, n=None):
    if n is None or n <= 0:
        yield from iterator
    else:
        for i, item in enumerate(iterator):
            if i >= n:
                break
            yield item
