                       Large Ultrasonic SIM


DESCRIPTION:
This README provides information about the Data Processing GUI Application developed in Python, designed for efficient data processing and visualization using Python libraries.

FEATURES:
- Graphical User Interface (GUI) built with PyQt5 for an interactive experience.
- File System Integration for easy management and navigation of data files.
- Data Visualization with 3D plotting capabilities for comprehensive data analysis.
- Customizable Settings for personalized application adjustments.
- Modular Design for easy maintenance and scalability.

INSTALLATION:
Requires Python and the following libraries: numpy, pandas, PyQt5, matplotlib, csv, shutil, os, multiprocessing, and sys

To install required packages:
pip install numpy pandas PyQt5 matplotlib csv

USAGE:
1. Start the application by running the main_application.py file:
   python main_application.py

2. Navigate the interface to manage .csv files.

3. Utilize 3D plotting features for data visualization.

4. Access the settings dialog to customize application window dimensions and modify 3D visualization

CONTRIBUTION:
To contribute:
1. Fork the repository.
2. Create a new branch for your feature.
3. Commit changes and push to the branch.
4. Open a pull request.

TECHNICAL DESCRIPTION:
Here is a technical description of the specific functionalities and technical implementations in the Ptyhon files of the large ultrasonic simulator. 
1. Calculation_dialog.py
   Class 'CalculationDialog' (inherits 'QDialog'): This class is a GUI component for handling calculations. It includes:
   a. An '__init__' method to initialize the dialog with a file path
   b. 'initUI' method for setting up user interface elements.
   c. 'runProcessing' for performing data processing tasks, which includes steps like CSV file reading, grid generation, 3D array processing, and calculations of magnitude 
       and phase.
   d. 'appendStatus' method for updating the dialog with messages to display calculation progress
2. 'data_entry.py'
   a. Class 'DataEntry': This class contains the properties ID, phase, position, and orientation of the transducers
3. 'data_entry_tree_view.py'
   Class 'DataEntryTreeView' (inherits 'QTreeView'): A specialized tree view for displaying data entries. It includes:
   a. 'contextMenuEvent' for handling right-click menu actions.
   b. Methods like 'viewFile', 'calculateFile', and 'deleteFile', interactive features for file manipulation within the UI
4. 
   

LICENSE:
This project is under the MIT License 

ACKNOWLEDGEMENTS:
- Thanks to all contributors and the Python community for support and resources.

CONTACT:
For more information or queries, contact the development team.

======================================================================
