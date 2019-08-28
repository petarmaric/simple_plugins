About
=====

A simple plugin framework inspired by the `work of Marty Alchin`_. 

`Continuous integration`_ is powered by `Jenkins`_.

.. image:: http://ci.petarmaric.com/job/simple_plugins/badge/icon
   :target: http://ci.petarmaric.com/job/simple_plugins/

.. _`work of Marty Alchin`: http://martyalchin.com/2008/jan/10/simple-plugin-framework/
.. _`Continuous integration`: http://ci.petarmaric.com/job/simple_plugins/
.. _`Jenkins`: https://jenkins-ci.org/


Installation
============

To install simple_plugins run::

    $ pip install simple_plugins


Usage examples
==============

Quick start::

    >>> from simple_plugins import PluginMount
     
    >>> class BaseHttpResponse(object):
    ...     """Mount point is not registered as a plugin"""
    ...     
    ...     status_code = None
    ...     
    ...     __metaclass__ = PluginMount
    ...     
    ...     class Meta:
    ...         id_field = 'status_code'
    ...     
    ...     def __repr__(self):
    ...         return "<%s: %s>" % (self.__class__.__name__, self.status_code)
    ...     
    
    >>> class OK(BaseHttpResponse):
    ...     status_code = 200
    ...     
     
    >>> class BaseRedirection(BaseHttpResponse):
    ...     """'Base*' classes are not registered as plugins"""
    ...     pass
    ...     
    
    >>> class MovedPermanently(BaseRedirection):
    ...     status_code = 301
    ...     
    
    >>> class NotModified(BaseRedirection):
    ...     status_code = 304
    ...     
    
    >>> class BadRequest(BaseHttpResponse):
    ...     status_code = 400
    ...     
    
    >>> class NotFound(BaseHttpResponse):
    ...     status_code = 404
    ...     
    
    # All plugin info
    >>> BaseHttpResponse.plugins.keys()
    ['valid_ids', 'instances_sorted_by_id', 'id_to_class', 'instances',
     'classes', 'class_to_id', 'id_to_instance']
    
    # Plugin info can be accessed using either dict...
    >>> BaseHttpResponse.plugins['valid_ids']
    set([304, 400, 404, 200, 301])
    
    # ... or object notation
    >>> BaseHttpResponse.plugins.valid_ids
    set([304, 400, 404, 200, 301])
    
    >>> BaseHttpResponse.plugins.classes
    set([<class '__main__.NotFound'>, <class '__main__.OK'>,
         <class '__main__.NotModified'>, <class '__main__.BadRequest'>,
         <class '__main__.MovedPermanently'>])
    
    >>> BaseHttpResponse.plugins.id_to_class[200]
    <class '__main__.OK'>
    
    >>> BaseHttpResponse.plugins.id_to_instance[200]
    <OK: 200>
    
    >>> BaseHttpResponse.plugins.instances_sorted_by_id
    [<OK: 200>, <MovedPermanently: 301>, <NotModified: 304>, <BadRequest: 400>, <NotFound: 404>]
    
    # Unregister the `NotFound` plugin
    >>> NotFound._unregister_plugin()
    >>> BaseHttpResponse.plugins.instances_sorted_by_id
    [<OK: 200>, <MovedPermanently: 301>, <NotModified: 304>, <BadRequest: 400>]
    
    # Coerce the passed value into the right instance
    >>> BaseHttpResponse.coerce(200)
    <OK: 200>

Please see `the tests`_, `beam_integrals`_ and `splatex`_ source code for more
examples.

.. _`the tests`: https://bitbucket.org/petar/simple_plugins/src/default/tests.py
.. _`beam_integrals`: http://bitbucket.org/petar/beam_integrals/src/
.. _`splatex`: http://bitbucket.org/petar/splatex/src/


Contribute
==========

If you find any bugs, or wish to propose new features `please let me know`_. 

If you'd like to contribute, simply fork `the repository`_, commit your changes
and send a pull request. Make sure you add yourself to `AUTHORS`_.

.. _`please let me know`: https://bitbucket.org/petar/simple_plugins/issues/new
.. _`the repository`: http://bitbucket.org/petar/simple_plugins
.. _`AUTHORS`: https://bitbucket.org/petar/simple_plugins/src/default/AUTHORS
