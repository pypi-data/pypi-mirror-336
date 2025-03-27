import collections
import logging
from enum import Enum
from typing import Any, Iterator

import pandas as pd
from textual import on
from textual.app import ComposeResult
from textual.containers import Grid
from textual.widget import Widget
from textual.widgets import Select
from textual_plotext import PlotextPlot


class PlotType(Enum):
    HISTOGRAM = 'Histogram'


class XnatPlot(Widget):
    DEFAULT_CSS = """
    XnatPlot {
        width: 1fr;
        height: 1fr;
    }
    
    #plot_grid {
        grid-size: 3;
        grid-rows: auto 1fr;
        grid-columns: 1fr 1fr 1fr;
    }

    #plotext_plot {
        column-span: 3;
    }
    """

    def __init__(self, logger: logging.Logger, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.logger = logger
        self.data: pd.DataFrame = pd.DataFrame()

    def compose(self) -> ComposeResult:
        plot_types = [(x.value, x.value) for x in PlotType]

        with Grid(id='plot_grid'):
            yield Select(plot_types, id='plot_type', prompt='Plot type', value=PlotType.HISTOGRAM.value)
            yield Select([], id='x_axis', prompt='X-axis')
            yield Select([], id='y_axis', prompt='Y-axis')
            yield PlotextPlot(id='plotext_plot')

    def update_x_axis(self, values: Iterator[str]) -> None:
        x_axis = self.query_one('#x_axis', Select)
        x_axis.set_options((x, x) for x in values)

    def update_y_axis(self, values: Iterator[str]) -> None:
        y_axis = self.query_one('#y_axis', Select)
        y_axis.set_options((y, y) for y in values)

    def set_data(self, data: pd.DataFrame) -> None:
        self.data = data
        if self.data is None:
            return
        self.update_x_axis(self.data.columns)

    @on(Select.Changed, '#x_axis')
    def axis_changed(self, _: Select.Changed) -> None:
        match PlotType(self.query_one('#plot_type', Select).value):
            case PlotType.HISTOGRAM:
                self._plot_histogram()

    def _plot_histogram(self) -> None:
        x_axis = self.query_one('#x_axis', Select).value
        histogram = collections.Counter(self.data[x_axis].to_list())
        plotextplot = self.query_one('#plotext_plot', PlotextPlot)
        plt = plotextplot.plt
        plt.clear_figure()
        plt.title(f'Histogram plot of "{x_axis}"')
        x_values, y_values = zip(*histogram.items())
        plt.bar(x_values, y_values)
        plotextplot.refresh()
