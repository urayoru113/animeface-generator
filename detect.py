import cv2
import sys
import os.path

def detect(filepath, cascade_file = "./lbpcascade_animeface.xml"):
    if not os.path.isfile(cascade_file):
        raise RuntimeError("%s: not found" % cascade_file)

    cascade = cv2.CascadeClassifier(cascade_file)
    i = 0
    for f in os.listdir(filepath):
        image = cv2.imread(filepath + '/' + f, cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        faces = cascade.detectMultiScale(gray,
                                     # detector options
                                     scaleFactor = 1.1,
                                     minNeighbors = 5,
                                     minSize = (24, 24))
        
        for x, y, w, h in faces:
            if w >= 64 and h >= 64:
                i += 1
                cv2.imwrite("data/face%06d.jpg" %i, image[y:y+h, x:x+w])
                print("Cut success. Total sample %d data" %i)
                
                
    print("Total sample %d data" %i)

if len(sys.argv) != 2:
    sys.stderr.write("usage: detect.py <filename>\n")
    sys.exit(-1)
    
if not os.path.isdir('data'):
    os.makedirs('data')
detect(sys.argv[1])
