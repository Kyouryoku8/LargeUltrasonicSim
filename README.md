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

TECHNICAL OVERVIEW:
This project is a Python-based application with a focus on data management, processing, and visualization, particularly of spatial data. It leverages the PyQt framework for its GUI components using classes like 'QDialog', 'QMainWindow', and 'QTreeView'. The application is structured in a modular fashion, separating concerns such as data entry, file operations, and UI management into different files. This approach enhances maintainability and scalability. The use of classes and methods for specific tasks like file manipulation, data processing, and UI actions into different files in order to enhance both maintainability and scalability. The program uses classes and methods for specific tasks like file maniuplation, data processing, and UI actions in an object-oriented approach, facilitating code reuse and organization.

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
4. 'data_processsing.py'
   Functions for data processing: Includes several standalone functions and a class for data processing:
   a. 'generate_grid', 'process_grid_chunk', and 'process_3d_array' for handling 3D spatial data.
   b. 'calculate_magnitude_phase' for post-processing results.
   c. Class 'DataProcessor': Methods like 'filter_data_by_z' and 'get_xyz_from_data' indicate functionalities for filtering and extracting spatial data.
5. 'File_operations.py'
   File related operations:
   a. 'read_csv' for reading CSV files with unit conversion (meters to millimeters).
   b. 'export_results_to_csv' for exporting processed data.
   c. 'copy_files_to_folder' for file management
6. 'main_application.py'
   Class 'MainApplication' (inherits 'QMainWindow'): The central class for the application's UI.
   a. Methods for UI initialization ('initUI'), settings dialog ('showSettingsDialog'), file import ('importFiles'), help dialog ('showHelpPopup'), and data visualization 
   ('visualizeData').
   b. 'clearLayout' for UI management, including dynamic UI updates.
   c. Class 'SettingsDialog' (inherits 'QDialog'): For handling application settings, with methods for retrieving settings.
7. 'file_utils.py'
   Class 'FileUtils': Contains utility methods like 'deleteFile', providing basic file manipulation functionalities.
8. 'output_files_tree_view.py'
   Class 'OutputFilesTreeView' (inherits 'QTreeView'): Similar to 'DataEntryTreeView', it's tailored for output file management with context menu actions and file 
   manipulation methods in the output files tab.

LICENSE:
This project is under the MIT License 

ACKNOWLEDGEMENTS:
- Thanks to all contributors and the Python community for support and resources.

CONTACT:
For more information or queries, contact the development team.

======================================================================
