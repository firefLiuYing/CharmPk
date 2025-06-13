import os
import glob
import face_recognition
import shutil
import picture_filter as pf

source_path = 'F:\\\\profession_work\\\\unfiltered_set'
target_path = 'F:\\\\profession_work\\\\train_set'

pf.images_with_face(source_path, target_path)
