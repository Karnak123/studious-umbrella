import pandas as pd
import cv2
import argparse

r, g, b, xp, yp, clicked = 0, 0, 0, 0, 0, False


def draw_function(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b, g, r, xpos, ypos, clicked
        xp, yp, clicked = x, y, True
        b, g, r = img[y, x]
        b, g, r = int(b), int(g), int(r)


def color_name(R, G, B):
    m = 10000
    for i in range(len(csv)):
        d = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
        if d <= m:
            m = d
            cname = csv.loc[i, "color_name"]
    return cname


ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=True, help='Image Path')
args = vars(ap.parse_args())
img_path = args['image']

img = cv2.imread(img_path)

index = ['color', 'color_name', 'hex', 'R', 'G', 'B']
csv = pd.read_csv('colors.csv', names=index, header=None)

cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_function)

while 1:
    cv2.imshow("image", img)
    if clicked:
        cv2.rectangle(img, (20, 20), (750, 60), (b, g, r), -1)
        text = color_name(r, g, b) + ' R='+ str(r) + ' G='+ str(g) + ' B='+ str(b)
        cv2.putText(img, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
        if(r+g+b) >= 600:
            cv2.putText(img, text, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)
        clicked=False
    if cv2.waitKey(20) & 0xFF == 27:
        break
cv2.destroyAllWindows()