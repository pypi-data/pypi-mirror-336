# AuleDFT

AuleDFT is a user-friendly application designed to simplify **Density Functional Theory (DFT)** simulations. It provides an intuitive graphical user interface (GUI) that supports popular DFT software packages, including **Quantum Espresso (QE)** and **VASP**. The application aims to make DFT simulations accessible to both beginners and experts in the field of computational chemistry and material science.

## Features

- **User-Friendly GUI**: A simple and intuitive interface for performing DFT simulations, even for users with no prior experience.
- **Support for Quantum Espresso and VASP**: Seamless integration with two of the most popular DFT engines in computational chemistry.
- **Easy Setup**: No need for complicated command-line instructions. The app handles the details for you.
- **Simulation Management**: Easily set up, run, and monitor DFT simulations from start to finish.
- **Visualization Tools**: View your simulation results directly within the app.
- **Error Handling & Warnings**: Provides useful feedback if something goes wrong during the simulation, guiding the user toward a solution.

## Requirements

To run **AuleDFT**, ensure you have the following installed:

### Dependencies:

- **Python 3.x**
- **Qt5** or **Qt6** (for the GUI)
- **Quantum Espresso** or **VASP** installed locally for simulation execution
- Additional Python libraries:
  - PyQt5 or PyQt6 (for GUI)
  - numpy, scipy (for numerical operations)
  - pandas (for data handling)
  - matplotlib (for plotting results)

You can install the required dependencies via pip:

```bash
pip install -r requirements.txt

```

## Usage

To launch the AuleDFT GUI, run the following command:

```bash
python run_auledft.py
```

The GUI will open, where you can easily configure and launch your DFT simulations.

### Key Features in the GUI:

- Input Structure: Load or create molecular structures for your simulations.
- Choose Software: Select whether you want to use Quantum Espresso or VASP.
- Set Parameters: Choose computational parameters like energy cutoffs, k-point grids, and other DFT settings.
- Run Simulations: Submit your jobs and monitor their progress.
- View Results: After completion, visualize energy, forces, and other simulation data.
- Export Results: Save the results and configurations for further analysis or reuse.

### Example Workflow

- Prepare Structure: Load or create a structure using the app's built-in tools or import it from a file (e.g., .xyz, .pdb).
- Set Parameters: Select the DFT software (QE or VASP), and configure your computational parameters.
- Run Simulation: Launch the simulation with just a click.
- Monitor Progress: Watch the simulation progress, and get real-time updates in the GUI.
- Analyze Results: View energy levels, charge densities, and other properties.
- Export Data: Save your results in a variety of formats.

## Testing

To run the tests for the application, use:

```bash
pytest
```

Alternatively, you can run individual tests by:

```bash
python -m unittest discover
```

## Contributing

We welcome contributions! If you'd like to contribute to the development of AuleDFT, feel free to fork the repository, create a new branch, and submit a pull request.

Please make sure your code is well-documented, and add tests where applicable.

## License

AuleDFT is licensed under the MIT License. See the LICENSE file for more details.
Acknowledgments

    Thanks to Quantum Espresso and VASP for providing powerful tools for DFT simulations.
    Developed and maintained by Kendrick Di Piro.
