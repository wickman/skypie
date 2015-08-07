skypie
======

skypie is a basic financial modeler for airplane ownership

to run from the source tree, use 'tox -e skypie'.  to build a standalone binary
that can be used to explore the models, use 'tox -e pex' which will dump a
standalone pex into dist/skypie.

a few example planes are provided, a Diamond DA40, Cessna T210 and Cessna 152.

sample simulations
==================

sample simulation: calculate the total cost per hour of ownership of a Diamond DA40.

.. code-block:: bash

    $ tox -e skypie -- table --breakeven=285 DA40 100,500,100 12,60,12
    GLOB sdist-make: /Users/wickman/clients/skypie/setup.py
    skypie inst-nodeps: /Users/wickman/clients/skypie/.tox/dist/skypie-0.1.0.zip
    skypie runtests: PYTHONHASHSEED='2229473308'
    skypie runtests: commands[0] | skypie table --breakeven=285 DA40 100,500,100 12,60,12
    Sell or keep: keep
    Plane:        DA40
    Acquisition:  120 month mortgage, rate: 6.25%, down payment: 15.00%
    Depreciation: 10.00% per 12 months
                  12         24         36         48         60 
      100    2853.90    1560.81    1126.35     906.38     772.07 
      200    1458.95     812.40     595.17     485.19     418.03 
      300     993.97     562.94     418.12     344.79     300.02 
      400     761.48     438.20     329.59     274.59     241.02 
      500     621.98     363.36     276.47     232.48     205.61 

the Y axis is number of hours flown per year.  the X axis is the number of
months of ownership.  by default the plane is kept, and total expenditures
are reflected.  the graph is colorized by the "breakeven" point of $285/hr,
which is the wet rate for renting a DA40 in my neck of the woods.

basic assumptions for the DA40: acquisition price of $239,000, yearly
insurance of $1500, annual $3500, engine overhaul $18,000, TBO 2000 hours,
exponential depreciation model and G1000 subscription costs.  hangaring is
not included.  these constants are defined in ``skypie/planes.py``.

all of these parameters can be overridden, for example:

.. code-block:: bash

    $ tox -e skypie -- \
        --price=269000 \           # acquisition price of $269,000
        --acquisition-type=cash \  # acquire the plane all-cash
        --housing=3600 \           # assume that hangaring is $300/mo
        --insurance=2500 \         # assume that insurance is $2500/yr
        --usage-rate=0.25 \        # assume that you use the plane 25% of the time
        --usage-revenue=245 \      # and the other 75% is billed to customers at $245/hr
        --usage-hobbs-ratio=1.3 \  # assume 1.3:1 hobbs:tachometer time
        --sell \                   # assume the plane is sold at the end of the term for the depreciated value
        table DA40 \               # inherit all the rest of the DA40 defaults
        50,500,50                  # show 50-500 in 50 hour/yr increments
        12,120,12                  # show ownership of 1-10 years in 1 year increments
..

the output being:

.. code-block::
Sell or keep: sell
Plane:        DA40
Acquisition:  all cash
Depreciation: 10.00% per 12 months
              12         24         36         48         60         72         84         96        108        120 
   50    1040.76     775.50     673.71     613.70     571.07     537.63     509.83     485.86     464.71     445.73 
  100     450.44     317.81     266.92     236.91     215.60     198.88     184.98     172.99     162.42     152.93 
  150     253.67     165.25     131.32     111.32      97.11      85.96      76.69      68.70      61.65      55.33 
  200     155.28      88.97      63.52      48.52      37.86      29.50      22.55      16.56      11.27       6.53 
  250      96.25      43.20      22.84      10.84       2.31      -4.37      -9.93     -14.73     -18.96     -22.75 
  300      56.90      12.69      -4.28     -14.28     -21.38     -26.96     -31.59     -35.59     -39.11     -42.27 
  350      28.79      -9.11     -23.65     -32.22     -38.31     -43.09     -47.06     -50.48     -53.51     -56.22 
  400       7.70     -25.45     -38.18     -45.68     -51.01     -55.19     -58.66     -61.66     -64.30     -66.67 
  450      -8.69     -38.17     -49.48     -56.14     -60.88     -64.60     -67.69     -70.35     -72.70     -74.81 
  500     -21.81     -48.34     -58.52     -64.52     -68.78     -72.12     -74.90     -77.30     -79.42     -81.31 
..
