Astropy performance benchmarks
==============================

About
-----

These benchmarks track the performance of various features in astropy
*over time*.

To view them, visit `this site
<http://astropy.org/astropy-benchmarks>`__.

The benchmarks are run using `airspeed velocity
<https://asv.readthedocs.io>`__.

Contributing a benchmark
------------------------

To add a benchmark, fork this repository and take a look inside the ``benchmarks`` folder - each module in astropy that
already has benchmarks has a corresponding file or directory with files for different parts of the module. Either add
your benchmark to one of the existing files or create a new file as needed.

A benchmark is a Python function whose name starts with ``time_``. A function should test as little as possible and therefore
be as short/simple as possible. Any required imports should be done outside the function. Here is an example of a benchmark to
test unit conversion:

.. code-block:: python

    from astropy import units as u

    def time_my_benchmark():
        (u.m / u.s).to(u.km / u.h)

Once you have added a benchmark, you can make sure it runs by installing asv with::

    pip install asv

and running the following in the astropy-benchmarks folder::

    asv dev

This will run all the benchmarks in fast mode (running each function once) using the installed version of Astropy. This is just to make sure that the benchmarks run properly, and the timings should not be considered accurate.

To run a single benchmark, you can do e.g.::

    asv dev --bench time_my_benchmark

Once you are happy with your benchmarks, open a pull request to the astropy-benchmarks repository.

You do not need to add any result files for the benchmarks - we have machines that automatically do this every night.

A bit more detailed howto to run the benchmarks locally to check performance
improvements is written up in the `following document <https://docs.google.com/document/d/1AoPBAbD8DiDVEM6HuOtPKekN3phtcCF4Qk6pxZ0ID-w/edit?usp=sharing>`__.

Notes to maintainers
--------------------

The ``master`` branch in this repository should not contain any results or built website. Results should be added to the ``results`` branch, and commits to the ``results`` branch trigger a build to the ``gh-pages`` branch.

.. image:: https://travis-ci.org/astropy/astropy-benchmarks.svg
    :target: https://travis-ci.org/astropy/astropy-benchmarks
