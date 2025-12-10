import os
from PIL import Image

def split_image_horizontally(image_path, num_parts=5, output_base_dir=None):
    """
    Делит изображение на num_parts частей по горизонтали и сохраняет в подпапку
    
    Args:
        image_path: путь к изображению
        num_parts: количество частей (по умолчанию 5)
        output_base_dir: базовая папка для сохранения (если None, используется папка с изображением)
    """
    img = Image.open(image_path)
    width, height = img.size

    part_width = width // num_parts
    base_name = os.path.splitext(os.path.basename(image_path))[0]

    if output_base_dir is None:
        output_base_dir = os.path.dirname(image_path)
    output_dir = os.path.join(output_base_dir, base_name)
    os.makedirs(output_dir, exist_ok=True)

    print(f"Обработка: {image_path}")
    print(f"Части сохраняются в: {output_dir}")

    for i in range(num_parts):
        left = i * part_width
        right = width if i == num_parts - 1 else (i + 1) * part_width
        part = img.crop((left, 0, right, height))
        output_path = os.path.join(output_dir, f"{base_name}_{i+1}.png")
        part.save(output_path)
        print(f"  Часть {i+1} сохранена: {output_path} ({right-left}x{height})")

    print()

if __name__ == "__main__":
    input_dir = '/Users/vlad/Desktop/DALER/2 этап/итоговые изображения/оригиналы после обрезки и preprocessing'

    png_files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith('.png')]

    for png_file in png_files:
        split_image_horizontally(png_file, num_parts=5, output_base_dir=input_dir)

    print("Готово!")
