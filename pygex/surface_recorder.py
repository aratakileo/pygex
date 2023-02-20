try:
    from cv2 import VideoWriter_fourcc as cv_get_fourcc, VideoWriter as cv_new_video_writer, rotate as cv_rotate
    from cv2 import flip as cv_flip, ROTATE_90_CLOCKWISE, COLOR_RGB2BGR as COLORSPACE_RGB2BGR
    from pygame.surfarray import pixels3d as np_to_pixels3d_array
    from pygame.display import get_caption as pg_win_get_caption
    from cv2 import cvtColor as cv_set_colorspace
    from pygame.surface import SurfaceType
    from os import makedirs, rename
    from datetime import datetime
    from typing import Sequence
    from os.path import isdir
    from time import time

    _TEMP_FILE_NAME = '#pygex.temp.avi.resource#.avi'


    class SurfaceRecorder:
        def __init__(self, video_size: Sequence[int], video_fps: float | int):
            self._is_recording = False
            self._video_resource = None
            self._fourcc = cv_get_fourcc(*'XVID')
            self._video_fps = float(video_fps)
            self._video_size = video_size
            self._recorded_content_frames = 0

        @property
        def is_recording(self):
            return self._is_recording

        @property
        def has_content(self):
            return self._recorded_content_frames > 0

        @property
        def recorded_content_frames(self):
            return self._recorded_content_frames

        def start_record(self):
            self._recorded_content_frames = 0
            self._is_recording = True
            self._video_resource = cv_new_video_writer(
                _TEMP_FILE_NAME,
                self._fourcc,
                self._video_fps,
                self._video_size
            )

        def process_frame(self, surface: SurfaceType):
            if not self._is_recording:
                return

            self._video_resource.write(
                cv_set_colorspace(
                    cv_flip(
                        cv_rotate(
                            np_to_pixels3d_array(surface),
                            ROTATE_90_CLOCKWISE
                        ),
                        1
                    ),
                    COLORSPACE_RGB2BGR
                )
            )

            self._recorded_content_frames += 1

        def stop_record(self):
            self._is_recording = False

        def save(self, save_directory='./screenshots'):
            self._video_resource.release()

            if not isdir(save_directory):
                makedirs(save_directory)

            file_name = 'record_' + datetime.now().strftime("%d-%m-%Y-%H-%M-%S-%f") + '_'
            file_name += pg_win_get_caption()[0].lower().replace(" ", "_") + '.avi'

            rename(_TEMP_FILE_NAME, save_directory + '/' + file_name)


    __all__ = 'SurfaceRecorder',

except ImportError:
    print('For using SurfaceRecorder needs to install cv2 module first: `pip install opencv-python`')
