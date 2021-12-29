.. _getting-started:

===============
Getting started
===============

Prerequisites
=============


For the efficient use of the histogram manipulation tools, knowledge about
python generators and generator expressions is kind of crucial. A nice guide
with practical application can be found at
http://www.dabeaz.com/generators/index.html
and also at 
http://anandology.com/python-practice-book/iterators.html
. Furthermore, the itertools package, at
http://docs.python.org/2/library/itertools.html
, is of great help.

- Root is needed: http://root.cern.ch
- CMSSW is optional


Installation
============

Installation is simple::

    git clone https://github.com/HeinAtCERN/Varial.git

Add this to your ``.bashrc`` or ``.bash_profile``::

    export PYTHONPATH=<your_path_to_varial>:$PYTHONPATH

**DISCLAIMER: The API is under permanent construction.** In order to ensure you
can always get back to the Varial version you've build against, you should
copy the ``pre-commit`` script in the Varial base directory to ``.git/hooks``
in your own project. Make sure to add the correct path to Varial into the
``pre-commit`` script. For every commit that you now do, the script will put a
``VARIAL_VERSION`` file with the version hash of Varial into your project
directory and commit it as well. You can later rollback Varial by changing into
its directory and issuing::

    git checkout <version hash here>


The real 'Getting Started'
==========================

Here's a simple list of points about central principles in Varial:

- No histogram, graph or canvas flies around independently. They are
  all wrapped in python objects that store meta information about them, e.g.
  name, title, is_data, lumi, sample name, legend string, and more.
  Here's the module with the Wrapper definitions: :ref:`wrapper-module`.

- Operations can be applied to wrapped histograms or iterables of them,
  manipulating them or forming new ones, e.g. rebin, sum, stack, and others.
  For better debuggability, operations are tracked in a history-object on each
  wrapper. The history can be printed onscreen or be outputted as you like.
  See :ref:`operations-module`.

- Since operations can only handle individual histogram wrappers, the
  generators module helps on streamlining the operations. Generators can be
  connected like unix-pipes and allow for efficient code.
  A lot of handy functions can be found in the :ref:`generators-module`.

- But for building up an anaylsis, more is needed than handy functions: Tools
  and toolchains provide a frame for every step in an analysis. Both create a
  directory structure on the harddisk were all intermediate results are
  stored. These intermediate results can be looked up by any following tool
  with a simple function call.
  By default, results of previous executions are reloaded if present on disk.
  The examples :ref:`make-a-tool-example` and :ref:`make-a-toolchain-example`
  show how to create and use tools and toolchains. All predefined tools are
  collected in :ref:`tools-module`.

- For completeness, :ref:`analysis-module`, :ref:`settings-module` and
  :ref:`sample-module` provide options to configure Varial.

- There are examples: :ref:`examples-package`.


Finally:
========

Feedback is very welcome, and so are pull-requests. The best place to ask a
question or to discuss a bug is probably the issues section at github,
https://github.com/HeinAtCERN/Varial/issues
, or asking me directly.

Again: Generators super important,
http://www.dabeaz.com/generators/index.html
, as much as living and breathing in the consciousness of the Zen of Python,
https://www.python.org/dev/peps/pep-0020/
.

