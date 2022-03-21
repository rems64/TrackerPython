import argparse

msg = "Reinsert tracked points"

parser = argparse.ArgumentParser(description = msg)
parser.add_argument("-i", "--input", help = "Input file", default="../../Footages/Clean2/Cam1/0001-0300.mp4")
parser.add_argument("-d", "--data", help = "Input data file", default="tracked.data")
parser.add_argument("-o", "--output", help = "Output file", default="reassociated.mp4")
parser.add_argument("-r", "--restrict", help = "Restrict frame count", default=100000)
parser.add_argument("-s", "--show", help = "Show raw result", default=False)
parser.add_argument("-f", "--fps", help = "Preview target FPS", default=30)
# parser.add_argument("-i", "--iterate", help = "Iterate frame by frame over the result", default=False)
args = parser.parse_args()

import cv2
import pickle

cap = cv2.VideoCapture(args.input)

tracks = []
with open(args.data, 'rb') as filehandle:
    tracks = pickle.load(filehandle)

frame = 0
limit = int(args.restrict)

deltaDelayMs = int(1000/float(args.fps))

colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255), (255, 0, 255)]

print("##### ABOUT VIDEO ######")
print("Video length : " + str(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))))
print("")
print("##### ABOUT TRACKS #####")
print("Number of tracks : " + str(len(tracks)))
print("Number of frames : " + str(len(tracks[0])))

print("")
print("###### PER TRACK #######")
i=0
for track in tracks:
    print("Track " + str(i) + " : " + str(len(track)))
    i+=1

paused = False

while cap.isOpened():
    ret, pic = cap.read()
    if ret:
        sized = cv2.resize(pic, (0, 0), fx=0.5, fy=0.5)
        withTrack = sized.copy()
        j=0
        for track in tracks:
            if track[frame] and track[frame]!=(0,0):
                cv2.circle(withTrack, track[frame], 5, colors[j], -1)
                cv2.putText(withTrack, str(j), (track[frame][0]+5, track[frame][1]+5), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 1)
                j+=1
        
        cv2.putText(withTrack, "Frame " + str(frame), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 1)
        cv2.putText(withTrack, "Tracks : " + str(j), (sized.shape[1]-200, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 1)
        cv2.putText(sized, "Frame " + str(frame), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 1)
        cv2.imshow("Original", sized)
        cv2.imshow("Tracked", withTrack)
        key = cv2.waitKey(deltaDelayMs)
        if key == ord('q'):
            break
        elif key == ord('p'):
            paused = True
        if paused:
            key = cv2.waitKey()
            if key == ord('p'):
                paused = False
            elif key == ord('l'):
                frame += 1
                cap.set(1, frame)
                continue
            elif key == ord('j'):
                frame -= 1
                cap.set(1, frame)
                continue
            elif key == ord('q'):
                break
        frame += 1
    else:
        break