import cv2
import face_recognition


known_image = face_recognition.load_image_file("image3.png")
face_locations = face_recognition.face_locations(known_image)
known_encodings = face_recognition.face_encodings(known_image)

draw_image = cv2.imread("image3.png")
#unknown_image = face_recognition.load_image_file("image3.jpg")

for known_encoding in known_encodings:
    print(known_encoding)
    print("\n")

num = 1
for face_location in face_locations:
    cv2.rectangle(draw_image,
                 (face_location[1],face_location[0]),
                 (face_location[3],face_location[2]),
                 (0,255,0),
                 2)
    cv2.putText(draw_image,
                f"bitch {num}",  # 文字内容
                (face_location[3],face_location[0]),  # 文字位置方位于框顶部
                cv2.FONT_HERSHEY_SIMPLEX,  # 字体
                0.5,  # 字体大小
                (0, 255, 0),  # 文字颜色（绿色）
                2)  # 文字粗细
    print(face_location)
    print("\n")
    num += 1

cv2.imshow("Image", draw_image)
cv2.waitKey(0)
cv2.destroyAllWindows()