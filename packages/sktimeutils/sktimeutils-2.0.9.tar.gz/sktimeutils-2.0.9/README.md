# sktimeutils
This package provides Universal Time conversion functions used by the usask-arg group. The
code tries to be friendly for arrays, sequences and scalars. This package currently supports UT time expressed as strings,
modified julian dates expressed as floats, Python DateTime and numpy Datetime64. We typically use the package to process  
arrays of measurement times read in from data records stored in netcdf files or similar. The code is focussed on Universal Time 
and has no provision for handling time zone conversions etc.  Nor do we attempt to rigorously manage leap-seconds and 
other earth-rotation issues. 

## Installation
    
    pip install sktimeutils

We recommend running the unit tests, see below, after installation to download Earth rotation data files.

### Building a wheel
The python wheel can also be built from source code,

    conda install setuptools build
    python -m build --wheel

## Usage
Documentation can be found at ReadTheDocs [sktimeutils](https://sktimeutils.readthedocs.io/en/latest/index.html)

## Unit Tests
It is useful to run the unit tests as the tests will automatically download leap-second files and earth rotation 
information. Needless to say you must have an internet connection to successfully run the unit tests 

    python -m unittest discover -s sktimeutils.tests

## License
This project is licensed under the MIT license.




