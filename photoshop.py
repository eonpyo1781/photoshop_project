import numpy as np
import copy
import cv2

def update_toolbar():
    if(mode[0]==True): img[:40,:40,:] = rect_able
    else: img[:40,:40,:] = rect_dis
    if(mode[1]==True): img[40:80,:40,:] = line_able
    else: img[40:80,:40,:] = line_dis
    if(mode[2]==True): img[80:120,:40,:] = circle_able
    else: img[80:120,:40,:] = circle_dis
    if(mode[3]==True): img[120:160,:40,:] = right_triangle_able
    else: img[120:160,:40,:] = right_triangle_dis
    if(mode[4]==True): img[160:200,:40,:] = triangle_able
    else: img[160:200,:40,:] = triangle_dis    
    cv2.imshow(title, img)

def onMouse(evt, x, y, flag, arg):
    global drawing
    if(evt == cv2.EVENT_LBUTTONDOWN):
        drawing = True
        mouse_stats[0] = x
        mouse_stats[1] = y
        print("start = x = " + str(x) + ", y = " + str(y))
    if(evt == cv2.EVENT_MOUSEMOVE):
        if(drawing):
            mouse_stats[2] = x
            mouse_stats[3] = y
            cmdqueue.append([current_mode, copy.deepcopy(mouse_stats[:4])])
            draw()
            cmdqueue.pop()
    if(evt == cv2.EVENT_LBUTTONUP):
        drawing = False
        mouse_stats[2] = x
        mouse_stats[3] = y
        print("end = x = " + str(x) + ", y = " + str(y))
        processing_by_position()
    
        
def processing_by_position():
    if(mouse_stats[0]<40 and mouse_stats[1]<200): #Toolbar position
        global current_mode
        for i in range(5): mode[i] = False
        current_mode = mouse_stats[1]//40
        print(current_mode)
        mode[current_mode]=True
        update_toolbar()
    else:
        cmdqueue.append([current_mode, copy.deepcopy(mouse_stats[:4])])
        draw()
        
def draw():
    img[103:597, 153:1197, :] = 255
    for mode, stat in cmdqueue:
        if(mode == 0):
            cv2.rectangle(img, stat[:2], stat[2:4], 3)
        elif(mode == 1):
            draw_line(img, stat[0], stat[2], stat[1], stat[3], (0,0,0))
        elif(mode == 2):
            cv2.circle(img, (stat[0], stat[1]),
                    int(distance(stat[0], stat[1], stat[2], stat[3])), (0,0,0))
        elif(mode == 3):
            draw_right_triangle(img, stat[0], stat[2], stat[1], stat[3], 0)
        elif(mode == 4):
            draw_triangle(img, stat[0], stat[2], stat[1], stat[3], (0,0,0))
    img[:100, 40:, :] = 255
    img[40:, 40:80, :] = 255
    cv2.imshow(title, img)

def distance(x1, y1, x2, y2):
    return np.sqrt(abs(x2-x1)**2 + abs(y2-y1)**2)

def square_area(img, x1, x2, y1, y2, width, color):
    img[x1:x1+width, y1:y2+1] = color
    img[x2-width+1:x2+1, y1:y2+1] = color
    img[x1+width:x2-width+1, y1:y1+width] = color
    img[x1+width:x2-width+1, y2-width+1:y2+1] = color

def draw_right_triangle(img, x1, x2, y1, y2, color):
    if(x1 > x2):
        x1, x2 = swap(x1, x2)
    if(y1 > y2):
        y1, y2 = swap(y1, y2)
        
    img[y1:y2+1, x1, :] = 0
    img[y2, x1:x2+1, :] = 0
    
    if(x1 != x2):
        coef = abs(y1 - y2) / abs(x1 - x2)
        intercept = y1 - x1 * coef
    if(x1 != x2):
        for i in range(x1, x2, 1): 
            img[int(coef*i + intercept), i, :] = 0

def draw_triangle(img, x1, x2, y1, y2, color):
    if(x1 < x2):
        img[y2, x1:x2+1, :] = 0
    else:
        img[y2, x2:x1+1, :] = 0
    draw_line(img, x1, int((x1+x2)/2), y2, y1, (0, 0, 0))
    draw_line(img, int((x1+x2)/2), x2, y1, y2, (0, 0, 0))
  
def draw_line(img, x1, x2, y1, y2, color):
    if(x1 == x2):
        if(y1 < y2):
            for i in range(y1, y2, 1):
                img[i, x1] = color
        else:
            for i in range(y2, y1, 1):
                img[i, x1] = color
    elif(y1 == y2):
        if(x1 < x2):
            for i in range(x1, x2, 1):
                img[y1, i] = color
        else:
            for i in range(x2, x1, 1):
                img[y1, i] = color
    else:
        coef = (y1-y2) / (x1-x2)
        intercept = y1 - coef*x1
        if(x1 < x2):
            for i in range(x1, x2, 1):
                img[int(coef*i+intercept), i] = color
        else:
            for i in range(x2, x1, 1):
                img[int(coef*i+intercept), i] = color
        intercept = -1 * intercept/coef
        coef = 1 / coef
        if(y1 < y2):
            for i in range(y1, y2, 1):
                img[i, int(coef*i+intercept)] = color
        else:
            for i in range(y2, y1, 1):
                img[i, int(coef*i+intercept)] = color

def swap(x, y):
    return y, x
 
###                 ###
### WIDTH 구현 예정  ###
###                 ###
mode = [False for _ in range(5)] #[0]=rectangle
current_mode = 0
cmdqueue = []
title = 'photoshop'
img = np.full((700, 1366, 3), 255, np.uint8)
mouse_stats = [0, 0, 0, 0, False]

line_dis = np.array(cv2.imread("photoshap_/img/line_disable.jpg", cv2.IMREAD_COLOR))
line_able = np.array(cv2.imread("photoshap_/img/line_able.jpg", cv2.IMREAD_COLOR))
rect_dis = np.array(cv2.imread("photoshap_/img/rect_disable.jpg", cv2.IMREAD_COLOR))
rect_able = np.array(cv2.imread("photoshap_/img/rect_able.jpg", cv2.IMREAD_COLOR))
circle_dis = np.array(cv2.imread("photoshap_/img/circle_disable.jpg", cv2.IMREAD_COLOR))
circle_able = np.array(cv2.imread("photoshap_/img/circle_able.jpg", cv2.IMREAD_COLOR))
right_triangle_dis = np.array(cv2.imread("photoshap_/img/right_triangle_disable.jpg", cv2.IMREAD_COLOR))
right_triangle_able = np.array(cv2.imread("photoshap_/img/right_triangle_able.jpg", cv2.IMREAD_COLOR))
triangle_dis = np.array(cv2.imread("photoshap_/img/triangle_disable.jpg", cv2.IMREAD_COLOR))
triangle_able = np.array(cv2.imread("photoshap_/img/triangle_able.jpg", cv2.IMREAD_COLOR))

update_toolbar()
square_area(img, 100, 600, 150, 1200, 3, (0, 0, 0))

cv2.namedWindow(title, cv2.WINDOW_AUTOSIZE)    
cv2.imshow(title, img)
cv2.setMouseCallback(title, onMouse)

while True:
    key = cv2.waitKey(100)
    if key == 27: break

    elif key == 26 and len(cmdqueue)!=0:
        cmdqueue.pop()
        draw()
        
cv2.destroyAllWindows()