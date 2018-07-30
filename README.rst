Astropy performance benchmarks
==============================

About
-----

This repository includes a set of benchmarks to regularly test the performance of
various parts of the astropy core package. These benchmarks are run for every
new commit in the core package repository and the results are published using a
user-friendly `web interface <http://astropy.org/astropy-benchmarks>`__. The
benchmarks are run using `airspeed velocity <https://asv.readthedocs.io>`__ on
dedicated physical machines belonging to members of the Astropy developer community.

Running the benchmarks locally
------------------------------

If you want to try and run the benchmarks locally you will first need to install asv::

    pip install asv

then clone the benchmarks repository::

    git clone git@github.com:astropy/astropy-benchmarks.git --single-branch
    cd astropy-benchmarks

Note that the ``--single-branch`` option is to avoid downloading the ``results``
branch, which is large.

The easiest/fastest way to try out the benchmarks is to make sure you have
either a stable or a developer version of astropy installed, then run::

    asv dev

This will run the benchmarks against the local astropy version and will do some
basic timing, but the timing will not be very accurate, because this only runs
each benchmark once instead of taking an average of many runs. Nevertheless,
this is the first step to make sure things are running correctly and can still
give order of magnitude timings.

To run asv properly on the latest commit in the upstream astropy master, you can
do::

    asv run

This will set up a temporary environment in which astropy will be installed, and
the benchmark functions will be run multiple times and averaged to get accurate
timings. The results from this will be saved into a ``results/<machine-name>``
directory, which will store one file per commit (or more than one file if the
tests are set up to run for multiple python or numpy versions, which they are
not configured to do by default for Astropy).

You can specify the commit(s) to run the benchmarks for by using the same syntax
as you would for the ``git log`` command. For example, to run the benchmarks for
a single specific commit, you can do::

    asv run 88fbbc33^!

replacing 88fbbc33 by the commit you want to test (the ``^!`` Indicates to just run
this commit, not all commits up to that point). If
you want to run a range of commits, use::

    asv run 827f322b..729abcf3

You can generate a user-friendly web interface for your results locally by
running::

    asv publish
    asv preview

The ``asv preview`` command will give the URL of the local web server (e.g.
http://127.0.0.1:21331) - go to this address in your favorite browser to see
the results.

Writing a benchmark
-------------------

To write a new benchmark, fork this repository and take a look inside the
``benchmarks`` folder - each module in astropy that already has benchmarks has a
corresponding file or directory with files for different parts of the module.
Either add your benchmark to one of the existing files or create a new file as
needed.

A benchmark is a Python function whose name starts with ``time_``. A function
should test as little as possible and therefore be as short/simple as possible.
Any required imports should be done outside the function. Here is an example of
a benchmark to test unit conversion:

.. code-block:: python

    from astropy import units as u

    def time_my_benchmark():
        (u.m / u.s).to(u.km / u.h)

Once you have added a benchmark, you can make sure it runs by installing asv with::

    pip install asv

and running the following in the astropy-benchmarks folder::

    asv dev

This will run all the benchmarks in fast mode (running each function once) using the installed version of Astropy. This is just to make sure that the benchmarks run properly, and the timings should not be considered accurate.

You can select just the benchmark you have written using the ``--bench`` option::

    asv dev --bench time_my_benchmark

Running benchmarks against a local commit
-----------------------------------------

If you are trying to improve the performance of astropy and you have made some
commits in your local repository that you want to test before opening a pull
request to astropy (or before a pull request is merged). To do this, we need
to switch from using the upstream repository to the repository on your computer,
which is done by editing the ``asv.conf.json`` file and finding the following
section::

    // The git URL to the project being tested. Comment the first line
    // and uncomment and edit the second if you are testing local changes.
    "repo": "https://github.com/astropy/astropy.git",
    //"repo": "/your/local/repository/”,

Comment out the first “repo” line and uncomment the second, replacing the path
with the absolute path to your local clone of Astropy. You will then be able to
run the benchmarks for a commit in your local repository using e.g.::

    asv run 827f322b^!

Comparing commits
-----------------

If you want to compare two commits (e.g. the latest upstream commit and a local
commit), you can use e.g.::

    asv compare 88fbbc33 827f322b

This will show a table with a comparison of the benchmark times for the two
commits.

Contributing benchmarks
-----------------------

Once you are happy with your benchmark(s), open a pull request to the
astropy-benchmarks repository. You do not need to add any result files for the
benchmarks - we have machines that automatically do this every night.

A bit more detailed howto to run the benchmarks locally to check performance
improvements is written up in the `following document <https://docs.google.com/document/d/1AoPBAbD8DiDVEM6HuOtPKekN3phtcCF4Qk6pxZ0ID-w/edit?usp=sharing>`__.

Notes to maintainers
--------------------

The ``master`` branch in this repository should not contain any results or built
website. Results should be added to the ``results`` branch, and commits to the
``results`` branch trigger a build to the ``gh-pages`` branch.

.. image:: https://travis-ci.org/astropy/astropy-benchmarks.svg
    :target: https://travis-ci.org/astropy/astropy-benchmarks
