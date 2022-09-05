
import pickle

from sklearn.model_selection import train_test_split
from keras.applications.vgg16 import VGG16
from keras.layers import Input, Flatten, Dense, Dropout
from keras.models import Model
from keras.callbacks import ModelCheckpoint
from keras.preprocessing.image import ImageDataGenerator

# Số lớp
num_class = 3
n_epoch = 10

# Hàm load dữ liệu từ file
def load_data():

    print("Bắt đầu load dữ liệu từ file....")
    file = open('data.pkl', 'rb')
    (pixels, labels) = pickle.load(file)
    file.close()

    print("Đã load xong dữ liệu từ file. Kích thước input và output:")
    print(pixels.shape)
    print(labels.shape)

    num_class = labels.shape[1]

    return pixels, labels, num_class


# Hàm xây dựng model Deep Leanring - Mạng Nơ ron transfer learning VGG16
def get_vgg_model(num_classes):
    model_vgg16_conv = VGG16(weights='imagenet', include_top=False)

    # Dong bang cac layer
    for layer in model_vgg16_conv.layers:
        layer.trainable = False

    # Tao model
    input = Input(shape=(128, 128, 3), name='image_input')
    output_vgg16_conv = model_vgg16_conv(input)

    # Them cac layer FC va Dropout
    x = Flatten(name='flatten')(output_vgg16_conv)
    x = Dense(4096, activation='relu', name='fc1')(x)
    x = Dropout(0.5)(x)
    x = Dense(4096, activation='relu', name='fc2')(x)
    x = Dropout(0.5)(x)
    if num_classes==1:
        x = Dense(num_classes, activation='sigmoid', name='predictions')(x)
    else:
        x = Dense(num_classes, activation='softmax', name='predictions')(x)

    # Compile
    my_model = Model(inputs=input, outputs=x)
    if num_classes==1:
        my_model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    else:
        my_model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    return my_model


print("Bắt đầu thực hiện chia dữ liệu train,test....")
X, y, num_class = load_data()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Đã chia xong dữ liệu. Kích thước dữ liệu train:")
print(X_train.shape)
print(y_train.shape)

# Load model
vggmodel = get_vgg_model(num_class)

# Cấu hình tham số checkpoint
filepath = "model_vgg_weights.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='val_accuracy', verbose=1, save_best_only=True, mode='max')
callbacks_list = [checkpoint]

# Augment ảnh cho phong phú hơn
aug = ImageDataGenerator(rotation_range=20, zoom_range=0.1,
                         rescale=1. / 255,
                         width_shift_range=0.1,
                         height_shift_range=0.1,
                         horizontal_flip=True,
                         brightness_range=[0.2, 1.5], fill_mode="nearest")

aug_val = ImageDataGenerator(rescale=1. / 255)

# Bắt đầu train
vgg_hist = vggmodel.fit_generator(aug.flow(X_train, y_train, batch_size=64),
                                 epochs=n_epoch,
                                 validation_data=aug.flow(X_test, y_test,
                                                          batch_size=len(X_test)),
                                 callbacks=callbacks_list)
# Lưu model
vggmodel.save("model_vgg.h5")
print("Đã train xong")
