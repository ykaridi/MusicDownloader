import ctypes
import sys
from io import BytesIO

import vlc

# Adapted from https://stackoverflow.com/questions/63508739/using-python-vlc-play-buffer-example
MediaOpenCb = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_void_p, ctypes.POINTER(ctypes.c_void_p), ctypes.POINTER(ctypes.c_uint64))
MediaReadCb = ctypes.CFUNCTYPE(ctypes.c_ssize_t, ctypes.c_void_p, ctypes.POINTER(ctypes.c_char), ctypes.c_size_t)
MediaSeekCb = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_void_p, ctypes.c_uint64)
MediaCloseCb = ctypes.CFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p)


class ByteStreamWrapper:
    def __init__(self, byts: bytes):
        self.bytes = byts
        self.stream = None

    def open(self):
        self.stream = BytesIO(self.bytes)

    def close(self):
        self.stream.close()


@MediaOpenCb
def media_open_cb(opaque, data_pointer, size_pointer):
    stream_wrapper: ByteStreamWrapper = ctypes.cast(opaque, ctypes.POINTER(ctypes.py_object)).contents.value
    stream_wrapper.open()

    data_pointer.contents.value = opaque
    size_pointer.contents.value = sys.maxsize
    return 0


@MediaReadCb
def media_read_cb(opaque, buffer, length):
    stream: BytesIO = ctypes.cast(opaque, ctypes.POINTER(ctypes.py_object)).contents.value.stream
    new_data = stream.read(length)
    for i in range(len(new_data)):
        buffer[i] = new_data[i]
    return len(new_data)


@MediaSeekCb
def media_seek_cb(opaque, offset):
    stream: BytesIO = ctypes.cast(opaque, ctypes.POINTER(ctypes.py_object)).contents.value.stream
    stream.seek(offset)
    return 0


@MediaCloseCb
def media_close_cb(opaque):
    stream_wrapper: ByteStreamWrapper = ctypes.cast(opaque, ctypes.POINTER(ctypes.py_object)).contents.value
    stream_wrapper.close()


def media_from_mp4_bytes(*songs: bytes) -> vlc.MediaListPlayer:
    instance: vlc.Instance = vlc.Instance()
    player: vlc.MediaListPlayer = instance.media_list_player_new()

    media_list: vlc.MediaList = instance.media_list_new()
    for song in songs[::-1]:
        bytes_io = ByteStreamWrapper(song)
        media = instance.media_new_callbacks(
            media_open_cb,
            media_read_cb,
            media_seek_cb,
            media_close_cb,
            ctypes.cast(ctypes.pointer(ctypes.py_object(bytes_io)), ctypes.c_void_p)
        )
        media_list.insert_media(media, 0)

    player.set_media_list(media_list)
    return player
