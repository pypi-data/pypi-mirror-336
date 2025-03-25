import os

from qtpy.QtWidgets import QVBoxLayout

from bec_widgets.qt_utils.error_popups import SafeSlot as Slot
from bec_widgets.qt_utils.settings_dialog import SettingWidget
from bec_widgets.utils import UILoader
from bec_widgets.utils.widget_io import WidgetIO


class AxisSettings(SettingWidget):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)

        current_path = os.path.dirname(__file__)
        self.ui = UILoader().load_ui(os.path.join(current_path, "axis_settings.ui"), self)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.ui)

        # Hardcoded values for best appearance
        self.setMinimumHeight(280)
        self.setMaximumHeight(280)
        self.resize(380, 280)

    @Slot(dict)
    def display_current_settings(self, axis_config: dict):

        if axis_config == {}:
            return

        # Top Box
        WidgetIO.set_value(self.ui.plot_title, axis_config["title"])
        self.ui.switch_outer_axes.checked = axis_config["outer_axes"]

        # X Axis Box
        WidgetIO.set_value(self.ui.x_label, axis_config["x_label"])
        WidgetIO.set_value(self.ui.x_scale, axis_config["x_scale"])
        WidgetIO.set_value(self.ui.x_grid, axis_config["x_grid"])
        if axis_config["x_lim"] is not None:
            WidgetIO.check_and_adjust_limits(self.ui.x_min, axis_config["x_lim"][0])
            WidgetIO.check_and_adjust_limits(self.ui.x_max, axis_config["x_lim"][1])
            WidgetIO.set_value(self.ui.x_min, axis_config["x_lim"][0])
            WidgetIO.set_value(self.ui.x_max, axis_config["x_lim"][1])
        if axis_config["x_lim"] is None:
            x_range = self.target_widget.fig.widget_list[0].plot_item.viewRange()[0]
            WidgetIO.set_value(self.ui.x_min, x_range[0])
            WidgetIO.set_value(self.ui.x_max, x_range[1])

        # Y Axis Box
        WidgetIO.set_value(self.ui.y_label, axis_config["y_label"])
        WidgetIO.set_value(self.ui.y_scale, axis_config["y_scale"])
        WidgetIO.set_value(self.ui.y_grid, axis_config["y_grid"])
        if axis_config["y_lim"] is not None:
            WidgetIO.check_and_adjust_limits(self.ui.y_min, axis_config["y_lim"][0])
            WidgetIO.check_and_adjust_limits(self.ui.y_max, axis_config["y_lim"][1])
            WidgetIO.set_value(self.ui.y_min, axis_config["y_lim"][0])
            WidgetIO.set_value(self.ui.y_max, axis_config["y_lim"][1])
        if axis_config["y_lim"] is None:
            y_range = self.target_widget.fig.widget_list[0].plot_item.viewRange()[1]
            WidgetIO.set_value(self.ui.y_min, y_range[0])
            WidgetIO.set_value(self.ui.y_max, y_range[1])

    @Slot()
    def accept_changes(self):
        title = WidgetIO.get_value(self.ui.plot_title)
        outer_axes = self.ui.switch_outer_axes.checked

        # X Axis
        x_label = WidgetIO.get_value(self.ui.x_label)
        x_scale = self.ui.x_scale.currentText()
        x_grid = WidgetIO.get_value(self.ui.x_grid)
        x_lim = (WidgetIO.get_value(self.ui.x_min), WidgetIO.get_value(self.ui.x_max))

        # Y Axis
        y_label = WidgetIO.get_value(self.ui.y_label)
        y_scale = self.ui.y_scale.currentText()
        y_grid = WidgetIO.get_value(self.ui.y_grid)
        y_lim = (WidgetIO.get_value(self.ui.y_min), WidgetIO.get_value(self.ui.y_max))

        self.target_widget.set(
            title=title,
            x_label=x_label,
            x_scale=x_scale,
            x_lim=x_lim,
            y_label=y_label,
            y_scale=y_scale,
            y_lim=y_lim,
        )
        self.target_widget.set_grid(x_grid, y_grid)
        self.target_widget.set_outer_axes(outer_axes)
