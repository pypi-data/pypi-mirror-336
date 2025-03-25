import importlib
import inspect
import os
from dataclasses import dataclass

from bec_lib.plugin_helper import _get_available_plugins
from qtpy.QtWidgets import QGraphicsWidget, QWidget

from bec_widgets.utils import BECConnector
from bec_widgets.utils.bec_widget import BECWidget


def get_plugin_widgets() -> dict[str, BECConnector]:
    """
    Get all available widgets from the plugin directory. Widgets are classes that inherit from BECConnector.
    The plugins are provided through python plugins and specified in the respective pyproject.toml file using
    the following key:

        [project.entry-points."bec.widgets.user_widgets"]
        plugin_widgets = "path.to.plugin.module"

    e.g.
        [project.entry-points."bec.widgets.user_widgets"]
        plugin_widgets = "pxiii_bec.bec_widgets.widgets"

        assuming that the widgets module for the package pxiii_bec is located at pxiii_bec/bec_widgets/widgets and
        contains the widgets to be loaded within the pxiii_bec/bec_widgets/widgets/__init__.py file.

    Returns:
        dict[str, BECConnector]: A dictionary of widget names and their respective classes.
    """
    modules = _get_available_plugins("bec.widgets.user_widgets")
    loaded_plugins = {}
    print(modules)
    for module in modules:
        mods = inspect.getmembers(module, predicate=_filter_plugins)
        for name, mod_cls in mods:
            if name in loaded_plugins:
                print(f"Duplicated widgets plugin {name}.")
            loaded_plugins[name] = mod_cls
    return loaded_plugins


def _filter_plugins(obj):
    return inspect.isclass(obj) and issubclass(obj, BECConnector)


@dataclass
class BECClassInfo:
    name: str
    module: str
    file: str
    obj: type
    is_connector: bool = False
    is_widget: bool = False
    is_plugin: bool = False


class BECClassContainer:
    def __init__(self):
        self._collection = []

    def add_class(self, class_info: BECClassInfo):
        """
        Add a class to the collection.

        Args:
            class_info(BECClassInfo): The class information
        """
        self.collection.append(class_info)

    @property
    def collection(self):
        """
        Get the collection of classes.
        """
        return self._collection

    @property
    def connector_classes(self):
        """
        Get all connector classes.
        """
        return [info.obj for info in self.collection if info.is_connector]

    @property
    def top_level_classes(self):
        """
        Get all top-level classes.
        """
        return [info.obj for info in self.collection if info.is_plugin]

    @property
    def plugins(self):
        """
        Get all plugins. These are all classes that are on the top level and are widgets.
        """
        return [info.obj for info in self.collection if info.is_widget and info.is_plugin]

    @property
    def widgets(self):
        """
        Get all widgets. These are all classes inheriting from BECWidget.
        """
        return [info.obj for info in self.collection if info.is_widget]

    @property
    def rpc_top_level_classes(self):
        """
        Get all top-level classes that are RPC-enabled. These are all classes that users can choose from.
        """
        return [info.obj for info in self.collection if info.is_plugin and info.is_connector]

    @property
    def classes(self):
        """
        Get all classes.
        """
        return [info.obj for info in self.collection]


def get_custom_classes(repo_name: str) -> BECClassContainer:
    """
    Get all RPC-enabled classes in the specified repository.

    Args:
        repo_name(str): The name of the repository.

    Returns:
        dict: A dictionary with keys "connector_classes" and "top_level_classes" and values as lists of classes.
    """
    collection = BECClassContainer()
    anchor_module = importlib.import_module(f"{repo_name}.widgets")
    directory = os.path.dirname(anchor_module.__file__)
    for root, _, files in sorted(os.walk(directory)):
        for file in files:
            if not file.endswith(".py") or file.startswith("__"):
                continue

            path = os.path.join(root, file)
            subs = os.path.dirname(os.path.relpath(path, directory)).split("/")
            if len(subs) == 1 and not subs[0]:
                module_name = file.split(".")[0]
            else:
                module_name = ".".join(subs + [file.split(".")[0]])

            module = importlib.import_module(f"{repo_name}.widgets.{module_name}")

            for name in dir(module):
                obj = getattr(module, name)
                if not hasattr(obj, "__module__") or obj.__module__ != module.__name__:
                    continue
                if isinstance(obj, type):
                    class_info = BECClassInfo(name=name, module=module_name, file=path, obj=obj)
                    if issubclass(obj, BECConnector):
                        class_info.is_connector = True
                    if issubclass(obj, BECWidget):
                        class_info.is_widget = True
                    if len(subs) == 1 and (
                        issubclass(obj, QWidget) or issubclass(obj, QGraphicsWidget)
                    ):
                        class_info.is_top_level = True
                    if hasattr(obj, "PLUGIN") and obj.PLUGIN:
                        class_info.is_plugin = True
                    collection.add_class(class_info)

    return collection
