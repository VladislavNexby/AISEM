import cv2
import numpy as np
import pandas as pd
import glob
import os

# Загрузка бинарных изображений (белые: 255, черные: 0)
folder = '/Users/vlad/Desktop/DALER/2 этап/с полимером 3'
output_csv = '/Users/vlad/Desktop/DALER/2 этап/с полимером 3/results.csv' 

filepaths = glob.glob(os.path.join(folder, '*.png'))
# Явно сортируем файлы по числу в имени
filepaths.sort(key=lambda x: int(os.path.basename(x).split('.')[0]))


results = []
for filepath in filepaths:  # Меняйте на нужное расширение
    image_name = os.path.basename(filepath)
    image = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
    if image is None:
        continue
    height, width = image.shape
    split_width = width // 5

    for i in range(5):
        start = i * split_width
        end = (i + 1) * split_width if i < 4 else width
        segment = image[:, start:end]

        # Количество белых пикселей
        white_pixels = np.sum(segment == 255)

        # Бинаризация
        segment_bin = (segment == 255).astype(np.uint8)

        # Поиск кластеров (connected components)
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(segment_bin)
        num_clusters = num_labels - 1  # не считать фон (0)

        # Площадь каждого кластера
        areas = stats[1:, cv2.CC_STAT_AREA] if num_clusters > 0 else np.array([0])

        # Плотность кластеров: сумма площадей кластеров / площадь сегмента
        density = areas.sum() / segment.size if segment.size > 0 else 0

        # Средний и максимальный размер кластера
        avg_area = areas.mean() if areas.size > 0 else 0
        max_area = areas.max() if areas.size > 0 else 0

        results.append({
            'Белые пиксели': int(white_pixels),
            'Число кластеров': int(num_clusters),
            'Плотность кластеров': float(density),
            'Средний размер кластера': float(avg_area),
            'Максимальный размер кластера': float(max_area)
        })

df = pd.DataFrame(results)
df.to_csv(output_csv, index=False)
print(f'Результаты сохранены в {output_csv}')