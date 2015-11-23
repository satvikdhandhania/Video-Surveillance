import cv2
import numpy as np

haars = [
        'haarcascade_frontalface_alt'
        ]

feature_params = dict( maxCorners = 100,
                       qualityLevel = 0.3,
                       minDistance = 7,
                       blockSize = 7 )

lk_params = dict( winSize  = (15,15),
                  maxLevel = 2,
                  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

def get_rects(gray,classifier):
    cascade = cv2.CascadeClassifier('haar_classifiers/' + classifier + '.xml')
    objs = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=2,flags = cv2.cv.CV_HAAR_SCALE_IMAGE)
    return objs
    for obj in objs:
        cv2.rectangle(img,(obj[0],obj[1]),(obj[0]+obj[2],obj[1]+obj[3]),(0,255,0),2)
    return objs

def detect(img):
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    sift = cv2.SIFT()
    pts = sift.detect(gray,None)
    points = []
    for haar in haars:
        rects = get_rects(gray,haar)
        for rect in rects:
            x1,y1,x2,y2 = rect[0],rect[1],rect[0]+rect[2],rect[1]+rect[3]
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
            for pt in pts:
                if pt.pt[0]> x1 and pt.pt[0]<x2 and pt.pt[1]>y1 and pt.pt[1]<y2:
                    l = [np.float32(pt.pt[0]),np.float32(pt.pt[1])]
                    points.append(np.array(l))
                    cv2.circle(img,(int(pt.pt[0]),int(pt.pt[1])),1,(0,255,0),2)
    points = np.array(points)
    return img,points

def build_frames(vid):
    cap = cv2.VideoCapture(vid)
    frames = []
    while True:
        ret, frame = cap.read()
        if ret == False:
            break
        else:
            frames.append(frame)
    cap.release()
    return frames

def track(old,new,pts):
    old_gray = cv2.cvtColor(old, cv2.COLOR_RGB2GRAY)
    new_gray = cv2.cvtColor(new, cv2.COLOR_RGB2GRAY)
    p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, new_gray, pts, None, **lk_params)
    return p1

def main():
    frames = build_frames('video_face.flv')
    output = []
    old = frames[100]
    img, p0 = detect(old)
    print len(p0)
    input()
    output.append(img)
    c=1
    for frame in frames:
        if c == 150:
            break
        if c<100:
            c+=1
            continue
        tracked_pts = track(old,frame,p0)
        l = []
        for p in tracked_pts:
            cv2.circle(frame,(int(p[0]),int(p[1])),1,(0,255,0),2)
            l.append([np.float32(p[0]),np.float32(p[1])])
        l = np.array(l)
        p2 = np.float32([tr[-1] for tr in tracked_pts]).reshape(-1, 1, 2)
        x,y,w,h = cv2.boundingRect(np.array([l]))
        x1,y1,x2,y2 = x,y,x+h,y+w
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
        #img, p0 = detect(frame)
        output.append(frame)
        old = frame
        c+=1
    c=1
    for frame in output:
        cv2.imshow("frame",frame)
        print "Face Detected."
        cv2.imwrite("output/" + str(c) + ".jpg",frame)
        c += 1
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
    cv2.destroyAllWindows()

def main_live():
    counter = 0
    cam = cv2.VideoCapture(0)
    while True:
        ret_val, img = cam.read()
        img, pts = detect(img)
        cv2.imshow('my webcam', img)
        if cv2.waitKey(1) == 27:
            break  # esc to quit
    cv2.destroyAllWindows()
    cam.release

if __name__ == '__main__':
    main()
    #main_live()