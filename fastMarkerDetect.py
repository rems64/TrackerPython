import cv2
import numpy as np
import matplotlib.pyplot as plt
import sys
import argparse
import utils



msg = "Fast marker detection"

parser = argparse.ArgumentParser(description = msg)
parser.add_argument("-i", "--input", help = "Input file", default="../../Footages/Clean2/Cam1/0001-0300.mp4")
parser.add_argument("-o", "--output", help = "Output file", default="tracked.data", required=True)
parser.add_argument("-r", "--restrict", help = "Restrict frame count", default=100000)
args = parser.parse_args()


cap = cv2.VideoCapture(args.input)

tracks = []

counter = 0
limit = int(args.restrict)

while True:
    if counter>limit:
        break
    counter+=1
    ret, frame = cap.read()
    if ret:
        sized = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        noise = np.random.randint(0, 100, (sized.shape[0], sized.shape[1], 3))

        sized = np.uint8(np.clip(sized + noise, 0, 255))
        ret, thresh = cv2.threshold(cv2.cvtColor(sized, cv2.COLOR_BGR2GRAY), 127, 255, 0)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        i=0
        for cnt in contours:
            if len(tracks) <= i:
                tracks.append([])
            M = cv2.moments(cnt)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                tracks[i].append((cX, cY))
            i+=1
    else:
        break


"""
for track in tracks:
    plt.plot([k for k in range(len(track))], [i[0] for i in track], 'r-')
    plt.plot([k for k in range(len(track))], [i[1] for i in track], 'g-')
plt.show()
"""

import pickle


with open(utils.check_extension(args.output, "data"), 'wb') as filehandle:
    # store the data as binary data stream
    pickle.dump(tracks, filehandle)