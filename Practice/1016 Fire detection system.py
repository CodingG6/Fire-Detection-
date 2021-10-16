# 튜토리얼: GR Tech School (2020) Fire Detection System in Python using Opencv https://www.youtube.com/watch?v=2uxfqlDbVV4&ab_channel=GRTechSchool

import cv2
import os
import numpy as np


# 사용한 비디오 출처: 터키 산불 관련 뉴스 https://www.youtube.com/watch?v=aL9c-4EerTo&ab_channel=NBCNews
video = cv2.VideoCapture("video/Homes Evacuated As Wildfire Threatens To Engulf Manavgat, Turkey.mp4")

# 비디오를 프레임 단위로(while true) 돌리는 동안 영상 추출
while True:

    ret, frame = video.read() # ret (boolean) - whether the frame data is there
    frame = cv2.resize(frame, dsize=(0,0), fx=0.65, fy=0.65)
    blur = cv2.GaussianBlur(frame, (15, 15), 0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    # 불과 연기의 색상 특성을 범위로 잡음
    lower = [18, 50, 50]
    upper = [35, 255, 255]
    
    lower = np.array(lower, dtype='uint8')  # 어레이 형태로 변환
    upper = np.array(upper, dtype='uint8')

    # 마스크 생성
    # HSV로 변환한 프레임에서 위의 불 특성 범위를 이용해 마스크를 설정
    mask = cv2.inRange(hsv, lower, upper)
    
    # frame과 hsv변환한 frame에서 둘다 마스크 범위에 걸리는 입자만 색상을 살리고 나머지는 검은색으로 죽임
    output = cv2.bitwise_and(frame, hsv, mask=mask)

    # 불 이미지를 불의 크기로 걸러냄(큰 불만 불로 인식하도록 설정)
    fire_size = cv2.countNonZero(mask)

    if int(fire_size) > 50000:
        print("Fire detected")

    if (ret == False):
        break           # if no frame, break out.

    cv2.imshow("Output", output)

    if cv2.waitKey(7) & 0xFF == ord("q"):
        break

cv2.destroyAllWindows()
video.release()
