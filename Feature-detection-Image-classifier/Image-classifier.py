#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# This script demonstrates image classification using feature detection. First the features of the images we wish to classify are extracted
# and then when the user provides a new image, it is classified based on how good the features of the user-defined image match with features
# of the pre-trained image
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
import os
import cv2

path = "images_train"  # Path to the images used for training
imageList = []  # List to store all the images
classList = []  # List to store the names

# Read images and populate the lists
for filename in os.listdir(path):
    img = cv2.imread(path + "\\" + filename)
    className = filename.split('.')[0]
    imageList.append(img)
    classList.append(className)

# Function to create descriptors from the read images and store it in a list
orb = cv2.ORB_create(nfeatures=1000)
print(classList)

# Decription list for every training image
def findDescriptors(images):
    descriptors = []
    keyPoints = []
    for image in images:
        kp, des = orb.detectAndCompute(image, None)
        descriptors.append(des)
        keyPoints.append(kp)
    return keyPoints, descriptors

kpList, descList = findDescriptors(imageList)

# Function to find the descriptors in the webcam feed and match them with the input images and return the id of that class with which the
# webcam image has the most matches with
def findClassID(descList, image, thresh=15):
    kp2, des2 = orb.detectAndCompute(image, mask=None)
    goodMatches = []
    matcher = cv2.BFMatcher()
    classID = -1

    try:
        for desc in descList:
            good = []
            matches = matcher.knnMatch(desc, des2, k=2)
            for m, n in matches:
                if m.distance < 0.75 * n.distance:
                    good.append([m])
            goodMatches.append(len(good))
    except:
        pass

    if (len(goodMatches) != 0) and (max(goodMatches) > thresh):
        classID = goodMatches.index(max(goodMatches))

    return classID

cap = cv2.VideoCapture(0)

# Define a while loop for obtaining the camera feed, convert to grayscale and pass it to the findClassID function.
while True:
    ret, frame = cap.read()
    frameOriginal = frame.copy()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cl_id = findClassID(descList, frame)
    print(cl_id)
    if cl_id != -1:
        cv2.putText(frameOriginal, classList[cl_id], (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
    cv2.imshow("Result", frameOriginal)

    if (cv2.waitKey(1) == 27):
        break