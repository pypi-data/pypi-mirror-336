# Imaris Convert

一个用于将图像转换为 Imaris 格式的 Python 工具包。

## 安装

```bash
pip install imaris-convert
```

## 使用方法

### 命令行使用

```bash
# 基本用法
imaris-convert input.tiff

# 指定输出目录
imaris-convert input.tiff -o /path/to/output/directory
```

### Python API 使用

```python
# 转换图像文件(.tiff)
from imaris_convert import tiff_to_imaris

tif_path = r'your_tiff_path'
tiff_to_imaris(tiff_path=tif_path)
# tiff_to_imaris(tiff_path=tif_path,out_path=out_path)

# 转换 np.ndarray 到 ims
from imaris_convert import numpy_to_imaris
import numpy as np

your_np_data = np.ones((100,100,100),dtype=np.uint16)
numpy_to_imaris(np_data=your_np_data,out_path='your_save_path')
```

## 依赖项

- Python >= 3.6
- numpy
- tifffile
- tqdm

## 许可证

MIT License 