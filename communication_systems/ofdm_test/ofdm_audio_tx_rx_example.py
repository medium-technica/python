import commpy
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal, misc
import scipy.interpolate
import scipy.io.wavfile as audio
import math
import binascii
import time as t

def Mapping(mapping_table, bits):
	return np.array([mapping_table[tuple(b)] for b in bits])

def SP(dataCarriers, bits, mu):
	return bits.reshape((len(dataCarriers), mu))

def OFDM_symbol(K, pilotCarriers, pilotValue, dataCarriers, QAM_payload):
	symbol = np.zeros(K, dtype=complex) # the overall K subcarriers
	symbol[pilotCarriers] = pilotValue  # allocate the pilot subcarriers 
	symbol[dataCarriers] = QAM_payload  # allocate the pilot subcarriers
	return symbol      

def IDFT(OFDM_data):
	return np.fft.ifft(OFDM_data)

def addCP(CP, OFDM_time):
	cp = OFDM_time[-CP:]               # take the last CP samples ...
	return np.hstack([cp, OFDM_time])  # ... and add them to the beginning
		
def generate_single_ofdm_block(data_block, K, mu, CP, P, pilotValue):

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
	demapping_table = {v : k for k, v in mapping_table.items()}
	allCarriers = np.arange(K)  # indices of all subcarriers ([0, 1, ... K-1])
	pilotCarriers = allCarriers[::K//P] # Pilots is every (K/P)th carrier.
	pilotCarriers = np.hstack([pilotCarriers, np.array([allCarriers[-1]])])
	dataCarriers = np.delete(allCarriers, pilotCarriers)
	payloadBits_per_OFDM = len(dataCarriers)*mu  # number of payload bits per OFDM symbol
	bits = data_block
	bits_SP = SP(dataCarriers, bits, mu)
	QAM = Mapping(mapping_table, bits_SP)
	OFDM_data = OFDM_symbol(K, pilotCarriers, pilotValue, dataCarriers, QAM)
	OFDM_time = IDFT(OFDM_data)
	OFDM_withCP = addCP(CP, OFDM_time)
	OFDM_TX = OFDM_withCP
	return OFDM_TX
	
def convert_complex_signal_to_quad_signal(complex_signal, Fs, fc, Ts):	
	print("Converting complex signal to quadrature modulated signal...")
	dk = complex_signal
	BN = 1/(2*Ts )   # the Nyquist bandwidth of the baseband signal.
	ups = int(Ts*Fs) # number of samples per symbol in the "analog" domain
	N = len(complex_signal) # number of transmitted baseband samples
	t0 = 3*Ts  
	_, rrc = commpy.filters.rrcosfilter(N=int(2*t0*Fs), alpha=1,Ts=Ts, Fs=Fs)
	t_rrc = np.arange(len(rrc)) / Fs  # the time points that correspond to the filter values
	t_symbols = Ts * np.arange(N)                         # time instants of the baseband samples
	x = np.zeros(ups*N, dtype='complex')
	x[::ups] = dk  # every ups samples, the value of dn is inserted into the sequence
	t_x = np.arange(len(x))/Fs
	u = np.convolve(x, rrc)
	t_u = np.arange(len(u))/Fs
	i = u.real
	q = u.imag
	iup = i * np.cos(2*np.pi*t_u*fc)  
	qup = q * -np.sin(2*np.pi*t_u*fc)
	s = iup + qup
	return s
	
def convert_quad_signal_to_complex_signal(quad_signal, Fs, fc, Ts):
	s = quad_signal
	N = len(s)
	BN = 1/(2*Ts )   # the Nyquist bandwidth of the baseband signal.
	ups = int(Ts*Fs) # number of samples per symbol in the "analog" domain	
	t0 = 3*Ts
	_, rrc = commpy.filters.rrcosfilter(N=int(2*t0*Fs), alpha=1,Ts=Ts, Fs=Fs)
	t_u = np.arange(N)/Fs
	idown = s * np.cos(2*np.pi*-fc*t_u) 
	qdown = s * -np.sin(2*np.pi*fc*t_u)
	cutoff = 5*BN        # arbitrary design parameters
	lowpass_order = 51   
	lowpass_delay = (lowpass_order // 2)/Fs  # a lowpass of order N delays the signal by N/2 samples (see plot)
	lowpass = scipy.signal.firwin(lowpass_order, cutoff/(Fs/2))
	t_lp = np.arange(len(lowpass))/Fs
	f_lp = np.linspace(-Fs/2, Fs/2, 2048, endpoint=False)
	H = np.fft.fftshift(np.fft.fft(lowpass, 2048))
	idown_lp = scipy.signal.lfilter(lowpass, 1, idown)
	qdown_lp = scipy.signal.lfilter(lowpass, 1, qdown)
	v = idown_lp + 1j*qdown_lp
	y = np.convolve(v, rrc) / (sum(rrc**2)) * 2
	delay = int((2*t0 + lowpass_delay)*Fs)
	t_y = np.arange(len(y))/Fs
	t_samples = t_y[delay::ups]
	y_samples = y[delay::ups]
	return y_samples

def convert_data_to_audio(data, file_name):
    print("Saving audio file..."+file_name)
    scaled = np.int16(data/np.max(np.abs(data)) * 32767)
    audio.write(file_name+".wav", 44100, scaled)


def read_audio_to_data_array(filename):
	print("Reading audio file..."+filename)
	sample_rate, samples = audio.read(filename+".wav")
	return samples

def channel(signal, SNRdb):
	print("Inserting Channel Noise...")
	channelResponse = np.array([1, 0, 0.3+0.3j])  # the impulse response of the wireless channel
	convolved = np.convolve(signal, channelResponse)
	signal_power = np.mean(abs(convolved**2))
	sigma2 = signal_power * 10**(-SNRdb/10)  # calculate noise power based on signal power and SNR
	noise = np.sqrt(sigma2/2) * (np.random.randn(*convolved.shape)+1j*np.random.randn(*convolved.shape))
	return convolved + noise

def removeCP(signal, K, CP):
	return signal[CP:(CP+K)]

def DFT(OFDM_RX):
    return np.fft.fft(OFDM_RX)

def channelEstimate(OFDM_demod, pilotCarriers, pilotValue, allCarriers):
	pilots = OFDM_demod[pilotCarriers]  # extract the pilot values from the RX signal
	Hest_at_pilots = pilots / pilotValue # divide by the transmitted pilot values
	Hest_abs = scipy.interpolate.interp1d(pilotCarriers, abs(Hest_at_pilots), kind='linear')(allCarriers)
	Hest_phase = scipy.interpolate.interp1d(pilotCarriers, np.angle(Hest_at_pilots), kind='linear')(allCarriers)
	Hest = Hest_abs * np.exp(1j*Hest_phase)
	return Hest

def equalize(OFDM_demod, Hest):
    return OFDM_demod / Hest

def get_payload(equalized, dataCarriers):
    return equalized[dataCarriers]

def Demapping(QAM, demapping_table):
	constellation = np.array([x for x in demapping_table.keys()])
	dists = abs(QAM.reshape((-1,1)) - constellation.reshape((1,-1)))
	const_index = dists.argmin(axis=1)
	hardDecision = constellation[const_index]
	return np.vstack([demapping_table[C] for C in hardDecision]), hardDecision

def PS(bits):
    return bits.reshape((-1,))

def adjust_string_length(string_data,len_adj):
	len_data = len(string_data)
	len_appended_data = len_adj*math.ceil(len_data/len_adj)
	appended_string_data = string_data.ljust(len_appended_data, '0')
	len_adjusted = len_appended_data - len_data
	return appended_string_data, len_adjusted

def convert_file_to_binary_string(filename):
	#filepath = "mysong.mp3"
	file = open(filename, "rb")
	with file:
		byte = file.read()
		hexadecimal = binascii.b2a_hex(byte)
		decimal = int(hexadecimal, 16)
		binary_string = bin(decimal)[2:].zfill(16)
	binary_string
	return binary_string
	
def convert_binary_string_to_file(binary_string):
	pass
	
def convert_array_data_to_binary_string(data_array):
	bin_data = ""
	for data in data_array:
		hexadecimal = binascii.hexlify(data)
		decimal = int(hexadecimal, 16)
		binary = bin(decimal)[2:].zfill(16)
		bin_data  = bin_data + binary
	return bin_data

def binary_string_to_numeric_array(binary_string):
	numeric_array = []
	char_array = list(binary_string)
	for char_element in char_array:
		numeric_array.append(int(char_element))
	return numeric_array

def recover_data_from_ofdm_block(ofdm_block, K, CP, P, pilotValue):
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
	demapping_table = {v : k for k, v in mapping_table.items()}
	allCarriers = np.arange(K)  # indices of all subcarriers ([0, 1, ... K-1])
	pilotCarriers = allCarriers[::K//P] # Pilots is every (K/P)th carrier.
	pilotCarriers = np.hstack([pilotCarriers, np.array([allCarriers[-1]])])
	dataCarriers = np.delete(allCarriers, pilotCarriers)
	OFDM_RX = ofdm_block
	OFDM_RX_noCP = removeCP(OFDM_RX, K, CP)
	OFDM_demod = DFT(OFDM_RX_noCP)
	Hest = channelEstimate(OFDM_demod, pilotCarriers, pilotValue, allCarriers)
	equalized_Hest = equalize(OFDM_demod, Hest)
	QAM_est = get_payload(equalized_Hest, dataCarriers)
	PS_est, hardDecision = Demapping(QAM_est, demapping_table)
	bits_est = PS(PS_est)
	return bits_est

def convert_audio_to_OFDM_payload_length_adjusted_binary_numeric_array(f_name, payloadBits_per_OFDM):
	audio_data = read_audio_to_data_array(f_name)
	print(len(audio_data))
	binary_data_string = convert_array_data_to_binary_string(audio_data)
	binary_data_string_len_adjusted = adjust_string_length(binary_data_string,payloadBits_per_OFDM)
	binary_numeric_array_len_adjusted = np.asarray(binary_string_to_numeric_array(binary_data_string_len_adjusted))
	return binary_numeric_array_len_adjusted

def length_adjust_binary_string(binary_string, len_adj):
	binary_data_string_len_adjusted, len_adjusted = adjust_string_length(binary_string,len_adj)
	binary_numeric_array_len_adjusted = np.asarray(binary_string_to_numeric_array(binary_data_string_len_adjusted))
	return binary_numeric_array_len_adjusted, len_adjusted

def decode_complex_signal_data_using_ofdm(rx_complex_signal_data, len_ofdm_block, K, CP, P, pilotValue):
	print("Decoding complex signal using OFDM Demodulation...")
	n_ofdm_blocks = len(rx_complex_signal_data)//len_ofdm_block
	rx_binary_message = []	
	for i in range(n_ofdm_blocks):
		ofdm_block = rx_complex_signal_data[i*len_ofdm_block:(i*len_ofdm_block)+len_ofdm_block]
		rx_binary_block = recover_data_from_ofdm_block(ofdm_block, K, CP, P, pilotValue)
		rx_binary_message = np.concatenate([rx_binary_message,rx_binary_block])
		#print("rx: "+str(i))
	
	return(rx_binary_message)

def find_bit_error_rate(tx_binary_message,rx_binary_message):
	bit_error_rate = np.sum(abs(tx_binary_message-rx_binary_message))/len(tx_binary_message)
	return bit_error_rate

def test_run():
	K = 64 # number of OFDM subcarriers
	CP = K//4  # length of the cyclic prefix: 25% of the block
	P = K//8 # number of pilot carriers per OFDM block
	pilotValue = 3+3j # The known value each pilot transmits
	allCarriers = np.arange(K)  # indices of all subcarriers ([0, 1, ... K-1])
	pilotCarriers = allCarriers[::K//P] # Pilots is every (K/P)th carrier.
	pilotCarriers = np.hstack([pilotCarriers, np.array([allCarriers[-1]])])
	dataCarriers = np.delete(allCarriers, pilotCarriers)
	mu = 4 # bits per symbol (i.e. 16QAM)
	payloadBits_per_OFDM = len(dataCarriers)*mu  # number of payload bits per OFDM symbol
	len_ofdm_block = K+CP
	'''
	binary_message = "0000"
	tx_binary_message = ""
	for i in range(1*55):
		tx_binary_message = tx_binary_message + binary_message
	print("No. of bits in message = "+str(len(tx_binary_message)))
	'''
	n_blocks = 1 # No. of OFDM blocks for Transmission
	tx_binary_message = np.random.binomial(n=1, p=0.5, size=(payloadBits_per_OFDM*n_blocks, ))
	'''
	#tx_binary_message = convert_file_to_binary_string("array_to_wave.py")
	tx_binary_message, len_adjusted = length_adjust_binary_string(tx_binary_message, payloadBits_per_OFDM)
	#tx_binary_message = convert_audio_to_OFDM_payload_length_adjusted_binary_numeric_array(f_name_tx, len_ofdm_block)
	'''
	n_blocks = int(len(tx_binary_message)/payloadBits_per_OFDM)
	tx_ofdm_signal = []
	for i in range(n_blocks):
		data_block = tx_binary_message[i*payloadBits_per_OFDM:(i*payloadBits_per_OFDM)+payloadBits_per_OFDM]
		tx_ofdm_signal = np.concatenate([tx_ofdm_signal,generate_single_ofdm_block(data_block, K, mu, CP, P, pilotValue)])

	fc = int(3e3)	# carrier frequency for quadrature modulation
	Fs = int(44100)	# the sampling frequency we use for the discrete simulation of analog signals
	Ts = 1.25e-3		# symbol spacing, i.e. the baseband samples are Ts seconds apart.
	
	SNRdb = 25  # signal to noise-ratio in dB at the receiver
	print("len: "+str(len_ofdm_block))
	tx_signal = channel(tx_ofdm_signal, SNRdb)
	#tx_signal_on_audio  = convert_complex_signal_to_quad_signal(tx_signal, Fs, fc, Ts)
	temp_a = np.random.randn(200)
	for i in range(1000):
		temp_a = np.hstack([temp_a, tx_signal])
	peakindex = 0
	y = np.zeros(CP)
	for i in range(len(temp_a)-len_ofdm_block):
		temp = temp_a[i:i+len_ofdm_block]
		y = y + np.correlate(temp[:CP],temp[-CP:], "same")
	
	y = abs(y/max(abs(y)))
	par = 1 / np.mean(y)
	peakindex = find_peaks(y)
	print(peakindex/par)
	plt.plot(y)
	plt.show()
	'''
	f_name_tx = "C:/Users/abraham/Music/ofdm_audio/ofdm_audio_tx"
	convert_data_to_audio(tx_signal_on_audio,f_name_tx) 
	f_name_rx = "C:/Users/abraham/Music/ofdm_audio/ofdm_audio_rx"
	f_name_rx = f_name_tx
	rx_signal_on_audio = read_audio_to_data_array(f_name_rx)
	
	rx_ofdm_signal = convert_quad_signal_to_complex_signal(rx_signal_on_audio, Fs, fc, Ts)
	rx_binary_message = decode_complex_signal_data_using_ofdm(rx_ofdm_signal, len_ofdm_block, K, CP, P, pilotValue)
	rx_b_m = []
	for i in rx_binary_message:
		rx_b_m.append(int(i))
	rx_binary_message = np.asarray(rx_b_m)
	bit_error_rate = find_bit_error_rate(tx_binary_message,rx_binary_message)
	#print(rx_binary_message)
	#print(tx_binary_message)
	print ("Obtained Bit error rate: ", bit_error_rate)
	'''

def find_peaks(array):
	max_value = 0
	index = 0
	for i in range(len(array)):
		if(max_value < array[i]):
			max_value = array[i]
			index = i
	return index

def add_sync_header_to_signal(signal):
	return np.concatenate([np.ones(1000), -1*np.ones(1000), signal, np.ones(1000), -1*np.ones(1000)])

def circular_convolution(x1, x2):
	N = max(len(x1), len(x1))
	n = np.arange(N)
	if(len(x1)>len(x2)):
		x2 = np.hstack([x2, np.zeros(len(x1)-len(x2))])
		plt.plot(x2)
	else:
		x1 = np.hstack([x1, np.zeros(len(x2)-len(x1))])
		plt.plot(x2)
	y = np.fft.ifft(np.fft.fft(x1[n]) * np.fft.fft(x2[n]))
	return y

test_run()
