import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Загрузка данных
df = pd.read_csv('/Users/vlad/Desktop/DALER/2 этап/с полимером 3/results.csv')

# Количество сегментов в одном изображении
segments_per_image = 5

# Создаем X-ось — последовательный номер сегмента по всем изображениям
df['global_segment_index'] = np.arange(len(df))

# Получаем количество изображений
num_images = len(df) // segments_per_image

# Цвета для групп сегментов по изображениям
colors = plt.cm.get_cmap('tab10', num_images)

# Характеристики для построения
metrics = ['Белые пиксели', 'Число кластеров', 'Плотность кластеров', 'Средний размер кластера', 'Максимальный размер кластера']

plt.figure(figsize=(15, 10))

labels = [f"{i}.png" for i in range(8)]  # создаём имена картинок от 0.png до 7.png

for idx, metric in enumerate(metrics, 1):
    plt.subplot(len(metrics), 1, idx)
    for i in range(num_images):
        segment_range = range(i * segments_per_image, (i + 1) * segments_per_image)
        subset = df.iloc[segment_range]
        plt.plot(subset['global_segment_index'], subset[metric], color=colors(i), marker='o', label=labels[i] if idx == 1 else "")
    plt.title(metric)
    plt.xlabel('Segment global index')
    plt.ylabel(metric, fontsize=8)
    if idx == 1:
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()
