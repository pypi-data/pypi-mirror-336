"""
A module for implementing convenient classes to get info from udalmap API.
"""

from .base import UdalMap
import pandas as pd
import matplotlib.pyplot as plt


class UdmDf(UdalMap):
    """Get Udalmap API info into Pandas dataframes.

    Attributes
    ----------
    timeout : float, optional
        Timeout for requests, in seconds

    """
    BODIES = {"entities", "regions", "municipalities"}

    def __init__(self, timeout=None):
        UdalMap.__init__(self, timeout=timeout)
        self.indicatorids = self._indicatorids()

    def _indicatorids(self):
        return {indicator["id"] for indicator in self.indicators()}

    def _raise_input_errors(self, indicatorId, body):
        if not isinstance(indicatorId, str):
            raise TypeError(
                f"str expected for indicatorId, got '{type(indicatorId).__name__}'")
        if indicatorId not in self.indicatorids:
            raise ValueError(
                f"indicator id should be one of these: {self.indicatorids}")
        if body not in UdmDf.BODIES:
            raise ValueError(
                f"body should be one of these: {UdmDf.BODIES}, got '{body}'")

    def find(self):
        """Provide all groups, subgroups and indicators.

        Returns
        -------
        pd.DataFrame
            A Pandas dataframe.
        """
        groups = self.groups()

        group_ls, subgroup_ls, indicator_ls = [], [], []
        for group in groups:
            for subgroup in group["subgroups"]:
                for indicator in subgroup["indicators"]:
                    indicator_ls.append(
                        f"{indicator["id"]}: {indicator["name"]}")
                    subgroup_ls.append(f"{subgroup["id"]}: {subgroup["name"]}")
                    group_ls.append(f"{group["id"]}: {group["name"]}")

        return pd.DataFrame({"group": group_ls,
                             "subgroup": subgroup_ls,
                             "indicator": indicator_ls})

    def get(self, indicatorId, body):
        """Provide an indicator's data for a body.

        Parameters
        ----------
        indicatorId : str
            The id number of the indicator
        body : {"entities", "regions", "municipalities"}
            The body of which to retrieve the indicator data

        Returns
        -------
        pd.DataFrame
            A Pandas dataframe.
        """
        self._raise_input_errors(indicatorId, body)

        data = self.indicator_data(indicatorId)

        names, years = [], []
        for item in data[body]:
            names.append(item["name"])
            years.append(item["years"][0])

        return pd.DataFrame(years, index=names)

    def plot(self, indicatorId, body, filters=None):
        """Plot an indicator data for a body with filters.

        Parameters
        ----------
        indicatorId : str
            The id number of the indicator
        body : {"entities", "regions", "municipalities"}
            The body of which to retrieve the indicator data
        filters : list of str, optional
            Selects the items to plot

        Returns
        -------

            Plots a Matplotlib plot.
        """
        self._raise_input_errors(indicatorId, body)

        df = self.get(indicatorId, body)
        if filters is not None:
            if not isinstance(filters, list):
                raise TypeError(
                    f"list type expected for filters, got '{type(filters).__name__}'")
            for item in filters:
                if item not in df.index:
                    raise ValueError(
                        f"filter item '{item}' is not in {list(df.index)}")
            df = df.loc[filters, :]

        lookup_name = {item["id"]: item["name"] for item in self.indicators()}

        fig, ax = plt.subplots()
        df.transpose().plot(ax=ax)
        ax.set_title(f"{indicatorId}: {lookup_name[indicatorId]}")
        plt.show()
