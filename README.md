<p align="center">
  <img src="docs/ResoFox_cover.png" alt="ResoFox Mascot" width="400"/>
</p>
<p align="center"><em>Illustration: ResoFox mascot explaining neutron diffraction and Bragg's Law.</em></p>

<h2 align="center">ResoFox</h2>
<p align="center"><em>A GUI-based tool for calculating resolution and flux of neutron powder diffractometers.</em></p>

---



## Abstract

ResoFox is a Python-based graphical tool designed for theoretical analysis of neutron powder diffractometers. It focuses on evaluating the influence of optical components—namely collimators and monochromators—on diffraction peak resolution and relative intensity. The software is built upon the resolution model proposed by Caglioti et al. in 1958, combined with Bragg’s law and fundamental diffraction equations. It allows users to perform simulations under various geometric and optical configurations.

The tool features an integrated graphical interface and real-time plotting, capable of displaying:
- Relative neutron beam intensity (luminosity)
- Diffraction peak full width at half maximum (FWHM) and angular resolution
- Theoretical powder diffraction patterns (supporting FCC and BCC lattices)

ResoFox was presented at the 2024 Taiwan Neutron Conference and has been benchmarked against Monte Carlo simulation results using McStas.

---

## Motivation and Background

Neutron diffraction is a vital technique for studying crystal structures and magnetism. Resolution and flux are two critical parameters in the design of neutron diffractometers. While Monte Carlo tools such as McStas offer detailed particle-level simulations, theoretical estimates of resolution and flux are more practical during the early stages of instrument design.

In 1958, Caglioti et al. proposed a widely adopted analytical model for calculating peak broadening using collimator divergences (α₁, α₂, α₃) and monochromator mosaic spread (β). Based on this model, ResoFox was developed to provide a user-friendly and visualized environment that enables designers to rapidly evaluate performance under varying design parameters.

---
## 📁 Repository Structure Overview
The following structure outlines the key components of the repository, including source code, simulation examples, and image assets used in the documentation:
```
ResoFox/
├── Examples/                                       # Simulation examples and McStas comparison data
│   ├── McStas_input_HOPG_Ag.instr                  # McStas instrument definition file
│   ├── Preliminary_Design_and_Performance_...pdf   # Simulation design and performance report
│   ├── McStas_input_HOPG_Ag_20250505_result/       # Output plots and data from McStas simulation
│   └── McStas_input_HOPG_Ag_20250505_instrument_.../  # Instrument geometry visualization (3D)
├── docs/                                           # Images used in README (e.g., diagrams, output plots)
├── LICENSE                                         # Software license (MIT License)
├── README.md                                       # Project description, usage, and citation info
├── ResoFox_v1.py                                   # Main program (GUI interface and core calculations)
├── main_png.py                                     # Script for generating figures and geometry plots
```
## 🔧 Requirements
This software requires Python 3.7+ and the following packages:

```
pip install matplotlib pillow pandas
```
tkinter is included by default in most Python distributions (Windows/macOS).
For Linux users, if the GUI does not launch, install tkinter with:

```
sudo apt-get install python3-tk
```

## 📦 Module Functions

| Package               | Purpose                                                                 |
|-----------------------|-------------------------------------------------------------------------|
| `tkinter`             | Build the graphical user interface (GUI) for input/output interaction   |
| `pillow`              | Load and render image files in the GUI (e.g., logos, figures)           |
| `matplotlib`          | Generate resolution/intensity plots and output figures                  |
| `pandas`              | Handle tabular data (e.g., export diffraction results to CSV)           |
| `math`, `csv`, `io`, `base64` | Built-in Python libraries for computation, file handling, and encoding |



## Software Architecture and Functional Overview

ResoFox is developed in Python with a graphical user interface built using `tkinter`. Users can input the following parameters for simulation:

- Three collimator divergence angles: α₁, α₂, α₃ (in radians)
- Monochromator mosaic spread β (in radians)
- Monochromator d-spacing and Bragg angle (in Å and degrees)
- Sample lattice constants a, b, c and lattice type (BCC = 1, FCC = 2)
- Neutron wavelength and plot color selection

### Output features include:
- Relative beam luminosity (not corrected for reflectivity)
- Minimum FWHM and resolution curve
- Theoretical powder diffraction pattern (2θ vs intensity), exportable as an image
- Full data tables displayed in the console, including each peak’s:
  - d-spacing, calculated lattice constant a,
  - FWHM, angular resolution, and lattice resolution (Δd/d)

📷 GUI Interface Example:

![ResoFox Main GUI](docs/gui_main_interface.png)

---
## 🖨️ Output and Data Export

ResoFox supports real-time generation and export of both plots and data tables:

- Users can save generated plots—such as diffraction patterns (2θ vs intensity) and resolution curves—as `.png` images via the **Save Image** button in the GUI.
- The program automatically prints detailed diffraction peak data—including 2θ, d-spacing, resolution, and relative intensity—to the console and optionally saves it as  `.csv` files.
- All output files are UTF-8 encoded and compatible with Excel or other scientific plotting software for downstream analysis.


## 📋 Console Output: Angular Resolution per Peak

The program automatically outputs the following resolution-related information for each diffraction angle:

- Calculated lattice constant (a-value)
- Full width at half maximum (FWHM) in degrees
- Angular resolution
- Lattice resolution (Δd/d)
- Standard deviation (if applicable)

These data can be used for further comparison with Monte Carlo simulations (e.g., McStas) or experimental results.

---


## Validation Against Classical Theory: Caglioti et al. (1958)

To validate the correctness of ResoFox calculations, we reproduced the analytical resolution model proposed by G. Caglioti et al. (1958), which relates the full width at half maximum (FWHM) to beam luminosity (L) under different collimator angular divergences (α₁, α₂, α₃) and a fixed monochromator mosaic spread (β = 20 arcmin).

The upper image shows the original figure from the Caglioti paper, while the lower plot is generated using ResoFox under the same conditions. Each dot represents a different collimator configuration, color-coded by  (a = 0, 1.5, 3).

The results demonstrate strong agreement with the classical model, successfully replicating the characteristic trend between luminosity and resolution. This confirms the analytical validity of ResoFox for preliminary instrument performance estimation.


![Validation vs Caglioti 1958](docs/validation_vs_caglioti1958.png)

---
## Example Input Configuration (ResoFox vs McStas)

The figure below presents a side-by-side comparison of the input interfaces for ResoFox and McStas:


![Input interface comparison](docs/resofox_mcstas_input_demo.png)

By applying the corresponding parameter values shown in the figure, users can replicate the diffraction pattern results for silver powder samples in both ResoFox and McStas, enabling direct comparison.

In addition, McStas offers various predefined sample types, as shown in the figure. Users can input the desired sample name in the `sample` field of the McStas interface to change the test material. Both FCC and BCC lattice structures are available for simulation, allowing users to compare how different crystal types affect resolution and intensity.
![Sample Image](docs/sample.png)

A detailed comparison between the angular resolution results simulated by McStas and those predicted by ResoFox has been published in a paper on arXiv. The full manuscript is included in the `examples/` folder.

🔍 Note: This example uses HOPG as the monochromator material, while the arXiv paper uses Ge(115). The difference in configuration is intentional, providing users with more options for cross-validation and parameter exploration.

---


## Comparison with McStas Simulation Results

To verify the consistency between ResoFox’s analytical calculations and Monte Carlo simulation results, a benchmark was conducted using McStas to simulate powder diffraction of silver (Ag) with a Ge(115) monochromator at λ = 1.65 Å. The comparison is shown below:

![Comparison with McStas](docs/comparison_with_mcstas.png)



---

## Case Files and Example: Silver Powder Benchmark

All data used in the benchmark comparison are provided in the following folder:


```
Examples/                                       # Simulation examples and McStas comparison data
├── McStas_input_HOPG_Ag.instr                  # McStas instrument definition file
├── Preliminary_Design_and_Performance_...pdf   # Simulation design and performance report
├── McStas_input_HOPG_Ag_20250505_result/       # Output plots and data from McStas simulation
└── McStas_input_HOPG_Ag_20250505_instrument_.../  # Instrument geometry visualization (3D)
```

Users can download these files to reproduce the benchmark and validation results.

---

## Development Environment and Usage

- Development environment: Python 3.8+
- Dependencies: `tkinter`, `matplotlib`, `pandas`, `PIL`
- For non-Python users, a standalone executable `ResoFox.exe` is available (no Python installation required)
- The software allows exporting of generated plots and console output data tables

---

## ResoFox v1.0 Executable (Windows 64-bit)

This version provides a precompiled standalone executable for ResoFox. It can be used directly to perform resolution and diffraction pattern simulations for neutron powder diffractometers.

- 🔧 Development environment: Python 3.8
- 🛠️ Packaging tool: PyInstaller
- ✅ No Python installation required—just download and run


---

### Installation Instructions
1. Click the link below to download the `.exe` file.
2. Run `ResoFox_v1.0.exe`.
3. If a security warning appears (e.g., Windows SmartScreen), choose “Run anyway” or add the file to your whitelist.

---

### Source Code and Example Files:
Please refer to the [main README](../README.md) and the `case_study_ag_powder` folder for detailed instructions and examples.

---

## ResoFox v1.0 Executable (Windows 64-bit)

This is the standalone executable version of ResoFox, built with PyInstaller.

- Python version: 3.8  
- No installation required. Simply download and run.

For details on parameters and example inputs, please refer to the main README.

## 📥 Download Executable

[🔗 Click here to download ResoFox_v1.0.exe (Windows 64-bit)](https://github.com/lifangchen2021/ResoFox/releases/download/v1.0/ResoFox_v1.0.exe)

This is a packaged version of the software and does not require Python to be installed.  
If a security or antivirus warning appears, please select “Run anyway” or add the file to your trusted list.


⚠️ Note:
`ResoFox_v1.exe` is a Windows-only executable and currently supports **Windows 10 / 11 (64-bit)** systems.  
If you are using macOS or Linux, please run the source file `ResoFox_v1.py` with the required Python dependencies installed.

---

## License and Citation

This software is released under the **MIT License**, allowing free use and modification with appropriate attribution.

### Citation Example:

```
Li-Fang Chen, Preliminary Design and Performance Simulation of a Thermal Neutron Diffractometer Using McStas, arXiv:2504.20341
Li-Fang Chen, ResoFox: A GUI Tool for Neutron Diffractometer Resolution and Intensity Estimation
```
---

📩 For technical support or collaboration inquiries, please contact:  
`lifangchen0507@gmail.com`

