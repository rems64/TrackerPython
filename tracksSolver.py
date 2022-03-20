import pickle
import argparse
import matplotlib.pyplot as plt
import numpy as np

msg = "Tracking line solving"

parser = argparse.ArgumentParser(description = msg)
parser.add_argument("-i", "--input", help = "Input file", default="data.data")
parser.add_argument("-o", "--output", help = "Output file", default="solved.data")
parser.add_argument("-t", "--type", help = "speed/raw/naive", default="speed")
parser.add_argument("-s", "--show", help = "Show plot results", default=False)
parser.add_argument("-r", "--restrict", help = "Restrict number of tracks", default=0)
parser.add_argument("-cp", "--compare", help = "Comapre the raw results with the solved ones", default=False)
args = parser.parse_args()

tracks = []
# Open the input list
with open(args.input, 'rb') as filehandle:
    tracks = pickle.load(filehandle)

alreadyDisplayedFrameDrops = False

def getNumberTracks(frames):
    global alreadyDisplayedFrameDrops
    numberTracks = []
    for frame in frames:
        numberTracks.append(len(frame[1]))
    if args.show and not alreadyDisplayedFrameDrops:
        alreadyDisplayedFrameDrops = True
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
            if len(potentials)<=0:
                track.append((0, 0))
                continue
            distances = []
            for potential in potentials:
                distances.append(np.linalg.norm((np.array(potential) - np.array(track[-1]))))
            indexOfMin = np.argmin(distances)
            track.append(potentials[indexOfMin])
            potentials.remove(potentials[indexOfMin])
    return associated


def associate_tracks_withSpeed(frames):
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
            if len(track)>=2:
                if len(potentials)<=0:
                    track.append((0, 0))
                    continue
                # Use speed to determine best match
                speed = np.linalg.norm(np.array(track[-1]) - np.array(track[-2]))
                # Compute the potential speeds
                potentials_speed = []
                for i in potentials:
                    potentials_speed.append(np.abs(np.linalg.norm(np.array(i) - np.array(track[-1]))-speed))
                # Find the best match
                best_match = potentials[np.argmin(potentials_speed)]
                track.append(best_match)
                potentials.remove(best_match)
            else:
                # Fallback to closest
                distances = []
                for potential in potentials:
                    distances.append(np.linalg.norm((np.array(potential) - np.array(track[-1]))))
                indexOfMin = np.argmin(distances)
                track.append(potentials[indexOfMin])
    return associated


def raw_associate(frames):
    associated = [[] for _ in range(getNumberTracks(frames))]
    for frame in frames:
        for i in range(len(associated)):
            if i>=len(frame[1]):
                associated[i].append((0, 0))
                continue
            associated[i].append(frame[1][i])
    return associated


solvedTracksSpeed = associate_tracks_withSpeed(tracks)
if args.restrict:
    solvedTracksSpeed = solvedTracksSpeed[:int(args.restrict)]

solvedTracks = associate_tracks(tracks)
rawTracks = raw_associate(tracks)
if args.restrict:
    solvedTracks = solvedTracks[:int(args.restrict)]
    rawTracks = rawTracks[:int(args.restrict)]

if args.compare:
    i=0
    for i in range(len(rawTracks)):
        nT = rawTracks[i]
        T = solvedTracks[i]
        Ts = solvedTracksSpeed[i]
        plt.figure()
        plt.subplot(3, 1, 1)
        plt.plot([k for k in range(len(nT))], [i[0] for i in nT], 'r-')
        plt.plot([k for k in range(len(nT))], [i[1] for i in nT], 'g-')
        plt.title("Raw track " + str(i))
        plt.subplot(3, 1, 2)
        plt.plot([k for k in range(len(T))], [i[0] for i in T], 'r-')
        plt.plot([k for k in range(len(T))], [i[1] for i in T], 'g-')
        plt.title("Track " + str(i))
        plt.subplot(3, 1, 3)
        plt.plot([k for k in range(len(Ts))], [i[0] for i in Ts], 'r-')
        plt.plot([k for k in range(len(Ts))], [i[1] for i in Ts], 'g-')
        plt.title("Track speed " + str(i))
        i+=1
    plt.show()
elif int(args.show)>=2:
    i=0
    for track in solvedTracksSpeed:
        plt.figure()
        plt.plot([k for k in range(len(track))], [i[0] for i in track], 'r-')
        plt.plot([k for k in range(len(track))], [i[1] for i in track], 'g-')
        plt.title("Track " + str(i))
        i+=1
    plt.show()

if args.output:
    with open(args.output, 'wb') as filehandle:
        if args.type == "speed":
            pickle.dump(solvedTracksSpeed, filehandle)
        elif args.type == "raw":
            pickle.dump(rawTracks, filehandle)
        elif args.type == "naive":
            pickle.dump(solvedTracks, filehandle)
        else:
            print("Unknown type")