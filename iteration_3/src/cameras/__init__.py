import sys
from from_video_camera import FromVideoCamera
from from_folder_camera import FromFolderCamera
from web_camera import WebCamera

c = ['FromVideoCamera', 'WebCamera', 'FromFolderCamera']

if sys.platform == 'linux2':
    from rpi_camera import RPiCamera
    c += ['RPiCamera']

__all__ = c