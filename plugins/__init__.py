import importlib

def import_plugins(plugins):
    d = {}
    for plugin in plugins:
        plugin_lib = importlib.import_module(plugin)
        plugin_class = plugin_lib.Plugin
        d[plugin_class.plugin_id] = plugin_class
    return d
