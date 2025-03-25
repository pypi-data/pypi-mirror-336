``lddecay`` version |release|
=============================

``lddecay`` is a script based on `EggLib <https://egglib.org/>`_. It is
available in a preliminary state with the hope it might be useful.

Usage
-----

The program must used by first running the ``compute`` command::

    $ lddecay compute -i <VCF> -o <DAT>

and then, if desired, the ``plot`` command::

    $ lddecay plot -i <DAT> -o <PICT> -b <d1>,<d2>,...
