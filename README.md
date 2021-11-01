# Code for showing layout of DHS & grism spectra

## NOTE on `pysiaf`:

Recommend using `pysiaf` 0.6.2 or later with PRDOPSSOC-M-026 or later. There were issues with earlier versions with PRDOPSSOC-H-015.
Note to self: use the "jwst_py3p9p5" environment, where I have installed a recent version of `pysiaf` that works. Also you can create a new Pyehon 3.9 environment and do `pip install -r requirements.txt`
In my "py36" environment, SIAF has big issues recovering original coordinates from 'sci' to 'tel' and back.
