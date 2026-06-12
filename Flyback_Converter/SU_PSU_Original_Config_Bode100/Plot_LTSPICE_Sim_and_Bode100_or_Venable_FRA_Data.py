import pyvisa as visa
import time
import numpy as np
import matplotlib.pyplot as plt
import os
import glob
import re
from matplotlib.pyplot import cm
import matplotlib as mpl

# Converts target LTSPICE bode .txt file to csv
def parse_ltspice_db_angle_data(textfile):
    with open(textfile, 'rb') as f:
        data = f.readlines()

    freq=[]
    mag_db=[]
    angle_deg=[]

    """ Patter to pick out all numbers (in scientific notation) from string using regular expressions"""
    regular_expression_pattern_for_sci_notation = '-?[\d.]+(?:[Ee][+-]?\d+)?'
 
    for k in range(1,len(data)):
        
        data[k] = re.findall(regular_expression_pattern_for_sci_notation, str(data[k]))
        
        freq.append(float(data[k][0]))
        mag_db.append(float(data[k][1]))
        angle_deg.append(float(data[k][2]))
        
    return np.array([np.array(freq),np.array(mag_db),np.array(angle_deg)])

def numerical_sort(file_list):
    def convert(text):
        return int(text) if text.isdigit() else text.lower()
    def alphanum_key(key):
        return [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(file_list, key=alphanum_key)
  
def get_venable_dat_files():
  """Returns a list of all CSV files in the current directory."""
  dat_files = glob.glob("*.dat")
  return numerical_sort(dat_files)

# Converts all Venable FRA .dat files to csv, without deleting original .dat files.
def convert_all_venable_dat_files_to_csv():
    data = []
    
    dat_file_list = get_venable_dat_files()     # Get all dat files in current directory
    for i in range(0,len(dat_file_list)):
        temp_list = []
        data.append(np.genfromtxt(dat_file_list[i]))

        for k in range(1, len(data[i])-1, 2):
            freq = (data[i][:,0][k])
            gain = (data[i][:,3][k]-data[i][:,3][k-1])
            phase = (data[i][:,4][k])
            temp_list.append([freq, gain, phase])

        np.savetxt(dat_file_list[i].replace('.dat','.csv'),np.column_stack((np.array(temp_list))),delimiter=',')

def convert_venable_dat_file_to_csv(venable_dat_file, swap_CH2_and_CH1=False):
    data = (np.genfromtxt(venable_dat_file))
    temp_list=[]
    for k in range(1, len(data)-1, 2):
        freq = (data[:,0][k])
        gain = (data[:,3][k]-data[:,3][k-1])
        phase = (data[:,4][k])
        if swap_CH2_and_CH1:
            temp_list.append([freq, -gain, -phase])
        else:
            temp_list.append([freq, gain, phase])
        
        
    np.savetxt(venable_dat_file.replace('.dat','.csv'),np.column_stack((np.array(temp_list))),delimiter=',')
    return data

def convert_LTSPICE_txt_and_Venable_FRA_dat_files_to_csv_and_plot(ltspice_txt_file, venable_dat_file, swap_CH2_and_CH1=False, venable_mag_scaling_factor_dB = 0):
    
    sim_data = parse_ltspice_db_angle_data(ltspice_txt_file)
    
    meas_data = convert_venable_dat_file_to_csv(venable_dat_file)
    meas_freq = meas_data[1::2,0]
    meas_gain = meas_data[1::2,3]-meas_data[::2,3]
    meas_phase = (meas_data[1::2,4])

    if swap_CH2_and_CH1:
        meas_gain = -meas_gain
        meas_phase = -meas_phase

    meas_gain_scaled = meas_gain + venable_mag_scaling_factor_dB

    fig, ax1 = plt.subplots()
    ax1.set_title('Frequency Response', fontsize=20 ,fontweight='bold')
    ax1.set_xlabel('Frequency (Hz)', fontsize=12 ,fontweight='bold')
    ax1.set_ylabel('Gain (dB)', fontsize=12 ,fontweight='bold')
    line1 = ax1.semilogx(sim_data[0], sim_data[1], color='#FF8C00', linestyle='-', label='Simulated Gain')
    line2 = ax1.semilogx(meas_freq, meas_gain_scaled, color='red', label='Measured Gain')
    ax1.tick_params(axis='y')
    ax1.set_xlim([100, 10.0E6])
    ax1.set_ylim([-80.,80.])
    ##ax1.grid(True, which='both')
    ax1.grid(True, which='major', color='0.25') # Solid lines, Black
    ax1.grid(True, which='minor', linestyle='--', color='0.7') # Dashed lines, light gray color


    # Create the second y-axis, sharing the same x-axis
    ax2 = ax1.twinx()

    ax2.set_ylabel('Phase (Deg)', fontsize=12 ,fontweight='bold')
    line3 = ax2.semilogx(sim_data[0], sim_data[2],  color='magenta', linestyle='-', label='Simulated Phase')
    line4 = ax2.semilogx(meas_freq, meas_phase,  color='blue', label='Measured Phase')
    ax2.set_xlim([100, 10.0E6])
    # Set y-axis increments
    ax2.set_yticks(np.arange(-180.0,180.001,45.0)) # Increments of 45
    ax2.set_ylim([-180.,180.])

    # Combine the lines from both axes for the legend
    lines = line1 + line2 + line3 + line4
    labels = [line.get_label() for line in lines]

    # Create the legend
    leg = ax1.legend(lines, labels,  framealpha=1.0, facecolor='white', loc='lower left', fontsize=16, frameon=True, edgecolor='black')

    plt.show()

def read_Bode_100_Impedance_Data(csv_file):
    data = np.genfromtxt(csv_file, delimiter=',', skip_header=1)
    freq = data[::,0]
    mag = data[::,3]
    phase = data[::,6]
    return np.array([freq,mag,phase])

def read_Bode_100_Gain_Data(csv_file):
    data = np.genfromtxt(csv_file, delimiter=',', skip_header=1)
    freq = data[::,0]
    mag = data[::,3]
    phase = data[::,6]
    return np.array([freq,mag,phase])


def convert_LTSPICE_txt_and_Bode_100_Impedance_files_to_csv_and_plot(ltspice_txt_file, bode_100_file):
    
    sim_data = parse_ltspice_db_angle_data(ltspice_txt_file)
    
    meas_data = read_Bode_100_Impedance_Data(bode_100_file)
    meas_freq = meas_data[0]
    meas_gain = 20.0*np.log10(meas_data[1])
    meas_phase = (meas_data[2])

    fig, ax1 = plt.subplots()
    ax1.set_title('Frequency Response', fontsize=20 ,fontweight='bold')
    ax1.set_xlabel('Frequency (Hz)', fontsize=12 ,fontweight='bold')
    ax1.set_ylabel('Magnitude (dB$\Omega$)', fontsize=12 ,fontweight='bold')
    line1 = ax1.semilogx(sim_data[0], sim_data[1], color='#FF8C00', linestyle='-', label='Simulated Magnitude')
    line2 = ax1.semilogx(meas_freq, meas_gain, color='red', label='Measured Magnitude')
    ax1.tick_params(axis='y')
    ax1.set_xlim([100, 40.0E6])
    ax1.set_ylim([-80.,80.])
    ##ax1.grid(True, which='both')
    ax1.grid(True, which='major', color='0.25') # Solid lines, Black
    ax1.grid(True, which='minor', linestyle='--', color='0.7') # Dashed lines, light gray color


    # Create the second y-axis, sharing the same x-axis
    ax2 = ax1.twinx()

    ax2.set_ylabel('Phase (Deg)', fontsize=12 ,fontweight='bold')
    line3 = ax2.semilogx(sim_data[0], sim_data[2],  color='magenta', linestyle='-', label='Simulated Phase')
    line4 = ax2.semilogx(meas_freq, meas_phase,  color='blue', label='Measured Phase')
    ax2.set_xlim([100, 40.0E6])
    # Set y-axis increments
    ax2.set_yticks(np.arange(-180.0,180.001,45.0)) # Increments of 45
    ax2.set_ylim([-180.,180.])

    # Combine the lines from both axes for the legend
    lines = line1 + line2 + line3 + line4
    labels = [line.get_label() for line in lines]

    # Create the legend
    leg = ax1.legend(lines, labels,  framealpha=1.0, facecolor='white', loc='lower left', fontsize=16, frameon=True, edgecolor='black')

    plt.show()
    

def convert_LTSPICE_txt_and_Bode_100_Gain_files_to_csv_and_plot(ltspice_txt_file, bode_100_file):
    
    sim_data = parse_ltspice_db_angle_data(ltspice_txt_file)
    
    meas_data = read_Bode_100_Gain_Data(bode_100_file)
    meas_freq = meas_data[0]
    meas_gain = (meas_data[1])
    meas_phase = (meas_data[2])

    fig, ax1 = plt.subplots()
    ax1.set_title('Frequency Response', fontsize=20 ,fontweight='bold')
    ax1.set_xlabel('Frequency (Hz)', fontsize=12 ,fontweight='bold')
    ax1.set_ylabel('Magnitude (dB)', fontsize=12 ,fontweight='bold')
    line1 = ax1.semilogx(sim_data[0], sim_data[1], color='#FF8C00', linestyle='-', label='Simulated Magnitude')
    line2 = ax1.semilogx(meas_freq, meas_gain, color='red', label='Measured Magnitude')
    ax1.tick_params(axis='y')
    ax1.set_xlim([100, 40.0E6])
    ax1.set_ylim([-80.,80.])
    ##ax1.grid(True, which='both')
    ax1.grid(True, which='major', color='0.25') # Solid lines, Black
    ax1.grid(True, which='minor', linestyle='--', color='0.7') # Dashed lines, light gray color


    # Create the second y-axis, sharing the same x-axis
    ax2 = ax1.twinx()

    ax2.set_ylabel('Phase (Deg)', fontsize=12 ,fontweight='bold')
    line3 = ax2.semilogx(sim_data[0], sim_data[2],  color='magenta', linestyle='-', label='Simulated Phase')
    line4 = ax2.semilogx(meas_freq, meas_phase,  color='blue', label='Measured Phase')
    ax2.set_xlim([100, 40.0E6])
    # Set y-axis increments
    ax2.set_yticks(np.arange(-180.0,180.001,45.0)) # Increments of 45
    ax2.set_ylim([-180.,180.])

    # Combine the lines from both axes for the legend
    lines = line1 + line2 + line3 + line4
    labels = [line.get_label() for line in lines]

    # Create the legend
    leg = ax1.legend(lines, labels,  framealpha=1.0, facecolor='white', loc='lower left', fontsize=16, frameon=True, edgecolor='black')

    plt.show()


if __name__ == "__main__":
    pass


    sim_ltspice_data1 = 'SU_PSU_Averaged_Model_Diode_Refed_to_Primary_Side_Sim.txt'
    meas_venable_data1 = 'SU_EPC_Converter_1.dat'
    convert_LTSPICE_txt_and_Venable_FRA_dat_files_to_csv_and_plot(sim_ltspice_data1,
                                                                  meas_venable_data1,
                                                                  swap_CH2_and_CH1 = True,
                                                                  venable_mag_scaling_factor_dB = 0)


    sim_ltspice_data2 = 'SU_PSU_Averaged_Model_Diode_Refed_to_Primary_Side_Sim.txt'
    meas_venable_data2 = 'SU_EPC_Converter_2.dat'
    convert_LTSPICE_txt_and_Venable_FRA_dat_files_to_csv_and_plot(sim_ltspice_data2,
                                                                  meas_venable_data2,
                                                                  swap_CH2_and_CH1 = True,
                                                                  venable_mag_scaling_factor_dB = 0)



















































    

    


    
