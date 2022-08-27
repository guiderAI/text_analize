import IPython.display as ipd
import librosa
import librosa.display
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from pydub import AudioSegment
from glob import glob
from itertools import cycle
from os import *
sns.set_theme(style="white", palette=None)
color_pal = plt.rcParams["axes.prop_cycle"].by_key()["color"]
color_cycle = cycle(plt.rcParams["axes.prop_cycle"].by_key()["color"])
zc_local = 0
rms_local = 0
def play_sound(path):
    global color_pal, zc_local, rms_local
    filename = path
    plt.figure(figsize=(20, 5))
    # , sr=22050, mono=True, offset=0.0, duration=50, res_type='kaiser_best'
    data, sample_rate1 = librosa.load(filename)
    librosa.display.waveshow(data, sr=sample_rate1, max_points=50000, x_axis='time', offset=0)
    pd.Series(data).plot(figsize=(10, 5),
                  lw=1,
                  title='Raw Audio Example',
                  color=color_pal[0])
    plt.show()
    audio_segment = AudioSegment.from_file(path)
    # Print attributes
    out_sound = []
    # out_sound.append(f"Channels: {audio_segment.channels}")
    # out_sound.append(f"Sample width: {audio_segment.sample_width}")
    # out_sound.append(f"Frame rate (sample rate): {audio_segment.frame_rate}")
    # out_sound.append(f"Frame width: {audio_segment.frame_width}")
    # out_sound.append(f"Length (ms): {len(audio_segment)}")
    # out_sound.append(f"Frame count: {audio_segment.frame_count()}")
    # out_sound.append(f"Intensity: {audio_segment.dBFS}")
    S, phase = librosa.magphase(librosa.stft(data))
    rms = librosa.feature.rms(S=S)
    print("root-mean-square (RMS)")
    sum_2 = 0
    for r in rms[0]:
        sum_2 = sum_2 + r
    print(sum_2)
    rms_local = sum_2
    out_sound.append(f"root-mean-square (RMS): {sum_2}")
    zc_local = sum(librosa.zero_crossings(data))
    print(f"Zero crossing rate: {rms_local}")
    out_sound.append(f"Zero crossing rate: {sum(librosa.zero_crossings(data))}")
    path_1 = getcwd()
    chdir("saved_sounds")
    g_rms = []
    g_zc = []
    sh_rms = []
    sh_zc = []
    q_rms = []
    q_zc = []
    for i in range(1,4):
        # for letter ج
        file_name = "ج" + str(i) + ".wav"
        data, sample_rate1 = librosa.load(file_name)
        S, phase = librosa.magphase(librosa.stft(data))
        rms = librosa.feature.rms(S=S)
        sum_2 = 0
        for r in rms[0]:
            sum_2 = sum_2 + r
        g_rms.append(sum_2)
        g_zc.append(sum(librosa.zero_crossings(data)))
        # for letter ش
        file_name = "ش" + str(i) + ".wav"
        data, sample_rate1 = librosa.load(file_name)
        S, phase = librosa.magphase(librosa.stft(data))
        rms = librosa.feature.rms(S=S)
        sum_2 = 0
        for r in rms[0]:
            sum_2 = sum_2 + r
        sh_rms.append(sum_2)
        sh_zc.append(sum(librosa.zero_crossings(data)))
        # for letter ق
        file_name = "ش" + str(i) + ".wav"
        data, sample_rate1 = librosa.load(file_name)
        S, phase = librosa.magphase(librosa.stft(data))
        rms = librosa.feature.rms(S=S)
        sum_2 = 0
        for r in rms[0]:
            sum_2 = sum_2 + r
        q_rms.append(sum_2)
        q_zc.append(sum(librosa.zero_crossings(data)))
    G_rms = sum(g_rms)/3
    G_zc = sum(g_zc)/3/100
    SH_rms = sum(sh_rms)/3
    SH_zc = sum(sh_zc)/3/100
    Q_rms = sum(q_rms)/3
    Q_zc = sum(q_zc)/3/100
    zc_local = zc_local / 100
    # print("sasasasasasasasasasssssssssssssssssssssssssssssssssssssssssss")
    # print(f"local {rms_local}")
    # # print(zc_local)
    # print(f"global {G_rms}")
    # # print(G_rms)
    # print(g_rms)
    # print(G_zc)
    # print(SH_rms)
    # print(SH_zc)
    # for i in range(3):
    #     letter=''
    #     g_temp = G_zc - zc_local
    #     sh_temp = SH_zc - zc_local
    #     q_temp = Q_zc - zc_local
    #     g_temp = G_zc - zc_local
    #     sh_temp = SH_zc - zc_local
    #     q_temp = Q_zc - zc_local
        # if g_temp < sh_temp and g_temp < q_temp :
        #     letter = 'جيم'
        #     out_sound.append("match result : " + )
        # elif sh_temp < g_temp and sh_temp < q_temp :
        #     letter = 'شين'
        # elif q_temp < g_temp and q_temp < sh_temp :
        #     letter = 'قاف'

    if (rms_local < G_rms + 0.2 and rms_local > G_rms +  0.2) and (zc_local < G_zc + 50 and zc_local > G_zc + 50) :
        print("جيم")
        out_sound.append("match result : " + "جيم")
    elif (rms_local < SH_rms + 0.2 and rms_local > SH_rms +  0.2) and (zc_local < SH_zc + 50 and zc_local > SH_zc + 50):
        print("شين")
        out_sound.append("match result : " + "شين")
    elif (rms_local < Q_rms + 0.2 and rms_local > Q_rms +  0.2) and (zc_local < Q_zc + 50 and zc_local > Q_zc + 50):
        print("قاف")
        out_sound.append("match result : " + "قاف")
    else:
        print("لا يوجد")
        out_sound.append("match result : " + "لا يوجد")
    chdir(path_1)
    return out_sound
