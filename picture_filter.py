import os
import glob
import face_recognition
import shutil

def images_with_face(source_folder, target_folder):
    # 确保目标文件夹存在
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    # 获取源文件夹中所有图片文件的路径
    image_files = glob.glob(os.path.join(source_folder, '*.[jp][pn]g'))  # 支持 jpg 和 png 格式
    image_files.extend(glob.glob(os.path.join(source_folder, '*.[JP][PN]G')))  # 支持 JPG 和 PNG 格式
    image_files.extend(glob.glob(os.path.join(source_folder, '*.[bmp][BMP]')))  # 支持 bmp 格式


    # 遍历所有图片文件
    for image_file in image_files:
        try:
            # 加载图片
            image = face_recognition.load_image_file(image_file)

            # 检测人脸
            face_locations = face_recognition.face_locations(image)

            # 如果检测到人脸，将图片移动到目标文件夹
            if len(face_locations) > 0:
                print(f"移动有人脸的图片: {image_file}")
                print(os.path.join(target_folder, os.path.basename(image_file)))
                shutil.move(image_file, os.path.join(target_folder,"\\"+os.path.basename(image_file)))
        except Exception as e:
            print(f"处理图片 {image_file} 时出错: {e}")

