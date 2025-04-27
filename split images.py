from PIL import Image
import os

# Входные папки
folder1 = '/Users/vlad/Desktop/Подходящие'
folder2 = '/Users/vlad/Desktop/Подходящие без полимера'

# Имя изображения (одинаковое в обеих папках)
filename = 'TAU80_Ag_Si_ann_NFP50_09_017.jpg'  # <<<ИМЯ ФАЙЛА

# Кол-во строк и колонок
rows = 4
cols = 4

# Выходные папки
base_output = '/Users/vlad/Desktop/sliced_images'
output1 = os.path.join(base_output, 'подходящие')
output2 = os.path.join(base_output, 'подходящие с полимером')
os.makedirs(output1, exist_ok=True)
os.makedirs(output2, exist_ok=True)

def slice_and_rotate_image(image_path, rows, cols, output_folder, base_name):
    img = Image.open(image_path)
    img_width, img_height = img.size
    tile_width = img_width // cols
    tile_height = img_height // rows

    count = 1
    for row in range(rows):
        for col in range(cols):
            left = col * tile_width
            upper = row * tile_height
            right = left + tile_width
            lower = upper + tile_height
            box = (left, upper, right, lower)
            tile = img.crop(box)

            # Оригинальный слайс
            tile.save(os.path.join(output_folder, f"{base_name}_{count}.png"))

            # Поворот на +90°
            rotated_90 = tile.rotate(90, expand=True)
            rotated_90.save(os.path.join(output_folder, f"{base_name}_{count}_+90.png"))

            # Поворот на -90°
            rotated_minus_90 = tile.rotate(-90, expand=True)
            rotated_minus_90.save(os.path.join(output_folder, f"{base_name}_{count}_-90.png"))

            # Поворот на 180°
            rotated_180 = tile.rotate(180, expand=True)
            rotated_180.save(os.path.join(output_folder, f"{base_name}_{count}_180.png"))

            count += 1

# Получаем имя файла без расширения
base_name = os.path.splitext(filename)[0]

# Режем изображение из "Подходящие"
path1 = os.path.join(folder1, filename)
slice_and_rotate_image(path1, rows, cols, output1, base_name)

# Режем изображение из "Подходящие без полимера"
path2 = os.path.join(folder2, filename)
slice_and_rotate_image(path2, rows, cols, output2, base_name)

print("Готово! Всё сохранено с поворотами.")
