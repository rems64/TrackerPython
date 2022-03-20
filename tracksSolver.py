import pickle
import argparse
import matplotlib.pyplot as plt
import numpy as np

msg = "Tracking line solving"

parser = argparse.ArgumentParser(description = msg)
parser.add_argument("-i", "--input", help = "Input file", default="data.data")
args = parser.parse_args()

tracks = []
# Open the input list
with open(args.input, 'rb') as filehandle:
    tracks = pickle.load(filehandle)

def associate_tracks(tracks):
    associated = [[] for _ in range(len(tracks))]
    for frame in range(len(tracks[0])):
        potentials = []
        for i in range(len(tracks)):
            print(tracks[i])
            print(len(tracks[i]))
            print(len(tracks[0]))
            potentials.append((tracks[i][frame]))
        for track in associated:
            track.append(potentials.pop(np.argmin([np.linalg.norm(i-j) for j in range(len(potentials))])))
    return associated


aTracks = associate_tracks(tracks)

for track in aTracks:
    plt.figure()
    plt.plot([k for k in range(len(track))], [i[0] for i in track], 'r-')
    plt.plot([k for k in range(len(track))], [i[1] for i in track], 'g-')
plt.show()

