=======
History
=======

0.2.5 (2019-03-10)
------------------
* Make it so the MemoryPolynomial is a superclass for PAs and DPDs
* Add a memory_stride parameter for memory polynomial modeling

0.2.4 (2019-03-10)
-------------------
* Fix an issue where the DPD was limited to 7th order with 4 taps. 

0.2.3 (2019-03-10)
--------------------
* Fix an issue where the memory taps in DPD were defaulting to "1" instead of 0.
* Change to plain LS since I didn't trust the regularization


0.2.2 (2019-03-01)
------------------------
* Includes what is probably a working DPD

0.2.1 (2019-02-18)
-----------------------
* Adds a random number seed to OFDM

0.2.0 (2019-02-01)
--------------------
* Add a DSP module with a frequency shifter


0.1.1 (2019-01-23)
---------------------
* Adds a working PA and OFDM modulator.
* Begins working on basic DPD


0.1.0 (2019-01-22)
------------------
* First release on PyPI.
