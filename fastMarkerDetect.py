import argparse

msg = "Fast marker detection"

parser = argparse.ArgumentParser(description = msg)
parser.add_argument("-i", "--input", help = "Input file", default="../../Footages/Clean2/Cam1/0001-0300.mp4")
parser.add_argument("-o", "--output", help = "Output file", default="tracked.data", required=True)
parser.add_argument("-r", "--restrict", help = "Restrict frame count", default=100000)
parser.add_argument("-n", "--noise", help = "Layer noise on top of the image", default=0)
parser.add_argument("-s", "--show", help = "Show raw result", default=False)
args = parser.parse_args()


import cv2
import numpy as np
import matplotlib.pyplot as plt
import utils
import pickle



cap = cv2.VideoCapture(args.input)

tracks = []

frame = 0

noiseLvl = int(255*float(args.noise))

limit = int(args.restrict)

while True:
    if frame>=limit:
        break
    frame+=1
    ret, pic = cap.read()
    if ret:
        sized = cv2.resize(pic, (0, 0), fx=0.5, fy=0.5)
        if noiseLvl>0:
            noise = np.random.randint(0, noiseLvl, (sized.shape[0], sized.shape[1], 3))

            sized = np.uint8(np.clip(sized + noise, 0, 255))
        # To replace with a more elaborate processing
        ret, thresh = cv2.threshold(cv2.cvtColor(sized, cv2.COLOR_BGR2GRAY), 127, 255, 0)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        detected = []
        for cnt in contours:
            if args.show:
                cv2.polylines(sized, cnt, True, (0, 255, 0), 2)
            M = cv2.moments(cnt)
            # print(M)
            # exit()
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                detected.append((cX, cY))
        tracks.append((frame, detected))
        if args.show:
            for c in detected:
                cv2.circle(sized, c, 10, (0, 0, 255), 2)
            cv2.imshow("Tracking...", sized)
            key = cv2.waitKey(1)
            if key==ord('q'):
                args.show = False
    else:
        break


# if args.show:
#     for track in range(len(tracks)):
#         plt.plot([k[0] for k in tracks], [k[1][track][0] for k in tracks], 'r-')
#         plt.plot([k[0] for k in tracks], [k[1][track][1] for k in tracks], 'g-')
#     plt.show()

print("Detected {} tracks".format(len(tracks)))

with open(utils.check_extension(args.output, "data"), 'wb') as filehandle:
    # store the data as binary data stream
    pickle.dump(tracks, filehandle)