import cv2 
img = cv2.imread('test1.jpg')

# Задание 3

# OpenCV использует H: 0-179, S: 0-255, V: 0-255
# Также, OpenCV использует формат BGR, а не RGB

# Конвертация BGR пикселя в RGB 

def convertpix(pixel):
    if pixel[0] == 0 and pixel[1] == 0 and pixel[2] == 0:
        return [0, 0, 0]
    b = pixel[0]/255
    g = pixel[1]/255
    r = pixel[2]/255
    mx = max(r, g, b)
    mn = min(r, g, b)
    dif = mx - mn
    v = mx
    s = 0
    h = 0
    if mx == 0:
        s = 0
    else:
        s = 1 - mn / mx
        
    if mx == mn:
        h = 0
    elif mx == r:
        if g >= b:
            h = 60 * (g - r) / dif
        else:
            h = 60 * (g - r) / dif + 360
    elif mx == g:
        h = 60 * (r - b) / dif + 120
    else:
        h = 60 * (b - g) / dif + 120
    return [int(h / 2), int(s * 255), int(v * 255)]


# Отображение пикселя
def mapimg(img, pixelfunc):
    for i in range(0, len(img)):
        for j in range (0, len(img[0])):
            img[i][j] = pixelfunc(img[i][j])
    return img


 
def sm(x, y):
    return x + y  

# Добавление тона 
# Добавление насыщенности
# Добавление яркости
# В зависимости от arg (h = 0, s = 1, v = 2)    
def mapdim(img, func, addh, adds, addv):
    for i in range(0, len(img)):
        for j in range (0, len(img[0])):
            img[i][j][0] = min(func(img[i][j][0], addh), 179)
            img[i][j][1] = min(func(img[i][j][0], adds), 255)
            img[i][j][2] = min(func(img[i][j][0], addv), 255)

def emptyFunction():
    pass

img = mapimg(img, convertpix)

windowName = 'HSV'
cv2.namedWindow(windowName)

cv2.createTrackbar('+ H', windowName, 0, 179, emptyFunction)
cv2.createTrackbar('+ S', windowName, 0, 255, emptyFunction)
cv2.createTrackbar('+ V', windowName, 0, 255, emptyFunction)
h, s, v = 0, 0, 0
h1, s1, v1 = 0, 0, 0   
cv2.imshow(windowName, img)

while(True):
    cv2.imshow(windowName, img)
  
    h = cv2.getTrackbarPos('+ H', windowName)
    s = cv2.getTrackbarPos('+ S', windowName)
    v = cv2.getTrackbarPos('+ V', windowName)
    img = mapdim(img, sm, h - h1, s - s1, v - v1)
    h1, s1, v1 = h, s, v
    if cv2.waitKey(1) == 27: # 27 - ESC key
        break
    
cv2.destroyAllWindows()       


