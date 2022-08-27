from django.shortcuts import render
from .main import call, function_sound
from .sound_processing import play_sound
##########################################
# sound recording libraries
import pyaudio
from pydub import AudioSegment
import wave
import time
from os import *
record = True
path = getcwd()
last_file_name = ''

def index(request):
    return render(request,'index.html')
def result(request):
    if request.method == 'POST':
        input = request.POST.get('text','default')
        b_1 = request.POST.get('b_1')
        print("sssssssssssssssssssssssssssssssssssss")
        print(b_1)
        if b_1 == '1':
            out = call(input)
            print("sssssssssssssssssssssssssssssssssssss")
            return render(request,'result.html', {'out_1': out})
        else:
            if input == '':
                text = 'للللل'
            else:
                text = input
            array = []
            path_1 = getcwd()
            chdir("sounds")
            for i , l in enumerate(text):
                if i+1 < len(text):
                    if text[i+1] == "ا":
                        l += text[i+1]
                if l != 'ا':
                    array.append(AudioSegment.from_file("{}.m4a".format(l), format="m4a"))
            # sound1 6 dB louder
            # louder = sound1 + 6
            # sound1, with sound2 appended (use louder instead of sound1 to append the louder version)
            combined = 0
            for i in range(len(array)):
                halfway_point = len(array[i]) // 2
                combined += array[i][halfway_point - 190 : len(array[i]) - 170]
            # simple export
            file_handle = combined.export("output.mp3", format="mp3")
            chdir(path_1)
            out = 'Done'
            return render(request,'result.html', {'out_1': out})
    else:
        out_1 = call()
        count = 1
        out={'out_1':out_1,'count': count}
        return render(request,'result.html', out)
def sound(request):
    global record
    return render(request,'sound.html', {'recording': record})
def sound_recording(request):
    global record,last_file_name
    timeout = 3   # [seconds]
    timeout_start = time.time()
    audio = pyaudio.PyAudio()
    stream = audio.open(format = pyaudio.paInt16, channels=1, rate=44100, input=True , frames_per_buffer=1024)
    frames = []
    if request.method == "POST":
        file_name = request.POST.get("file_name")
        try:
            while time.time() < timeout_start + timeout:
                data = stream.read(1024)
                frames.append(data)
        except InterruptedError:
            pass
        path_1 = getcwd()
        chdir("new_sounds")
        path_2 = getcwd()
        stream.stop_stream()
        stream.close()
        audio.terminate()
        file_name = file_name + ".wav"
        last_file_name = path_2 + "\\" + file_name
        sound_file = wave.open(file_name, "wb")
        sound_file.setnchannels(1)
        sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        sound_file.setframerate(44100)
        sound_file.writeframes(b''.join(frames))
        sound_file.close()
        chdir(path_1)
        print(last_file_name)
        play = last_file_name
        return render(request,'sound.html', {'recording': 'Recording succeeded',
                                                'try': record, 'play': play})
    else:
        record = False
        return render(request,'sound.html', {'recording': 'Recording succeeded', 'try': record})
from time import sleep
def play_tts(request):
    function_sound()
    out = 'Done'
    return render(request,'result.html', {'out_1': out})

def sound_result(request):
    out_sound = play_sound(last_file_name)
    return render(request,'sound.html', {'recording': 'Recording succeeded', 'try': record,'out_s': out_sound})
def sound_result_plt1(request):
    out_sound = find_letters()
    return render(request,'sound.html', {'recording': 'Recording succeeded', 'try': record,'out_s': out_sound})


# def sound_result(request):
#     global record
#     if request.method == "POST":
#         file_name = request.POST.get("file_name")
#         start = request.POST.get("Recording_sound")
#         if stop == "False":
#             record = False
#         else:
#             record = True
#         recording(file_name)
#         print(file_name)
#     return render(request,'sound.html', {'recording': 'stored'})
