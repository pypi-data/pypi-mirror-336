CGC circle plot
==================

.. click:: dbcan.main:cli
   :prog: run_dbcan
   :commands: cgc_circle_plot
   :nested: full

CGC circle plot is a tool to visualize the CGC results. It generates a circular plot showing the distribution of CAZymes and CGCs across the genome.
It requires the output from CGCFinder and CAZyme annotation tools.

Usage Examples
----------------
Generate CGC circle plot (need run cgc_finder and CGCFinder first, or could run easy_CGC directly)

.. code-block:: bash

   run_dbcan cgc_circle_plot --output_dir test
