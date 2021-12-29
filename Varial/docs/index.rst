.. Varial documentation master file, created by
   sphinx-quickstart on Tue Nov 20 14:11:41 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.



Varial. Toolkit for analysis with ROOT.
=======================================

This package provides a toolkit for performing a data-analysis with ROOT. No gui,
just library. Varial has a specific focus on the CMS Experiment and has
extensions for running CMSSW jobs.

Varial has two main design features (both leaning on UNIX-principles, sort of):

- **Pipelining of Histograms**: Loading, manipulating, drawing and storing of
  Histograms is a task that cannot be standardized. For any plot you need the
  ability to manipulate data at any stage, e.g. loading a histogram from
  another file, normalize differently, or plot axes in a different color.
  With Python generators, *pipelines* of manipulation tools are setup for
  histogram data, making it possible to exchange a manipulation function at
  many stages.

  For standard-operations on histograms -- such as sum, division, stack and
  many more -- a history is created that lets you track all operations that
  where applied to a given histogram.

- **Directory-based execution of analysis steps**: As an analysis comprises
  many different parts, a framework is set inplace to design an analysis
  quickly. In order to perform a step, e.g. stacking histograms or performing a
  fit, a subclass of Tool (``varial.tools.Tool``) has to be created.

  Every tool has its own output directory, in which results are automatically
  stored. Tools can be put into toolchain, which are also represented by
  directories, thus creating an organized directory structure of all results.


Furthermore, there are many utility functions with reasonable default settings.
These help to get to first results fast. Starting from first results,
everything can be customized up to publication-ready plots.

See :ref:`getting-started` for installation and running examples.


Contents:

.. toctree::
   :maxdepth: 2

   getting-started.rst
   examples.rst
   api-reference.rst



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


(The original "Varial": https://www.youtube.com/watch?v=X0dxKbJ08d4)
