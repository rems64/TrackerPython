import argparse

msg = "Tracking line solving"

parser = argparse.ArgumentParser(description = msg)
parser.add_argument("-i", "--input", help = "Input file", default="data.data")
parser.add_argument("-o", "--output", help = "Output file", default="solved.data")
parser.add_argument("-t", "--type", help = "speed/raw/naive", default="speed")
parser.add_argument("-s", "--show", help = "Show plot results", default=False)
parser.add_argument("-r", "--restrict", help = "Restrict number of tracks", default=0)
parser.add_argument("-cp", "--compare", help = "Compare the raw results with the solved ones", default=False)
parser.add_argument("-d", "--derivatives", help = "Compute discrete derivatives", default=False)
args = parser.parse_args()

import pickle
import matplotlib.pyplot as plt
import numpy as np
import utils

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
    return int(max(numberTracks))
    return int(np.median(numberTracks))


def associate_tracks(frames):
    associated = [[] for _ in range(getNumberTracks(frames))]
    for frame in frames:
        potentials = []
        for i in frame[1]:
            # print(i)
            potentials.append(i)
        for track in associated:
            if len(potentials)<=0:
                # if len(track)>0:
                #     track.append(track[-1])
                # else:
                track.append((0, 0))
                continue
            if len(track)<=0:
                track.append(potentials.pop(0))
                continue
            distances = []
            for potential in potentials:
                distances.append(np.linalg.norm((np.array(potential) - np.array(track[-1]))))
            indexOfMin = np.argmin(distances)
            track.append(potentials[indexOfMin])
            potentials.remove(potentials[indexOfMin])
    return associated


def associate_tracks_withSpeed(frames):
    associatedCount = getNumberTracks(frames)
    associated = [[] for _ in range(associatedCount)]
    cFrame = 0
    for frame in frames:
        cFrame+=1
        potentials = []
        for i in frame[1]:
            # print(i)
            potentials.append(i)
        
        # Perform matching
        selected = []
        associatedTmp = associated.copy()
        # if len(potentials)<associatedCount:
        #     for potential in potentials:
        #         distances = [np.linalg.norm((np.array(potential) - np.array(track[-1]))) if len(track)>0 else 0 for track in associatedTmp]
        #         selected.append(associatedTmp[np.argmin(distances)])
        #         associatedTmp.remove(associatedTmp[np.argmin(distances)])
        # else:
        selected = associated
        for track in selected:
            if len(potentials)<=0:
                if len(track)>0:
                    track.append(track[-1])
                else:
                    track.append((0, 0))
                continue
            if len(track)<=0:
                track.append(potentials.pop(0))
                continue
            # if len(track)>=4000:
            #     acceleration = np.array(track[-1]) - np.array(track[-2]) - np.array(track[-3]) + np.array(track[-4])
            #     potential_accelerations = []
            #     for potential in potentials:
            #         potential_accelerations.append(np.linalg.norm(np.array(potential) - np.array(track[-1]) - np.array(track[-2]) + np.array(track[-3] - acceleration)))
            #     best_match = potentials[np.argmin(potential_accelerations)]
            #     track.append(best_match)
            #     potentials.remove(best_match)
            elif len(track)>=2:
                # Fallback to speed
                speed = np.array(track[-1]) - np.array(track[-2])
                # Compute the potential speeds
                deltas = []
                for i in potentials:
                    deltas.append(np.linalg.norm(np.array(i) - np.array(track[-1]) - speed))
                # Find the best match
                best_match = potentials[np.argmin(deltas)]
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
    if args.derivatives:
        i=0
        for i in range(len(rawTracks)):
            nT = rawTracks[i]
            T = solvedTracks[i]
            Ts = solvedTracksSpeed[i]
            plt.figure()
            plt.subplot(3, 2, 1)
            plt.plot([i[0] for i in nT], 'r-')
            plt.plot([i[1] for i in nT], 'g-')
            plt.title("Raw " + str(i))
            plt.subplot(3, 2, 2)
            plt.plot(utils.deriveeUniformeDiscrete([i[0] for i in nT]), 'r-')
            plt.plot(utils.deriveeUniformeDiscrete([i[1] for i in nT]), 'g-')
            plt.title("Raw derivitive" + str(i))

            plt.subplot(3, 2, 3)
            plt.plot([i[0] for i in T], 'r-')
            plt.plot([i[1] for i in T], 'g-')
            plt.title("Naive " + str(i))
            plt.subplot(3, 2, 4)
            plt.plot(utils.deriveeUniformeDiscrete([i[0] for i in T]), 'r-')
            plt.plot(utils.deriveeUniformeDiscrete([i[1] for i in T]), 'g-')
            plt.title("Naive derivitive" + str(i))

            plt.subplot(3, 2, 5)
            plt.plot([i[0] for i in Ts], 'r-')
            plt.plot([i[1] for i in Ts], 'g-')
            plt.title("Smooth " + str(i))
            plt.subplot(3, 2, 6)
            plt.plot(utils.deriveeUniformeDiscrete([i[0] for i in Ts]), 'r-')
            plt.plot(utils.deriveeUniformeDiscrete([i[1] for i in Ts]), 'g-')
            plt.title("Smooth derivitive" + str(i))

            i+=1
    else:
        i=0
        for i in range(len(rawTracks)):
            nT = rawTracks[i]
            T = solvedTracks[i]
            Ts = solvedTracksSpeed[i]
            plt.figure()
            plt.subplot(3, 1, 1)
            plt.plot([i[0] for i in nT], 'r-')
            plt.plot([i[1] for i in nT], 'g-')
            plt.title("Raw " + str(i))
            plt.subplot(3, 1, 2)
            plt.plot([i[0] for i in T], 'r-')
            plt.plot([i[1] for i in T], 'g-')
            plt.title("Naive " + str(i))
            plt.subplot(3, 1, 3)
            plt.plot([i[0] for i in Ts], 'r-')
            plt.plot([i[1] for i in Ts], 'g-')
            plt.title("Smooth " + str(i))
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