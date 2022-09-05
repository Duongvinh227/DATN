from os import listdir
import cv2
import numpy as np
import pickle
import os

# File xử lý ảnh thô trong thư mục train_data và lưu vào file dữ liệu
# Mục đích để load dữ liệu nhanh hơn và xử lý thuận tiện hơn

raw_folder = "train_data"
dest_size = (128, 128)

print("Bắt đầu xử lý ảnh...")

pixels = []
labels = []


# Lặp qua các folder con trong thư mục raw
for folder in listdir(raw_folder):
    if folder[0] != ".":  # Bỏ qua cac thư mục không hợp lệ
        print("Processing folder ", folder)

        # Lặp qua các file trong từng thư mục chứa
        for file in listdir(os.path.join(raw_folder,folder)):
            if file[0] != '.':
                print("---- Processing file = ", file)
                pixels.append(cv2.resize(cv2.imread(os.path.join(raw_folder, folder, file)), dsize=dest_size))
                labels.append(folder)

pixels = np.array(pixels)
labels = np.array(labels)

# Xử lý nhãn của dữ liệu
from sklearn.preprocessing import LabelBinarizer

encoder = LabelBinarizer()
labels = encoder.fit_transform(labels)
print(encoder.classes_)

# Lưu dữ liệu vào file data.pkl
file = open('data.pkl', 'wb')
pickle.dump((pixels, labels), file)
file.close()

# Lưu các nhãn vào file labels.pkl
file = open('labels.pkl', 'wb')
pickle.dump(encoder, file)
file.close()