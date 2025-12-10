import os
import numpy as np
from PIL import Image
from pathlib import Path


class SlidingWindowDatasetGenerator:
    def __init__(self, patch_size=650, base_dirs=None):
        """
        Args:
            patch_size: размер кусочка (650x650)
            base_dirs: словарь с путями к папкам со слайсами
        """
        self.patch_size = patch_size
        self.base_dirs = base_dirs or {
            'без полимера': '/Users/vlad/Desktop/DALER/2 этап/итоговые изображения/без полимера 3/5',
            'с полимером': '/Users/vlad/Desktop/DALER/2 этап/итоговые изображения/с полимером 3/5'
        }
        
    def get_augmentations(self, patch):
        """Возвращает аугментированные версии кусочка"""
        augmented = {
            '': patch,                                                  # original
            '+90': Image.fromarray(np.rot90(np.array(patch), k=1)),    # +90°
            '180': Image.fromarray(np.rot90(np.array(patch), k=2)),    # 180°
            '-90': Image.fromarray(np.rot90(np.array(patch), k=3)),    # -90°
        }
        return augmented
    
    def extract_patches_with_sliding_window(self, img, stride=None):
        """
        Извлекает кусочки с скользящим окном
        Возвращает (patches, coordinates_with_indices)
        где coordinates_with_indices содержит (row, col)
        """
        if stride is None:
            stride = self.patch_size  # без перекрытия
        
        width, height = img.size
        patches = []
        coordinates = []
        
        row = 0
        y = 0
        while y + self.patch_size <= height:
            col = 0
            x = 0
            while x + self.patch_size <= width:
                patch = img.crop((x, y, x + self.patch_size, y + self.patch_size))
                patches.append(patch)
                coordinates.append((row, col))
                col += 1
                x += stride
            row += 1
            y += stride
        
        return patches, coordinates
    
    def process_category(self, category_name, slices_dir, stride=None):
        """
        Обрабатывает все вертикальные слайсы для категории
        Создает отдельную папку patches для каждого слайса
        """
        # Находим все PNG файлы (вертикальные слайсы)
        slice_files = sorted([f for f in os.listdir(slices_dir) if f.endswith('.png')])
        
        print(f"\n{'='*80}")
        print(f"Обработка категории: {category_name}")
        print(f"Папка со слайсами: {slices_dir}")
        print(f"Найдено вертикальных слайсов: {len(slice_files)}")
        print(f"{'='*80}")
        
        # Обрабатываем каждый вертикальный слайс
        for slice_idx, slice_file in enumerate(slice_files):
            slice_path = os.path.join(slices_dir, slice_file)
            slice_name = os.path.splitext(slice_file)[0]
            
            # Создаем отдельную папку patches для каждого слайса
            patches_output_dir = os.path.join(slices_dir, f"patches_{slice_idx}")
            os.makedirs(patches_output_dir, exist_ok=True)
            
            # Открываем вертикальный слайс
            img = Image.open(slice_path)
            width, height = img.size
            
            # Извлекаем кусочки со скользящим окном
            patches, coordinates = self.extract_patches_with_sliding_window(img, stride=stride)
            
            print(f"\n {slice_file}")
            print(f"   Размер: {width}x{height}")
            print(f"   Кусочков: {len(patches)}")
            print(f"   Сохраняются в: patches_{slice_idx}")
            
            # Обрабатываем каждый кусочек
            for patch, (row, col) in zip(patches, coordinates):
                augmentations = self.get_augmentations(patch)
                
                # Сохраняем все аугментированные версии в папку patches
                for aug_suffix, aug_patch in augmentations.items():
                    # Формирование имени файла
                    if aug_suffix == '':
                        filename = f"{slice_name}_{row}_{col}.png"
                    else:
                        filename = f"{slice_name}_{row}_{col}_{aug_suffix}.png"
                    
                    output_path = os.path.join(patches_output_dir, filename)
                    aug_patch.save(output_path)
            
            print(f"  Завершено: {len(patches)} кусочков × 4 аугментации = {len(patches) * 4} файлов")
    
    def run(self, stride=None):
        """
        Запускает обработку обеих категорий с одинаковыми параметрами
        """
        print(f"\nНАЧАЛО ОБРАБОТКИ ДАТАСЕТА")
        print(f"Размер кусочка: {self.patch_size}x{self.patch_size}")
        print(f"Шаг скольжения: {stride if stride else 'без перекрытия'}")
        
        # Обрабатываем обе категории с одинаковыми параметрами
        for category, slices_dir in self.base_dirs.items():
            self.process_category(category, slices_dir, stride=stride)
        
        print(f"\n{'='*80}")
        print(f"ОБРАБОТКА ЗАВЕРШЕНА")
        print(f"{'='*80}\n")


if __name__ == "__main__":
    generator = SlidingWindowDatasetGenerator(
        patch_size=650,
        base_dirs={
            'без полимера': '/Users/vlad/Desktop/DALER/2 этап/итоговые изображения/оригиналы после обрезки и preprocessing/5',
            'с полимером': '/Users/vlad/Desktop/DALER/2 этап/итоговые изображения/оригиналы после обрезки и preprocessing/5'
        }
    )
    
    # stride=125 → примерно 19% перекрытие
    # stride=None → без перекрытия кусочков
    # stride=325 → 50% перекрытие
    generator.run(stride=100)
