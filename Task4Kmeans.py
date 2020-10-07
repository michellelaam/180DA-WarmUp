# Reference code:
# Finding Dominant Colour on an Image —
# https://code.likeagirl.io/finding-dominant-colour-on-an-image-b4e075f98097
# ——— Combined code snippet above with previous code to enable choosing dominant color from
# ——— a live video feed rather than a static image
# ——— Adjusted the code snippet to determine the dominant color within a designated rectangle
# ————— rather than the whole frame

import numpy as np
import cv2
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans


def find_histogram(clt):
    """
    create a histogram with k clusters
    :param: clt
    :return:hist
    """
    numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
    (hist, _) = np.histogram(clt.labels_, bins=numLabels)

    hist = hist.astype("float")
    hist /= hist.sum()

    return hist

def plot_colors2(hist, centroids):
    bar = np.zeros((50, 300, 3), dtype="uint8")
    startX = 0

    for (percent, color) in zip(hist, centroids):
        # plot the relative percentage of each cluster
        endX = startX + (percent * 300)
        cv2.rectangle(bar, (int(startX), 0), (int(endX), 50),
                      color.astype("uint8").tolist(), -1)
        startX = endX

    # return the bar chart
    return bar


cap = cv2.VideoCapture(0)


while(cap.isOpened()):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Select ROI
    section = frame[500:700, 350:550] # height x width

    # For debugging that I selected the correct ROI
    # frame[350:550, 500:700] = section

    # Draw designated rectangle around ROI
    cv2.rectangle(frame,(350,500),(550,700),(0,255,0),1) # img, x-coord, y-coord, color, thickness

    ### RGB ###
	# Convert BGR to RGB
    img = cv2.cvtColor(section, cv2.COLOR_BGR2RGB)
    img = img.reshape((img.shape[0] * img.shape[1],3)) #represent as row*column,channel number
    clt = KMeans(n_clusters=3) #cluster number
    clt.fit(img)

    hist = find_histogram(clt)
    bar = plot_colors2(hist, clt.cluster_centers_)

    cv2.imshow('frame',frame)

    plt.axis("off")
    plt.imshow(bar)
    plt.show()

    k = cv2.waitKey(60) & 0xff
    # Press Escape to exit
    if k == 27:
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
