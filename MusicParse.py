from pydub import AudioSegment
import os
import pymongo
import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt
from IPython.display import Audio

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["mydatabase"]
MusicCollection = db["MusicCollection"]

######## Hyper-Param ##########
time_unit = 60 * 1000 # one min
n_peaks = 20 # 20 hashes 
spacing = 200
###############################

# HELPERS
def slice_song(path, time_unit):
    dir_path, file_name = os.path.split(path)
    file_name = file_name.split(".")[0]
    print("Directory Path:", dir_path)
    print("File Name:", file_name)
    os.mkdir(dir_path + "\\" + file_name)

    song = AudioSegment.from_file(path, format = 'wav')
    length_in_seconds = len(song) / 1000

    i = 0
    while i < (int(length_in_seconds // (time_unit/1000))):
        segment = song[i*time_unit : (i+1)*time_unit]
        segment.export(dir_path + "\\" + file_name + "\\" + file_name + str(i) + ".wav",format="wav")
        i += 1
    segment = song[i*time_unit : length_in_seconds*1000]
    segment.export(dir_path + "\\" + file_name + "\\" + file_name + str(i) + ".wav",format="wav")

def insert_DB(my_document):
    MusicCollection.insert_one(my_document)

def Convert_WaveFFT(path):
    freq, amplitude_arr = wavfile.read(path)
    #print(amplitude_arr)

    FFT_arr = np.fft.fft(amplitude_arr)
    FFT_arr_abs = np.abs(FFT_arr.real)
    
    
    N = len(amplitude_arr)
    freq_axis = np.linspace(0, freq/2, N//2)
    
    CreateSigniture(N, freq_axis[:N//2], FFT_arr_abs[:N//2])

    # print(FFT_arr_abs[:15])
    # print(FFT_arr_abs[:,0])
    # print(freq_axis)
    plt.plot(freq_axis[:N//2], FFT_arr_abs[0:N//2])
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude')
    plt.show()

def CreateSigniture(N, freq_axis, amplitude_arr):
    hash_arry = [None] * (20000//spacing)
    x_axs = [None] * (20000//spacing)

    temp_freq = spacing
    cnt = 0
    i = 0
    i_start = i
    i_end = i
    while cnt < len(hash_arry):
        while freq_axis[i] < temp_freq:
            i_end += 1
            i += 1

        i -= 1
        
        hash_arry[cnt] = np.max(amplitude_arr[i_start:i_end])
        x_axs[cnt] = freq_axis[i]
        print("Less than " + str(freq_axis[i]) + ": " + str(hash_arry[cnt]))
        temp_freq += spacing
        i_start = i_end
        cnt += 1

    print(len(hash_arry))
    print(hash_arry)
    # plt.plot(x_axs, hash_arry)
    return hash_arry

def AddToTable():


# MAIN FUNC
def main():
    path = "C:\\Users\\Patrick\\Desktop\\MusicReco\\src\\Aimer-StarRingChild.wav"
    # slice_song(path, time_unit)
    Convert_WaveFFT("C:\\Users\\Patrick\\Desktop\\MusicReco\\src\\Aimer-StarRingChild\\Aimer-StarRingChild0.wav")
    
if __name__ == "__main__":
    main()