import cv2
import numpy as np
import os

input_folder = '/Users/vlad/Desktop/DALER/2 этап/оригиналы после обрезки и preprocessing'
output_folder = '/Users/vlad/Desktop/DALER/2 этап/с полимером 4'

# Пороговые значения
lower_thresh = 62
upper_thresh = 255

# Параметры морфологии
kernel_size = 2 # размер ядра морфологии

# Порог минимальной площади объекта
min_area = 90 #все объекты меньше этой площади будут удалены

# Имя файл
target_filename = '0.png'

#сохранение
os.makedirs(output_folder, exist_ok=True)

input_path = os.path.join(input_folder, target_filename)

if not os.path.exists(input_path):
    raise FileNotFoundError(f"Файл '{target_filename}' не найден в папке '{input_folder}'.")

# Чтение изображения в градациях серого
img = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)

# Бинаризация по диапазону
binary_mask = cv2.inRange(img, lower_thresh, upper_thresh)

# Морфологический closing
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))
closed_mask = cv2.morphologyEx(binary_mask, cv2.MORPH_CLOSE, kernel)

# Нахождение контуров
contours, _ = cv2.findContours(closed_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Создание чистой маски
final_mask = np.zeros_like(closed_mask)

# Оставляем только большие объекты
for cnt in contours:
    area = cv2.contourArea(cnt)
    if area >= min_area:
        cv2.drawContours(final_mask, [cnt], -1, 255, thickness=cv2.FILLED)

output_path = os.path.join(output_folder, target_filename)
cv2.imwrite(output_path, final_mask)

print(f"Готово! Маска для '{target_filename}' сохранена в папке '{output_folder}' с удалением мелких объектов.")