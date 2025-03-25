from typing import Optional
from itertools import chain
import io
import numpy as np
from h5py import *


class ExtendedFile(File):
    def __init__(
        self, file, mode='r', driver=None, libver=None, userblock_size=None, swmr=False,
        rdcc_nslots=None, rdcc_nbytes=None, rdcc_w0=None, track_order=None,
        fs_strategy=None, fs_persist=False, fs_threshold=1, fs_page_size=None,
        page_buf_size=None, min_meta_keep=0, min_raw_keep=0, locking=None,
        alignment_threshold=1, alignment_interval=1, meta_block_size=None, **kwds
    ):
        if issubclass(type(file), io.IOBase):
            file = file.name
        super().__init__(
            file, mode, driver, libver, userblock_size, swmr,
            rdcc_nslots, rdcc_nbytes, rdcc_w0, track_order, fs_strategy,
            fs_persist, fs_threshold, fs_page_size, page_buf_size, min_meta_keep,
            min_raw_keep, locking, alignment_threshold, alignment_interval, meta_block_size, **kwds
        )
    
    def __setitem__(self, name, obj):
        if isinstance(name, int):
            name = f'{name}'
        return super().__setitem__(name, obj)
    
    def __getitem__(self, name):
        if isinstance(name, int):
            name = f'{name}'
        return super().__getitem__(name)
    
    def __del__(self):
        self.close()


class ArrayFile:
    def __new__(cls, file, mode: str = 'r', mmap_mode: str = 'r'):
        if mmap_mode is None:
            return ExtendedFile(file, mode)
        else:
            if issubclass(type(file), io.IOBase):
                file = file.name
            hdf5_file = File(file, 'r')
            arrays = {}
            def collect_datasets(name, item):
                if isinstance(item, Dataset):
                    offset = item.id.get_offset()
                    if offset is None:
                        raise ValueError(f"could not get the offset of the dataset '{name}', probably not a continuous array")
                    else:
                        arrays[name] = np.memmap(file, dtype=item.dtype, shape=item.shape, order='C', mode=mmap_mode, offset=offset)
            hdf5_file.visititems(collect_datasets)
            hdf5_file.close()
            return arrays


class LoadedFile:
    def __new__(cls, file):
        if issubclass(type(file), io.IOBase):
            file = file.name
        return ExtendedFile(file, 'r')


def save(
    path: str,
    *args,
    **kwargs
):
    with ExtendedFile(path, 'w') as file:
        for name, data in chain(((f'{i}', data) for i, data in enumerate(args)), kwargs.items()):
            file.create_dataset(name, data=data)


def load(path: str, mmap_mode: Optional[str] = None):
    if mmap_mode is None:
        return LoadedFile(path)
    else:
        return ArrayFile(path, 'r', mmap_mode)