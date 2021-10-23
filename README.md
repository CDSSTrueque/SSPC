# Welcome to SSPC-Clear-Sky-Model
The purpose of this GitHub is to complement the information presented in our research publication titled "An easy-to-calibrate DNI clear-sky model: a performance comparison in different geographic locations" published in the Journal <<Journal name>> and authored by César D. Sánchez-Segura and Manuel I. Peña-Cruz.

Our clear-sky model was compared against 13 clear-sky models using an 11-year database (2010-2020) that includes 71 solarimetric stations, showing high performance regardless of the type of climate and geographic characteristics. This model is calibrated using a couple of clear-sky instants. Detailed results can be found within this GitHub.
  
  
This GitHub contains the following impelled codes:
  - Extraction of Linke turbidity coefficient *TL* from SoDA images.
  - Processing of database configured for Pangaea nomenclature.
    - Approximation of the DNI curve under clear-sky conditions by SSPC and 13 other clear-sky models for each day of analysis. This process is performed for each solarimetric station.
    - Compilation of results per solarimetric station. 
  - Plotting of box plots.
All the code present in this GitHub was developed at 💻 &nbsp; ![Python](https://img.shields.io/badge/-Python-333333?style=flat&logo=python)3.

  
The Python code available in this repository was written by César D. Sánchez-Segura.

  
We obtained these input data from Pangaea database (https://www.pangaea.de/). 
## Disclaimer
We do not offer support for these models, however, we welcome suggested fixes or edits by users. 
The intellectual property of these models remains with the authors credited within the paper. 
All models made available are already in the public domain.
