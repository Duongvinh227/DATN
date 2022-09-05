import cv2
import os

while True:
    class_name = input("Hãy nhập vào tên sản phẩm (viết liền, không dấu)/hoặc bấm q để thoát: ").strip()
    if class_name=="q":
        break
    else:
        frame_count = 0
        record = False
        cat_folder = os.path.join("train_data", class_name)
        print("Destination folder ", cat_folder)
        print("Bấm phím R lấy mẫu/dừng lấy mẫu. Bấm Q để thoát")

        import shutil
        if os.path.exists(cat_folder):
            shutil.rmtree(cat_folder)
        os.mkdir(cat_folder)

        cap = cv2.VideoCapture(1)
        while True:
            ret, frame = cap.read()
            if ret:
                frame = cv2.resize(frame, dsize=(640,640), fx=0.5, fy=0.5)
                frame = cv2.flip(frame,1)
                # Hiển thị
                cv2.imshow('frame', frame)
            if record:
                # Write file
                dest_file = 'img' + str(frame_count) + ".png"
                dest_file = os.path.join(cat_folder, dest_file)
                cv2.imwrite(dest_file, frame)
                frame_count += 1
                print(frame_count)
                if frame_count==200:
                    print("Đã lấy đủ 200 ảnh!")
                    break
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            if key == ord('r'):
                record = not record
        cap.release()
        cv2.destroyAllWindows()

