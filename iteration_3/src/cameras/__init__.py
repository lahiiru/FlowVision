import sys
from from_file_camera import FromFileCamera
from web_camera import WebCamera

c = ['FromFileCamera', 'WebCamera']

if sys.platform=='linux2':
    from rpi_camera import RPiCamera
    c += ['RPiCamera']

__all__ = c