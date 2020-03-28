import cv2 as cv
import numpy as np
from PIL import Image

cap = cv.VideoCapture(1) #захват видео
color_name = ['orange','red','blue','green']
karlik = [0,0,0,0]
fed_color = False
dolg =50 # сколько нунжно кадров для определения цвета

while not fed_color: #пока не определился цвет
    ret, frame = cap.read()
    frameCopy = frame.copy()
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    hsv = cv.blur(hsv, (3,3))
      
    mask = cv.inRange(hsv, (0 ,122, 37), (187, 249, 255)) #бинаризую картинку 
    mask = cv.erode(mask, None, iterations = 1)
    mask = cv.dilate(mask, None, iterations = 2)
    #cv.imshow('binary_hsv', mask)
    
    contours0, hierarchy = cv.findContours( mask.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    if contours0:
        contours = sorted(contours0, key = cv.contourArea, reverse = True) #если нашлись контуры, то сортирую
                                                                           # контуры по размеру области 
    
        for cnt in contours:
            (x,y,w,h) = cv.boundingRect(cnt)
            rect = cv.minAreaRect(cnt) # пытаемся вписать прямоугольник
            box = cv.boxPoints(rect) # поиск четырех вершин прямоугольника
            box = np.int0(box) # округление координат
            cv.drawContours(frame,[box],0,(255,0,255),2) # рисуем прямоугольник
            
            roImg = frameCopy[y:y+h, x:x+w] # обрезаю контур
            roImg = cv.resize(roImg, (64,64))
            cv.imshow('obrez', roImg)
            
            color_pix = [0,0,0,0]
            
            
            colorset =[
            [15, 160, 215], #orange
            [20,25,160], #red
            [150, 43, 25], #blue
            [30, 125, 15] #green
            ]
            min_razn = 50000
            zzz = 0
            
            #попиксильное сравнивание и выделение цвета
            
            for i in range(0,len(roImg),2):
                for k in range(0,len(roImg[i]),2):
                    for j in range(4):
                        razn = abs(roImg[i][k][0] - colorset[j][0])+abs(roImg[i][k][1] - colorset[j][1])+abs(roImg[i][k][2] - colorset[j][2])
                        if razn< min_razn:
                            min_razn = razn 
                            zzz = j
                    color_pix[zzz] += 1     
                    
            max_color = 0
            mxdex = 0
            for i in range(4):
                if color_pix[i] > max_color:
                    max_color = color_pix[i]
                    mxdex = i
                    
            cv.putText(frame, color_name[mxdex], (20, 20), cv.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2) #вывод надписи цвета
            karlik[mxdex] += 1
            for k in range(len(karlik)):
                if karlik[k] > dolg:
                    print(color_name[k])
                    fed_color = True
                    break

            break

    cv.imshow('contours', frame) # вывод обработанного кадра в окно
        
    if cv.waitKey(1) == 27:
        break

cap.release()
cv.destroyAllWindows()