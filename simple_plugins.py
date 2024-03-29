from warnings import warn


__version__ = '1.0.3'


class PerformanceWarning(UserWarning):
    """Warning issued when something causes a performance degradation"""


class CoercionError(Exception):
    """The given value can't be coerced to a valid instance"""


# From http://stackoverflow.com/questions/224026/javascript-style-dot-notation-for-dictionary-keys-unpythonic
class AttrDict(dict):
    __getattr__= dict.__getitem__
    __setattr__= dict.__setitem__
    __delattr__= dict.__delitem__


# Based on `django.db.models`, http://djangosnippets.org/snippets/542/
class PluginMount(type):
    def __init__(cls, name, bases, attrs): #@UnusedVariable
        if not hasattr(cls, '_plugin_registry'):
            # This branch only executes when processing the mount point itself.
            # So, since this is a new plugin type, not an implementation, this
            # class shouldn't be registered as a plugin. Instead, it sets up a
            # list where plugins can be registered later.
            cls._plugin_registry = []

            meta = getattr(cls, 'Meta', object())
            def override_options(options):
                return dict(
                    (name, getattr(meta, name, default_value))
                    for name, default_value in options.items()
                )

            cls._meta = AttrDict(_base_class=cls)
            cls._meta.update(override_options({
                'id_field': 'id',
                'id_field_coerce': int,
            }))
        else:
            # Don't register 'Base*' classes as plugin implementations
            if not name.startswith('Base'):
                # This must be a plugin implementation, which should be registered.
                # Simply appending it to the list is all that's needed to keep
                # track of it later.
                cls._plugin_registry.append(cls)

        base_cls = cls._meta._base_class
        base_cls._plugins = None # Clear plugin cache

    def _unregister_plugin(self):
        base_cls = self._meta._base_class
        base_cls._plugin_registry.remove(self)
        base_cls._plugins = None # Clear plugin cache

    @property
    def plugins(self):
        base_cls = self._meta._base_class
        if base_cls._plugins is None:
            x = AttrDict()
            x.classes = set(self._plugin_registry)
            x.instances = set(cls() for cls in x.classes)
            x.id_to_instance = dict((getattr(obj, self._meta.id_field), obj) for obj in x.instances)
            x.id_to_class = dict((k, type(v)) for k, v in x.id_to_instance.items())
            x.class_to_id = dict((v, k) for k, v in x.id_to_class.items())
            x.instances_sorted_by_id = [v for _, v in sorted(x.id_to_instance.items())]
            x.valid_ids = set(x.id_to_instance)

            if hasattr(base_cls, '_contribute_to_plugins'):
                base_cls._contribute_to_plugins(_plugins=x)

            base_cls._plugins = x

        return base_cls._plugins

    def coerce(self, value):
        """Coerce the passed value into the right instance"""
        perf_warn_msg = "Creating too many %s instances may be expensive, passing "\
                        "the objects id is generally preferred" % self._meta._base_class

        # Check if the passed value is already a `_base_class` instance
        if isinstance(value, self._meta._base_class):
            warn(perf_warn_msg, category=PerformanceWarning)
            return value # No coercion needed

        # Check if the passed value is a `_base_class` subclass
        try:
            if issubclass(value, self._meta._base_class):
                warn(perf_warn_msg, category=PerformanceWarning)
                return value()
        except TypeError:
            pass # Passed value is not a class

        # Check if the passed value is a valid object id
        try:
            object_id = self._meta.id_field_coerce(value)
            try:
                return self.plugins.id_to_instance[object_id]
            except KeyError:
                raise CoercionError("%d is not a valid object id" % object_id)
        except (TypeError, ValueError):
            pass # Passed value can't be coerced to the object id type

        # Can't coerce an unknown type
        raise CoercionError("Can't coerce %r to a valid %s instance" % (
            value, self._meta._base_class)
        )
