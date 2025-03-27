from lightningchart.series import Series2D, ComponentWithPaletteColoring
from lightningchart.charts import Chart
from lightningchart import Themes


class ParallelCoordinateSeries(Series2D, ComponentWithPaletteColoring):
    """Represents a single series within a ParallelCoordinateChart.

    This series is associated with one ParallelCoordinateChart and is used to visualize data across the chart's axes.
    """

    def __init__(
        self,
        chart: Chart,
        theme: Themes = Themes.Light,
        name: str = None,
    ):
        """
        Initialize a ParallelCoordinateSeries.

        Args:
            chart (Chart): The parent ParallelCoordinateChart to which this series belongs.
            theme (Themes): The theme of the series, default is `Themes.White`.
            name (str, optional): The name of the series. Defaults to None.
        """

        Series2D.__init__(self, chart)
        self.instance.send(
            self.id,
            'addSeries',
            {
                'chart': self.chart.id,
                'theme': theme.value,
                'name': name,
            },
        )

    def set_name(self, name: str):
        """
        Set the name of the series.

        The name is displayed in the legend and other components where the series is referenced.

        Args:
            name (str): The name to assign to the series.

        Returns:
            The instance of the series for fluent interface.
        """
        self.instance.send(self.id, 'setName', {'name': name})
        self.name = name
        return self

    def set_data(self, data: dict[str, float]):
        """
        Set data points for the series.

        Data is provided as a dictionary mapping axis names to values. Each axis name must match the axes defined
        in the associated ParallelCoordinateChart.

        Args:
            data (dict[str, float]): A dictionary where the keys are axis names and the values are the corresponding data values.

        Returns:
            The instance of the series for fluent interface.
        """
        self.data = data
        self.instance.send(self.id, 'setData', {'data': data})
        return self

    def get_data(self) -> dict[str, float] | None:
        """
        Retrieve the data of the series.

        The data is returned as a dictionary mapping axis names to their corresponding values.

        Returns:
            dict[str, float] | None: A dictionary of axis-value pairs if data is set, otherwise None.
        """
        return self.data
