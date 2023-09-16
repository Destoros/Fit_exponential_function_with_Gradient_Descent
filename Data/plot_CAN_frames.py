import matplotlib.pyplot as plt
import os

from modules.candump_reader import CandumpReader

FIGUREFOLDER = "Figures/"
LOGSFOLDER = "Logs/"


def main():

    #init the read
    candump_reader = CandumpReader()

    for filename in os.listdir(LOGSFOLDER):
        if ".log" in filename:

            print(f"Working on {filename}")

            #load the logfile into the candump reader class
            candump_reader.read_log_file_and_clean_data(LOGSFOLDER + filename)        

            #get the temperatures
            temp_1,t = candump_reader.get_data_from_can_frame(601, [13, 14])
            temp_2,t = candump_reader.get_data_from_can_frame(601, [14, 15])
            temp_3,t = candump_reader.get_data_from_can_frame(601, [15, 16])
            temp_4,t = candump_reader.get_data_from_can_frame(601, [16, 17])


            #plot the data
            fig, (ax0, ax1, ax2) = plt.subplots(3,1)
            ax0.plot(t,temp_1, label="T1")
            ax0.plot(t,temp_2, label="T2")
            ax0.plot(t,temp_3, label="T3")
            ax0.plot(t,temp_4, label="T4")
            ax0.set_ylabel("temperature \nin °C")
            ax0.set_title(f"{filename}\nTemperature, Fan speed, bellow pressure over time")
            ax0.legend()
            ax0.grid("on")


            #get the fan speed in %
            fan_speed_in_percent,t = candump_reader.get_data_from_can_frame(202, [5, 6])

            #and plot it
            ax1.plot(t, fan_speed_in_percent, label="fan speed in %")
            ax1.grid("on")
            # ax1.legend()
            ax1.set_ylabel("current fan speed \nin %")
            ax1.set_xlabel("time in s")

            #get the pressure data in hPa
            bellow_pressure_hPa,t = candump_reader.get_data_from_can_frame(601, [2, 4], "little-endian")

            #and plot it
            ax2.plot(t, bellow_pressure_hPa, label="bellow pressure in hPa")
            ax2.grid("on")
            # ax1.legend()
            ax2.set_ylabel("bellow pressure \nin hPa")
            ax2.set_xlabel("time in s")

            # #get the fan motor driver temp
            # fan_motor_driver_temp,t = candump_reader.get_data_from_can_frame(202, [10, 12])

            # #and plot it
            # ax3.plot(t, fan_motor_driver_temp, label="Fan motor driver temp in °C")
            # ax3.grid("on")
            # # ax1.legend()
            # ax3.set_ylabel("Fan motor driver temp \nin °C")
            # ax3.set_xlabel("time in s")


            #make figure folder if it does not exist
            if not os.path.exists(FIGUREFOLDER):
                os.mkdir(FIGUREFOLDER)
            
            #save the figure inside the FIGUREFOLDER
            fig_filename = str.split(filename, "/")[-1]
            fig_filename = str.split(fig_filename, ".")[0]
            fig_filename = FIGUREFOLDER + fig_filename + ".png"
            fig.savefig(fig_filename)

          

         
        

    
    plt.show()




if __name__ == "__main__":
    main()

