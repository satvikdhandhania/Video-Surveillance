import numpy as np
import cv2

lk_params = dict( winSize  = (15, 15),
                  maxLevel = 2,
                  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

class OpticalFlowTracker():
    def track(self,img0,img1,pts):
#         img0, img1 = prev_gray, gray
        p0 = np.float32([tr[-1] for tr in pts]).reshape(-1, 1, 2)
        if len(p0) < 5:
            return []
#                 print "p0",p0
        p1, st, err = cv2.calcOpticalFlowPyrLK(img0, img1, p0, None, **lk_params)

        p0r, st, err = cv2.calcOpticalFlowPyrLK(img1, img0, p1, None, **lk_params)

        d = abs(p0-p0r).reshape(-1, 2).max(-1)
        good = d < 1
        new_tracks = []
        trackedPoints = []
        for tr, (x, y), good_flag in zip(pts, p1.reshape(-1, 2), good):
            if not good_flag:
                continue
            tr.append((x, y))
            trackedPoints.append([(x,y)])
#                     if len(tr) > self.track_len:
#                         del tr[0]
            new_tracks.append(tr)
        return trackedPoints