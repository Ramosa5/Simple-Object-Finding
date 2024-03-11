import cv2
import numpy as np

img = cv2.imread('./dublin.jpg')
img2 = cv2.imread('./dublin_edited.jpg')

height, width, x = img.shape
height2, width2, x2 = img.shape

r = np.zeros((height, width))
g = np.zeros((height, width))
b = np.zeros((height, width))
r2 = np.zeros((height, width))
g2 = np.zeros((height, width))
b2 = np.zeros((height, width))

for i in range(height):
    for j in range(width):
        r[i, j] = img[i, j, 0]
        g[i, j] = img[i, j, 1]
        b[i, j] = img[i, j, 2]
        r2[i, j] = img2[i, j, 0]
        g2[i, j] = img2[i, j, 1]
        b2[i, j] = img2[i, j, 2]

print(height, width)

bound_r = np.zeros((height, width), dtype=np.uint8)
bound_g = np.zeros((height, width), dtype=np.uint8)
bound_b = np.zeros((height, width), dtype=np.uint8)
check = np.zeros((height, width), dtype=np.uint8)

highest = 0
lowest = height
right = 0
left = width
detected = []
det_buf = 0

for i in range(int(height)):
    for j in range(int(width)):
        norm1 = (int(r[i, j])+int(g[i, j])+int(b[i, j]))/3
        norm2 = (int(r2[i, j])+int(g2[i, j])+int(b2[i, j]))/3
        if np.abs(norm1 - norm2) > 40 and check[i, j] != 254:
            detected.append([highest, lowest, right, left])
            for k in range(i, i+100):
                for l in range(j-50, j+50):
                    cur_x = k-i
                    cur_y = l-j+50
                    if np.abs((int(r[k, l])+int(g[k, l])+int(b[k, l]))/3 - (int(r2[k, l])+int(g2[k, l])+int(b2[k, l]))/3) > 30:
                        if detected[det_buf][0] == 0:
                            detected[det_buf][0] = k
                        detected[det_buf][1] = k
                        if detected[det_buf][2] < l:
                            detected[det_buf][2] = l
                        if detected[det_buf][3] > l:
                            detected[det_buf][3] = l
                    check[k, l] = 254
            det_buf += 1

        bound_r[i, j] = r2[i, j]
        bound_g[i, j] = g2[i, j]
        bound_b[i, j] = b2[i, j]

for box in detected:
    highest = box[0]
    lowest = box[1]
    right = box[2]
    left = box[3]
    # print(highest, lowest, right, left)
    for i in range(highest-1, lowest+2):
        if i > 1079:
            break
        bound_r[i, left-1] = 0
        bound_g[i, left-1] = 255
        bound_b[i, left-1] = 0
        bound_r[i, right+1] = 0
        bound_g[i, right+1] = 255
        bound_b[i, right+1] = 0
    for i in range(left-1, right+2):
        if i > 1919:
            break
        bound_r[highest-1, i] = 0
        bound_g[highest-1, i] = 255
        bound_b[highest-1, i] = 0
        bound_r[lowest+1, i] = 0
        bound_g[lowest+1, i] = 255
        bound_b[lowest+1, i] = 0


chosen_cut = 0

out_height, out_width = np.abs(detected[chosen_cut][1]-detected[chosen_cut][0]), np.abs(detected[chosen_cut][2]-detected[chosen_cut][3])
r_out = np.zeros((out_height, out_width), dtype=np.uint8)
g_out = np.zeros((out_height, out_width), dtype=np.uint8)
b_out = np.zeros((out_height, out_width), dtype=np.uint8)
alpha = np.full((out_height, out_width), 255, dtype=np.uint8)

for i in range(detected[chosen_cut][0], detected[chosen_cut][1]):
    for j in range(detected[chosen_cut][3], detected[chosen_cut][2]):
        cur_x = i - detected[chosen_cut][1]
        cur_y = j - detected[chosen_cut][3]
        if np.abs(int(r[i, j]) - int(r2[i, j]))+np.abs(int(g[i, j]) - int(g2[i, j]))+np.abs(int(b[i, j]) - int(b2[i, j])) < 30:
            alpha[cur_x, cur_y] = 0
        r_out[cur_x, cur_y] = r2[i, j]
        g_out[cur_x, cur_y] = g2[i, j]
        b_out[cur_x, cur_y] = b2[i, j]

for i in range(1, out_height-1):
    for j in range(out_width):
        if int(alpha[i-1][j]) - int(alpha[i+1][j]) == 0:
            alpha[i][j] = alpha[i-1][j]
for i in range(out_height):
    for j in range(1, out_width-1):
        if int(alpha[i][j-1]) - int(alpha[i][j+1]) == 0:
            alpha[i][j] = alpha[i][j-1]

rgb_array = np.dstack((r_out, g_out, b_out, alpha))
rgb_array2 = np.dstack((bound_r, bound_g, bound_b))

# cv2.imshow('Keviniarz', rgb_array)
# cv2.imshow('Dubliniarz', rgb_array2)
cv2.imwrite('output_kevin.png', rgb_array)
cv2.imwrite('output_Dublin.png', rgb_array2)
cv2.waitKey(0)
cv2.destroyAllWindows()
