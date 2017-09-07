"""
    Configuration parameters
    once you pulled this file change as your configuration then exclude from git
"""
class DevConfig:
    BUILD_IN_CAM_INDEX = 1
    BUILD_IN_CAM_F = 10
    WEB_CAM_INDEX = 2
    WEB_CAM_F = 1350
    VIDEO_DIR = '../'

class ProdConfig:
    BUILD_IN_CAM_INDEX = 0
    BUILD_IN_CAM_F = 3.85
    WEB_CAM_INDEX = 1
    WEB_CAM_F = 1350