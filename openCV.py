import numpy as np
import cv2
import imutils
import pytesseract
#import các thư viện cần thiết

def show_img(image):
    cv2.imshow("image_name",image)
    cv2.waitKey(0)
#Hàm hiển thị ảnh

def img_load(file_name):
     image = cv2.imread(file_name) # load ảnh
     image = imutils.resize(image, height = 500)  #resize ảnh 
     return image
#Hàm load ảnh từ file

def img_retouch(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #ảnh xám
    blur = cv2.GaussianBlur(gray, (5, 5), 0) # làm mờ ảnh
    bilateral = cv2.bilateralFilter(blur, 5, 10, 10) # làm mịn ảnh
    return bilateral
#Hàm xử lí ảnh

def find_contours(bilateral,image):
    #_, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    edged = cv2.Canny(bilateral, 30, 120) # tìm cạnh bằng Canny
    contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # đường viền
    largest_area = sorted(contours, key = cv2.contourArea)

    for cnts in largest_area:
        peri = cv2.arcLength(cnts, True)
        approx = cv2.approxPolyDP(cnts, 0.09 * peri, True)

    cv2.drawContours(image, [approx], 0, (0, 255, 255), 5) # vẽ đường viền
    return approx # trả về đỉnh
#Hàm tìm đường viền

def crop_contours(approx, image):
    coordinates_0 = (approx[0,0,0], approx[0,0,1])
    coordinates_1 = (approx[1,0,0], approx[1,0,1])
    coordinates_2 = (approx[2,0,0], approx[2,0,1])
    coordinates_3 = (approx[3,0,0], approx[3,0,1])

    if approx[0,0,0] < 320:
        top_left = coordinates_0
        bottom_left = coordinates_1
        bottom_right = coordinates_2
        top_right = coordinates_3

    else:
        top_right = coordinates_0
        top_left = coordinates_1
        bottom_left = coordinates_2
        bottom_right = coordinates_3

    pts1 = np.float32([[top_left], [top_right], [bottom_right], [bottom_left]])
    pts2 = np.float32([[0, 0], [450, 0], [450, 300], [0, 300]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    result = cv2.warpPerspective(image, matrix, (450, 300))
    return result
#Hàm cắt các đường viền

def crop_cmnd(result):
    img_cmnd = result[70:103, 225:390]
    return img_cmnd
#Hàm cắt trường cmnd

def crop_hoten(result):
    img_hoten = result[100:150, 187:420]
    return img_hoten
#Hàm cắt trường họ tên

def char_recog(img):
    custom_config = r'-c tessedit_char_whitelist=0123456789' #cấu hình
    text_recog = pytesseract.image_to_string(img, lang='eng',config=custom_config)#nhận dạng
    return text_recog #trả về kiểu test

def main():
    image = img_load('./Image/cmnd5.jpg')
    bilateral = img_retouch(image)
    approx = find_contours(bilateral,image)
    result = crop_contours(approx, image)
    show_img(result)
    so_cmnd = crop_cmnd(result)
    show_img(so_cmnd)
    ho_ten = crop_hoten(result)
    show_img(ho_ten)
    so_cmnd_retouch = img_retouch(so_cmnd)
    show_img(so_cmnd_retouch)
    ho_ten_retouch = img_retouch(ho_ten)
    show_img(ho_ten_retouch)
    print('So cmnd : ', char_recog(so_cmnd_retouch))
    print('Ho va ten : ', char_recog(ho_ten_retouch))

    
main()



# # # def edit_image_after(image):
# # #     gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# # #     blur_image = cv2.GaussianBlur(gray_image, (3, 3), 1)
# # #     bilateral_image = cv2.bilateralFilter(blur_image, 5, 10, 10)
# # #     # thresh_ho_ten = cv2.adaptiveThreshold(bilateral_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 3, 3)
# # #     # _, thresh_ho_ten = cv2.threshold(bilateral_image ,125,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

# # #     return bilateral_image



