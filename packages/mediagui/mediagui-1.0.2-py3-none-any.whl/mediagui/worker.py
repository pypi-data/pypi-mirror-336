# worker.py
# Last Modified: 2025-02-07

import cv2
import os, bz2, tempfile
import numpy as np
import time, platform
from PyQt6.QtCore import QThread, pyqtSignal
import urllib.request

debug = True

class VideoConcatenationWorker(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, video_files, output_path, frames_per_video=0, output_fps=30, output_format='mp4'):
        super().__init__()
        self.video_files = video_files
        self.output_path = output_path
        self.frames_per_video = frames_per_video
        self.output_fps = output_fps
        self.output_format = output_format[1:] if output_format.startswith('.') else output_format

        self.total_frames_read = 0
        self.total_frames_wrote = 0
        self.total_frames = len(self.video_files) * self.frames_per_video
        
        # GPU capabilities detection
        self.use_gpu = False
        try:
            if platform.system() != 'Darwin' and cv2.cuda.getCudaEnabledDeviceCount():
                self.use_gpu = True
                cv2.cuda.setDevice(0)
                print(f"Using CUDA device: {cv2.cuda.getDeviceName(0)}")
        except Exception as e:
            print(f"GPU detection error: {e}")

    def sanitize_path(self, path):
        path = os.path.abspath(path)
        path = os.path.normpath(path)
        return path

    def download_and_unpack_openh264_dll(self):
        url = "http://ciscobinary.openh264.org/openh264-1.8.0-win64.dll.bz2"
        temp_dir = tempfile.mkdtemp()
        compressed_path = os.path.join(temp_dir, "openh264-1.8.0-win64.dll.bz2")
        dll_path = os.path.join(temp_dir, "openh264-1.8.0-win64.dll")

        try:
            if not os.path.exists(dll_path):
                print("Downloading OpenH264 DLL...")
                urllib.request.urlretrieve(url, compressed_path)
                print("Download complete. Unpacking...")
                
                with bz2.BZ2File(compressed_path, 'rb') as compressed_file:
                    with open(dll_path, 'wb') as dll_file:
                        dll_file.write(compressed_file.read())
                
                os.remove(compressed_path)
                print("Unpacking complete.")
            else:
                print("OpenH264 DLL already exists.")
        except Exception as e:
            print(f"Error downloading OpenH264 DLL: {e}")
            self.error.emit(str(e))
            

    def gpu_extract_frames(self, video_path, frame_indices, width, height, batch_size=10):
        frames = []
        cap = cv2.VideoCapture(str(video_path))
        if not cap.isOpened():
            raise ValueError(f"Failed to open video file: {video_path}")
        
        stream = cv2.cuda.Stream()
        gpu_resizer = cv2.cuda.createResizeFilter(
            src_size=(int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), 
                    int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))),
            dst_size=(width, height),
            interpolation=cv2.INTER_LINEAR
        )
        
        for i in range(0, len(frame_indices), batch_size):
            batch_indices = frame_indices[i:i + batch_size]
            for frame_idx in batch_indices:
                try:
                    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
                    ret, cpu_frame = cap.read()
                    if not ret:
                        print(f'Failed to read frame {frame_idx}!')
                        continue
                    
                    gpu_frame = cv2.cuda.GpuMat()
                    gpu_frame.upload(cpu_frame, stream)
                    
                    gpu_resized = cv2.cuda.GpuMat()
                    gpu_resizer.apply(gpu_frame, gpu_resized, stream)
                    
                    resized_frame = gpu_resized.download(stream)
                    frames.append(resized_frame)
                    self.total_frames_read += 1
                except Exception as e:
                    print(f"GPU frame extraction error: {e}")
        
        stream.waitForCompletion()
        cap.release()
        return frames

    def cpu_extract_frames(self, video_path, frame_indices, width, height, batch_size=10):
        frames = []
        cap = cv2.VideoCapture(str(video_path))
        
        for i in range(0, len(frame_indices), batch_size):
            batch_indices = frame_indices[i:i + batch_size]
            for frame_idx in batch_indices:
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
                ret, frame = cap.read()
                if not ret:
                    break
                
                if frame.shape[1] != width or frame.shape[0] != height:
                    frame = cv2.resize(frame, (width, height))
                
                frames.append(frame)
                self.total_frames_read += 1
                self.updateProgressBar()

        cap.release()
        return frames
    
    def updateProgressBar(self):
        stage_one = int((self.total_frames_read / self.total_frames) * 80)
        stage_two = int((self.total_frames_wrote / self.total_frames) * 20)
        self.progress.emit(stage_one + stage_two)

    def run(self):
        try:
            start_time = time.time()

            # Get width and height from the first video
            first_video = cv2.VideoCapture(self.sanitize_path(str(self.video_files[0])))
            if not first_video.isOpened():
                raise Exception(f"Failed to open video: {self.video_files[0]}")
            width = int(first_video.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(first_video.get(cv2.CAP_PROP_FRAME_HEIGHT))
            first_video.release()

            if platform.system() == 'Windows':
                self.download_and_unpack_openh264_dll()

            # Codec configuration
            if self.output_format.lower() == 'mp4':
                if platform.system() == 'Darwin':
                    fourcc = cv2.VideoWriter_fourcc(*'avc1')
                elif platform.system() == 'Windows':
                    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                else:
                    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            elif self.output_format.lower() == 'avi':
                fourcc = cv2.VideoWriter_fourcc(*'MJPG')
            else:
                raise Exception(f"Unsupported output format: {self.output_format}")

            self.out = cv2.VideoWriter(str(self.output_path), fourcc, self.output_fps, (width, height))
            if not self.out.isOpened():
                raise Exception(f"Failed to open output video: {self.output_path}")

            # Process videos
            for video_path in self.video_files:
                cap = cv2.VideoCapture(str(video_path))
                if not cap.isOpened():
                    raise Exception(f"Failed to open video: {video_path}")
                total_video_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                cap.release()

                # If the video has less frames than the desired frames per video, extract all frames
                if total_video_frames < self.frames_per_video:
                    frame_indices = list(range(total_video_frames))
                # Otherwise, extract evenly spaced frames
                else:
                    frame_indices = list(np.linspace(0, total_video_frames - 1, self.frames_per_video, dtype=int))

                # Select extract frames based on GPU availability
                extract_func = self.gpu_extract_frames if self.use_gpu else self.cpu_extract_frames
                frames = extract_func(video_path, frame_indices, width, height)

                # Write frames to output video
                for frame in frames:
                    self.out.write(frame)
                    self.total_frames_wrote += 1
                    self.updateProgressBar()
        
            end_time = time.time()
            print(f"Concatenation complete in {end_time - start_time:.2f} seconds")
        except Exception as e:
            self.error.emit(str(e))
        finally:
            try:
                self.out.release()
                self.finished.emit()
            except:
                pass
    
    def cancel(self):
        if self.out:
            self.out.release()
        if os.path.exists(self.output_path):
            os.remove(self.output_path)
        self.terminate()