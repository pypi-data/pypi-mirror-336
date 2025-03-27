"""
A module for implementing a base class for Udalmap.
"""

import requests


class UdalMap:
    """Implement all available GET queries in Udalmap API.

    Attributes
    ----------
    timeout : float, optional
        Timeout for requests, in seconds
    """
    BASE_URI = "https://api.euskadi.eus/udalmap"
    HEADERS = {"accept": "application/json"}
    TIMEOUT = 5

    def __init__(self, timeout=None):
        self.timeout = timeout if timeout is not None else UdalMap.TIMEOUT

    def _get_complete_url(self, path):
        return f"{UdalMap.BASE_URI}/{path}"

    def _request(self, path, params=None):
        url = self._get_complete_url(path)

        response = requests.get(url,
                                params=params,
                                headers=UdalMap.HEADERS,
                                timeout=self.timeout
                                )
        response.raise_for_status()
        response.encoding = "utf-8"
        return response.json()

    def groups(self, **kwargs):
        """Find all groups.

        Parameters
        ----------
        **kwargs
            lang: {"SPANISH", "BASQUE"}
            summarized: {"false", "true"}

        Returns
        -------
        list of dict
            Representation of the JSON returned from the API.
        """
        path = "groups"
        return self._request(path, kwargs)

    def group(self, groupId, **kwargs):
        """Get a group.

        Parameters
        ----------
        groupId : str
            The id number of the group
        **kwargs
            lang: {"SPANISH", "BASQUE"}
            summarized: {"false", "true"}

        Returns
        -------
        dict
            Representation of the JSON returned from the API.
        """
        path = f"groups/{groupId}"
        return self._request(path, kwargs)

    def subgroups(self, **kwargs):
        """Find subgroups of all groups.

        Parameters
        ----------
        **kwargs
            lang: {"SPANISH", "BASQUE"}
            summarized: {"false", "true"}

        Returns
        -------
        list of dict
            Representation of the JSON returned from the API.
        """
        path = "subgroups"
        return self._request(path, kwargs)

    def subgroup(self, subgroupId, **kwargs):
        """Get a subgroup.

        Parameters
        ----------
        subgroupId : str
            The id number of the subgroup
        **kwargs
            lang: {"SPANISH", "BASQUE"}
            summarized: {"false", "true"}

        Returns
        -------
        dict
            Representation of the JSON returned from the API.
        """
        path = f"subgroups/{subgroupId}"
        return self._request(path, kwargs)

    def group_subgroups(self, groupId, **kwargs):
        """Find all subgroups of a group.

        Parameters
        ----------
        groupId : str
            The id number of the group
        **kwargs
            lang: {"SPANISH", "BASQUE"}
            summarized: {"false", "true"}

        Returns
        -------
        dict
            Representation of the JSON returned from the API.
        """
        path = f"groups/{groupId}/subgroups"
        return self._request(path, kwargs)

    def indicators(self, **kwargs):
        """Find all indicators.

        Parameters
        ----------
        **kwargs
            lang: {"SPANISH", "BASQUE"}

        Returns
        -------
        list of dict
            Representation of the JSON returned from the API.
        """
        path = "indicators"
        return self._request(path, kwargs)

    def subgroup_indicators(self, subgroupId, **kwargs):
        """Find all indicators of a subgroup.

        Parameters
        ----------
        subgroupId : str
            The id number of the subgroup
        **kwargs
            lang: {"SPANISH", "BASQUE"}
            summarized: {"false", "true"}

        Returns
        -------
        list of dict
            Representation of the JSON returned from the API.
        """
        path = f"subgroups/{subgroupId}/indicators"
        return self._request(path, kwargs)

    def municipality_indicators_data(self, municipalityId, **kwargs):
        """Find indicators' data for a municipality.

        Parameters
        ----------
        municipalityId : str
            The id number of the municipality
        **kwargs
            lang: {"SPANISH", "BASQUE"}

        Returns
        -------
        dict
            Representation of the JSON returned from the API.
        """
        path = f"indicators/municipalities/{municipalityId}"
        return self._request(path, kwargs)

    def indicator_data(self, indicatorId, **kwargs):
        """Get an indicator data.

        Parameters
        ----------
        indicatorId : str
            The id number of the indicator
        **kwargs
            lang: {"SPANISH", "BASQUE"}

        Returns
        -------
        dict
            Representation of the JSON returned from the API.
        """
        path = f"indicators/{indicatorId}"
        return self._request(path, kwargs)

    def indicator_entities_data(self, indicatorId, **kwargs):
        """Get indicators' data for all entities.

        Parameters
        ----------
        indicatorId : str
            The id number of the indicator
        **kwargs
            lang: {"SPANISH", "BASQUE"}

        Returns
        -------
        dict
            Representation of the JSON returned from the API.
        """
        path = f"indicators/{indicatorId}/entities"
        return self._request(path, kwargs)

    def indicator_entity_data(self, indicatorId, entityId, **kwargs):
        """Get indicator data of an entity.

        Parameters
        ----------
        indicatorId : str
            The id number of the indicator
        entityId : str
            The id number of the entity
        **kwargs
            lang: {"SPANISH", "BASQUE"}

        Returns
        -------
        dict
            Representation of the JSON returned from the API.
        """
        path = f"indicators/{indicatorId}/entities/{entityId}"
        return self._request(path, kwargs)

    def indicator_regions_data(self, indicatorId, **kwargs):
        """Get indicators' data for all regions.

        Parameters
        ----------
        indicatorId : str
            The id number of the indicator
        **kwargs
            lang: {"SPANISH", "BASQUE"}

        Returns
        -------
        dict
            Representation of the JSON returned from the API.
        """
        path = f"indicators/{indicatorId}/regions"
        return self._request(path, kwargs)

    def indicator_region_data(self, indicatorId, regionId, **kwargs):
        """Get indicator data of a region.

        Parameters
        ----------
        indicatorId : str
            The id number of the indicator
        regionId : str
            The id number of the region
        **kwargs
            lang: {"SPANISH", "BASQUE"}

        Returns
        -------
        dict
            Representation of the JSON returned from the API.
        """
        path = f"indicators/{indicatorId}/regions/{regionId}"
        return self._request(path, kwargs)

    def indicator_municipalities_data(self, indicatorId, **kwargs):
        """Get indicators' data for all municipalities.

        Parameters
        ----------
        indicatorId : str
            The id number of the indicator
        **kwargs
            lang: {"SPANISH", "BASQUE"}

        Returns
        -------
        dict
            Representation of the JSON returned from the API.
        """
        path = f"indicators/{indicatorId}/municipalities"
        return self._request(path, kwargs)

    def indicator_municipality_data(self, indicatorId, municipalityId, **kwargs):
        """Get indicator data of a municipality.

        Parameters
        ----------
        indicatorId : str
            The id number of the indicator
        municipalityId : str
            The id number of the municipality
        **kwargs
            lang: {"SPANISH", "BASQUE"}

        Returns
        -------
        dict
            Representation of the JSON returned from the API.
        """
        path = f"indicators/{indicatorId}/municipalities/{municipalityId}"
        return self._request(path, kwargs)
