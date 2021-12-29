.. image:: https://travis-ci.org/HeinerTholen/Varial.svg?branch=master
    :target: https://travis-ci.org/HeinerTholen/Varial


======
Varial
======


Toolbox for physics analysis with ROOT.

Documentation can be found at:
http://desy.de/~tholenhe/varial_doc/html/index.html


Installation
============


At UHH / DESY
-------------

For everybody with access to the NAF at DESY, Varial is installed under /nfs/dust.
Execute these statements or add them to your ``.bashrc`` file in order to use this
installation::

   export PYTHONPATH=$PYTHONPATH:/nfs/dust/cms/user/tholenhe/installs/varial-stable/Varial
   export PATH=$PATH:/nfs/dust/cms/user/tholenhe/installs/varial-stable/Varial/bin


Everywhere else
---------------

Varial is installed by cloning the git repository. In order to make it work in
your environment, you need to add the Varial base directory to the
``PYTHONPATH`` environment variable and the bin directory to your ``PATH``
variable::

   export PYTHONPATH=$PYTHONPATH:<path-to-Varial>
   export PATH=$PATH:<path-to-Varial>/bin


Basic plotting
==============

In your shell, type ``varial_plotter.py`` (without arguments) to get a
help message on how to specify inputs.


Run systematic uncertainties with SFrame:
=========================================

Copy the script ``varial_example/e04_sframe_uncerts.py`` and change it to your needs.


hQuery
======

Interactive event selection and plotting, driven with Apache Spark.

.. image:: https://raw.githubusercontent.com/HeinerTholen/Varial/master/docs/sc_hQuery.png
