import pickle
import argparse
import matplotlib.pyplot as plt
import numpy as np

msg = "Tracking line solving"

parser = argparse.ArgumentParser(description = msg)
parser.add_argument("-i", "--input", help = "Input file", default="data.data")
parser.add_argument("-s", "--show", help = "Show plot results", default=False)
parser.add_argument("-r", "--restrict", help = "Restrict number of tracks", default=0)
parser.add_argument("-cp", "--compare", help = "Comapre the raw results with the solved ones", default=False)
args = parser.parse_args()

tracks = []
# Open the input list
with open(args.input, 'rb') as filehandle:
    tracks = pickle.load(filehandle)

def getNumberTracks(frames):
    numberTracks = []
    for frame in frames:
        numberTracks.append(len(frame[1]))
    if args.show:
        plt.plot(numberTracks)
        plt.show()
    return int(np.median(numberTracks))

def associate_tracks(frames):
    associated = [[] for _ in range(getNumberTracks(frames))]
    for frame in frames:
        potentials = []
        for i in frame[1]:
            # print(i)
            potentials.append(i)
        for track in associated:
            if len(track)<=0:
                track.append(potentials.pop(0))
                continue
            distances = []
            for potential in potentials:
                distances.append(np.linalg.norm((potential[0] - track[-1][0], potential[1] - track[-1][1])))
            indexOfMin = np.argmin(distances)
            track.append(potentials[indexOfMin])
    return associated


def naive_associate(frames):
    associated = [[] for _ in range(getNumberTracks(frames))]
    for frame in frames:
        for i in range(len(frame[1])):
            associated[i].append(frame[1][i])
    return associated


solvedTracks = associate_tracks(tracks)
if args.restrict:
    solvedTracks = solvedTracks[:int(args.restrict)]

if args.compare:
    naiveTracks = naive_associate(tracks)
    if args.restrict:
        naiveTracks = naiveTracks[:int(args.restrict)]
    i=0
    for i in range(len(naiveTracks)):
        nT = naiveTracks[i]
        T = solvedTracks[i]
        plt.figure()
        plt.subplot(2, 1, 1)
        plt.plot([k for k in range(len(nT))], [i[0] for i in nT], 'r-')
        plt.plot([k for k in range(len(nT))], [i[1] for i in nT], 'g-')
        plt.title("Raw track " + str(i))
        plt.subplot(2, 1, 2)
        plt.plot([k for k in range(len(T))], [i[0] for i in T], 'r-')
        plt.plot([k for k in range(len(T))], [i[1] for i in T], 'g-')
        plt.title("Track " + str(i))
        i+=1
    plt.show()
else:
    i=0
    for track in solvedTracks:
        plt.figure()
        plt.plot([k for k in range(len(track))], [i[0] for i in track], 'r-')
        plt.plot([k for k in range(len(track))], [i[1] for i in track], 'g-')
        plt.title("Track " + str(i))
        plt.show()
        i+=1

