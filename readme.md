<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>
<div class="container">
    <h1>Hướng Dẫn Sử Dụng</h1>
    <h2>Bước 1:</h2>
    <p>Mở terminal và chạy những lệnh sau:</p>
    <code>git clone https://github.com/NguyenTrung2002/Leaf_Detection.git</code><br>
    <code>cd Leaf_Detection</code><br>
    <code>pip install -r requirements.txt</code>
    <h2>Bước 2:</h2>
    <p>Chạy lệnh này trong terminal: <code>python result.py</code></p>
    <ul>
        <li>Cửa sổ đầu tiên hiện lên, chọn hình ảnh chứa vật tham chiếu (Ở đây là file <code>A415-5.jpg</code>)</li>
        <li>Cửa sổ thứ hai hiện lên, chọn hình ảnh chứa lá cây cần nhận diện (Ở đây là file <code>Copb15-5.jpg</code>), kết quả sẽ được lưu ở thư mục <code>leaf</code></li>
        <li>Cửa sổ thứ ba hiện lên, chọn tất cả hình ảnh đã được nhận diện và cắt từng bounding box (Hình ảnh sẽ được lưu ở <code>leaf/Copb15-5/crops/leaf</code>)</li>
    </ul>
    <h2>Bước 3:</h2>
    <p>Sau khi đã làm những điều trên, kết quả tính diện tích lá cây sẽ được hiện ra.</p>
</div>
</body>
</html>
