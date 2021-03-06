pyhandy
=======

Python implementation of the Human and Nature Dynamics (HANDY) model (http://www.atmos.umd.edu/~ekalnay/pubs/2014-03-18-handy1-paper-draft-safa-motesharrei-rivas-kalnay.pdf)

NOTE: The authors of the HANDY model are not associated with this implementation or endorses it.

Installation
============
From source:

    $ python setup.py install

pyhandy requires scipy >= 0.10.0 and matplotlib

Usage
=====

Command line
------------
pyhandy support running and plotting predefined society evolutions from the command line e.g.

    $ handy_model_run.py equitable cyclic 1000

resulting in the following plot being shown:

![Plot goes here](/images/equitable_cyclic.png?raw=true)

To see the full set of supported society types supported by the command line tool run

    $ handy_model_run.py -h

Directly
--------
pyhandy supports custom society calculations by using the **Society** class from **pyhandy.handy**

The **Society** class takes the following arguments as initial conditions for a society:

 * min\_required\_consumption
 * output\_division
 * salary
 * commoner\_population
 * elite\_population
 * nature
 * nature\_regeneration 
 * nature\_capacity
 * depletion
 * wealth
 * commoner\_birth_rate,
 * elite\_birth\_rate
 * normal\_death\_rate
 * famine\_death\_rate
 * year

It should be straight forward to match the variable names with the notation used in http://www.atmos.umd.edu/~ekalnay/pubs/2014-03-18-handy1-paper-draft-safa-motesharrei-rivas-kalnay.pdf

Variable values for the scenarios shown in the article can be found in the dict **pyhandy.handy.socity_types**

First initialize society:

    >>> from pyhandy import handy
    >>> my_soc = handy.Society(*handy.socity_types['unequal']['soft'])

then run the society simulation for a specified number of years

    >>> time, commoner_population, elite_population, nature, wealth, carrying_capacity = my_soc.evolve(1000)

all of the result variables are lists with a value for each simulation timestep.

The result can be plotted using:

    >>> handy.plot_society(time, commoner_population, elite_population, nature, wealth, carrying_capacity)



MIT License
===========
Copyright (C) 2014 Esben S. Nielsen

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
