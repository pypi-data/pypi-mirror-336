# _*_ coding: utf-8 _*_
# @Time    : 2025/3/20 15:50
# @Author  : Guanhao Sun
# @File    : imaris_convert.py
# @IDE     : PyCharm
import argparse
import os
import sys
from . import PyImarisWriter as PW
import numpy as np
import tifffile as tf
from datetime import datetime

from tqdm import tqdm


class Configuration:
    def __init__(self, id, title, np_type, imaris_type, out_path: str = 'out.ims'):  # color_table
        self.mId = id
        self.mTitle = title
        self.mNp_type = np_type
        self.mImaris_type = imaris_type
        self.out_path = out_path
        # self.mColor_table = color_table


def set_configuration(id, title, np_type, imaris_type, out_path):
    return Configuration(id, title, np_type, imaris_type, out_path)


class MyCallbackClass(PW.CallbackClass):
    def __init__(self):
        self.mUserDataProgress = 0

    def RecordProgress(self, progress, total_bytes_written):
        progress100 = int(progress * 100)
        if progress100 - self.mUserDataProgress >= 5:
            self.mUserDataProgress = progress100
            print('User Progress {}, Bytes written: {}'.format(self.mUserDataProgress, total_bytes_written))


def write_data_to_ims(data: np.ndarray, config: Configuration):
    shape = data.shape
    image_size = PW.ImageSize(x=shape[2], y=shape[1], z=shape[0], c=1, t=1)
    dimension_sequence = PW.DimensionSequence('x', 'y', 'z', 'c', 't')
    block_size = image_size
    sample_size = PW.ImageSize(x=1, y=1, z=1, c=1, t=1)
    output_filename = config.out_path

    options = PW.Options()
    options.mNumberOfThreads = 12
    options.mCompressionAlgorithmType = PW.eCompressionAlgorithmGzipLevel2
    options.mEnableLogProgress = True

    # np_data = np.zeros((image_size.z, image_size.y, image_size.x), dtype=config.mNp_type)
    # x1 = int(image_size.x / 3)
    # x2 = int(image_size.x / 3 * 2)
    # np_data[:, :, 0:x1] = 10.0
    # np_data[:, :, x1:x2] = 130.0
    # np_data[:, :, x2:] = 240.0

    application_name = 'PyImarisWriter'
    application_version = '1.0.0'

    callback_class = MyCallbackClass()
    converter = PW.ImageConverter(config.mImaris_type, image_size, sample_size, dimension_sequence, block_size,
                                  output_filename, options, application_name, application_version, callback_class)

    num_blocks = image_size / block_size

    block_index = PW.ImageSize()
    for c in range(num_blocks.c):
        block_index.c = c
        for t in range(num_blocks.t):
            block_index.t = t
            for z in range(num_blocks.z):
                block_index.z = z
                for y in range(num_blocks.y):
                    block_index.y = y
                    for x in range(num_blocks.x):
                        block_index.x = x
                        if converter.NeedCopyBlock(block_index):
                            converter.CopyBlock(data, block_index)

    adjust_color_range = True
    image_extents = PW.ImageExtents(0, 0, 0, image_size.x, image_size.y, image_size.z)
    parameters = PW.Parameters()
    # parameters.set_value('Image', 'ImageSizeInMB', 2400)
    parameters.set_value('Image', 'Info', config.mTitle)
    parameters.set_channel_name(0, 'Channel 1')
    time_infos = [datetime.today()]
    color_infos = [PW.ColorInfo() for _ in range(image_size.c)]
    # color_infos[0].set_color_table(configuration.mColor_table)

    converter.Finish(image_extents, parameters, time_infos, color_infos, adjust_color_range)

    converter.Destroy()
    print('Wrote to {}'.format(config.out_path))


def tiff_to_imaris(tiff_path, out_path: str = None):
    tif = tf.TiffFile(tiff_path)
    shape = tif.series[0].shape
    np_data = np.zeros(shape, dtype=np.uint16)

    for page in tqdm(range(shape[0]), desc='reading'):
        np_data[page, :, :] = tf.imread(tiff_path, key=page)

    dir_name = os.path.dirname(tiff_path)
    basename = os.path.basename(tiff_path)
    name, ext = os.path.splitext(basename)

    if out_path is None:
        out_path = dir_name
    if not os.path.exists(out_path):
        os.makedirs(out_path)

    out_path = os.path.join(out_path, name + '.ims')

    configurations = set_configuration(id=0,
                                       title='test',
                                       np_type=np_data.dtype,
                                       imaris_type=str(np_data.dtype),
                                       out_path=out_path)

    write_data_to_ims(data=np_data, config=configurations)


def numpy_to_imaris(np_data: np.ndarray, out_path: str):
    shape = np_data.shape

    if out_path.endswith('.ims') and os.path.exists(os.path.dirname(out_path)):

        configurations = set_configuration(id=0,
                                           title='test',
                                           np_type=np_data.dtype,
                                           imaris_type=str(np_data.dtype),
                                           out_path=out_path)

        write_data_to_ims(data=np_data, config=configurations)
    else:
        exit(0x001)


def main_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=str, help='path to tiff file')
    parser.add_argument('--out', '-o', type=str, help='', default=None)
    args = parser.parse_args()
    tiff_to_imaris(tiff_path=args.file, out_path=args.out)


if __name__ == "__main__":
    main_cli()
