Metromaps
=========

Welcome to Metromaps, an innovative way of extracting story-lines from your chronological text domain.

# Version
0.1.1


# Install
Metromaps is fueled by Python 2.7. If you are running on MAC OS X, make sure you have the [brew version] of Python. 

You will need [networkx], soon to be migrated to [SNAP] in 1.0.0(stay tuned). You might also want to get [nltk] but it's not required for basic functionality. 

Once you have these packages, just clone this github repository! Write to us if you have any problems.

[networkx]: http://networkx.github.io/
[SNAP]: http://snap.stanford.edu/snap/index.html
[nltk]: http://www.nltk.org/
[brew version]: http://docs.python-guide.org/en/latest/starting/install/osx/

# Running MetroMaps
Each domain requires its own configuration file (see docs/ for some tips). Once you have your configuration ready, run it with:

	python2.7 mmrun.py configuration.yaml

Default `lotr.yaml` configuration works on the Lord of the Rings domain, and outputs the final MetroMap into `lotr.mm`




