import cv2
import drone

haars = [
        'haarcascade_frontalface_alt'
        ]

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
    for haar in haars:
        rects = get_rects(gray,haar)
        for rect in rects:
            x1,y1,x2,y2 = rect[0],rect[1],rect[0]+rect[2],rect[1]+rect[3]
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
            for pt in pts:
                if pt.pt[0]> x1 and pt.pt[0]<x2 and pt.pt[1]>y1 and pt.pt[1]<y2:
                    cv2.circle(img,(int(pt.pt[0]),int(pt.pt[1])),1,(0,255,0),2)
    return img

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

def main():
    vid_ip = 'video_face2.flv'
    frames = build_frames(vid_ip)
    output = []
    c=1
    for frame in frames:
        if c == 200:
            break
        if c<150:
            c+=1
            continue
        img = detect(frame)
        output.append(img)
        c+=1
    c=1
    for frame in output:
        cv2.imshow("frame",frame)
        if c==1:
            #response = drone.notify("Face Detected")
            print "Face detected"
        cv2.imwrite("output/" + str(c) + ".jpg",frame)
        c += 1
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
    cv2.destroyAllWindows()

def main_test():
    img = cv2.imread("sign.jpg")
    img = detect(img)
    cv2.imshow("frame",img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()