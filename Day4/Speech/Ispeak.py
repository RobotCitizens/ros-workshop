from playsound import playsound
import pyaudio
import wave

print(' Speaking ...')
playsound('./nictomeet.mp3')
playsound('./angus.mp3')
print(' Start to ask for speak')
playsound("./speak_after.mp3")
playsound("./signal.mp3")

chunk = 1024  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 2
fs = 44100  # Record at 44100 samples per second
seconds = 4
filename = "sound_out.wav"

print('Recording ......')
p = pyaudio.PyAudio()  # Create an interface to PortAudio
stream = p.open(format=sample_format,
                channels=channels,
                rate=fs,
                frames_per_buffer=chunk,
                input=True)

frames = []  # Initialize array to store frames

# Store data in chunks for 4 seconds
for i in range(0, int(fs / chunk * seconds)):
    data = stream.read(chunk)
    frames.append(data)

# Stop and close the stream 
stream.stop_stream()
stream.close()
# Terminate the PortAudio interface
p.terminate()

print('Finished recording ....')

# Save the recorded data as a WAV file
wf = wave.open(filename, 'wb')
wf.setnchannels(channels)
wf.setsampwidth(p.get_sample_size(sample_format))
wf.setframerate(fs)
wf.writeframes(b''.join(frames))
wf.close()

playsound("./signal.mp3")
playsound('./ihear.mp3')
playsound('./sound_out.wav')
playsound('./UV_Room.mp3')
playsound('./thanks.mp3')
