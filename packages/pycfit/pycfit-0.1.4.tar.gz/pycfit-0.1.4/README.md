# Python Component Fitting Tool  (pycfit)

Python program to replicate many spectral fitting functions of the CFIT system from SolarSoft IDL.  



# Installation

`pip install pycfit`

### 🛠 Important: Conda Environments Must Have Python Installed
If using Conda, ensure your environment includes Python before installing:

```sh
conda create --name myenv python
conda activate myenv

pip install pycfit
```
 

# Use
### Use interactive fitter to find an initial model based on an averaged spectra

```python
from pycfit import cfit_gui
from pycfit.data import load_example_single_spectra

# Load sample data
wavelength, intensity, uncertainty = load_example_single_spectra()

# Call the GUI fitter
model = cfit_gui(wavelength, intensity, uncertainty=uncertainty)
```


### Use the interactive viewer to fit each point of the raster to the initial model and adjust or mask individual point fittings as needed
```python
from pycfit import cfit_grid_gui
from pycfit.data import load_example_grid_spectra

# Load a small-patch of sample data
wavelength, intensity, uncertainty, mask = load_example_grid_spectra(patch=True)

# Create Grid fitter, fit the whole raster, inspect and modify, get results
myGrid = cfit_grid(model, wavelength, intensity, 
                uncertainty=uncertainty, mask=mask)

myGrid.fit()

myGrid = cfit_grid_gui(myGrid)

results = myGrid.get_results()
```


# Contacts:
### Software Maintenance:
Ayris Narock:  ayris.a.narock@nasa.gov
### NASA Official:
Therese Kucera:  therese.a.kucera@nasa.gov



# License

This project is Copyright (c) National Aeronautics and Space Administration and licensed under
the terms of the Apache Software License 2.0 license. This package is based upon
the `Openastronomy packaging guide <https://github.com/OpenAstronomy/packaging-guide>`_
which is licensed under the BSD 3-clause licence. See the licenses folder for
more information.
