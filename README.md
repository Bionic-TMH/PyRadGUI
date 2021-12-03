# PyRadGUI
AI Project Work

**PyRadGUI** is a GUI tool to extract radiomics features from CT DICOM and RT-structure in batch. 
It uses plastimatch in backend to convert the dicoms to nrrd and mha format required by pyradiomics to calculate features.

**Requirements:**
Windows 10.
We have not yet tested on Linux and Mac.

Dependancies.
Python > 3.5

Plastimatch: version 1.8.0.

Pyradiomics: version 3.0.

tk==0.1.0

**Installation:**

**Option 1:**
1. Download and install python from https://www.python.org/downloads/

2. Download and install plastimatch from https://plastimatch.org/

3. Install the required python packages using "python -m pip install package-name"

4. After succesfull installation, you can start the tool by typing 'python PyRadGUI.py' from the terminal.

**Option 2:**
1. Download the zip file which contains all the  packages pre-installed in it.
2. Unzip the file using either 7z or winzip software.
3. Locate to the unzipped folder and click on the PyRadGUI.exe file to start the program.
