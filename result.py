import subprocess

def run_script(script_path):
    """Hàm chạy một script Python và in kết quả. Ngừng nếu không có ảnh được chọn."""
    try:
        result = subprocess.run(['python', script_path], check=True, text=True, capture_output=True)
        # Kiểm tra kết quả để xác định có lỗi không được chọn ảnh hay không
        if "No files selected" in result.stdout:
            print("No image selected. Stopping the execution.")
            return False  # Trả về False nếu không có ảnh được chọn
        print(f"Output of {script_path}:\n{result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_path}:\n{e.stderr}")
        return False  # Trả về False nếu có lỗi khi chạy script

if __name__ == '__main__':
    # Đường dẫn đến các script
    script_paths = [
        'AreaContour/area_A4.py',
        'AreaContour/detect.py',
        'AreaContour/area_leaf.py'
    ]

    # Chạy từng script, dừng nếu không có ảnh được chọn
    for script in script_paths:
        if not run_script(script):
            break  # Dừng vòng lặp nếu một script trả về False
