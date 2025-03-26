###########
sktimeutils
###########
Package ``sktimeutils`` provides a suite of utility functions for manipulating time. Its primary purpose is to convert
scalar and arrays of time objects from one time format to another. The package supports the following time formats

..  list-table::
    :header-rows: 1

    * - Data Type
      - Description
    * - ``datetime``
      - The builtin datetime object supplied with python.
    * - ``numpy.datetime64``
      - The builtin datetime object used by ``numpy``. This datatype is often used when creating arrays of time variables.
    * - ``str``
      - Strings are often convenient to represent time. We assume all strings represent Universal Time and are encoded in an isoformat
    * - ``float``
      - We assume floats are modified julian date (mjd)

The package provides functions that converts one time format to another, but perhaps more usefully, it provides functions
that convert arrays of time values, which are expressed in any one of the above formats, to arrays of time expressed in
the desired format.

We developed this package to handle arrays of Universal Time within scientific data records stored in netcdf files and similar.
As such, the code is focussed on Universal Time and has no provision for handling time zone conversions etc.  Nor do we
attempt to rigorously manage leap-seconds and other earth-rotation issues.

The package also provides functions to convert from ECI/TEME coordinates to ECEF/ITRF coordinate as this is intimately
linked with sidereal time calculations.

.. toctree::
   :maxdepth: 1

   installation
   mjd
   juliandate
   eci


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
