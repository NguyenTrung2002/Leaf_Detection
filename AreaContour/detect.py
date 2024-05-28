import subprocess
import cv2
import os
import tkinter as tk
from tkinter import filedialog

def select_image():
    root = tk.Tk()
    root.withdraw()  # Ẩn cửa sổ tkinter chính
    file_path = filedialog.askopenfilename()  # Mở hộp thoại chọn file
    return file_path

def run_detection(image_path, result_folder):
    # Đường dẫn đến script nhận diện của YOLOv5
    detect_script = 'yolov5/detect.py'
    # Tùy chỉnh các tham số cho dòng lệnh
    weights = 'yolov5/best.pt'
    project = 'leaf'
    save_crop = '--save-crop'
    
    # Xây dựng dòng lệnh đầy đủ
    command = f'python {detect_script} --weights {weights} --source "{image_path}" --project {project} --name {result_folder} {save_crop}'
    
    # Chạy dòng lệnh
    subprocess.run(command, shell=True)

def display_images(project_folder, experiment_name):
    # Xây dựng đường dẫn đến thư mục chứa ảnh đã nhận diện
    detected_images_path = os.path.join(project_folder, experiment_name, 'crops')

    # Lấy danh sách tất cả các file trong thư mục
    images = [img for img in os.listdir(detected_images_path) if img.endswith(('.png', '.jpg', '.jpeg'))]
    
    # Hiển thị mỗi ảnh
    for image_file in images:
        image_path = os.path.join(detected_images_path, image_file)
        image = cv2.imread(image_path)
        cv2.imshow('Detected Image', image)
        cv2.waitKey(0)  # Chờ nhấn phím bất kỳ để hiển thị ảnh tiếp theo
        cv2.destroyAllWindows()

if __name__ == '__main__':
    image_path = select_image()
    if image_path:
        # Tạo tên thư mục kết quả từ tên tập tin
        result_folder = os.path.splitext(os.path.basename(image_path))[0]
        run_detection(image_path, result_folder)
        display_images('leaf', result_folder)
    else:
        print("No files selected.")
