import os
import re
import argparse
import tifffile

import numpy as np
from glob import glob

try:
    from .modules import stitching
except ImportError:
    from modules import stitching
from typing import Union


def search_files(file_path, exts):
    files_ = list()
    for root, dirs, files in os.walk(file_path):
        if len(files) == 0:
            continue
        for f in files:
            fn, ext = os.path.splitext(f)
            if ext in exts: files_.append(os.path.join(root, f))

    return files_


def rc_key(row: int, col: int):
    return '{}_{}'.format(str(row).zfill(4), str(col).zfill(4))


def filename2index(file_name, style='motic', row_len=None):
    file_name = os.path.basename(file_name)
    if style.lower() in ['motic', 'cghd']:
        tags = os.path.splitext(file_name)[0].split('_')
        xy = list()
        for tag in tags:
            if (len(tag) == 4) and tag.isdigit():
                if int(tag) < 999:
                    xy.append(tag)
        x_str = xy[0]
        y_str = xy[1]
        return [int(y_str), int(x_str)]
    elif style.lower() == 'zeiss':
        line = os.path.splitext(file_name)[0].split('_')
        c = int(float(line[2]))
        r = int(float(line[1]))
        return [c, r]
    elif style.lower() == "leica dm6b":
        num = file_name.split("_")[1][1:]
        x = int(int(num) / row_len)
        y = int(int(num) % row_len)
        if x % 2 == 1:
            y = row_len - y - 1
        return [y, x]
    else:
        return None


def chip_qc_filename2index(file_name):

    file_name = os.path.basename(file_name)
    pat = re.compile(r'C\d+R\d+')
    res = pat.search(file_name).group(0)

    r = int(res[1:4])
    c = int(res[5:])
    return [c, r]


def select_row_col(src_fovs, row, col):
    st_row, end_row = map(int, row.split('_'))
    st_col, end_col = map(int, col.split('_'))

    new_rows = end_row - st_row
    new_cols = end_col - st_col

    new_src_fovs = dict()
    for k, v in src_fovs.items():
        _r, _c = map(int, k.split('_'))
        if st_row <= _r < end_row and st_col <= _c < end_col:
            new_src_fovs[f'{_r - st_row:04}_{_c - st_col:04}'] = v

    return new_src_fovs, new_rows, new_cols


def images_path2dict(
        images_path,
        stereo_data = 'cellbin',
        file_type = '',
):
    """

    Args:
        images_path:
        style:
        row_len:
        stereo_data:
        file_type:

    Returns:

    """
    if len(file_type) == 0:
        image_support = ['.jpg', '.png', '.tif', '.tiff', '.TIFF']
        fov_images = search_files(images_path, exts=image_support)
    else:
        fov_images = glob(os.path.join(images_path, file_type))

    src_fovs = dict()
    rows = cols = -1
    for it in fov_images:
        if stereo_data == "cellbin":
            col, row = filename2index(it)
        else:
            col, row = chip_qc_filename2index(it)
            if stereo_data == 't1':
                col, row = row, col

        if row > rows: rows = row
        if col > cols: cols = col

        if "dolphin" in stereo_data:
            if stereo_data == "dolphin":
                if col % 2 == 0:
                    fov = stitching.ImageBase(it, flip_ud = True)
                else:
                    fov = stitching.ImageBase(it)
            elif stereo_data == 'dolphin-2l':
                fov = stitching.ImageBase(it)
            elif stereo_data == 'dolphin-1l':
                fov = stitching.ImageBase(it, flip_ud=True)
            else:
                fov = stitching.ImageBase(it)
        else:
            fov = stitching.ImageBase(it)

        src_fovs[rc_key(row, col)] = fov

    return src_fovs, rows + 1, cols + 1


class MFWS(object):
    def __init__(self,
                 overlap: str = '0.1',
                 row_slice: str = '-1_-1',
                 col_slice: str = '-1_-1',
                 stereo_data: str = 'cellbin'):
        """
        Image stitch function
        The format of the small image is as follows：
        -------------------------
           0_0, 0_1, ... , 0_n
           1_0, 1_1, ... , 1_n
           ...
           m_0, m_1, ... , m_n
        -------------------------
        Of which, m and n denote row and col

        Args:
            image_path:

            name: image name

            process_rule:

            overlap: scope overlap

            fuse_flag: whether or not fuse image

            scope_flag: scope stitch | algorithm stitch

            down_size: down-simpling size

            row_slice: means stitch start row and end row,
                 if image has 20 rows and 20 cols, row = '0_10' express only stitch row == 0 -> row == 9,
                 same as numpy slice, and other area will not stitch

            col_slice: same as 'row'

            stereo_data:
                - V3:
                - dolphin:
                - T1:
                - cellbin:

            file_type: re lambda, like '*.A.*.tif'

            debug:

        Returns:

        Examples:
            >>>

        """
        self._overlap: str = overlap
        self._row_slice: str = row_slice
        self._col_slice: str = col_slice
        self._stereo_data: str = stereo_data.lower()
        self._image_path: str = ''

        self._rows: int = 0
        self._cols: int = 0
        self._src_fovs: dict = {}
        self.stitch = stitching.Stitching()

        self._file_type: str = ''
        self.fov_x_jitter: np.ndarray = np.array([])
        self.fov_y_jitter: np.ndarray = np.array([])
        self.fov_location: np.ndarray = np.array([])
        self.mosaic: np.ndarray = np.array([])

    def prepare_data(self, image_path: str, channel: str = ''):
        self._image_path = image_path
        self._file_type = channel
        # 构建 image_base， 通道选择
        if isinstance(self._image_path, str) and os.path.isdir(self._image_path):
            src_fovs, rows, cols = images_path2dict(
                self._image_path, stereo_data=self._stereo_data, file_type=self._file_type
            )  # , style="leica dm6b", row_len=5)

        elif isinstance(self._image_path, dict):
            src_fovs = self._image_path
            rows, cols = np.array(
                [list(map(int, k.split('_'))) for k in self._image_path.keys()]
            ).max(axis=0) + 1

        else:
            raise ImportError("Image path format error.")

        # 行列范围过滤
        if '-1' not in self._row_slice and '-1' not in self._col_slice:
            self._src_fovs, self._rows, self._cols = select_row_col(
                src_fovs, self._row_slice, self._col_slice
            )

    # 多类型拼接，主要是获取坐标
    def stitching(self, loc = None, scope_flag: bool = False):
        self.stitch.set_size(self._rows, self._cols)

        if '_' in self._overlap:
            overlap_x, overlap_y = map(float, self._overlap.split('_'))
        else:
            overlap_x = overlap_y = float(self._overlap)

        self.stitch.set_overlap([overlap_x, overlap_y])

        # 用户指定拼接坐标
        if loc is not None:
            self.stitch.fov_location = loc
        else:
            # 利用硬件参数完成拼接
            if scope_flag:
                _img = list(self._src_fovs.items())[0][1]
                shape = _img.get_image().shape
                self.stitch.hardware_stitch(self._rows, self._cols, shape, [overlap_x, overlap_y])
                self.fov_x_jitter = np.zeros_like(self.stitch.fov_location)
                self.fov_y_jitter = np.zeros_like(self.stitch.fov_location)
            else:
                # 算法拼接
                self.stitch.stitch(
                    self._src_fovs,
                    stitch_method='LS-V' if 'dolphin' in self._stereo_data else 'cd'
                )
                self.fov_x_jitter = self.stitch.xy_jitter['x']
                self.fov_y_jitter = self.stitch.xy_jitter['y']
                vv = self.stitch.jitter_diff
        self.fov_location = self.stitch.fov_location

    # 生成图
    def whole_slide_image(self, fuse_flag: bool = False, down_size: int = 1):
        self.mosaic = self.stitch.get_image(self._src_fovs, fuse_flag, down_size)


def stitch_image(
        image_path: str = '',
        overlap: str = '0.1',
        name: str = '',
        fuse_flag: bool = True,
        scope_flag: bool = False,
        down_size: int = 1,
        row_slice: str = '-1_-1',
        col_slice: str = '-1_-1',
        output_path: str = '',
        stereo_data: str = 'cellbin',
        file_type: str = '',
        debug: bool = False
) -> Union[None, np.ndarray]:

    stitcher = MFWS(overlap, row_slice, col_slice, stereo_data)
    stitcher.prepare_data(image_path, file_type)
    stitcher.stitching(scope_flag=scope_flag)
    stitcher.whole_slide_image(fuse_flag, down_size)

    image = stitcher.mosaic

    if debug and os.path.isdir(output_path):
        np.save(os.path.join(output_path, 'fov_x_jitter.npy'), stitcher.fov_x_jitter)
        np.save(os.path.join(output_path, 'fov_y_jitter.npy'), stitcher.fov_y_jitter)

    if debug and os.path.isdir(output_path):
        np.save(os.path.join(output_path, 'fov_location.npy'), stitcher.fov_location)
    #
    if os.path.isdir(output_path):
        if len(name) == 0: name = 'image'
        tifffile.imwrite(
            os.path.join(output_path, f'{name}_fov_stitched.tif'), image
        )
    else:
        return image

    # for chn in ['A', 'C', 'G', 'T']:
    #     stitcher.prepare_data('*.{}.*.tif'.format(chn))
    #     stitcher.stitching(loc=stitcher.fov_location, scope_flag=scope_flag)
    #     stitcher.whole_slide_image(fuse_flag=False, down_size=5)
    #     tifffile.imwrite(
    #         os.path.join(output_path, f'{chn}_fov_stitched.tif'), stitcher.mosaic
    #     )


def main(args, para):
    stitch_image(
        image_path = args.input,
        overlap = args.overlap,
        name = args.name,
        fuse_flag = args.fuse,
        down_size = args.down,
        scope_flag = args.scope,
        row_slice = args.row,
        col_slice = args.col,
        output_path = args.output,
        stereo_data = args.id,
        file_type = args.file_type,
        debug = args.debug
    )


def arg_parser():

    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--input", action="store", dest="input", type=str, required=True,
                        help="Tar file / Input image dir.")

    # scope overlap
    parser.add_argument("-overlap", "--overlap", action="store", dest="overlap", type=str, required=False,
                        default='0.1', help="Overlap - 0.1 or 0.1_0.1 .")

    # scope stitch or algorithm stitch
    parser.add_argument("-s", "--scope", action = "store_true", dest = "scope",
                        required = False, help = "Scope stitch.")

    # fuse
    parser.add_argument("-f", "--fuse", action = "store_true", dest = "fuse", required = False, help = "Fuse.")

    # down-sampling
    parser.add_argument("-d", "--down", action = "store", dest = "down", type = float, required = False,
                        default = 1, help = "Down-sampling.")

    # block selection
    parser.add_argument("-row", "--row", action = "store", dest = "row", type = str, required = False,
                        default = '-1_-1', help = "Image select block - row.")
    parser.add_argument("-col", "--col", action = "store", dest = "col", type = str, required = False,
                        default = '-1_-1', help = "Image select block - col.")

    parser.add_argument("-n", "--name", action="store", dest="name", type=str, required=False,
                        default = '', help="Name.")
    parser.add_argument("-o", "--output", action="store", dest="output", type=str, required=False,
                        default = '', help="Result output dir.")

    parser.add_argument("-debug", "--debug", action = "store_true", dest = "debug", required = False, help = "debug.")

    """
    interface by stereo data --
       V3: 
       dolphin:
       T1:
       cellbin:
    any case is fine. 
    """
    parser.add_argument("-id", "--id", action = "store", dest = "id", type = str, required = False,
                        default = 'cellbin', help = "Stereo data id.")
    parser.add_argument("-file_type", "--file_type", action = "store", dest = "file_type", type = str,
                        required = False, default = '', help = "File name -- such as '*.A.*.tif'.")

    parser.set_defaults(func=main)
    (para, args) = parser.parse_known_args()
    para.func(para, args)


if __name__ == "__main__":
    arg_parser()


