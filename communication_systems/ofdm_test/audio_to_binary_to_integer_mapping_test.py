import numpy as np
import matplotlib.pyplot as plt
from scipy import signal, misc
import scipy.interpolate
import scipy.io.wavfile as audio
import math
import binascii

mapping_table = {
		(0,0,0,0) : -3-3j,
		(0,0,0,1) : -3-1j,
		(0,0,1,0) : -3+3j,
		(0,0,1,1) : -3+1j,
		(0,1,0,0) : -1-3j,
		(0,1,0,1) : -1-1j,
		(0,1,1,0) : -1+3j,
		(0,1,1,1) : -1+1j,
		(1,0,0,0) :  3-3j,
		(1,0,0,1) :  3-1j,
		(1,0,1,0) :  3+3j,
		(1,0,1,1) :  3+1j,
		(1,1,0,0) :  1-3j,
		(1,1,0,1) :  1-1j,
		(1,1,1,0) :  1+3j,
		(1,1,1,1) :  1+1j
	}

def map_binary_array_to_symbol_array(mapping_table, binary_array):
		return np.array([mapping_table[tuple(b)] for b in bits])
		
def adjust_string_length(string_data,len_adj):
	len_data = len(string_data)
	len_appended_data = len_adj*math.ceil(len_data/len_adj)
	appended_string_data = string_data.ljust(len_appended_data, '0')
	return appended_string_data

def group_binary_message_to_binary_word_array(binary_message, word_size):
	return binary_message.reshape(len(binary_message)//word_size, word_size)


def convert_complex_data_to_quadrature_data(complex_data, Fs, fc, T_symbol):
	global Fs, fc, Ts, BN, t_u

	#Fs = int(44100)    # the sampling frequency we use for the discrete simulation of analog signals

	#fc = int(3e3)
	#Ts = 1e-3        # 1 ms symbol spacing, i.e. the baseband samples are Ts seconds apart.
	Ts = T_symbol
	BN = 1/(2*Ts )   # the Nyquist bandwidth of the baseband signal.
	
	t_u = np.arange(len(ofdm_data))/Fs
	tx_i = ofdm_data.real
	tx_q = ofdm_data.imag

	tx_iup = tx_i * np.cos(2*np.pi*t_u*fc)  
	tx_qup = tx_q * -np.sin(2*np.pi*t_u*fc)

	quad_ofdm_data = tx_iup + tx_qup
	return quad_ofdm_data	

x = np.asarray([1,0,1,1,1,1])
print(group_binary_message_to_binary_word_array(x,2))
