=====================================
Ernestas_Monkevicius_14493758_Project
=====================================



Term project for COMP20230. Finds out optimal route for a list of input airports.

* pip install https://github.com/ernest4/COMP20230_Project.git
* From terminal, run the following command to learn usage:
    
  comp20230_project -h


* Free software: GNU General Public License v3


Features
--------

* Read in itinerary .csv with 5 airports (1 home and 4 destinations) and an aircraft.
* Use user provided airport, aircraft, countrycurrency and currencyrates .csv files, or load defaults if none were give.
* Clean the input .csv data.
* Compute using brute force the most optimal flight plan for each itinerary.
* Output the result to user specified output file or default bestroutes.csv file.

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
