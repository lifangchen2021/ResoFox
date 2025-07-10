# -*- coding: utf-8 -*-
"""
Created on Thu May  1 15:40:11 2025

@author: LiFang Chen
"""
# =============================================================================
# This program implements analytical expressions for the resolution function
# of neutron diffractometers, based on the theoretical model proposed in:
#
#   G. Caglioti, A. Paoletti, and F. P. Ricci,
#   "Choice of Collimators for a Crystal Spectrometer for Neutron Diffraction,"
#   Nuclear Instruments and Methods, vol. 3, pp. 223–228, 1958.
#
# The resolution model and FWHM calculations follow the formulation of the
# Caglioti function, which relates instrumental broadening to geometric
# and mosaic parameters of the collimators and monochromator.
#
# This implementation is for research and educational use.
# Please cite the original paper if the analytical model is referenced.
# =============================================================================

"""GUI Program"""

from tkinter import *
from PIL import Image, ImageTk
import math
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from main_png import main_png
import pandas as pd
import tkinter.messagebox as messagebox
from tkinter import Toplevel, filedialog, Button
import csv

"""Create Window"""
window = Tk()
window.title("ResoFox")
window.geometry("1000x1000")
plot_window = None

"""Variable Declarations"""
# Collimator constants
alpha1 =  DoubleVar()
alpha2 =  DoubleVar()
alpha3 =  DoubleVar()

# Monochromator constants
beta = DoubleVar()
d_monochromate = DoubleVar()
theta_monochromate = DoubleVar()
# Lattice constants
lattice_vector1 = DoubleVar()
lattice_vector2 = DoubleVar()
lattice_vector3 = DoubleVar()
# Neutron wavelength
style_choose = IntVar()
style_choose.set(1)
# Line color
linecolor = StringVar()
linecolor.set(1)
weighting = DoubleVar()
weighting.set(1)

# Angles in lattice constants
lattice_anguler_alpha = float(90.0)
lattice_anguler_beta = float(90.0)
lattice_anguler_gamma = float(90.0)

# Constant definition
Pi = math.pi

"""Custom Functions"""
# Trigonometric calculations
cos_alpha_star = (math.cos(lattice_anguler_beta/180*Pi)* math.cos(lattice_anguler_gamma/180*Pi)\
                  - math.cos(lattice_anguler_alpha/180*Pi))/math.sin(lattice_anguler_beta/180*Pi)/ math.sin(lattice_anguler_gamma/180*Pi)
cos_beta_star = (math.cos(lattice_anguler_alpha/180*Pi)* math.cos(lattice_anguler_gamma/180*Pi)\
                 - math.cos(lattice_anguler_beta/180*Pi))/math.sin(lattice_anguler_alpha/180*Pi)/ math.sin(lattice_anguler_gamma/180*Pi)
cos_gamma_star = (math.cos(lattice_anguler_alpha/180*Pi)* math.cos(lattice_anguler_beta/180*Pi)\
                  - math.cos(lattice_anguler_gamma/180*Pi))/math.sin(lattice_anguler_alpha/180*Pi)/ math.sin(lattice_anguler_beta/180*Pi)

# Create lattice spacing calculation function
def lattice_distance(h,k,l):
    global lattice_vector1, lattice_vector2, lattice_vector3, cos_alpha_star, cos_beta_star,\
        cos_gamma_star
    d = 1/((h/lattice_vector1)**2 + (k/lattice_vector2)**2 + (l/lattice_vector1)**2 + \
           2*(h/lattice_vector1)*(k/lattice_vector2)*cos_gamma_star + 2*(k/lattice_vector2)*(l/lattice_vector3)*cos_alpha_star +\
               2*(l/lattice_vector3)*(h/lattice_vector1)*cos_beta_star  )**0.5 
    return d


"""Read the converted image"""
byte_data = base64.b64decode(main_png)
image_data = BytesIO(byte_data)

"""Define objects in the GUI interface"""
# label0 =  Label(window, text = "Assessment of Neutron Flux and Resolution in a Neutron Diffractometer", font=("Arial", 18, "bold"))  # Create window title
label1 = Label(window, text = "    Design of Collimator and Monochromator Parameters for Neutron Diffractometer Resolution Analysis", font=("Arial", 14, "bold"))  # Create window title

img1 = Image.open(image_data)        # Open image and insert conceptual geometric design of neutron diffractometer
img1 = img1.resize((800, 400))       # Resize to 800x400 (modifiable)
tk_img1 = ImageTk.PhotoImage(img1)    # Convert to tk image object
label2 = Label(window, image=tk_img1)  # Create neutron diffractometer image in window

# Create geometry parameters for Collimator 1
label3 = Label(window, text = "Collimator 1 Divergence (rad)=", font=("Arial", 14))
entry1 = Entry(window, textvariable = alpha1)  # Insert single-line input box


# Create geometry parameters for Collimator 2
label4 = Label(window, text = "Collimator 2 Divergence (rad)=", font=("Arial", 14))
entry2 = Entry(window, textvariable = alpha2)  # Insert single-line input box


# Create geometry parameters for Collimator 3
label5 = Label(window, text = "Collimator 3 Divergence (rad)=", font=("Arial", 14))
entry3 = Entry(window, textvariable = alpha3)  # Insert single-line input box


# Create monochromator parameters
label6 = Label(window, text = "Mosaic Spread of the Monochromator(unit: rad)=", font=("Arial", 14))
entry4 = Entry(window, textvariable = beta)  # Insert single-line input box
label7 = Label(window, text = "Monochromator d-spacing (Å) =", font=("Arial", 14))
entry5 = Entry(window, textvariable = d_monochromate)  # Insert single-line input box
label8 = Label(window, text = "Bragg Angle of the Monochromator(unit：degree) =", font=("Arial", 14))
entry6 = Entry(window, textvariable = theta_monochromate)  # Insert single-line input box

# Create sample diffraction parameters
label9 = Label(window, text = "Lattice constant a (Å) =", font=("Arial", 14))
entry7 = Entry(window, textvariable = lattice_vector1)  # Insert single-line input box
label10 = Label(window, text = "Lattice constant b (Å) =", font=("Arial", 14))
entry8 = Entry(window, textvariable = lattice_vector2)  # Insert single-line input box
label11= Label(window, text = "Lattice constant c (Å) =", font=("Arial", 14))
entry9 = Entry(window, textvariable = lattice_vector3)  # Insert single-line input box

# Create Crystal Structure Selection parameters
label12 = Label(window, text = "Crystal Structure Selection  1: BCC   2: FCC  =" , font=("Arial", 14))
entry10 = Entry(window, textvariable = style_choose)  # Insert single-line input box

# Input for neutron wavelength and curve style
label121 = Label(window, text = "Selection of Curve Color (1:Blue, 2:Red, 3:Green) =" , font=("Arial", 14))
entry101 = Entry(window, textvariable = linecolor)  # Insert single-line input box
hint_color = Label(window, text="↑ Used to distinguish different simulation cases", font=("Arial", 10), fg="gray")
label122 = Label(window, text = "Neutron Intensity Weighting =" , font=("Arial", 14))
entry102 = Entry(window, textvariable = weighting)  # Insert single-line input box
hint_weight = Label(window, text="↑ Optional: for adjusting peak heights in plotting", font=("Arial", 10), fg="gray")

# Footer / citation
label13 = Label(window, text = " " , font=("Arial", 10))
label14 = Label(window, text = "Reference: G. CAGLIOTI, A. PAOLETTIt and F. P. RICC1, CHOICE OF COLLIMATORS FOR A CRYSTAL" , font=("Arial", 12))
label15 = Label(window, text = " SPECTROMETER FOR " , font=("Arial", 12))
label16 = Label(window, text = "NEUTRON DIFFRACTION, 1958." , font=("Arial", 12))
label18 = Label(window, text = " " , font=("Arial", 10))
label19 = Label(window, text = "Program designer: LiFang Chen" , font=("Arial", 10))


"""Create function button related function library"""
def calculate():
    global lattice_vector1, lattice_vector2, lattice_vector3, cos_alpha_star, cos_beta_star,\
        cos_gamma_star, n_range, collimator1_length, collimator1_width,  collimator2_length, \
            collimator2_width,  collimator3_length, collimator3_width, linecolor, weighting
    # Read parameters related to the collimators
    alpha1 = float(entry1.get())
    alpha2 = float(entry2.get()) 
    alpha3 = float(entry3.get())

    # Read parameters related to the monochromator
    beta = float(entry4.get())
    d_monochromate = float(entry5.get())
    thita_monochromate = float(entry6.get())
    # Read parameters related to the simulated sample
    lattice_vector1 = float(entry7.get())
    lattice_vector2 = float(entry8.get())
    lattice_vector3 = float(entry9.get())
    # Read neutron wavelength
    n_ray = 2*d_monochromate*math.sin( math.radians(thita_monochromate))
    style_choose = int(entry10.get())
    # Read curve color and neutron intensity weighting
    linecolor = str(entry101.get())
    weighting = float(entry102.get())
    
    
    # Create empty lists angle_intensity_x/y to store intensity at different angles
    angle_intensity_x = []
    angle_intensity_y = []
    total_angle_intensity = []

    # Define an empty list to store calculation results later
    total_peak_message = []
    
    # Square of the parameters for collimators and monochromator
    alpha1_square = alpha1*alpha1
    alpha2_square = alpha2*alpha2
    alpha3_square = alpha3*alpha3
    beta_square = beta*beta

    # Separator line
    print ("===============================Table 1: Input, Relative Intensity, and FWHM Output Information==================================")
    # Calculate intensity
    luminosity = (alpha1*alpha2*alpha3*beta)/((alpha1_square+alpha2_square+4*beta_square)**0.5)
    print ("Input Data: alpha1 = ", alpha1, "alpha2 = ", alpha2, "alpha3 = ", alpha3, "beta = ", beta, "neutron wavelength = ", n_ray)
    print ("             d_monochromate =", d_monochromate, "theta_monochromate =", theta_monochromate)
    print ("             lattice_vector1 =", lattice_vector1,  "lattice_vector2 =", lattice_vector2, "lattice_vector3 =", lattice_vector3)
    print ("Output data:")
    print ("Relative intensity of diffraction pattern (luminosity) = ", luminosity)
    
    # Calculate the denominator part of the resolution due to collimators and monochromator
    a_1_over_2_denominator = alpha1_square + alpha2_square + 4*beta_square

    # Calculate the numerator part and best resolution caused by collimators and monochromator, which occurs at a_parameter=0.5
    a_1_over_2_numerator = (alpha1_square*alpha2_square + alpha1_square*alpha3_square + alpha2_square*alpha3_square + \
                   4*beta_square*(alpha2_square + alpha3_square) - 4*0.5*alpha2_square*(alpha1_square + 2*beta_square) +\
                       4*0.5*0.5*(alpha1_square*alpha2_square + alpha1_square*beta_square + alpha2_square*beta_square))
    a_1_over_2_min = (a_1_over_2_numerator/a_1_over_2_denominator)**0.5
    print ("Best (smallest) FWHM of the diffraction pattern due to collimators and monochromator occurs at a = 0.5, FWHM =", round(a_1_over_2_min, 4))

    # Resolution at a = 0, for comparison with literature
    a_1_over_2_numerator = (alpha1_square*alpha2_square + alpha1_square*alpha3_square + alpha2_square*alpha3_square + \
                   4*beta_square*(alpha2_square + alpha3_square) - 4*0*alpha2_square*(alpha1_square + 2*beta_square) +\
                       4*0*(alpha1_square*alpha2_square + alpha1_square*beta_square + alpha2_square*beta_square))
    a_1_over_2_0 = (a_1_over_2_numerator/a_1_over_2_denominator)**0.5
    print ("FWHM when a = 0:", round(a_1_over_2_0, 4))

    # Resolution at a = 0.5
    a_1_over_2_numerator = (alpha1_square*alpha2_square + alpha1_square*alpha3_square + alpha2_square*alpha3_square + \
                   4*beta_square*(alpha2_square + alpha3_square) - 4*0.5*alpha2_square*(alpha1_square + 2*beta_square) +\
                       4*0.5*0.5*(alpha1_square*alpha2_square + alpha1_square*beta_square + alpha2_square*beta_square))
    a_1_over_2_15 = (a_1_over_2_numerator/a_1_over_2_denominator)**0.5
    print ("FWHM when a = 0.5:", round(a_1_over_2_15, 4))

    # Resolution at a = 1.0
    a_1_over_2_numerator = (alpha1_square*alpha2_square + alpha1_square*alpha3_square + alpha2_square*alpha3_square + \
                   4*beta_square*(alpha2_square + alpha3_square) - 4*1.0*alpha2_square*(alpha1_square + 2*beta_square) +\
                       4*1.0*1.0*(alpha1_square*alpha2_square + alpha1_square*beta_square + alpha2_square*beta_square))
    a_1_over_2_15 = (a_1_over_2_numerator/a_1_over_2_denominator)**0.5
    print ("FWHM when a = 1.0:", round(a_1_over_2_15, 4))

    # Resolution at a = 1.5
    a_1_over_2_numerator = (alpha1_square*alpha2_square + alpha1_square*alpha3_square + alpha2_square*alpha3_square + \
                   4*beta_square*(alpha2_square + alpha3_square) - 4*1.5*alpha2_square*(alpha1_square + 2*beta_square) +\
                       4*1.5*1.5*(alpha1_square*alpha2_square + alpha1_square*beta_square + alpha2_square*beta_square))
    a_1_over_2_15 = (a_1_over_2_numerator/a_1_over_2_denominator)**0.5
    print ("FWHM when a = 1.5:", round(a_1_over_2_15, 4))

    # Resolution at a = 2.0
    a_1_over_2_numerator = (alpha1_square*alpha2_square + alpha1_square*alpha3_square + alpha2_square*alpha3_square + \
                   4*beta_square*(alpha2_square + alpha3_square) - 4*2.0*alpha2_square*(alpha1_square + 2*beta_square) +\
                       4*2.0*2.0*(alpha1_square*alpha2_square + alpha1_square*beta_square + alpha2_square*beta_square))
    a_1_over_2_15 = (a_1_over_2_numerator/a_1_over_2_denominator)**0.5
    print ("FWHM when a = 2.0:", round(a_1_over_2_15, 4))
    
    # Resolution at a = 3.0
    a_1_over_2_numerator = (alpha1_square*alpha2_square + alpha1_square*alpha3_square + alpha2_square*alpha3_square + \
                   4*beta_square*(alpha2_square + alpha3_square) - 4*3*alpha2_square*(alpha1_square + 2*beta_square) +\
                       4*3*3*(alpha1_square*alpha2_square + alpha1_square*beta_square + alpha2_square*beta_square))
    a_1_over_2_3 = (a_1_over_2_numerator/a_1_over_2_denominator)**0.5
    print ("FWHM when a = 3.0:", round(a_1_over_2_3, 4))
    
#%%    
    # Separator line
    print ("========================================Table 2: Lattice Diffraction Peak Information=========================================")

    # Calculate sample diffraction angle
    # Create diffraction peak calculation loop
    for n in [1]:
        for h in range(5):
            for k in range(5):
                for l in range(5):
                    if h + k + l == 0:
                        print("")
                    elif style_choose == 1:
                        if (h + k + l) % 2 == 0:
                            if n * n_ray > 2 * lattice_distance(h, k, l):
                                pass
                            else:
                                thita = math.asin(n * n_ray / 2 / lattice_distance(h, k, l)) * 180 / Pi
                                multiply_factor = (2 ** (math.ceil(h / (h + 1)) + math.ceil(k / (k + 1)) + math.ceil(l / (l + 1))))
                                # Intensity explanation: I = a * b * c, where a: polarization factor, b: multiplicity factor, c: thermal attenuation factor
                                intensity = (0.5 + 0.5 * math.cos(2 * thita / 180 * Pi) ** 2 / math.sin(2 * thita / 180 * Pi) / math.sin(thita / 180 * Pi)) \
                                            * multiply_factor * math.exp(-n / lattice_distance(h, k, l))
                                a = (d_monochromate * math.cos(thita_monochromate / 180 * Pi)) / (lattice_distance(h, k, l) * math.cos(thita / 180 * Pi))
                                # Create a list to store all lattice and diffraction information
                                all_message = [n, h, k, l, round(2 * thita, 3), round(intensity, 3), a]
                                total_peak_message.append(all_message)
                                # Print diffraction result
                                print(f"Order {n} ({h}{k}{l}) at {2 * thita:.3f}° , d = {lattice_distance(h, k, l):.4f} Å , a = {a:.4f} ")

                        else:
                            # Extinction condition
                            pass
                    elif style_choose == 2:
                        if (h + k == 2 or k + l == 2 or h + k == 4 or k + l == 4 or l + h == 2 or l + h == 4) and ((h % 2) == (k % 2) == (l % 2) == 1 or (h % 2) == (k % 2) == (l % 2) == 0):
                            if n * n_ray > 2 * lattice_distance(h, k, l):
                                pass
                            else:
                                thita = math.asin(n * n_ray / 2 / lattice_distance(h, k, l)) * 180 / Pi
                                multiply_factor = (2 ** (math.ceil(h / (h + 1)) + math.ceil(k / (k + 1)) + math.ceil(l / (l + 1))))
                                intensity = (0.5 + 0.5 * math.cos(2 * thita / 180 * Pi) ** 2 / math.sin(2 * thita / 180 * Pi) / math.sin(thita / 180 * Pi)) \
                                            * multiply_factor * math.exp(-n / lattice_distance(h, k, l))
                                a = (d_monochromate * math.cos(thita_monochromate / 180 * Pi)) / (lattice_distance(h, k, l) * math.cos(thita / 180 * Pi))
                                all_message = [n, h, k, l, round(2 * thita, 3), round(intensity, 3), a]
                                total_peak_message.append(all_message)
                                print(f"Order {n} ({h}{k}{l}) at {2 * thita:.3f}° , d = {lattice_distance(h, k, l):.4f} Å , a = {a:.4f} ")

                        else:
                            pass
                    else:
                        messagebox.showwarning("Unsupported Structure", "Please select another crystal structure.")
                        return  # Exit current function or stop further processing


    x = []
    y = []
    a_parameter = []
    a_parameter_square = []
    for i in range(len(total_peak_message)):
        x.append(total_peak_message[i][4])
        y.append(total_peak_message[i][5])
        a_parameter.append(total_peak_message[i][6])
        a_parameter_square.append(total_peak_message[i][6] * total_peak_message[i][6])
#%%
    print ("===================================Table 3: FWHM and Resolution at Different Diffraction Angles====================================")
    print ("diffraction angle   a-value   FWHM(degree)   Angular Resolution   lattice resolution ")
    for i in range(17):
        call_a_parameter = 2 * d_monochromate * math.cos((thita_monochromate / 180) * 3.1416) * math.tan((i + 1) * 5 * 3.1416 / 180) / n_ray
        a_1_over_2_numerator = (alpha1_square * alpha2_square + alpha1_square * alpha3_square + alpha2_square * alpha3_square + \
                       4 * beta_square * (alpha2_square + alpha3_square) - 4 * call_a_parameter * alpha2_square * (alpha1_square + 2 * beta_square) +\
                           4 * call_a_parameter * call_a_parameter * (alpha1_square * alpha2_square + alpha1_square * beta_square + alpha2_square * beta_square))
        a_1_over_2 = (a_1_over_2_numerator / a_1_over_2_denominator) ** 0.5
        resolution_d = round(a_1_over_2 * 0.5 / math.tan((i + 1) * 5 * 3.1416 / 180), 4)
        print ( (i + 1) * 10, "                ", round(call_a_parameter,4), "    ", round(a_1_over_2 * 180 / Pi, 4),   \
               "    ", round((a_1_over_2 * 180 / Pi) / ((i + 1) * 10), 4), "    ", resolution_d )

    # Separator line
#%%
    print ("====================================Table 4: Diffraction Angles and Resolution Information=====================================")

    # Create a list for total diffraction pattern intensity, with initial intensity set to 0 for each angle
    for k in range(1800):
        total_angle_intensity.append(0)
        
    results = []
    for i in range(len(x)):
        # First calculate numerator of resolution caused by collimators and monochromator
        a_1_over_2_numerator = (alpha1_square * alpha2_square + alpha1_square * alpha3_square + alpha2_square * alpha3_square + \
                       4 * beta_square * (alpha2_square + alpha3_square) - 4 * a_parameter[i] * alpha2_square * (alpha1_square + 2 * beta_square) + \
                           4 * a_parameter_square[i] * (alpha1_square * alpha2_square + alpha1_square * beta_square + alpha2_square * beta_square))

        # Calculate FWHM of the diffraction peak
        a_1_over_2 = (a_1_over_2_numerator / a_1_over_2_denominator) ** 0.5        
        
        # Convert FWHM to degrees
        fwhm = a_1_over_2 * 180 / 3.1416
        # Calculate standard deviation
        sigma = fwhm / 2.355
        angle = x[i]
        a_val = a_parameter[i]
        resolution = fwhm / angle
        results.append({
            "Peak Angle (°)": round(angle, 3),
            "a-value (Å)": round(a_val, 5),
            "Angular Resolution": round(resolution, 5),
            "FWHM (°)": round(fwhm, 5),
            "Std Dev": round(sigma, 5)
        })
       
        # Calculate Gaussian distribution of each peak, sampling every 0.1 degrees
        # Create lists to store intensity at different angles
        angle_intensity_x = []
        angle_intensity_y = []
        for j in range(1800):
            intensity = y[i] * (1 / (sigma * ((2 * Pi) ** 0.5))) * math.exp(-(((j / 10) - x[i]) ** 2 / (2 * (sigma ** 2)))) * weighting
            angle_intensity_x.append(j / 10)
            angle_intensity_y.append(intensity)
            total_angle_intensity[j] = total_angle_intensity[j] + angle_intensity_y[j]

        # Set axis labels        
        plt.xlabel("2*theta")
        plt.ylabel("Relative Intensity")

    # Set plot color
    if linecolor == "1":
        linecolor = "b"
    elif linecolor == "2":
        linecolor = "r"
    else:
        linecolor = "g"

    # Plot the curve
    plt.plot(angle_intensity_x, total_angle_intensity, linecolor)

    # Set y-axis max value and determine text placement height
    if max(total_angle_intensity) >= 12:
        y_max = max(total_angle_intensity) - 1
    else:
        y_max = 12
        plt.ylim(0, 13)

    # Set y-axis max value and determine text placement height
    if max(total_angle_intensity) >= 12:
        y_max = max(total_angle_intensity) - 1
    else:
        y_max = 12
        plt.ylim(0, 13)

    # Set y-axis max value and determine text placement height
    if max(total_angle_intensity) >= 12:
        y_max = max(total_angle_intensity) - 1
    else:
        y_max = 12
        plt.ylim(0, 13)

    # Dynamically determine text start position and line spacing
    if max(total_angle_intensity) >= 20:
        text_y_start = max(total_angle_intensity) * 0.75
        line_spacing = max(total_angle_intensity) * 0.04
    else:
        text_y_start = 12
        line_spacing = 0.7



    # Automatically generate legend text (including α, β, Bragg angle, d-spacing, and FWHM)
    label = (
        f"α₁={round(alpha1, 4)}, "
        f"α₂={round(alpha2, 4)}, "
        f"α₃={round(alpha3, 4)}, "
        f"β={round(beta, 4)}, "
        f"d={round(d_monochromate, 2)} Å, "
        f"θ={round(thita_monochromate, 2)}°, "
        f"λ={round(n_ray, 4)}, "
#        f"FWHMₘᵢₙ={round(a_1_over_2_min, 4)}"
    )

    # Plot the curve and add legend
    plt.gcf().set_size_inches(10, 6)
    plt.plot(angle_intensity_x, total_angle_intensity, color=linecolor, label=label)
    plt.legend(fontsize=7, loc="upper right")
    
    # Convert to DataFrame
    df = pd.DataFrame(results)

    # Remove duplicate entries (same angle and a-value)
    df_cleaned = df.drop_duplicates(subset=["Peak Angle (°)", "a-value (Å)"])

    # Sort the data (optional)
    df_cleaned = df_cleaned.sort_values(by="Peak Angle (°)")

    # Print a well-formatted table
    print(df_cleaned.to_string(index=False))
    
    # === Replace plt.show() with embedded TkAgg window ===
    from tkinter import Toplevel
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

    # build new window
    global plot_window
    if plot_window is not None and plot_window.winfo_exists():
        plot_window.destroy()
    plot_window = Toplevel()
    plot_window.title("Simulated Diffraction Pattern")

    # add Fig
    canvas = FigureCanvasTkAgg(plt.gcf(), master=plot_window)
    canvas.draw()
    canvas.get_tk_widget().pack()
    
    # === save fig botton ===
    def save_figure():
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Image", "*.png"), ("All Files", "*.*")],
            title="Save Diffraction Plot"
        )
        if file_path:
            plt.gcf().savefig(file_path, dpi=300, bbox_inches="tight")

    Button(plot_window, text="Save Image", command=save_figure).pack(pady=5) 
    
    # === Export Data ===
    def save_data():
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title="Save 2theta-Intensity Data"
        )
        if file_path:
            with open(file_path, "w", newline="") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["2theta (deg)", "Intensity"])
                for xi, yi in zip(angle_intensity_x, total_angle_intensity):
                    writer.writerow([round(xi, 3), round(yi, 5)])

    # === add botton ===
    Button(plot_window, text="Export Data", command=save_data).pack(pady=3)
    
    def clear_figure():
        plt.clf()
        canvas.draw()

    Button(plot_window, text="Clear Plot", command=clear_figure).pack(pady=2)
    
#%%
"""Create the function button"""
button = Button(window, text='Start Calculation', command=calculate, font=("Arial", 16))  # Create button to execute function when clicked

"""Place the created widgets into the GUI interface in order"""
# Title and image
label1.grid(row=1, column=0, columnspan=2, sticky="n")
label2.grid(row=2, column=0, columnspan=2)

# Collimator parameters
label3.grid(row=3, column=0)
entry1.grid(row=3, column=1)

label4.grid(row=4, column=0)
entry2.grid(row=4, column=1)

label5.grid(row=5, column=0)
entry3.grid(row=5, column=1)

# Monochromator parameters
label6.grid(row=6, column=0)
entry4.grid(row=6, column=1)
label7.grid(row=7, column=0)
entry5.grid(row=7, column=1)
label8.grid(row=8, column=0)
entry6.grid(row=8, column=1)

# Sample lattice constants
label9.grid(row=9, column=0)
entry7.grid(row=9, column=1)
label10.grid(row=10, column=0)
entry8.grid(row=10, column=1)
label11.grid(row=11, column=0)
entry9.grid(row=11, column=1)

# Neutron parameters
label12.grid(row=12, column=0)
entry10.grid(row=12, column=1)

# Plot color
label121.grid(row=13, column=0)
entry101.grid(row=13, column=1)
hint_color.grid(row=14, column=0)
label122.grid(row=15, column=0)
entry102.grid(row=15, column=1)
hint_weight.grid(row=16, column=0)

# Function button
button.grid(row=17, column=0, columnspan=2)

# Reference and author
label13.grid(row=18, column=0)
label14.grid(row=19, column=0)
label15.grid(row=19, column=1)
label16.grid(row=20, column=0)
label18.grid(row=21, column=0)
label19.grid(row=22, column=1)

"""Run the window program"""
window.mainloop()



