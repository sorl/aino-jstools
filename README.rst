============
aino-jstools
============

aino-jstools is a set of tools for working with JavaScript and Django.
Primarily it compiles javascripts.


Design background
-----------------
We wanted to make a tool that made including a bunch of JavaScripts in a
template easy and clean and compiling all those JavaScripts into packed pieces
in production for optimal performance. The other goal we wanted to achive was
to expose urls defined in ``urls.py``, ``MEDIA_URL``, ``DEBUG`` settings to
JavaScript code. Our future includes making a cleaner implementation for i18n
in JavaScript than the one provided by Django.


Requirements
------------
- Django 1.x
- Python 2.5+
- Java (for compiling JavaScripts)


Install
-------
Include ``jstools`` in ``INSTALLED_APPS`` in your project settings.
Optionally include the jstools/urls.py in your ``urls.py``::

   (r'^jstools/', include('jstools.urls'))


Template usage
--------------
First define your scripts in a template as follows::

    {% scripts "js/mysite-min.js" %}
        http://yui.yahooapis.com/3.1.0/build/yui/yui-min.js
        js/a.js
        js/b.js
        {% url jshelper %}
    {% endscripts %}

When ``settings.DEBUG`` is ``True`` this will translate to::

    <script src="http://yui.yahooapis.com/3.1.0/build/yui/yui-min.js"></script>
    <script src="{{ MEDIA_URL }}js/a.js"></script>
    <script src="{{ MEDIA_URL }}js/b.js"></script>
    <script src="{% url jshelper %}"></script>

When ``settings.DEBUG`` is ``False`` this will translate to::

    <script src="{{ MEDIA_URL }}js/mysite-min.js?TIMESTAMP"></script>

where ``TIMESTAMP`` is based on modification date of
``{{ MEDIA_ROOT }}js/myste-min.js``


Compiling
---------
Compiling all defined scripts is as simple as running::

    python manage.py buildjs

If you are using the default ``filesystem`` and/or
``app_directories`` this management command will find all templates with
``{% scripts %}`` tags and compile its contents into the first argument of the
tag.


jshelper view
-------------
This view will output named urls, ``settings.MEDIA_URL``, ``settings.DEBUG``
(I suggest you override this in your template unless you want to recompile the
script when you change your ``DEBUG`` setting) for use in your JavaScript code. You
will have access to a JavaScript object named ``JSTOOLS`` by default, you can
change the name by setting ``JSTOOLS_NAMESPACE``.

``JSTOOLS.settings.MEDIA_URL``
    ``settings.MEDIA_URL``

``JSTOOLS.settings.DEBUG``
    ``settings.DEBUG``

``JSTOOLS.get_url``
    This function will get named urls defined in your ``urls.py``. First argument is
    the name of the named url, subsequent arguments are arguments passed to that
    pattern. Examples::

        JSTOOLS.get_url('jshelper');
        JSTOOLS.get_url('blog_entry', 2010, 04, 25, 'aino-jstools');

