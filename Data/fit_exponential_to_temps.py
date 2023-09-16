import matplotlib.pyplot as plt
import os
import numpy as np

from modules.candump_reader import CandumpReader
from modules.fit_exponential_function import FitExponentialFunction

FIGUREFOLDER = "Figures/"
LOGSFOLDER = "Logs/"
COEFFICIENTSFOLDER = "Coefficients/"

#T_RANGE is the range within which the temperature rises. This is used to window only the wanted part for which an exponential functin should be fitted

FILENAME = "fan_10_percent.log"; T_RANGE = [42, 245]; 
# FILENAME = "fan_20_percent.log"; T_RANGE = [90, 475]; 
# FILENAME = "fan_30_percent.log"; T_RANGE = [65, 387]; 
# FILENAME = "fan_40_percent.log"; T_RANGE = [64, 850]; 
# FILENAME = "fan_50_percent.log"; T_RANGE = [67, 317]; 
# FILENAME = "fan_60_percent.log"; T_RANGE = [53, 501]; 
# FILENAME = "fan_70_percent.log"; T_RANGE = [28, 850]; 
# FILENAME = "fan_80_percent.log"; T_RANGE = [22, 541]; 
# FILENAME = "fan_90_percent.log"; T_RANGE = [55, 434]; 



def main():

    print(f"Working on {FILENAME}")

    #init the reader
    candump_reader = CandumpReader()

    #load the logfile into the candump reader class
    candump_reader.read_log_file_and_clean_data(LOGSFOLDER + FILENAME)        

    #get the temperatures
    temp_1,t_all = candump_reader.get_data_from_can_frame(601, [13, 14])
    temp_2,t_all = candump_reader.get_data_from_can_frame(601, [14, 15])
    temp_3,t_all = candump_reader.get_data_from_can_frame(601, [15, 16])
    temp_4,t_all = candump_reader.get_data_from_can_frame(601, [16, 17])


    # #Take the average of T2 to T4 (T1 is at a the neutral line, which experiences way less heat)
    # avg_temp_curve = np.mean(np.array([temp_2, temp_3, temp_4]), axis=0) 
    #not useful, because it changes the shape from an exponential to a different one


    #window the range, in which the actual temperature rises
    t_valid = np.logical_and(t_all > T_RANGE[0], t_all < T_RANGE[1])

    #Take T4 all the time, since it is has the highest values over all fan speeds
    d = temp_4[t_valid]
    t = t_all[t_valid]

    #EXECUTE FITTING ALGORITHM
    #define some plausible init values (determine this from the plot of the data d)
    init_values = np.array([53,10,130,120], dtype=np.float64).reshape(-1,1) 

    #for best performance, fix the parameter a, since it has a huge impact on the other parameters
    fix_init_values = [False, False, False, False]

    #define the class, providing the time, measurements, step size, initial values, max iteration amount an which parameters of the inital values should stay fixed
    fitter = FitExponentialFunction(t, d, gamma=2, initial_values=init_values, iter_max=2000, fix_initial_values=fix_init_values)

    #fit the exponential, may take some time
    fitter.fit_exponential()

    #get the fitted exponential in form of a lambda function
    f = fitter.get_fitted_function()

    #print the coefficients
    coeffs = fitter.print_coefficients()
    u = fitter.get_coefficients()

    with open(COEFFICIENTSFOLDER + str.split(FILENAME,".")[0] +".txt", 'w') as file:
        file.write(str(coeffs))


    # plot the data
    fig, (ax0) = plt.subplots()
    ax0.plot(t_all,temp_1, label="T1")
    ax0.plot(t_all,temp_2, label="T2")
    ax0.plot(t_all,temp_3, label="T3")
    ax0.plot(t_all,temp_4, label="T4")
    ax0.plot(t,f(t), label="T4 fitted")
    ax0.set_ylabel("temperature \nin °C")
    ax0.set_title(f"{FILENAME}\nT4 fitted exponential function with tau = {u[3][0]:.2f}s ")
    ax0.legend()
    ax0.grid("on")
    ax0.set_xlabel("time in s")


    #save the figure inside the FIGUREFOLDER
    fig_filename = str.split(FILENAME, ".")[0]
    fig_filename = FIGUREFOLDER + fig_filename + "fitted_exponential" + ".png"
    fig.savefig(fig_filename)


    plt.show()




if __name__ == "__main__":
    main()

