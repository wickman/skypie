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
        --output=outlay \          # tabulate by total outlay instead of per-hour cost
        50,500,50 \                # show 50-500 in 50 hour/yr increments
        24,120,24                  # show ownership of 1-10 years in 1 year increments
..

the output being::

    Sell or keep: sell
    Plane:        DA40
    Acquisition:  all cash
    Depreciation: 10.00% per 12 months
                  24         48         72         96        120 
       50   77549.69  122740.38  161287.76  194344.78  222864.32 
      100   63562.19   94765.38  119325.26  138394.78  152926.82 
      150   49574.69   66790.38   77362.76   82444.78   82989.32 
      200   35587.19   38815.38   35400.26   26494.78   13051.82 
      250   21599.69   10840.38   -6562.24  -29455.22  -56885.68 
      300    7612.19  -17134.62  -48524.74  -85405.22 -126823.18 
      350   -6375.31  -45109.62  -90487.24 -141355.22 -196760.68 
      400  -20362.81  -73084.62 -132449.74 -197305.22 -266698.18 
      450  -34350.31 -101059.62 -174412.24 -253255.22 -336635.68 
      500  -48337.81 -129034.62 -216374.74 -309205.22 -406573.18 


this means that for every 100 hours the plane is flown, you fly 25 hours for
personal use and 75 is leased back as part of part 91 operations (100-hour
inspections are factored into the per-hour price and are based off annual
inspection prices.) while the plane is flown 75 hours (tachometer), it is
billed 97.5 hours (hobbs) owing to the 1.3 hobbs-to-tachometer ratio.  this
is common when flown for a flight school.  the plane is then sold at the end
of the period for the depreciated price.

the cost of G1000 subscriptions, hangar, insurance, gas, overhaul, use tax,
property tax (california only, todo: make configurable), etc are included.

taking for example the 250 / 72 column: if the plane is flown 250 hours per
year (63 by you and 187 by a club/fbo) and sold after 6 years of ownership,
a profit of roughly $6,500 is turned.  this is of course assuming that the
plane has depreciated from $269,000 to $151,800 in that period of time.

other factors such as inflation or the pre-tax/post-tax cost basis of money
is *not* reflected.  TODO :-)
