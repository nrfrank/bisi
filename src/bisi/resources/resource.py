
from typing import Type


class Resource:
    resources = list()

    def __init__(self):
        """A base class for all resources and is also responsible for gathering all the created resources"""
        self.resources.append(self)

    @classmethod
    def get_resources(cls, resource_type: Type = None, name: str = None):
        """Returns the created resources

        Args:
            resource_type: optionally filter by a resource type
            name: optionally filter by a name
        """
        resources = cls.resources
        if resource_type:
            resources = list(filter(lambda x: isinstance(x, resource_type), resources))
        if name:
            resources = list(filter(lambda x: x.name == name, resources))

        return resources

    @classmethod
    def clear_resources(cls):
        """Clears the internal list of resources"""
        cls.resources = list()
