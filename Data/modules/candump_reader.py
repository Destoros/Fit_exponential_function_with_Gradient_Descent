import numpy as np
import pandas as pd

class CandumpReader():

    df: pd.DataFrame

    def read_log_file_and_clean_data(self, filename: str) -> pd.DataFrame:
        col_names = ["Timestamp", "CAN interface", "Frame"]
        df = pd.read_csv(filename, sep=" ",header=None, names=col_names)


        # data cleaning
        #remove brackets, convert to float and shift the time
        df["Timestamp"] = df["Timestamp"].str.replace("(", "")
        df["Timestamp"] = df["Timestamp"].str.replace(")", "").astype(float) #convert to float
        df["Timestamp"] -= df["Timestamp"][0] #the first entry should equal 0

        df["Frame"] = df["Frame"].str.replace("##", "#") #replace all occurings of two hashtags, marking CAN FD frames, with only one
        df[["ID", "Data"]] = df["Frame"].str.split("#", expand=True)

        #delete the frame column, its redundant
        df = df.drop("Frame", axis=1)


        df["Data"] = df["Data"].str[1:] #remove the first hex number of the Data col, because it is not part of the actual data

        self.df = df

    @staticmethod
    def change_endianess(input: str) -> str:
        #Reverses the endianess of a hex string
        #e.g. DE03AB > AB03DE
        ba = bytearray.fromhex(input)
        ba.reverse()
        return ba.hex()

    def get_data_from_can_frame(self, arbitration_id: int, byte_range: list, endianess: str = "big-endian") -> np.ndarray:

        #create a local copy of df, do not change the base data frame
        df = self.df

        arbitration_id = str(arbitration_id) #convert the number to a string

        df = df[df["ID"] == arbitration_id] #remove all entries but the wanted arbitration ID

        if df.empty:
            raise Exception("Data frame is empty")

        
        y = df["Data"].str[2*(byte_range[0]-1):2*(byte_range[1]-1)].to_numpy()#extract the relevant databytes

        match endianess:
            case "big-endian": #higher order byte first
                pass #reading from left to right is already big endianess
            case "little-endian": #lower order byte first
                #apply the change_endianess function to element in the y array
                y = np.array([self.change_endianess(yi) for yi in y])   
                    
            case _:
                print("endianess can be either 'big-endian' or 'little-endian'")

        y = np.array([int(xi, 16) for xi in y])#convert all hex bytes to int

        #get the time (x -axis)
        t = df["Timestamp"].to_numpy()

        return y, t
