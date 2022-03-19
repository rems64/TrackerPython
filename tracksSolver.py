import pickle
import argparse
import matplotlib.pyplot as plt

msg = "Tracking line solving"

parser = argparse.ArgumentParser(description = msg)
parser.add_argument("-i", "--input", help = "Input file", default="data.data")
args = parser.parse_args()

tracks = []
# Open the input list
with open(args.input, 'rb') as filehandle:
    tracks = pickle.load(filehandle)

for track in tracks:
    plt.figure()
    plt.plot([k for k in range(len(track))], [i[0] for i in track], 'r-')
    plt.plot([k for k in range(len(track))], [i[1] for i in track], 'g-')
plt.show()