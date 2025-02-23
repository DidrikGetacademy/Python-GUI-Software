import sys
from functools  import cache
from time       import sleep
from webbrowser import open as open_browser
from subprocess import run  as subprocess_run
from shutil     import rmtree as remove_directory
from timeit     import default_timer as timer
from PIL import Image, ImageTk, ImageSequence
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
import cv2
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Logger import logging
from typing    import Callable
from threading import Thread
from itertools import repeat
from concurrent.futures import ThreadPoolExecutor
from multiprocessing.pool import ThreadPool
import yt_dlp
import time
from PIL import Image, ImageDraw, ImageFont  # Add these imports at the top
from multiprocessing import ( 
    Process, 
    Queue          as multiprocessing_Queue,
    freeze_support as multiprocessing_freeze_support
)

from json import (
    load  as json_load, 
    dumps as json_dumps
)

import logging

logging.basicConfig(level=logging.INFO)
logging.info("LearnReflectAI.py started.")

from os import (
    sep        as os_separator,
    devnull    as os_devnull,
    environ    as os_environ,
    cpu_count  as os_cpu_count,
    makedirs   as os_makedirs,
    listdir    as os_listdir,
    remove     as os_remove
)

from os.path import (
    basename   as os_path_basename,
    dirname    as os_path_dirname,
    abspath    as os_path_abspath,
    join       as os_path_join,
    exists     as os_path_exists,
    splitext   as os_path_splitext,
    expanduser as os_path_expanduser
)

# Third-party library imports
from natsort          import natsorted
from moviepy.video.io import ImageSequenceClip 
from onnxruntime      import InferenceSession as onnxruntime_inferenceSession

from PIL.Image import (
    open      as pillow_image_open,
    fromarray as pillow_image_fromarray
)

from cv2 import (
    CAP_PROP_FPS,
    CAP_PROP_FRAME_COUNT,
    CAP_PROP_FRAME_HEIGHT,
    CAP_PROP_FRAME_WIDTH,
    COLOR_BGR2RGB,
    COLOR_GRAY2RGB,
    COLOR_BGR2RGBA,
    COLOR_RGB2GRAY,
    IMREAD_UNCHANGED,
    INTER_LINEAR,
    INTER_AREA,
    INTER_CUBIC,
    VideoCapture as opencv_VideoCapture,
    cvtColor     as opencv_cvtColor,
    imdecode     as opencv_imdecode,
    imencode     as opencv_imencode,
    addWeighted  as opencv_addWeighted,
    cvtColor     as opencv_cvtColor,
    resize       as opencv_resize,
)
import numpy as np
from numpy import (
    ndarray     as numpy_ndarray,
    frombuffer  as numpy_frombuffer,
    concatenate as numpy_concatenate, 
    transpose   as numpy_transpose,
    full        as numpy_full, 
    zeros       as numpy_zeros, 
    expand_dims as numpy_expand_dims,
    squeeze     as numpy_squeeze,
    clip        as numpy_clip,
    mean        as numpy_mean,
    repeat      as numpy_repeat,
    max         as numpy_max, 
    float32,
    uint8
)

# GUI imports
from tkinter import StringVar, DISABLED, NORMAL
from customtkinter import (
    CTk,
    CTkButton,
    CTkFrame,
    CTkEntry,
    CTkFont,
    CTkImage,
    CTkLabel,
    CTkOptionMenu,
    CTkScrollableFrame,
    CTkToplevel,
    filedialog,
    set_appearance_mode,
    set_default_color_theme
)

import os


if sys.stdout is None: sys.stdout = open(os_devnull, "w")
if sys.stderr is None: sys.stderr = open(os_devnull, "w")

def find_by_relative_path(relative_path: str) -> str:
    base_path = getattr(sys, '_MEIPASS', os_path_dirname(os_path_abspath(__file__)))
    return os_path_join(base_path, relative_path)


app_name   = "LearnReflect AI"
app_name_color = "#F0F8FF"
dark_color     = "#080808"
background_color        = "#000000"
text_color              = "#B8B8B8"
widget_background_color = "#181818"
very_low_VRAM  = 4
low_VRAM       = 3
medium_VRAM    = 2.2
very_high_VRAM = 0.6

AI_LIST_SEPARATOR           = [ "----" ]
IRCNN_models_list           = [ "IRCNN_Mx1", "IRCNN_Lx1" ]
SRVGGNetCompact_models_list = [ "RealESR_Gx4", "RealSRx4_Anime" ]
RRDB_models_list            = [ "BSRGANx4", "BSRGANx2", "RealESRGANx4" ]

#Video Preview
video_cache = {}
frame_cache = {}
preview_ai_instance = None
last_model_config = None
preview_executor = ThreadPoolExecutor(max_workers=1)
global preview_shown
global original_preview
global upscaled_preview
current_loaded_model = None
model_loading_thread = None
model_loading_lock = threading.Lock()

AI_models_list         = ( SRVGGNetCompact_models_list + AI_LIST_SEPARATOR + RRDB_models_list + AI_LIST_SEPARATOR + IRCNN_models_list )
gpus_list              = ["Auto", "GPU 1", "GPU 2", "GPU 3", "GPU 4" ]
keep_frames_list       = [ "Disabled", "Enabled" ]
image_extension_list   = [ ".png", ".jpg", ".bmp", ".tiff" ]
video_extension_list   = [ ".mp4 (x264)", ".mp4 (x265)", ".avi" ]
interpolation_list     = [ "Low", "Medium", "High", "Disabled" ]
audio_mode_list        = ["Disabled", "Audio Enchancement", "Vocal Isolation"] 
AI_multithreading_list = [ "1 threads", "2 threads", "3 threads", "4 threads", "5 threads", "6 threads"]
OUTPUT_PATH_CODED    = "Same path as input files"
DOCUMENT_PATH        = os_path_join(os_path_expanduser('~'), 'Documents')
USER_PREFERENCE_PATH = find_by_relative_path(f"{DOCUMENT_PATH}{os_separator}{app_name}_UserPreference.json")
FFMPEG_EXE_PATH      = find_by_relative_path(f"Assets{os_separator}ffmpeg.exe")
os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "video_codec;h264_cuvid"

EXIFTOOL_EXE_PATH    = find_by_relative_path(f"Assets{os_separator}exiftool.exe")
FRAMES_FOR_CPU       = 30


if os_path_exists(FFMPEG_EXE_PATH): 
    print(f"[{app_name}] External ffmpeg.exe file found")
    os_environ["IMAGEIO_FFMPEG_EXE"] = FFMPEG_EXE_PATH

if os_path_exists(USER_PREFERENCE_PATH):
    print(f"[{app_name}] Preference file exist")
    with open(USER_PREFERENCE_PATH, "r") as json_file:
        json_data = json_load(json_file)
        default_AI_model          = json_data["default_AI_model"]
        default_AI_multithreading = json_data["default_AI_multithreading"]
        default_gpu               = json_data.get("default_gpu", gpus_list[0])
        default_image_extension   = json_data["default_image_extension"]
        default_video_extension   = json_data["default_video_extension"]
        default_interpolation     = json_data["default_interpolation"]
        default_keep_frames       = json_data.get("default_keep_frames",        keep_frames_list[0])
        default_audio_mode        = json_data.get("default_audio_mode",audio_mode_list[0]) 
        default_output_path       = json_data["default_output_path"]
        default_resize_factor     = json_data["default_resize_factor"]
        default_VRAM_limiter      = json_data["default_VRAM_limiter"]
        default_cpu_number        = json_data["default_cpu_number"]
else:
    print(f"[{app_name}] Preference file does not exist, using default coded value")
    default_AI_model          = AI_models_list[0]
    default_AI_multithreading = AI_multithreading_list[0]
    default_gpu               = gpus_list[0]
    default_keep_frames       = keep_frames_list[0]
    default_image_extension   = image_extension_list[0]
    default_video_extension   = video_extension_list[0]
    default_interpolation     = interpolation_list[0]
    default_audio_mode        = audio_mode_list[0] 
    default_output_path       = OUTPUT_PATH_CODED
    default_resize_factor     = str(50)
    default_VRAM_limiter      = str(4)
    default_cpu_number        = str(int(os_cpu_count()/2))

COMPLETED_STATUS = "Completed"
ERROR_STATUS     = "Error"
STOP_STATUS      = "Stop"

offset_y_options = 0.105
row0_y = 0.52
row1_y = row0_y + offset_y_options
row2_y = row1_y + offset_y_options
row3_y = row2_y + offset_y_options
row4_y = row3_y + offset_y_options
row5_y = row4_y + offset_y_options



offset_x_options = 0.28
column1_x = 0.5
column0_x = column1_x - offset_x_options
column2_x = column1_x + offset_x_options
column1_5_x = column1_x + offset_x_options/2
column_info1  = 0.625
column_1_5    = column_info1 + 0.08
column_1_4    = column_1_5 - 0.0127
column_info2  = 0.858
column_3      = column_info2 + 0.08


little_textbox_width = 74
little_menu_width = 98

supported_file_extensions = [
    '.heic', '.jpg', '.jpeg', '.JPG', '.JPEG', '.png',
    '.PNG', '.webp', '.WEBP', '.bmp', '.BMP', '.tif',
    '.tiff', '.TIF', '.TIFF', '.mp4', '.MP4', '.webm',
    '.WEBM', '.mkv', '.MKV', '.flv', '.FLV', '.gif',
    '.GIF', '.m4v', ',M4V', '.avi', '.AVI', '.mov',
    '.MOV', '.qt', '.3gp', '.mpg', '.mpeg', ".vob"
]

supported_video_extensions = [
    '.mp4', '.MP4', '.webm', '.WEBM', '.mkv', '.MKV',
    '.flv', '.FLV', '.gif', '.GIF', '.m4v', ',M4V',
    '.avi', '.AVI', '.mov', '.MOV', '.qt', '.3gp',
    '.mpg', '.mpeg', ".vob"
]




    

def show_preview_if_files_selected():
    global selected_file_list
 
    if not selected_file_list:
        show_error_message("Select files first!")
        return
    print(f"selected file list: {selected_file_list[0]}")
    async_preview(selected_file_list[0])






def async_preview(video_path):
    if current_loaded_model != selected_AI_model.get():
        show_error_message("Model not loaded yet")
        return
    if video_path not in frame_cache:
        cap = cv2.VideoCapture(video_path)
        _, frame = cap.read()
        frame_cache[video_path] = frame 
    future = preview_executor.submit(process_and_show_preview, frame_cache[video_path])
    future.add_done_callback(lambda f: update_ui(f.result()))



def update_ui(result):
    print("READY (UPDATE_UI)")
    pass



def check_if_file_is_image(file_path: str) -> bool:
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp']
    return any(file_path.lower().endswith(ext) for ext in image_extensions)


class LoadingIcon:
    def __init__(self,master):
        self.master = master
        self.loading_gif = Image.open(find_by_relative_path("Assets" + os_separator + "Loading.gif"))
        self.frames = [CTkImage(frame.convert('RGBA'), size=(100, 100)) 
               for frame in ImageSequence.Iterator(self.loading_gif)]

        self.label = CTkLabel(master,text="", image=self.frames[0])
        self.label.place(relx=0.5, rely=0.5, anchor="center")
        self.current_frame = 0
        self.animating = False

    def start(self):
        self.animating = True
        print("Started animate")
        self.animate()

    def stop(self):
        self.animating = False 
        self.label.destroy()
    
    def animate(self):
        if self.animating:
            self.label.configure(image=self.frames[self.current_frame])
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.master.after(50,self.animate)





def process_and_show_preview(video_path, loading_icon):
    global preview_ai_instance, last_model_config

    if not selected_AI_model or selected_AI_model == AI_LIST_SEPARATOR[0]:
        show_error_message("Select an AI model first!")
        return

    try:
        current_config = (
            selected_AI_model,
            selected_gpu,
            int(float(selected_input_resize_factor.get())),
            float(selected_VRAM_limiter.get())
        )

        if not preview_ai_instance or last_model_config != current_config:
            resize_factor = int(float(selected_input_resize_factor.get()))
            vram_limiter = float(selected_VRAM_limiter.get())
            
        tiles_resolution = 100 * int(float(str(selected_VRAM_limiter.get())))
        if tiles_resolution > 0: 
            vram_multiplier = very_low_VRAM

            max_resolution = int(vram_multiplier * vram_limiter * 100)
            
            preview_ai_instance = AI(
                selected_AI_model,
                selected_gpu,
                resize_factor,
                max_resolution
            )
            preview_ai_instance.inferenceSession.set_providers(
                ['DmlExecutionProvider'], 
                [{'device_id': 0}]
            )

     
            dummy_input = np.zeros((512, 512, 3), dtype=np.uint8)
            _ = preview_ai_instance.AI_orchestration(dummy_input)
            last_model_config = current_config

            if check_if_file_is_image(video_path):
                frame =cv2.imread(video_path)
                if frame is None:
                    raise ValueError("Could not read image..")
                
                frame = cv2.resize(frame, (512, 512), interpolation=cv2.INTER_AREA)
            else:
               cap = video_cache.get(video_path)
               if not cap:
                    cap = cv2.VideoCapture(video_path)
                    video_cache[video_path] = cap
               if not os.path.exists(video_path):
                  raise ValueError(f"File not found: {video_path}")
               
               cap = cv2.VideoCapture(video_path)
               if not cap.isOpened():
                    error_code = cap.get(cv2.CAP_PROP_POS_MSEC)
                    raise ValueError(f"OpenCV error {int(error_code)}: Could not open video file")
               
               success, frame = cap.read()
               if not success:
                   raise ValueError("Frame read failed.")
               
               frame = cv2.resize(frame, (960, 540), interpolation=cv2.INTER_AREA)


   
            start_time = time.perf_counter()
            upscaled_frame = preview_ai_instance.AI_orchestration(frame)
            processing_time = time.perf_counter() - start_time

    
            original_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            upscaled_rgb = cv2.cvtColor(upscaled_frame, cv2.COLOR_BGR2RGB)

            print(f"Preview processed in {processing_time:.2f}s")

            window.after(0, lambda: show_preview_frames(
                original_rgb,
                upscaled_rgb,
                loading_icon
            ))

    except Exception as e:
        print(f"Preview error: {str(e)}")
        loading_icon.stop()
        window.after(0, lambda: info_message.set(f"Preview failed: {str(e)}"))  # Update this line
        info_message.set("Preview failed")





def show_preview_frames(original, upscaled, loading_icon):
    global original_preview, upscaled_preview, preview_shown
    loading_icon.stop()


    for widget in window.preview_frame.winfo_children():
        widget.destroy()

    container_width = 800  
    container_height = 445  
    target_width = int(container_width / 2 - 40)  
    target_height = int(container_height - 60)   


    def resize_image(image, target_w, target_h):
        h, w = image.shape[:2]
        scale = min(target_w/w, target_h/h)
        return cv2.resize(image, (int(w*scale), int(h*scale)), interpolation=cv2.INTER_AREA)

    original = resize_image(original, target_width, target_height)
    original_rgb = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)
    original_pil = Image.fromarray(original_rgb)
    

    upscaled = resize_image(upscaled, target_width, target_height)
    upscaled_rgb = cv2.cvtColor(upscaled, cv2.COLOR_BGR2RGB)
    upscaled_pil = Image.fromarray(upscaled_rgb)

    original_image = CTkImage(original_pil, size=original_pil.size)
    upscaled_image = CTkImage(upscaled_pil, size=upscaled_pil.size)


    container = CTkFrame(window.preview_frame, fg_color=dark_color)
    container.pack(pady=20, padx=20, fill='both', expand=True)


    original_frame = CTkFrame(container, fg_color=dark_color)
    original_frame.pack(side='left', fill='both', expand=True, padx=10)
    CTkLabel(original_frame, text="Original", font=bold14, text_color=app_name_color).pack(pady=5)
    original_preview = CTkLabel(original_frame, image=original_image, text="")
    original_preview.pack()


    upscaled_frame = CTkFrame(container, fg_color=dark_color)
    upscaled_frame.pack(side='right', fill='both', expand=True, padx=10)
    CTkLabel(upscaled_frame, text="Upscaled Preview", font=bold14, text_color=app_name_color).pack(pady=5)
    upscaled_preview = CTkLabel(upscaled_frame, image=upscaled_image, text="")
    upscaled_preview.pack()

    preview_shown = True
    info_message.set("Preview Ready!")






# AI -------------------
class AI:
    # CLASS INIT FUNCTIONS
    def __init__(
            self, 
            AI_model_name: str, 
            directml_gpu: str, 
            input_resize_factor: int,
            max_resolution: int,
            audio_model_type: str = None 
            ):
        
        # Passed variables
        self.AI_model_name  = AI_model_name
        self.directml_gpu   = directml_gpu
        self.input_resize_factor  = input_resize_factor
        self.max_resolution = max_resolution

        # Calculated variables
        self.AI_model_path    = find_by_relative_path(f"AI-onnx{os_separator}{self.AI_model_name}_fp16.onnx")
        self.Audio_model_path = None
        self.inferenceSession = self._load_inferenceSession()
        self.upscale_factor   = self._get_upscale_factor()
        
        if audio_model_type:
           self.Audio_model_path = find_by_relative_path(f"AI-onnx{os_separator}{self.getAudioModelName(audio_model_type)}UNet.onnx")
           self.Audio_inferenceSession = self._load_Audio_inferencesession()
        else: 
            self.Audio_model_path = None
        
    def _get_upscale_factor(self) -> int:
        if   "x1" in self.AI_model_name: return 1
        elif "x2" in self.AI_model_name: return 2
        elif "x4" in self.AI_model_name: return 4
        
        
    

    def _load_inferenceSession(self) -> onnxruntime_inferenceSession:     
        import onnxruntime
        providers = ['CPUExecutionProvider']

        if 'DmlExecutionProvider' in onnxruntime.get_available_providers():
            match self.directml_gpu:
                case 'Auto':
                    #lets ort choose the best model.
                    providers = [('DmlExecutionProvider', {})] + providers
                case 'GPU 1' | 'GPU 2' | 'GPU 3' | 'GPU 4':
                    device_id = int(self.directml_gpu.split()[-1]) - 1
                    providers = [
                        ('DmlExecutionProvider', {'device_id': device_id}),
                        'CPUExecutionProvider'
                    ]
                case 'CPU':
                    providers = ['CPUExecutionProvider']

        session_options = onnxruntime.SessionOptions()
        session_options.graph_optimization_level = onnxruntime.GraphOptimizationLevel.ORT_ENABLE_ALL
        session_options.execution_mode = onnxruntime.ExecutionMode.ORT_PARALLEL
        try:
            inference_session = onnxruntime_inferenceSession(
                path_or_bytes=self.AI_model_path,
                providers=providers,
                sess_options=session_options
            )
        except Exception as e:
                print(f"Session creation failed: {str(e)}")

                #fallback to CPU if GPU fails
                inference_session = onnxruntime_inferenceSession(
                    path_or_bytes=self.AI_model_path,
                    providers=['CPUExecutionProvider']
                )
        print(f"Using providers: {inference_session.get_providers()}")
        if 'DmlExecutionProvider' in inference_session.get_providers():
            options = inference_session.get_provider_options()['DmlExecutionProvider']
            print(f"DirectML device ID: {options.get('device_id', 'default')}")

        return inference_session




    def getAudioModelName(self, model_type: str)-> str:
        if model_type == "Vocal_Isolation_":
            return "Vocal_Isolation_"
        elif model_type == "Audio_enchancement_":
            return  "Audio_enchancement_"
        else: 
            raise ValueError(f"Uknown model_type: {model_type}")
    
    
    
    def Run_Audio_inference(self, model_type: str, Model_audio_input_path: str) -> str:
        self.Audio_model_path = find_by_relative_path(f"AI-onnx{os_separator}{self.getAudioModelName(model_type)}UNet.onnx")

        if model_type == "Vocal_Isolation_":
           self.Audio_inferenceSession = self._load_Audio_inferencesession()
           return self.run_vocal_isolation(Model_audio_input_path)
           
        elif model_type == "Audio_enchancement_":
           self.Audio_inferenceSession = self._load_Audio_inferencesession()
           return self.run_Audio_Enchancement(Model_audio_input_path)
        else:
            raise ValueError(F"Uknown model_type: {model_type}")
   
        
        

    def _load_Audio_inferencesession(self) -> onnxruntime_inferenceSession:  
        match self.directml_gpu:
           case 'GPU 1': directml_backend = [('DmlExecutionProvider', {"device_id": "0"})]
           case 'GPU 2': directml_backend = [('DmlExecutionProvider', {"device_id": "1"})]
           case 'GPU 3': directml_backend = [('DmlExecutionProvider', {"device_id": "2"})]
           case 'GPU 4': directml_backend = [('DmlExecutionProvider', {"device_id": "3"})]
           case 'CPU': directml_backend = [('DmlExecutionProvider')]
        inference_Session_Audio = onnxruntime_inferenceSession(path_or_bytes=self.Audio_model_path,providers=directml_backend)
        return inference_Session_Audio
    
    
    
    

    def extract_audio_from_video(self, video_path: str) -> str:
        video_dir = os.path.dirname(video_path)
        audio_output_path = os.path.join(video_dir, "extracted_audio.wav")
        command = ["ffmpeg",  "-y", "-i", video_path, "-q:a", "0", "-map", "0:a", audio_output_path]
        subprocess_run(command, check=True)
        print(f"Returning audio_output_path for extracted audio at: {audio_output_path}")
        return audio_output_path #Returns the extracted audio from video_path in wav format 
    
    
  
    def run_vocal_isolation(self, Model_audio_input_path: str) -> str:
        from scipy.io.wavfile import write, read
        sample_rate, audio_data = read(Model_audio_input_path)
        if len(audio_data.shape) > 1:
            audio_data = np.mean(audio_data, axis=1)
        audio_data = (audio_data.astype(np.float32) / 32767.0) 
        target_height = 513
        target_width = 10000
        audio_flattened = audio_data.flatten()
        audio_padded = np.zeros((target_height, target_width), dtype=np.float32)
        num_samples = min(audio_flattened.size, target_height * target_width)
        audio_padded.flat[:num_samples] = audio_flattened[:num_samples]
        audio_input = np.expand_dims(audio_padded, axis=0)
        audio_input = np.expand_dims(audio_input,axis=1)
        input_name = self.Audio_inferenceSession.get_inputs()[0].name
        output_name = self.Audio_inferenceSession.get_outputs()[0].name
        isolated_audio = self.Audio_inferenceSession.run([output_name], {input_name: audio_input})[0]
        isolated_audio = np.squeeze(isolated_audio) 
        isolated_audio = (isolated_audio * 32767).astype(np.int32) 
        isolated_output_path = Model_audio_input_path.replace("extracted_audio", "isolated_audio")
        write(isolated_output_path,sample_rate,isolated_audio)
        print(f"isolated audio saved at {isolated_output_path}")
        return isolated_output_path
    
    
    
    def run_Audio_Enchancement(self, Model_audio_input_path: str) -> str:
        Enchanced_output_path = Model_audio_input_path.replace("extracted_audio", "enhanced_audio")
        return Enchanced_output_path
        
        



        
    #Returns AI onnx model that will be run else Stops process (EXPECTS A PARAMETER WITH THE SELECTED AUDIO MODE FROM GUI)
    def Return_AI_Audio_model_name(self, selected_audio_mode: str) -> str: 
        global Audio_model_name
        print(f"Selected Audio Mode before proccessing audio: {selected_audio_mode}")
        if selected_audio_mode == "Vocal Isolation":
               Audio_model_name = "Vocal_Isolation_"
               print(f"selected is vocal isolation, Audio_model_name: {Audio_model_name}")
               return Audio_model_name
        elif selected_audio_mode == "Audio Enchancement":
                Audio_model_name = "Audio_enchancement_"
                print(f"selected is Audio Enchncement:  Audio_model_name: {Audio_model_name}")
                return Audio_model_name
        elif selected_audio_mode == "Disabled":
             print("Audio Mode Disabled")
             return None
       
       
         
         
    #Returns the upscaled audio
    def process_Audio_Inference(self,video_path: str, selected_audio_mode: str) -> str:
        if selected_audio_mode == "Disabled":
            print("Audio inference is disabled. Skipping audio processing...")
            return None
        

        print(f"Selected audio mode before model_type: {selected_audio_mode}")
        Model_type = self.Return_AI_Audio_model_name(selected_audio_mode)
        print(f"Model_type returned: {Model_type}")
        if Model_type is None:
            print("No valid model selected for  audio inference. skipping...")
            return None
        
        #Extracts the audio from video
        extracted_audio_path = self.extract_audio_from_video(video_path)
        
        #Running Audio Inference
        print(f"Running audio inference with the extracted audio: {extracted_audio_path}")
        Audio_Inference_output = self.Run_Audio_inference(Model_type, extracted_audio_path) 

        #Remove extracted Audio
        print(f"Audio Inference Successfully finished.")
        if os.path.exists(extracted_audio_path):
            print(f"Removing extracted audio at: {extracted_audio_path}")
            os.remove(extracted_audio_path)
            
        print(f"Returning Enchanced audio at: {Audio_Inference_output}")
        if Audio_Inference_output != None:
            return Audio_Inference_output
        else:
            return None

    
          

    
    
    #INTERNAL CLASS FUNCTIONS
    def get_image_mode(self, image: numpy_ndarray) -> str:
        match image.shape:
            case (rows, cols):
                return "Grayscale"
            case (rows, cols, channels) if channels == 3:
                return "RGB"
            case (rows, cols, channels) if channels == 4:
                return "RGBA"

    def get_image_resolution(self, image: numpy_ndarray) -> tuple:
        height = image.shape[0]
        width  = image.shape[1]

        return height, width 

    def calculate_target_resolution(self, image: numpy_ndarray) -> tuple:
        height, width = self.get_image_resolution(image)
        target_height = height * self.upscale_factor
        target_width  = width  * self.upscale_factor

        return target_height, target_width

    def resize_with_input_factor(self, image: numpy_ndarray) -> numpy_ndarray:
        
        old_height, old_width = self.get_image_resolution(image)

        new_width  = int(old_width * self.input_resize_factor)
        new_height = int(old_height * self.input_resize_factor)

        match self.input_resize_factor:
            case factor if factor > 1:
                return opencv_resize(image, (new_width, new_height), interpolation = INTER_CUBIC)
            case factor if factor < 1:
                return opencv_resize(image, (new_width, new_height), interpolation = INTER_AREA)
            case _:
                return image
            


    def resize_image_with_target_resolution(
            self,
            image: numpy_ndarray, 
            t_height: int,
            t_width: int
            ) -> numpy_ndarray:
        
        old_height, old_width = self.get_image_resolution(image)
        old_resolution = old_height + old_width
        new_resolution = t_height + t_width

        if new_resolution > old_resolution:
            return opencv_resize(image, (t_width, t_height), interpolation = INTER_LINEAR)
        else:
            return opencv_resize(image, (t_width, t_height), interpolation = INTER_AREA) 







 # VIDEO CLASS FUNCTIONS
    def calculate_multiframes_supported_by_gpu(self, video_frame_path: str) -> int:
        resized_video_frame  = self.resize_with_input_factor(image_read(video_frame_path))
        height, width        = self.get_image_resolution(resized_video_frame)
        image_pixels         = height * width
        max_supported_pixels = self.max_resolution * self.max_resolution

        frames_simultaneously = max_supported_pixels // image_pixels 

        print(f" Frames supported simultaneously by GPU: {frames_simultaneously}")

        return frames_simultaneously







    # TILLING FUNCTIONS
    def video_need_tilling(self, video_frame_path: str) -> bool:       
        resized_video_frame  = self.resize_with_input_factor(image_read(video_frame_path))
        height, width        = self.get_image_resolution(resized_video_frame)
        image_pixels         = height * width
        max_supported_pixels = self.max_resolution * self.max_resolution

        if image_pixels > max_supported_pixels:
            return True
        else:
            return False

    def image_need_tilling(self, image: numpy_ndarray) -> bool:
        height, width = self.get_image_resolution(image)
        image_pixels  = height * width
        max_supported_pixels = self.max_resolution * self.max_resolution

        if image_pixels > max_supported_pixels:
            return True
        else:
            return False

    def add_alpha_channel(self, image: numpy_ndarray) -> numpy_ndarray:
        if image.shape[2] == 3:
            alpha = numpy_full((image.shape[0], image.shape[1], 1), 255, dtype = uint8)
            image = numpy_concatenate((image, alpha), axis = 2)
        return image

    def calculate_tiles_number(
            self, 
            image: numpy_ndarray, 
            ) -> tuple:
        
        height, width = self.get_image_resolution(image)

        tiles_x = (width  + self.max_resolution - 1) // self.max_resolution
        tiles_y = (height + self.max_resolution - 1) // self.max_resolution

        return tiles_x, tiles_y
    
    def split_image_into_tiles(
            self,
            image: numpy_ndarray, 
            tiles_x: int, 
            tiles_y: int
            ) -> list[numpy_ndarray]:

        img_height, img_width = self.get_image_resolution(image)

        tile_width  = img_width // tiles_x
        tile_height = img_height // tiles_y

        tiles = []

        for y in range(tiles_y):
            y_start = y * tile_height
            y_end   = (y + 1) * tile_height

            for x in range(tiles_x):
                x_start = x * tile_width
                x_end   = (x + 1) * tile_width
                tile    = image[y_start:y_end, x_start:x_end]
                tiles.append(tile)

        return tiles

    def combine_tiles_into_image(
            self,
            image: numpy_ndarray,
            tiles: list[numpy_ndarray], 
            t_height: int, 
            t_width: int,
            num_tiles_x: int, 
            ) -> numpy_ndarray:

        match self.get_image_mode(image):
            case "Grayscale": tiled_image = numpy_zeros((t_height, t_width, 3), dtype = uint8)
            case "RGB":       tiled_image = numpy_zeros((t_height, t_width, 3), dtype = uint8)
            case "RGBA":      tiled_image = numpy_zeros((t_height, t_width, 4), dtype = uint8)

        for tile_index in range(len(tiles)):
            actual_tile = tiles[tile_index]

            tile_height, tile_width = self.get_image_resolution(actual_tile)

            row     = tile_index // num_tiles_x
            col     = tile_index % num_tiles_x
            y_start = row * tile_height
            y_end   = y_start + tile_height
            x_start = col * tile_width
            x_end   = x_start + tile_width

            match self.get_image_mode(image):
                case "Grayscale": tiled_image[y_start:y_end, x_start:x_end] = actual_tile
                case "RGB":       tiled_image[y_start:y_end, x_start:x_end] = actual_tile
                case "RGBA":      tiled_image[y_start:y_end, x_start:x_end] = self.add_alpha_channel(actual_tile)

        return tiled_image

    





    # AI CLASS FUNCTIONS
    def normalize_image(self, image: numpy_ndarray) -> tuple:
        range = 255
        if numpy_max(image) > 256: range = 65535
        normalized_image = image / range

        return normalized_image, range
    
    
    
    def preprocess_image(self, image: numpy_ndarray) -> numpy_ndarray:
        image = numpy_transpose(image, (2, 0, 1))
        image = numpy_expand_dims(image, axis=0)

        return image



    def onnxruntime_inference(self, image: numpy_ndarray) -> numpy_ndarray:

        # IO BINDING
        
        # io_binding = self.inferenceSession.io_binding()
        # io_binding.bind_cpu_input(self.inferenceSession.get_inputs()[0].name, image)
        # io_binding.bind_output(self.inferenceSession.get_outputs()[0].name, element_type = float32)
        # self.inferenceSession.run_with_iobinding(io_binding)
        # onnx_output = io_binding.copy_outputs_to_cpu()[0]

        onnx_input  = {self.inferenceSession.get_inputs()[0].name: image}
        onnx_output = self.inferenceSession.run(None, onnx_input)[0]

        return onnx_output



    def postprocess_output(self, onnx_output: numpy_ndarray) -> numpy_ndarray:
        onnx_output = numpy_squeeze(onnx_output, axis=0)
        onnx_output = numpy_clip(onnx_output, 0, 1)
        onnx_output = numpy_transpose(onnx_output, (1, 2, 0))

        return onnx_output.astype(float32)



    def de_normalize_image(self, onnx_output: numpy_ndarray, max_range: int) -> numpy_ndarray:    
        match max_range:
            case 255:   return (onnx_output * max_range).astype(uint8)
            case 65535: return (onnx_output * max_range).round().astype(float32)




    def AI_upscale(self, image: numpy_ndarray) -> numpy_ndarray:
        image_mode   = self.get_image_mode(image)
        image, range = self.normalize_image(image)
        image        = image.astype(float32)

        match image_mode:
            case "RGB":
                image = self.preprocess_image(image)
                onnx_output  = self.onnxruntime_inference(image)
                onnx_output  = self.postprocess_output(onnx_output)
                output_image = self.de_normalize_image(onnx_output, range)

                return output_image
            
            case "RGBA":
                alpha = image[:, :, 3]
                image = image[:, :, :3]
                image = opencv_cvtColor(image, COLOR_BGR2RGB)

                image = image.astype(float32)
                alpha = alpha.astype(float32)

                # Image
                image = self.preprocess_image(image)
                onnx_output_image = self.onnxruntime_inference(image)
                onnx_output_image = self.postprocess_output(onnx_output_image)
                onnx_output_image = opencv_cvtColor(onnx_output_image, COLOR_BGR2RGBA)

                # Alpha
                alpha = numpy_expand_dims(alpha, axis=-1)
                alpha = numpy_repeat(alpha, 3, axis=-1)
                alpha = self.preprocess_image(alpha)
                onnx_output_alpha = self.onnxruntime_inference(alpha)
                onnx_output_alpha = self.postprocess_output(onnx_output_alpha)
                onnx_output_alpha = opencv_cvtColor(onnx_output_alpha, COLOR_RGB2GRAY)

                # Fusion Image + Alpha
                onnx_output_image[:, :, 3] = onnx_output_alpha
                output_image = self.de_normalize_image(onnx_output_image, range)

                return output_image
            
            case "Grayscale":
                image = opencv_cvtColor(image, COLOR_GRAY2RGB)
                
                image = self.preprocess_image(image)
                onnx_output  = self.onnxruntime_inference(image)
                onnx_output  = self.postprocess_output(onnx_output)
                output_image = opencv_cvtColor(onnx_output, COLOR_RGB2GRAY)
                output_image = self.de_normalize_image(onnx_output, range)

                return output_image



    def AI_upscale_with_tilling(self, image: numpy_ndarray) -> numpy_ndarray:
        t_height, t_width = self.calculate_target_resolution(image)
        tiles_x, tiles_y  = self.calculate_tiles_number(image)
        tiles_list        = self.split_image_into_tiles(image, tiles_x, tiles_y)
        tiles_list        = [self.AI_upscale(tile) for tile in tiles_list]

        return self.combine_tiles_into_image(image, tiles_list, t_height, t_width, tiles_x)




    # EXTERNAL FUNCTION
    def AI_orchestration(self, image: numpy_ndarray) -> numpy_ndarray:

        resized_image = self.resize_with_input_factor(image)
        
        if self.image_need_tilling(resized_image):
            return self.AI_upscale_with_tilling(resized_image)
        else:
            return self.AI_upscale(resized_image)







# GUI utils ---------------------------
class MessageBox(CTkToplevel):

    def __init__(
            self,
            messageType: str,
            title: str,
            subtitle: str,
            default_value: str,
            option_list: list,
            ) -> None:

        super().__init__()

        self._running: bool = False

        self._messageType = messageType
        self._title = title        
        self._subtitle = subtitle
        self._default_value = default_value
        self._option_list = option_list
        self._ctkwidgets_index = 0

        self.title('')
        self.lift()                         
        self.attributes("-topmost", True)   
        self.protocol("WM_DELETE_WINDOW", self._on_closing)
        self.after(10, self._create_widgets) 
        self.resizable(False, False)
        self.grab_set()                       

    def _ok_event(
            self, 
            event = None
            ) -> None:
        self.grab_release()
        self.destroy()

    def _on_closing(
            self
            ) -> None:
        self.grab_release()
        self.destroy()

    def createEmptyLabel(
            self
            ) -> CTkLabel:
        
        return CTkLabel(master = self, 
                        fg_color = "transparent",
                        width    = 500,
                        height   = 17,
                        text     = '')

    def placeInfoMessageTitleSubtitle(
            self,
            ) -> None:

        spacingLabel1 = self.createEmptyLabel()
        spacingLabel2 = self.createEmptyLabel()

        if self._messageType == "info":
            title_subtitle_text_color = "#3399FF"
        elif self._messageType == "error":
            title_subtitle_text_color = "#FF3131"

        titleLabel = CTkLabel(
            master     = self,
            width      = 500,
            anchor     = 'w',
            justify    = "left",
            fg_color   = "transparent",
            text_color = title_subtitle_text_color,
            font       = bold22,
            text       = self._title
            )
        
        if self._default_value != None:
            defaultLabel = CTkLabel(
                master     = self,
                width      = 500,
                anchor     = 'w',
                justify    = "left",
                fg_color   = "transparent",
                text_color = "#3399FF",
                font       = bold17,
                text       = f"Default: {self._default_value}"
                )
        
        subtitleLabel = CTkLabel(
            master     = self,
            width      = 500,
            anchor     = 'w',
            justify    = "left",
            fg_color   = "transparent",
            text_color = title_subtitle_text_color,
            font       = bold14,
            text       = self._subtitle
            )
        
        spacingLabel1.grid(row = self._ctkwidgets_index, column = 0, columnspan = 2, padx = 0, pady = 0, sticky = "ew")
        
        self._ctkwidgets_index += 1
        titleLabel.grid(row = self._ctkwidgets_index, column = 0, columnspan = 2, padx = 25, pady = 0, sticky = "ew")
        
        if self._default_value != None:
            self._ctkwidgets_index += 1
            defaultLabel.grid(row = self._ctkwidgets_index, column = 0, columnspan = 2, padx = 25, pady = 0, sticky = "ew")
        
        self._ctkwidgets_index += 1
        subtitleLabel.grid(row = self._ctkwidgets_index, column = 0, columnspan = 2, padx = 25, pady = 0, sticky = "ew")
        
        self._ctkwidgets_index += 1
        spacingLabel2.grid(row = self._ctkwidgets_index, column = 0, columnspan = 2, padx = 0, pady = 0, sticky = "ew")

    def placeInfoMessageOptionsText(
            self,
            ) -> None:
        
        for option_text in self._option_list:
            optionLabel = CTkLabel(master = self,
                                    width  = 600,
                                    height = 45,
                                    corner_radius = 6,
                                    anchor     = 'w',
                                    justify    = "left",
                                    text_color = "#C0C0C0",
                                    fg_color   = "#282828",
                                    bg_color   = "transparent",
                                    font       = bold12,
                                    text       = option_text)
            
            self._ctkwidgets_index += 1
            optionLabel.grid(row = self._ctkwidgets_index, column = 0, columnspan = 2, padx = 25, pady = 4, sticky = "ew")

        spacingLabel3 = self.createEmptyLabel()

        self._ctkwidgets_index += 1
        spacingLabel3.grid(row = self._ctkwidgets_index, column = 0, columnspan = 2, padx = 0, pady = 0, sticky = "ew")

    def placeInfoMessageOkButton(
            self
            ) -> None:
        
        ok_button = CTkButton(
            master  = self,
            command = self._ok_event,
            text    = 'OK',
            width   = 125,
            font         = bold11,
            border_width = 1,
            fg_color     = "#282828",
            text_color   = "#E0E0E0",
            border_color = "#0096FF"
            )
        
        self._ctkwidgets_index += 1
        ok_button.grid(row = self._ctkwidgets_index, column = 1, columnspan = 1, padx = (10, 20), pady = (10, 20), sticky = "e")

    def _create_widgets(
            self
            ) -> None:

        self.grid_columnconfigure((0, 1), weight=1)
        self.rowconfigure(0, weight=1)

        self.placeInfoMessageTitleSubtitle()
        self.placeInfoMessageOptionsText()
        self.placeInfoMessageOkButton()    






#SCROLLFRAME---------
class FileWidget(CTkScrollableFrame):

    def __init__(
            self, 
            master,
            selected_file_list, 
            input_resize_factor  = 0,
            upscale_factor = 1,
            **kwargs
            ) -> None:
       
        super().__init__(master, height=300,**kwargs)

        self.file_list      = selected_file_list
        self.input_resize_factor  = input_resize_factor
        self.upscale_factor = upscale_factor

        self.label_list = []
        self._create_widgets()

    def _destroy_(self) -> None:
        self.file_list = []
        self.destroy()
        place_loadFile_section(window)

    def _create_widgets(self) -> None:
        self.add_clean_button()
        index_row = 1
        for file_path in self.file_list:
            label = self.add_file_information(file_path, index_row)
            self.label_list.append(label)
            index_row +=1
    def add_file_information(self, file_path, index_row) -> CTkLabel:
        # Create a container frame for the file entry
        file_frame = CTkFrame(self, fg_color="transparent")
        file_frame.grid(row=index_row, column=0, sticky="ew", pady=3, padx=3)

        # File information label
        infos, icon = self.extract_file_info(file_path)
        label = CTkLabel(
            file_frame,  # Parent changed to file_frame
            text=infos,
            image=icon,
            font=bold12,
            text_color="#C0C0C0",
            compound="left",
            anchor="w",
            padx=10,
            pady=5,
            justify="left",
        )
        label.pack(side="left", fill="x", expand=True)

        # Preview button
        preview_button = CTkButton(
            file_frame,
            text="Preview",
            width=80,
            height=24,
            font=bold11,
            command=lambda path=file_path: self.preview_file(path)
        )
        preview_button.pack(side="right", padx=(0, 10))

        return file_frame  # Return the container frame instead of the label

    def preview_file(self, file_path):
        loading_icon = LoadingIcon(window)
        loading_icon.start()
        preview_executor.submit(process_and_show_preview, file_path, loading_icon)

    

    def add_clean_button(self) -> None:
        
        button = CTkButton(
            self, 
            image        = clear_icon,
            font         = bold11,
            text         = "CLEAN", 
            compound     = "left",
            width        = 100, 
            height       = 28,
            border_width = 1,
            fg_color     = "#282828",
            text_color   = "#E0E0E0",
            border_color = "#0096FF"
            )

        button.configure(command=lambda: self._destroy_())
        button.grid(row = 0, column=2, pady=(7, 7), padx = (0, 7))
        
    @cache
    def extract_file_icon(self, file_path) -> CTkImage:
        max_size = 50

        if check_if_file_is_video(file_path):
            video_cap   = opencv_VideoCapture(file_path)
            _, frame    = video_cap.read()
            source_icon = opencv_cvtColor(frame, COLOR_BGR2RGB)
            video_cap.release()
        else:
            source_icon = opencv_cvtColor(image_read(file_path), COLOR_BGR2RGB)

        ratio       = min(max_size / source_icon.shape[0], max_size / source_icon.shape[1])
        new_width   = int(source_icon.shape[1] * ratio)
        new_height  = int(source_icon.shape[0] * ratio)
        source_icon = opencv_resize(source_icon,(new_width, new_height))
        ctk_icon    = CTkImage(pillow_image_fromarray(source_icon, mode="RGB"), size = (new_width, new_height))

        return ctk_icon
        
        
        
        

        
        
    def extract_file_info(self, file_path) -> tuple:
        
        if check_if_file_is_video(file_path):
            cap          = opencv_VideoCapture(file_path)
            width        = round(cap.get(CAP_PROP_FRAME_WIDTH))
            height       = round(cap.get(CAP_PROP_FRAME_HEIGHT))
            num_frames   = int(cap.get(CAP_PROP_FRAME_COUNT))
            frame_rate   = cap.get(CAP_PROP_FPS)
            duration     = num_frames/frame_rate
            minutes      = int(duration/60)
            seconds      = duration % 60
            cap.release()

            video_name = str(file_path.split("/")[-1])
            file_icon  = self.extract_file_icon(file_path)

            file_infos = (f"{video_name}\n"
                          f"Resolution {width}x{height} • {minutes}m:{round(seconds)}s • {num_frames}frames\n")
            
            if self.input_resize_factor != 0 and self.upscale_factor != 0 :

                input_resized_height  = int(height * (self.input_resize_factor/100))
                input_resized_width   = int(width * (self.input_resize_factor/100))

                upscaled_height = int(input_resized_height * self.upscale_factor)
                upscaled_width  = int(input_resized_width * self.upscale_factor)



                file_infos += (
                    f"AI input ({self.input_resize_factor}%) ➜ {input_resized_width}x{input_resized_height} \n"
                    f"AI output (x{self.upscale_factor}) ➜ {upscaled_width}x{upscaled_height} \n"
                    f"{output_resized_width}x{output_resized_height}"
                )
        else:
            image_name    = str(file_path.split("/")[-1])
            height, width = get_image_resolution(image_read(file_path))
            file_icon     = self.extract_file_icon(file_path)

            file_infos = (f"{image_name}\n"
                          f"Resolution {width}x{height}\n")
            
            if self.input_resize_factor != 0 and self.upscale_factor != 0 :
                input_resized_height = int(height * (self.input_resize_factor/100))
                input_resized_width  = int(width * (self.input_resize_factor/100))

                upscaled_height = int(input_resized_height * self.upscale_factor)
                upscaled_width  = int(input_resized_width * self.upscale_factor)

                
          
            file_infos += (
                                f"AI input ({self.input_resize_factor}%) ➜ {input_resized_width}x{input_resized_height} \n"
                                f"AI output (x{self.upscale_factor}) ➜ {upscaled_width}x{upscaled_height} \n"
                            )

        return file_infos, file_icon







  # EXTERNAL FUNCTIONS
    def clean_file_list(self) -> None:
        for label in self.label_list:
            label.grid_forget()
    
    def get_selected_file_list(self) -> list: 
        return self.file_list 

    def set_upscale_factor(self, upscale_factor) -> None:
        self.upscale_factor = upscale_factor

    def set_resize_factor(self, input_resize_factor) -> None:
        self.input_resize_factor = input_resize_factor
 

 
def get_values_for_file_widget() -> tuple:
    # Upscale factor
    upscale_factor = get_upscale_factor()

    # Input resolution %
    try:
        input_resize_factor = int(float(str(selected_input_resize_factor.get())))
    except:
        input_resize_factor = 0
    
    return  input_resize_factor, upscale_factor




 
def update_file_widget(a, b, c) -> None:
    try:
        global file_widget
        file_widget
    except:
        return
    
    upscale_factor = get_upscale_factor()

    try:
        resize_factor = int(float(str(selected_input_resize_factor.get())))
    except:
        resize_factor = 0

    file_widget.clean_file_list()
    file_widget.set_resize_factor(resize_factor)
    file_widget.set_upscale_factor(upscale_factor)
    file_widget._create_widgets()

    

def create_info_button(
        command: Callable, 
        text: str,
        width: int = 150,
        ) -> CTkButton:
    
    bg_image = Image.open("./Assets/1.jpg")
    bg_image = bg_image.resize((width, 22))  
    bg_image_ctk = CTkImage(bg_image)

    
    return CTkButton(
        master  = window, 
        command = command,
        text          = text,
        fg_color      = "transparent",
        hover_color   = "black",
        text_color    = text_color,
        anchor        = "w",
        corner_radius = 10,
        height        = 14,
        width         = width,
        font          = bold12,
        image         = bg_image_ctk,
        border_width  = 1,
        border_color  = "#404040"  
    
    )




def create_option_menu(
        command: Callable, 
        values: list,
        default_value: str
        ) -> CTkOptionMenu:
    
    option_menu = CTkOptionMenu(
        master  = window, 
        command = command,
        values  = values,
        width         = 150,
        height        = 30,
        corner_radius = 5,
        dropdown_font = bold11,
        font          = bold11,
        anchor        = "center",
        text_color    = text_color,
        fg_color      = widget_background_color,
        button_color       = widget_background_color,
        button_hover_color = "#282828",
        dropdown_fg_color  = text_color
    )
    option_menu.set(default_value)
    return option_menu




def create_text_box(textvariable: StringVar) -> CTkEntry:
    return CTkEntry(
        master        = window, 
        textvariable  = textvariable,
        corner_radius = 5,
        width         = 150,
        height        = 30,
        font          = bold11,
        justify       = "center",
        text_color    = text_color,
        fg_color      = widget_background_color,
        border_width  = 1,
        border_color  = "#404040",  
    )



def create_text_box_output_path(textvariable: StringVar) -> CTkEntry:
    return CTkEntry(
        master        = window, 
        textvariable  = textvariable,
        border_width  = 1,
        corner_radius = 5,
        width         = 300,
        height        = 30,
        font          = bold11,
        justify       = "center",
        text_color    = "#C0C0C0",
        fg_color      = "#000000",
        border_color  = "#404040",
        state         = DISABLED
    )



def create_active_button(
        command: Callable,
        text: str,
        icon: CTkImage = None,
        width: int = 140,
        height: int = 30,
        border_color: str = "#0096FF"
        ) -> CTkButton:
    
    return CTkButton(
        master     = window, 
        command    = command,
        text       = text,
        image      = icon,
        width      = width,
        height     = height,
        font         = bold11,
        border_width = 1,
        fg_color     = widget_background_color,
        hover_color  = "#282828",  # Lysere grå ved hover
        text_color   = "white",
        border_color = border_color
    )




# File Utils functions ------------------------
def create_dir(name_dir: str) -> None:
    if os_path_exists(name_dir):
        remove_directory(name_dir)
    if not os_path_exists(name_dir): 
        os_makedirs(name_dir, mode=0o777)

def stop_thread() -> None: stop = 1 + "x"

def image_read(file_path: str) -> numpy_ndarray: 
    with open(file_path, 'rb') as file:
        return opencv_imdecode(numpy_frombuffer(file.read(), uint8), IMREAD_UNCHANGED)

def image_write(file_path: str, file_data: numpy_ndarray) -> None: 
    _, file_extension = os_path_splitext(file_path)
    opencv_imencode(file_extension, file_data)[1].tofile(file_path)



def prepare_output_image_filename(
        image_path: str, 
        selected_output_path: str,
        selected_AI_model: str, 
        resize_factor: int, 
        selected_image_extension: str,
        selected_interpolation_factor: float
        ) -> str:
        
    if selected_output_path == OUTPUT_PATH_CODED:
        file_path_no_extension, _ = os_path_splitext(image_path)
        output_path = file_path_no_extension
    else:
        file_name   = os_path_basename(image_path)
        output_path = f"{selected_output_path}{os_separator}{file_name}"

    # Selected AI model
    to_append = f"_{selected_AI_model}"

    # Selected resize
    to_append += f"_Resize-{str(int(resize_factor * 100))}"

    # Selected intepolation
    match selected_interpolation_factor:
        case 0.3:
            to_append += "_Interpolation-Low"
        case 0.5:
            to_append += "_Interpolation-Medium"
        case 0.7:
            to_append += "_Interpolation-High"

    # Selected image extension
    to_append += f"{selected_image_extension}"
        
    output_path += to_append

    return output_path



def prepare_output_video_frame_filename(
        frame_path: str, 
        selected_AI_model: str, 
        resize_factor: int, 
        selected_interpolation_factor: float
        ) -> str:
            
    file_path_no_extension, _ = os_path_splitext(frame_path)
    output_path = file_path_no_extension

    # Selected AI model
    to_append = f"_{selected_AI_model}"

    # Selected resize
    to_append += f"_Resize-{str(int(resize_factor * 100))}"

    # Selected intepolation
    match selected_interpolation_factor:
        case 0.3:
            to_append += "_Interpolation-Low"
        case 0.5:
            to_append += "_Interpolation-Medium"
        case 0.7:
            to_append += "_Interpolation-High"

    # Selected image extension
    to_append += f".jpg"
        
    output_path += to_append

    return output_path



def prepare_output_video_filename(
        video_path: str, 
        selected_output_path: str,
        selected_AI_model: str, 
        input_resize_factor: int, 
        selected_video_extension: str,
        selected_interpolation_factor: float
        ) -> str:
    
    match selected_video_extension:
        case '.mp4 (x264)': selected_video_extension = '.mp4'
        case '.mp4 (x265)': selected_video_extension = '.mp4'
        case '.avi':        selected_video_extension = '.avi'

    if selected_output_path == OUTPUT_PATH_CODED:
        file_path_no_extension, _ = os_path_splitext(video_path)
        output_path = file_path_no_extension
    else:
        file_name   = os_path_basename(video_path)
        output_path = f"{selected_output_path}{os_separator}{file_name}"
    
    # Selected AI model
    to_append = f"_{selected_AI_model}"

    # Selected resize
    to_append += f"_Resize-{str(int(input_resize_factor * 100))}"

    # Selected intepolation
    match selected_interpolation_factor:
        case 0.3:
            to_append += "_Interpolation-Low"
        case 0.5:
            to_append += "_Interpolation-Medium"
        case 0.7:
            to_append += "_Interpolation-High"

    # Selected video extension
    to_append += f"{selected_video_extension}"
        
    output_path += to_append

    return output_path



def prepare_output_video_directory_name(
        video_path: str, 
        selected_output_path: str,
        selected_AI_model: str, 
        input_resize_factor: int, 
        selected_interpolation_factor: float
        ) -> str:
    
    if selected_output_path == OUTPUT_PATH_CODED:
        file_path_no_extension, _ = os_path_splitext(video_path)
        output_path = file_path_no_extension
    else:
        file_name   = os_path_basename(video_path)
        output_path = f"{selected_output_path}{os_separator}{file_name}"

    # Selected AI model
    to_append = f"_{selected_AI_model}"

    # Selected resize
    to_append += f"_Resize-{str(int(input_resize_factor * 100))}"

    # Selected intepolation
    match selected_interpolation_factor:
        case 0.3:
            to_append += "_Interpolation-Low"
        case 0.5:
            to_append += "_Interpolation-Medium"
        case 0.7:
            to_append += "_Interpolation-High"

    output_path += to_append

    return output_path






# Image/video Utils functions ------------------------
def get_video_fps(video_path: str) -> float:
    video_capture = opencv_VideoCapture(video_path)
    frame_rate    = video_capture.get(CAP_PROP_FPS)
    video_capture.release()
    return frame_rate
   
def get_image_resolution(image: numpy_ndarray) -> tuple:
    height = image.shape[0]
    width  = image.shape[1]

    return height, width 

def save_extracted_frames(
        extracted_frames_paths: list[str], 
        extracted_frames: list[numpy_ndarray], 
        cpu_number: int
        ) -> None:
    
    pool = ThreadPool(cpu_number)
    pool.starmap(image_write, zip(extracted_frames_paths, extracted_frames))
    pool.close()
    pool.join()

def extract_video_frames(
        processing_queue: multiprocessing_Queue,
        file_number: int,
        target_directory: str,
        video_path: str, 
        cpu_number: int
    ) -> list[str]:

    create_dir(target_directory)

    # Video frame extraction
    frames_number_to_save = cpu_number * FRAMES_FOR_CPU
    video_capture         = opencv_VideoCapture(video_path)
    frame_count           = int(video_capture.get(CAP_PROP_FRAME_COUNT))

    extracted_frames       = []
    extracted_frames_paths = []
    video_frames_list      = []

    for frame_number in range(frame_count):
        success, frame = video_capture.read()
        if success:
            frame_path = f"{target_directory}{os_separator}frame_{frame_number:03d}.jpg"            
            extracted_frames.append(frame)
            extracted_frames_paths.append(frame_path)
            video_frames_list.append(frame_path)

            if len(extracted_frames) == frames_number_to_save:
                percentage_extraction = (frame_number / frame_count) * 100

                write_process_status(processing_queue, f"{file_number}. Extracting video frames ({round(percentage_extraction, 2)}%)")
                save_extracted_frames(extracted_frames_paths, extracted_frames, cpu_number)
                extracted_frames       = []
                extracted_frames_paths = []

    video_capture.release()

    if len(extracted_frames) > 0: save_extracted_frames(extracted_frames_paths, extracted_frames, cpu_number)
    
    return video_frames_list






def video_encoding(
        video_path: str,
        video_output_path: str,
        upscaled_frame_paths: list[str], 
        cpu_number: int,
        selected_video_extension: str, 
        Audio_Inference_output: str = None
        ) -> None:
        
    match selected_video_extension:
        case ".mp4 (x264)": codec = "libx264"
        case ".mp4 (x265)": codec = "libx265"
        case ".avi":        codec = "png"

    no_audio_path = f"{os_path_splitext(video_output_path)[0]}_no_audio{os_path_splitext(video_output_path)[1]}"
    video_fps     = get_video_fps(video_path)
    video_clip    = ImageSequenceClip.ImageSequenceClip(sequence = upscaled_frame_paths, fps = video_fps)

    video_clip.write_videofile(
        filename = no_audio_path,
        fps      = video_fps,
        codec    = codec,
        threads  = cpu_number,
        logger   = None,
        audio    = None,
        bitrate  = "12M",
        preset   = "ultrafast"
    )

        
    audio_source = Audio_Inference_output if Audio_Inference_output else video_path
    # Copy the audio from original video
    audio_passthrough_command = [
        FFMPEG_EXE_PATH,
        "-y",
        "-i", audio_source,
        "-i", no_audio_path,
        "-c:v", "copy",
        "-c:a", "copy",
        "-b:a", "192k", #Audio bitrate
        "-map", "1:v:0", #Map video from no_audio_path
        "-map", "0:a:0", #map audio from isolated audio
        video_output_path
    ]
    try: 
        subprocess_run(audio_passthrough_command, check = True, shell = "False")
        if os_path_exists(no_audio_path):
            os_remove(no_audio_path)
    except Exception as e:
        print(f"Error during video encoding: {e}")
        pass
    
def check_video_upscaling_resume(
        target_directory: str, 
        selected_AI_model: str
        ) -> bool:
    
    if os_path_exists(target_directory):
        directory_files      = os_listdir(target_directory)
        upscaled_frames_path = [file for file in directory_files if selected_AI_model in file]

        if len(upscaled_frames_path) > 1:
            return True
        else:
            return False
    else:
        return False



def get_video_frames_for_upscaling_resume(
        target_directory: str,
        selected_AI_model: str,
        ) -> list[str]:
    
    # Only file names
    directory_files      = os_listdir(target_directory)
    original_frames_path = [file for file in directory_files if file.endswith('.jpg')]
    original_frames_path = [file for file in original_frames_path if selected_AI_model not in file]

    # Adding the complete path to file
    original_frames_path = natsorted([os_path_join(target_directory, file) for file in original_frames_path])

    return original_frames_path






def calculate_time_to_complete_video(
        time_for_frame: float,
        remaining_frames: int,
        ) -> str:
    
    remaining_time = time_for_frame * remaining_frames

    hours_left   = remaining_time // 3600
    minutes_left = (remaining_time % 3600) // 60
    seconds_left = round((remaining_time % 3600) % 60)

    time_left = ""

    if int(hours_left) > 0: 
        time_left = f"{int(hours_left):02d}h"
    
    if int(minutes_left) > 0: 
        time_left = f"{time_left}{int(minutes_left):02d}m"

    if seconds_left > 0: 
        time_left = f"{time_left}{seconds_left:02d}s"

    return time_left        








def interpolate_images_and_save(
        target_path: str,
        starting_image: numpy_ndarray,
        upscaled_image: numpy_ndarray,
        starting_image_importance: float,
        ) -> None:
    
    def add_alpha_channel(image: numpy_ndarray) -> numpy_ndarray:
        if image.shape[2] == 3:
            alpha = numpy_full((image.shape[0], image.shape[1], 1), 255, dtype = uint8)
            image = numpy_concatenate((image, alpha), axis = 2)
        return image
    
    def get_image_mode(image: numpy_ndarray) -> str:
        match image.shape:
            case (rows, cols):
                return "Grayscale"
            case (rows, cols, channels) if channels == 3:
                return "RGB"
            case (rows, cols, channels) if channels == 4:
                return "RGBA"


    ZERO = 0
    upscaled_image_importance       = 1 - starting_image_importance
    starting_height, starting_width = get_image_resolution(starting_image)
    target_height, target_width     = get_image_resolution(upscaled_image)

    starting_resolution = starting_height + starting_width
    target_resolution   = target_height + target_width

    if starting_resolution > target_resolution:
        starting_image = opencv_resize(starting_image,(target_width, target_height), INTER_AREA)
    else:
        starting_image = opencv_resize(starting_image,(target_width, target_height), INTER_LINEAR)

    try: 
        if get_image_mode(starting_image) == "RGBA":
            starting_image = add_alpha_channel(starting_image)
            upscaled_image = add_alpha_channel(upscaled_image)

        interpolated_image = opencv_addWeighted(starting_image, starting_image_importance, upscaled_image, upscaled_image_importance, ZERO)
        image_write(
            file_path = target_path, 
            file_data = interpolated_image
        )
    except:
        image_write(
            file_path = target_path, 
            file_data = upscaled_image
        )






def manage_upscaled_video_frame_save_async(
        upscaled_frame: numpy_ndarray,
        starting_frame: numpy_ndarray,
        upscaled_frame_path: str,
        selected_interpolation_factor: float
    ) -> None:

    if selected_interpolation_factor > 0:
        thread = Thread(
            target = interpolate_images_and_save,
            args = (
                upscaled_frame_path, 
                starting_frame,
                upscaled_frame,
                selected_interpolation_factor
            )
        )
    else:
        thread = Thread(
            target = image_write,
            args = (
                upscaled_frame_path, 
                upscaled_frame
            )
        )

    thread.start()






def update_process_status_videos(
        processing_queue: multiprocessing_Queue, 
        file_number: int, 
        frame_index: int, 
        how_many_frames: int,
        average_processing_time: float,
        ) -> None:

    if frame_index != 0 and (frame_index + 1) % 8 == 0:  
        remaining_frames = how_many_frames - frame_index
        remaining_time   = calculate_time_to_complete_video(average_processing_time, remaining_frames)
        if remaining_time != "":
            percent_complete = (frame_index + 1) / how_many_frames * 100 
            write_process_status(processing_queue, f"{file_number}. Upscaling video {percent_complete:.2f}% ({remaining_time})")








def copy_file_metadata(
        original_file_path: str, 
        upscaled_file_path: str
        ) -> None:
    
    exiftool_cmd = [
        EXIFTOOL_EXE_PATH, 
        '-fast', 
        '-TagsFromFile', 
        original_file_path, 
        '-overwrite_original', 
        '-all:all',
        '-unsafe',
        '-largetags', 
        upscaled_file_path
    ]
    
    try: 
        subprocess_run(exiftool_cmd, check = True, shell = "False")
    except:
        pass






# Core functions ------------------------
def check_upscale_steps() -> None:
    sleep(1)

    try:
        while True:
            actual_step = read_process_status()

            if actual_step == COMPLETED_STATUS:
                info_message.set(f"All files completed! :)")
                stop_upscale_process()
                stop_thread()

            elif actual_step == STOP_STATUS:
                info_message.set(f"Upscaling stopped")
                stop_upscale_process()
                stop_thread()

            elif ERROR_STATUS in actual_step:
                info_message.set(f"Error while upscaling :(")
                show_error_message(actual_step.replace(ERROR_STATUS, ""))
                stop_thread()

            else:
                info_message.set(actual_step)

            sleep(1)
    except:
        place_upscale_button()
        
def read_process_status() -> str:
    return processing_queue.get()

def write_process_status(
        processing_queue: multiprocessing_Queue,
        step: str
        ) -> None:
    
    print(f"{step}")
    while not processing_queue.empty(): processing_queue.get()
    processing_queue.put(f"{step}")

def stop_upscale_process() -> None:
    global process_upscale_orchestrator
    try:
        process_upscale_orchestrator
    except:
        pass
    else:
        process_upscale_orchestrator.kill()

def stop_button_command() -> None:
    stop_upscale_process()
    write_process_status(processing_queue, f"{STOP_STATUS}") 

def upscale_button_command() -> None: 
    global selected_file_list
    global selected_AI_model
    global selected_gpu
    global selected_keep_frames
    global selected_AI_multithreading
    global selected_interpolation_factor
    global selected_image_extension
    global selected_video_extension
    global tiles_resolution
    global input_resize_factor
    global cpu_number
    global selected_audio_mode
    global process_upscale_orchestrator
    global selected_audio_mode
    selected_audio_mode = default_audio_mode

    if user_input_checks():
        info_message.set("Loading")

        print("=" * 50)
        print("> Starting upscale:")
        print(f"  Files to upscale: {len(selected_file_list)}")
        print(f"  Output path: {(selected_output_path.get())}")
        print(f"  Selected AI model: {selected_AI_model}")
        print(f"  Selected GPU: {selected_gpu}")
        print(f"  AI multithreading: {selected_AI_multithreading}")
        print(f"  Interpolation factor: {selected_interpolation_factor}")
        print(f"  Selected image output extension: {selected_image_extension}")
        print(f"  Selected video output extension: {selected_video_extension}")
        print(f"  Tiles resolution for selected GPU VRAM: {tiles_resolution}x{tiles_resolution}px")
        print(f"  input_resize_factor: {int(input_resize_factor * 100)}%")
        print(f"  Cpu number: {cpu_number}")
        print(f" Save frames: {selected_keep_frames}")
        print(f" selected_audio_mode : {selected_audio_mode}")
        print("=" * 50)

        place_stop_button()

        process_upscale_orchestrator = Process(
            target = upscale_orchestrator,
            args = (
                processing_queue, 
                selected_file_list, 
                selected_output_path.get(),
                selected_AI_model, 
                selected_gpu,
                selected_image_extension,
                tiles_resolution, 
                input_resize_factor, 
                cpu_number, 
                selected_video_extension,
                selected_interpolation_factor,
                selected_AI_multithreading,
                selected_keep_frames,
                selected_audio_mode 
            )
        )
        process_upscale_orchestrator.start()

        thread_wait = Thread(target = check_upscale_steps)
        thread_wait.start()










# ORCHESTRATOR
def upscale_orchestrator(
        processing_queue: multiprocessing_Queue,
        selected_file_list: list,
        selected_output_path: str,
        selected_AI_model: str,
        selected_gpu: str,
        selected_image_extension: str,
        tiles_resolution: int,
        input_resize_factor: int,
        cpu_number: int,
        selected_video_extension: str,
        selected_interpolation_factor: float,
        selected_AI_multithreading: int,
        selected_keep_frames: bool,
        selected_audio_mode: str
        ) -> None:

    write_process_status(processing_queue, f"Loading AI model")
    AI_instance = AI(selected_AI_model, selected_gpu, input_resize_factor, tiles_resolution)
    AI_instance_list = []
    AI_instance_list.append(AI_instance)

    if selected_AI_multithreading > 1:
        for _ in range(selected_AI_multithreading - 1):
            AI_instance_list.append(AI(selected_AI_model, selected_gpu, input_resize_factor,  tiles_resolution))

    try:
        how_many_files = len(selected_file_list)
        for file_number in range(how_many_files):
            file_path   = selected_file_list[file_number]
            file_number = file_number + 1

            if check_if_file_is_video(file_path):
                upscale_video(
                    processing_queue,
                    file_path, 
                    file_number,
                    selected_output_path, 
                    AI_instance,
                    AI_instance_list,
                    selected_AI_model,
                    input_resize_factor,
                    cpu_number, 
                    selected_video_extension, 
                    selected_interpolation_factor,
                    selected_AI_multithreading,
                    selected_keep_frames,
                    selected_audio_mode
                )
            else:
                upscale_image(
                    processing_queue,
                    file_path, 
                    file_number,
                    selected_output_path,
                    AI_instance,
                    selected_AI_model,
                    selected_image_extension, 
                    input_resize_factor, 
                    selected_interpolation_factor
                )

        write_process_status(processing_queue, f"{COMPLETED_STATUS}")

    except Exception as exception:
        write_process_status(processing_queue, f"{ERROR_STATUS} {str(exception)}")










# IMAGES
def upscale_image(
        processing_queue: multiprocessing_Queue,
        image_path: str, 
        file_number: int,
        selected_output_path: str,
        AI_instance: AI,
        selected_AI_model: str,
        selected_image_extension: str,
        input_resize_factor: int, 
        selected_interpolation_factor: float
        ) -> None:
    
    starting_image = image_read(image_path)
    upscaled_image_path = prepare_output_image_filename(image_path, selected_output_path, selected_AI_model, input_resize_factor, selected_image_extension, selected_interpolation_factor)

    write_process_status(processing_queue, f"{file_number}. Upscaling image")
    upscaled_image = AI_instance.AI_orchestration(starting_image)

    if selected_interpolation_factor > 0:
        interpolate_images_and_save(
            upscaled_image_path,
            starting_image,
            upscaled_image,
            selected_interpolation_factor
        )

    else:
        image_write(
            file_path = upscaled_image_path,
            file_data = upscaled_image
        )

    copy_file_metadata(image_path, upscaled_image_path)





# VIDEOS
def upscale_video(
        processing_queue: multiprocessing_Queue,
        video_path: str, 
        file_number: int,
        selected_output_path: str,
        AI_instance: AI,
        AI_instance_list: list[AI],
        selected_AI_model: str,
        input_resize_factor: int, 
        cpu_number: int, 
        selected_video_extension: str,
        selected_interpolation_factor: float,
        selected_AI_multithreading: int,
        selected_keep_frames: bool,
        selected_audio_mode: str
        ) -> None:

    global processed_frames_async
    global processing_times_async
    processed_frames_async = 0
    processing_times_async = []
    
    # 1.Preparation
    target_directory  = prepare_output_video_directory_name(video_path, selected_output_path, selected_AI_model, input_resize_factor, selected_interpolation_factor)
    video_output_path = prepare_output_video_filename(video_path, selected_output_path, selected_AI_model, input_resize_factor, selected_video_extension, selected_interpolation_factor)
    
    Audio_Inference_output = AI_instance.process_Audio_Inference(video_path,selected_audio_mode,) 
    
    # 2. Resume upscaling OR Extract video frames
    video_upscale_continue = check_video_upscaling_resume(target_directory, selected_AI_model)
    if video_upscale_continue:
        write_process_status(processing_queue, f"{file_number}. Resume video upscaling")
        extracted_frames_paths = get_video_frames_for_upscaling_resume(target_directory, selected_AI_model)
    else:
        write_process_status(processing_queue, f"{file_number}. Extracting video frames")
        extracted_frames_paths = extract_video_frames(processing_queue, file_number, target_directory, video_path, cpu_number)

    upscaled_frame_paths = [prepare_output_video_frame_filename(frame_path, selected_AI_model, input_resize_factor,selected_interpolation_factor) for frame_path in extracted_frames_paths]

    # 3. Check if video need tiles OR video multithreading upscale
    first_frame_path             = extracted_frames_paths[0]
    video_need_tiles             = AI_instance.video_need_tilling(first_frame_path)
    multiframes_supported_by_gpu = AI_instance.calculate_multiframes_supported_by_gpu(first_frame_path)
    multiframes_number           = min(multiframes_supported_by_gpu, selected_AI_multithreading)

    write_process_status(processing_queue, f"{file_number}. Upscaling video") 
    if video_need_tiles or multiframes_number <= 1:
        upscale_video_frames(
            processing_queue,
            file_number,
            AI_instance,
            extracted_frames_paths,
            upscaled_frame_paths,
            selected_interpolation_factor
        )
    else:
        upscale_video_frames_multithreading(
            processing_queue,
            file_number,
            AI_instance_list,
            extracted_frames_paths,
            upscaled_frame_paths,
            multiframes_number,
            selected_interpolation_factor
        )

    # 4. Check for forgotten video frames
    check_forgotten_video_frames(processing_queue, file_number, AI_instance, extracted_frames_paths, upscaled_frame_paths, selected_interpolation_factor)

    # 5. Video encoding
    write_process_status(processing_queue, f"{file_number}. Processing upscaled video")
    video_encoding(video_path, video_output_path, upscaled_frame_paths, cpu_number, selected_video_extension,Audio_Inference_output)
    copy_file_metadata(video_path, video_output_path)
    
    #6 delete frames folder
    if selected_keep_frames == False:
        if os_path_exists(target_directory): remove_directory(target_directory)

def upscale_video_frames(
        processing_queue: multiprocessing_Queue,
        file_number: int,
        AI_instance: AI,
        extracted_frames_paths: list[str],
        upscaled_frame_paths: list[str],
        selected_interpolation_factor: float
        ) -> None:
    
    frame_processing_times = []

    for frame_index, frame_path in enumerate(extracted_frames_paths):
        upscaled_frame_path = upscaled_frame_paths[frame_index]
        already_upscaled    = os_path_exists(upscaled_frame_path)
        
        if already_upscaled == False:
            start_timer = timer()
            
            starting_frame = image_read(frame_path)
            upscaled_frame = AI_instance.AI_orchestration(starting_frame)
            manage_upscaled_video_frame_save_async(upscaled_frame, starting_frame, upscaled_frame_path, selected_interpolation_factor)
        
            end_timer    = timer()
            elapsed_time = end_timer - start_timer
            frame_processing_times.append(elapsed_time)
            
            if (frame_index + 1) % 8 == 0:
                average_processing_time = numpy_mean(frame_processing_times)
                update_process_status_videos(processing_queue, file_number, frame_index, len(extracted_frames_paths), average_processing_time)

            if (frame_index + 1) % 100 == 0: frame_processing_times = []

def upscale_video_frames_multithreading(
        processing_queue: multiprocessing_Queue,
        file_number: int,
        AI_instance_list: list[AI],
        extracted_frames_paths: list[str],
        upscaled_frame_paths: list[str],
        multiframes_number: int,
        selected_interpolation_factor: float,
        ) -> None:
    
    def upscale_single_video_frame_async(
            processing_queue: multiprocessing_Queue,
            file_number: int,
            multiframes_number: int,
            total_video_frames: int,
            AI_instance: AI,
            extracted_frames_paths: list[str],
            upscaled_frame_paths: list[str],
            selected_interpolation_factor: float,
            ) -> None:

        global processed_frames_async
        global processing_times_async

        for frame_index in range(len(extracted_frames_paths)):
            upscaled_frame_path = upscaled_frame_paths[frame_index]
            already_upscaled    = os_path_exists(upscaled_frame_path)

            if already_upscaled == False:
                start_timer = timer()

                starting_frame = image_read(extracted_frames_paths[frame_index])
                upscaled_frame = AI_instance.AI_orchestration(starting_frame)

                manage_upscaled_video_frame_save_async(upscaled_frame, starting_frame, upscaled_frame_path, selected_interpolation_factor)

                end_timer    = timer()
                elapsed_time = end_timer - start_timer
                processing_times_async.append(elapsed_time)

                if (processed_frames_async + 1) % 8 == 0:
                    average_processing_time = float(numpy_mean(processing_times_async)/multiframes_number)
                    update_process_status_videos(processing_queue, file_number, processed_frames_async, total_video_frames, average_processing_time)

                if (processed_frames_async + 1) % 100 == 0: processing_times_async = []
        
            processed_frames_async +=1

    
    total_video_frames         = len(extracted_frames_paths)
    chunk_size                 = total_video_frames // multiframes_number
    frame_list_chunks          = [extracted_frames_paths[i:i + chunk_size] for i in range(0, len(extracted_frames_paths), chunk_size)]
    upscaled_frame_list_chunks = [upscaled_frame_paths[i:i + chunk_size] for i in range(0, len(upscaled_frame_paths), chunk_size)]

    write_process_status(processing_queue, f"{file_number}. Upscaling video ({multiframes_number} threads)")

    pool = ThreadPool(multiframes_number)
    pool.starmap(
        upscale_single_video_frame_async,
        zip(
            repeat(processing_queue),
            repeat(file_number),
            repeat(multiframes_number),
            repeat(total_video_frames),
            AI_instance_list,
            frame_list_chunks,
            upscaled_frame_list_chunks,
            repeat(selected_interpolation_factor)
        )
    )
    pool.close()
    pool.join()

def check_forgotten_video_frames(
        processing_queue: multiprocessing_Queue,
        file_number: int,
        AI_instance: AI,
        extracted_frames_paths: list[str],
        upscaled_frame_paths: list[str],
        selected_interpolation_factor: float,
        ):
    
    # Check if all the upscaled frames exist
    frame_path_todo_list          = []
    upscaled_frame_path_todo_list = []

    for frame_index in range(len(upscaled_frame_paths)):
        
        if not os_path_exists(upscaled_frame_paths[frame_index]):
            frame_path_todo_list.append(extracted_frames_paths[frame_index])
            upscaled_frame_path_todo_list.append(upscaled_frame_paths[frame_index]) 

    if len(upscaled_frame_path_todo_list) > 0:
        upscale_video_frames(
            processing_queue,
            file_number,
            AI_instance,
            frame_path_todo_list,
            upscaled_frame_path_todo_list,
            selected_interpolation_factor
        )















# GUI utils function ---------------------------
def check_if_file_is_video(
        file: str
        ) -> bool:
    
    return any(video_extension in file for video_extension in supported_video_extensions)

def check_supported_selected_files(
        uploaded_file_list: list
        ) -> list:
    
    return [file for file in uploaded_file_list if any(supported_extension in file for supported_extension in supported_file_extensions)]

def user_input_checks() -> bool:
    global selected_file_list
    global selected_AI_model
    global selected_image_extension
    global tiles_resolution
    global input_resize_factor
    global cpu_number

    # Selected files 
    try: selected_file_list = file_widget.get_selected_file_list()
    except:
        info_message.set("Please select a file")
        return False

    if len(selected_file_list) <= 0:
        info_message.set("Please select a file")
        return False


    # AI model
    if selected_AI_model == AI_LIST_SEPARATOR[0]:
        info_message.set("Please select the AI model")
        return False


    # Input resize factor 
    try: input_resize_factor = int(float(str(selected_input_resize_factor.get())))
    except:
        info_message.set("Resize % must be a numeric value")
        return False

    if input_resize_factor > 0: input_resize_factor = input_resize_factor/100
    else:
        info_message.set("Resize % must be a value > 0")
        return False
    

   

    
     
   # VRAM limiter
    # Tiles resolution 
    try: tiles_resolution = 100 * int(float(str(selected_VRAM_limiter.get())))
    except:
        info_message.set("VRAM/RAM value must be a numeric value")
        return False

    if tiles_resolution > 0: 
        if selected_AI_model in RRDB_models_list:          
            vram_multiplier = very_high_VRAM
        elif selected_AI_model in SRVGGNetCompact_models_list: 
            vram_multiplier = medium_VRAM
        elif selected_AI_model in IRCNN_models_list:
            vram_multiplier = very_low_VRAM

        selected_vram = (vram_multiplier * int(float(str(selected_VRAM_limiter.get()))))
        tiles_resolution = int(selected_vram * 100)

        
    else:
        info_message.set("VRAM/RAM value must be > 0")
        return False

    # Cpu number 
    try: cpu_number = int(float(str(selected_cpu_number.get())))
    except:
        info_message.set("Cpu number must be a numeric value")
        return False

    if cpu_number <= 0:         
        info_message.set("Cpu number value must be > 0")
        return False
    else: 
        cpu_number = int(cpu_number)

    return True

def show_error_message(exception: str) -> None:
    messageBox_title    = "Upscale error"
    messageBox_subtitle = "Please report the error on Github or Telegram"
    messageBox_text     = f"\n {str(exception)} \n"

    MessageBox(
        messageType   = "error",
        title         = messageBox_title,
        subtitle      = messageBox_subtitle,
        default_value = None,
        option_list   = [messageBox_text]
    )

def get_upscale_factor() -> int:
    global selected_AI_model
    if AI_LIST_SEPARATOR[0] in selected_AI_model: upscale_factor = 0
    elif 'x1' in selected_AI_model: upscale_factor = 1
    elif 'x2' in selected_AI_model: upscale_factor = 2
    elif 'x4' in selected_AI_model: upscale_factor = 4

    return upscale_factor



def open_files_action():
    global selected_file_list  
    def check_supported_selected_files(uploaded_file_list: list) -> list:
        return [file for file in uploaded_file_list if any(supported_extension in file for supported_extension in supported_file_extensions)]

    info_message.set("Selecting files")

    uploaded_files_list    = list(filedialog.askopenfilenames())
    uploaded_files_counter = len(uploaded_files_list)

    supported_files_list    = check_supported_selected_files(uploaded_files_list)
    supported_files_counter = len(supported_files_list)
    
    print("> Uploaded files: " + str(uploaded_files_counter) + " => Supported files: " + str(supported_files_counter))

    if supported_files_counter > 0:
        if supported_files_list:
                selected_file_list = supported_files_list
        upscale_factor = get_values_for_file_widget()

        global file_widget
        file_widget = FileWidget(
            master               = window, 
            selected_file_list   = supported_files_list,
            upscale_factor       = upscale_factor,
            fg_color             = background_color, 
            bg_color             = background_color
        )
        file_widget.place(relx = 0.0, rely = 0.0, relwidth = 0.5, relheight = 0.4)
        info_message.set("Ready")
    else: 
        info_message.set("Not supported files :(")
    

def open_output_path_action():
    asked_selected_output_path = filedialog.askdirectory()
    if asked_selected_output_path == "":
        selected_output_path.set(OUTPUT_PATH_CODED)
    else:
        selected_output_path.set(asked_selected_output_path)








# GUI select from menus functions ---------------------------
def select_audio_mode_from_menu(selected_mode):
    global selected_audio_mode
    selected_audio_mode = selected_mode
    print(f"Print global selected audio mode: {selected_audio_mode}, print selected_mode: {selected_mode}")
    if selected_audio_mode == "Vocal Isolation":
        print(f"Selected Audio Mode: Vocal isolation:  {selected_audio_mode}")
    
    if selected_audio_mode == "Audio Enchancement":
        print(f"Selected audio mode is Vocal Enchancement: {selected_audio_mode}")
        
    if selected_audio_mode == "Disabled":
        print(f"Selected audio mode is disabled: {selected_audio_mode}")
    
    return selected_audio_mode
    
    

def select_AI_from_menu(selected_option: str) -> None:
    global selected_AI_model, current_loaded_model, model_loading_thread

    #exit early if model already loaded 
    if selected_option == current_loaded_model or selected_option in AI_LIST_SEPARATOR:
        return
    
    #Updates ui immedietaly 
    window.preview_button.configure(state=DISABLED)
    info_message.set(f"Loading {selected_option}...")
    selected_AI_model = selected_option
    update_file_widget(1, 2, 3) #exsisting UI update 

    #stops any ongoing loading thread 
    if model_loading_thread and model_loading_thread.is_alive():
        model_loading_thread.join(timeout=0.5)
       
        #starts a new loading thread on model.
        model_loading_thread = threading.Thread(
            target=load_model_if_needed,
            args=(selected_option, ),
            daemon=True
        )
        model_loading_thread.start()

        #checks loding status
        window.after(100, check_model_loading_progress)

def check_model_loading_progress():
    global model_loading_thread
    if model_loading_thread.is_alive():
        window.after(100, check_model_loading_progress)
    else:
        if current_loaded_model == selected_AI_model:
            window.preview_button.configure(state=NORMAL)
            info_message.set("Ready for preview")
        else:
            window.preview_button.configure(state=DISABLED)
            info_message.set("Model load failed")



def load_model_if_needed(model_name):
    import gc
    global preview_ai_instance, current_loaded_model
    with model_loading_lock:
        #Returns early if model already is loaded
        if current_loaded_model == model_name:
            return 
        

        try:
            print(f"Loading {model_name} model...")
            info_message.set(f"Loading {model_name} model...")
            if preview_ai_instance:
                preview_ai_instance.inferenceSession = None
                del preview_ai_instance
                preview_ai_instance = None
                gc.collect()

            
            preview_ai_instance = AI(
                model_name,
                selected_gpu,
                int(float(selected_input_resize_factor.get())),
                float(selected_VRAM_limiter.get())
            )


            dummy_input = np.zeros((512, 512, 3) dtype=np.uint8)
            for _ in range(2):
                _ = preview_ai_instance.AI_orchestration(dummy_input)

            current_loaded_model = model_name
            info_message.set(f"Model: {model_name} Ready!")
            print(f"{model_name} loaded successfully")
        except Exception as e:
            info_message.set(f"Model load failed: {str(e)}")
            current_loaded_model = None
            preview_ai_instance = None


def select_AI_multithreading_from_menu(selected_option: str) -> None:
    global selected_AI_multithreading
    if selected_option == "Disabled":
        selected_AI_multithreading = 1
    else: 
        selected_AI_multithreading = int(selected_option.split()[0])


def select_interpolation_from_menu(selected_option: str) -> None:
    global selected_interpolation_factor

    match selected_option:
        case "Disabled":
            selected_interpolation_factor = 0
        case "Low":
            selected_interpolation_factor = 0.3
        case "Medium":
            selected_interpolation_factor = 0.5
        case "High":
            selected_interpolation_factor = 0.7

def select_gpu_from_menu(selected_option: str) -> None:
    global selected_gpu    
    selected_gpu = selected_option
    
def select_save_frame_from_menu(selected_option: str):
    global selected_keep_frames
    if   selected_option == 'Enabled':  selected_keep_frames = True
    elif selected_option == 'Disabled': selected_keep_frames = False

def select_image_extension_from_menu(selected_option: str) -> None:
    global selected_image_extension   
    selected_image_extension = selected_option
    
def select_video_extension_from_menu(selected_option: str) -> None:
    global selected_video_extension   
    selected_video_extension = selected_option














# GUI info functions ---------------------------
def open_info_output_path():
    option_list = [
        "\n The default path is defined by the input files."
        + "\n For example uploading a file from the Download folder,"
        + "\n the app will save the generated files in the Download folder \n",

        " Otherwise it is possible to select the desired path using the SELECT button",
    ]

    MessageBox(
        messageType   = "info",
        title         = "Output path",
        subtitle      = "This widget allows to choose upscaled files path",
        default_value = default_output_path,
        option_list   = option_list
    )

def open_info_AI_model():
    option_list = [
        "\n IRCNN (2017) - Very simple and lightweight AI architecture\n" + 
        " Only denoising (no upscaling)\n" + 
        " Recommended for both image/video denoising\n" + 
        "  • IRCNN_Mx1 - (medium denoise)\n" +
        "  • IRCNN_Lx1 - (high denoise)\n",

        "\n SRVGGNetCompact (2022) - Fast and lightweight AI architecture\n" + 
        " Good-quality upscale\n" + 
        " Recommended for video upscaling\n" + 
        "  • RealESR_Gx4\n" + 
        "  • RealSRx4_Anime\n",

        "\n RRDB (2020) - Complex and heavy AI architecture\n" + 
        " High-quality upscale\n" + 
        " Recommended for image upscaling\n" +
        "  • BSRGANx2\n" + 
        "  • BSRGANx4\n" +
        "  • RealESRGANx4\n",

    ]

    MessageBox(
        messageType = "info",
        title       = "AI model",
        subtitle    = "This widget allows to choose between different AI models for upscaling",
        default_value = default_AI_model,
        option_list   = option_list
    )

def open_info_gpu():
    option_list = [
        "\n It is possible to select up to 4 GPUs, via the index (also visible in the Task Manager):\n" +
        "  • Auto (the app will select the most powerful GPU)\n" + 
        "  • GPU 1 (GPU 0 in Task manager)\n" + 
        "  • GPU 2 (GPU 1 in Task manager)\n" + 
        "  • GPU 3 (GPU 2 in Task manager)\n" + 
        "  • GPU 4 (GPU 3 in Task manager)\n",

        "\n NOTES\n" +
        "  • Keep in mind that the more powerful the chosen gpu is, the faster the upscaling will be\n" +
        "  • For optimal performance, it is essential to regularly update your GPUs drivers\n" +
        "  • Selecting the index of a GPU not present in the PC will cause the app to use the CPU for AI operations\n"+
        "  • In the case of a single GPU, select 'GPU 1' or 'Auto'\n"
    ]

    MessageBox(
        messageType = "info",
        title       = "GPU",
        subtitle    = "This widget allows to select the GPU for AI upscale",
        default_value = default_gpu,
        option_list   = option_list
    )


def open_info_audio_mode(): 
    option_list = [
        "Audio Mode Options:"
        "\n • Audio Enhancement: Improve overall sound quality, reducing background noise and clarifying audio details.\n" +
        "   • Vocal Isolation: Separate and isolate vocals from the background music or environment, allowing you to emphasize or remove singing or speech.\n"
    ]
    
    MessageBox(
        messageType= "info",
        title = "Audio Enchancement",
        subtitle = "This Widget allows to choose Vocal isolation or Audio Enchancement",
        default_value = default_audio_mode,
        option_list = option_list
    )
    

def open_info_keep_frames():
    option_list = [
        "\n ENABLED \n" + 
        " The app does not delete the video frames after creating the upscaled video \n",

        "\n DISABLED \n" + 
        " The app deletes the video frames after creating the upscaled video \n"
    ]

    MessageBox(
        messageType   = "info",
        title         = "Keep frames",
        subtitle      = "This widget allows to choose to keep video frames",
        default_value = None,
        option_list   = option_list
    )
    

def open_info_AI_interpolation():
    option_list = [
        " Interpolation is the fusion of the upscaled image produced by AI and the original image",

        " \n INTERPOLATION OPTIONS\n" +
        "  • Disabled - 100% upscaled\n" + 
        "  • Low - 30% original / 70% upscaled\n" +
        "  • Medium - 50% original / 50% upscaled\n" +
        "  • High - 70% original / 30% upscaled\n",

        " \n NOTES\n" +
        "  • Can increase the quality of the final result\n" + 
        "  • Especially when using the tilling/merging function (with low VRAM)\n" +
        "  • Especially at low Input resolution % values (<50%) \n",

    ]

    MessageBox(
        messageType = "info",
        title       = "AI Interpolation", 
        subtitle    = "This widget allows to choose interpolation between upscaled and original image/frame",
        default_value = default_interpolation,
        option_list   = option_list
    )

def open_info_AI_multithreading():
    option_list = [
        " This option can improve video upscaling performance, especially with powerful GPUs",

        " \n AI MULTITHREADING OPTIONS\n"
        + "  • 1 threads - upscaling 1 frame\n" 
        + "  • 2 threads - upscaling 2 frame simultaneously\n" 
        + "  • 3 threads - upscaling 3 frame simultaneously\n" 
        + "  • 4 threads - upscaling 4 frame simultaneously\n" ,

        " \n NOTES \n"
        + "  • As the number of threads increases, the use of CPU, GPU and RAM memory also increases\n" 
        + "  • In particular, the GPU is put under a lot of stress, and may reach high temperatures\n" 
        + "  • Keep an eye on the temperature of your PC so that it doesn't overheat \n" 
        + "  • The app selects the most appropriate number of threads if the chosen number exceeds GPU capacity\n" ,

    ]

    MessageBox(
        messageType = "info",
        title       = "AI multithreading", 
        subtitle    = "This widget allows to choose how many video frames are upscaled simultaneously",
        default_value = default_AI_multithreading,
        option_list   = option_list
    )

def open_info_image_output():
    option_list = [
        " \n PNG\n  • very good quality\n  • slow and heavy file\n  • supports transparent images\n",
        " \n JPG\n  • good quality\n  • fast and lightweight file\n",
        " \n BMP\n  • highest quality\n  • slow and heavy file\n",
        " \n TIFF\n  • highest quality\n  • very slow and heavy file\n",
    ]

    MessageBox(
        messageType = "info",
        title       = "Image output",
        subtitle    = "This widget allows to choose the extension of upscaled images",
        default_value = default_image_extension,
        option_list   = option_list
    )

def open_info_video_extension():
    option_list = [
        "\n MP4 (x264)\n" + 
        "   • produces well compressed video using x264 codec\n",

        "\n MP4 (x265)\n" + 
        "   • produces well compressed video using x265 codec\n",

        "\n AVI\n" + 
        "   • produces the highest quality video\n" +
        "   • the video produced can also be of large size\n"
    ]

    MessageBox(
        messageType = "info",
        title = "Video output",
        subtitle = "This widget allows to choose the extension of the upscaled video",
        default_value = default_video_extension,
        option_list = option_list
    )

def open_info_vram_limiter():
    option_list = [
        " It is important to enter the correct value according to the VRAM of selected GPU ",
        " Selecting a value greater than the actual amount of GPU VRAM may result in upscale failure",
        " For integrated GPUs (Intel-HD series • Vega 3,5,7) - select 2 GB",
    ]

    MessageBox(
        messageType = "info",
        title       = "GPU Vram (GB)",
        subtitle    = "This widget allows to set a limit on the GPU VRAM memory usage",
        default_value = default_VRAM_limiter,
        option_list   = option_list
    )

def open_info_input_resolution():
    option_list = [
        " A high value (>70%) will create high quality photos/videos but will be slower",
        " While a low value (<40%) will create good quality photos/videos but will much faster",

        " \n For example, for a 1080p (1920x1080) image/video\n" + 
        " • Input resolution 25% => input to AI 270p (480x270)\n" +
        " • Input resolution 50% => input to AI 540p (960x540)\n" + 
        " • Input resolution 75% => input to AI 810p (1440x810)\n" + 
        " • Input resolution 100% => input to AI 1080p (1920x1080) \n",
    ]

    MessageBox(
        messageType = "info",
        title       = "Input resolution %",
        subtitle    = "This widget allows to choose the resolution input to the AI",
        default_value = default_resize_factor,
        option_list   = option_list
    )

def open_info_cpu():
    option_list = [
        " When possible the app will use the number of cpus selected",

        "\n Currently this value is used for: \n" +
        "  • video frames extraction \n" +
        "  • video encoding \n",
    ]

    MessageBox(
        messageType = "info",
        title       = "Cpu number",
        subtitle    = "This widget allows to choose how many cpus to devote to the app",
        default_value = default_cpu_number,
        option_list   = option_list
    )









def create_placeholder_image(width, height):
    img = Image.new('RGB', (width, height), color='#000000')
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", 100)
    except IOError:
        font = ImageFont.load_default()
    text = "?"
    text_width = draw.textlength(text, font=font)
    text_height = font.size
    x = (width - text_width) // 2
    y = (height - text_height) // 2
    draw.text((x, y), text, fill="#FFFFFF", font=font)
    return img



# GUI place functions ---------------------------
def place_loadFile_section(window):
    background = CTkFrame(master = window, fg_color = background_color, corner_radius = 1)

    global preview_frame_button, original_preview, upscaled_preview, input_file_button
    
    window.preview_frame = CTkFrame(
    master=window,
    width=800,
    height=445,
    fg_color=dark_color,
    corner_radius=10
    )
    window.preview_frame.place(relx=0.80, rely=0.215, anchor="center")


    # Create placeholder images
    placeholder_img = create_placeholder_image(340, 400)
    placeholder_photo = CTkImage(placeholder_img, size=(350, 370))

    # Create container
    container = CTkFrame(window.preview_frame, fg_color=dark_color)
    container.pack(pady=20, padx=20, fill='both', expand=True)

    # Original frame with placeholder
    original_frame = CTkFrame(container, fg_color=dark_color)
    original_frame.pack(side='left', fill='both', expand=True, padx=10)
    CTkLabel(original_frame, text="Original", font=bold14, text_color=app_name_color).pack(pady=5)
    original_preview = CTkLabel(original_frame, image=placeholder_photo, text="")
    original_preview.pack()

    # Upscaled frame with placeholder
    upscaled_frame = CTkFrame(container, fg_color=dark_color)
    upscaled_frame.pack(side='right', fill='both', expand=True, padx=10)
    CTkLabel(upscaled_frame, text="Upscaled Preview", font=bold14, text_color=app_name_color).pack(pady=5)
    upscaled_preview = CTkLabel(upscaled_frame, image=placeholder_photo, text="")
    upscaled_preview.pack()
    
    input_file_button = CTkButton(
        master = window,
        command  = open_files_action,
        text     = "SELECT FILES",
        width    = 140,
        height   = 30,
        font     = bold11,
        border_width = 1,
        fg_color     = "#282828",
        text_color   = "#E0E0E0",
        border_color = "#0096FF"
        )
    background.place(relx = 0.0, rely = 0.0, relwidth = 1.0, relheight = 0.42)
    input_file_button.place(relx = 0.55, rely = 0.4, anchor = "center")


def place_output_path_textbox():
    output_path_button  = create_info_button(open_info_output_path, "Output path", width = 300)
    output_path_textbox = create_text_box_output_path(selected_output_path) 
    select_output_path_button = create_active_button(
        command = open_output_path_action,
        text    = "SELECT",
        width   = 85,
        height  = 25,

    )



  
    output_path_button.place(relx = column1_5_x - 0.37, rely = row0_y + 0.47, anchor = "center")
    output_path_textbox.place(relx = column1_5_x - 0.53, rely  = row0_y + 0.47, anchor = "center")
    select_output_path_button.place(relx = column2_x - 0.41, rely  = row0_y + 0.47, anchor = "center")

def place_AI_menu():
    AI_menu_button = create_info_button(open_info_AI_model, "AI model")
    AI_menu        = create_option_menu(select_AI_from_menu, AI_models_list, default_AI_model)

    AI_menu_button.place(relx = column0_x - 0.15, rely = row1_y - 0.05, anchor = "center")
    AI_menu.place(relx = column0_x- 0.15, rely = row1_y, anchor = "center")

def place_AI_interpolation_menu():
    interpolation_button = create_info_button(open_info_AI_interpolation, "AI Interpolation")
    interpolation_menu   = create_option_menu(select_interpolation_from_menu, interpolation_list, default_interpolation)
    
    interpolation_button.place(relx = column0_x- 0.15, rely = row3_y - 0.05, anchor = "center")
    interpolation_menu.place(relx = column0_x- 0.15, rely  = row3_y, anchor = "center")
 

def place_AI_multithreading_menu():
    AI_multithreading_button = create_info_button(open_info_AI_multithreading, "AI multithreading")
    AI_multithreading_menu   = create_option_menu(select_AI_multithreading_from_menu, AI_multithreading_list, default_AI_multithreading)
    
    AI_multithreading_button.place(relx = column0_x- 0.15, rely = row2_y - 0.05, anchor = "center")
    AI_multithreading_menu.place(relx = column0_x- 0.15, rely  = row2_y, anchor = "center")


def place_input_resolution_textbox():
    resize_factor_button  = create_info_button(open_info_input_resolution, "Input resolution %")
    resize_factor_textbox = create_text_box(selected_input_resize_factor) 

    resize_factor_button.place(relx=column1_x- 0.35,rely=row4_y - 0.05,anchor="center")
    resize_factor_textbox.place(relx=column1_x- 0.35,rely=row4_y,anchor="center")


def place_gpu_menu():
    gpu_button = create_info_button(open_info_gpu, "GPU")
    gpu_menu   = create_option_menu(select_gpu_from_menu, gpus_list, default_gpu)
    
    gpu_button.place(relx = column1_x- 0.35, rely = row1_y - 0.053, anchor = "center")
    gpu_menu.place(relx = column1_x- 0.35, rely  = row1_y, anchor = "center")


def place_vram_textbox():
    vram_button  = create_info_button(open_info_vram_limiter, "GPU Vram (GB)")
    vram_textbox = create_text_box(selected_VRAM_limiter) 
  
    vram_button.place(relx = column1_x- 0.35, rely = row2_y - 0.05, anchor = "center")
    vram_textbox.place(relx = column1_x- 0.35, rely  = row2_y, anchor = "center")


def place_cpu_textbox():
    cpu_button  = create_info_button(open_info_cpu, "CPU number")
    cpu_textbox = create_text_box(selected_cpu_number)

    cpu_button.place(relx = column1_x- 0.35, rely = row3_y - 0.05, anchor = "center")
    cpu_textbox.place(relx = column1_x- 0.35, rely  = row3_y, anchor = "center")

    
def place_Audio_Selection_menu():
    audio_mode_button = create_info_button(open_info_audio_mode,"Audio Mode",width=150)
    Audio_mode_menu = create_option_menu(select_audio_mode_from_menu,audio_mode_list,default_audio_mode)
  
    audio_mode_button.place( relx = column0_x- 0.15, rely = row4_y - 0.05, anchor = "center")
    Audio_mode_menu.place(relx = column0_x- 0.15, rely = row4_y, anchor = "center")


def place_keep_frames_menu():
    keep_frames_button = create_info_button(open_info_keep_frames, "Keep frames")
    keep_frames_menu   = create_option_menu(select_save_frame_from_menu, keep_frames_list, default_keep_frames)
    
    keep_frames_button.place(relx = column1_x- 0.4, rely = row4_y - 0.053, anchor = "center")
    keep_frames_menu.place(relx = column1_x- 0.4, rely = row4_y, anchor = "center")
    

def place_image_output_menu():
    file_extension_button = create_info_button(open_info_image_output, "Image output")
    file_extension_menu   = create_option_menu(select_image_extension_from_menu, image_extension_list, default_image_extension)
    
    file_extension_button.place(relx = column2_x- 0.6277, rely = row1_y - 0.1455, anchor = "center")
    file_extension_menu.place(relx = column2_x- 0.63, rely = row1_y -0.1, anchor = "center")

def place_video_extension_menu():
    video_extension_button = create_info_button(open_info_video_extension, "Video output")
    video_extension_menu   = create_option_menu(select_video_extension_from_menu, video_extension_list, default_video_extension)
    
    video_extension_button.place(relx = column2_x- 0.71, rely = row2_y - 0.25, anchor = "center")
    video_extension_menu.place(relx = column2_x- 0.71, rely = row2_y - 0.205, anchor = "center")



def place_message_label():
    message_label = CTkLabel(
        master  = window, 
        textvariable = info_message,
        height       = 25,
        font         = bold11,
        fg_color     = "#ffbf00",
        text_color   = "#000000",
        anchor       = "center",
        corner_radius = 12
    )
    message_label.place(relx = column2_x - 0.23, rely = row4_y - 0.615, anchor = "center")

def place_stop_button(): 
    stop_button = create_active_button(
        command = stop_button_command,
        text    = "STOP",
        icon    = stop_icon,
        width   = 140,
        height  = 30,
        border_color = "#EC1D1D"
    )
    stop_button.place(relx = column2_x- 0.475 , rely = row4_y , anchor = "center")

def place_upscale_button(): 
    upscale_button = create_active_button(
        command = upscale_button_command,
        text    = "UPSCALE",
        icon    = upscale_icon,
        width   = 140,
        height  = 30
    )
    upscale_button.place(relx = column2_x - 0.23, rely = row4_y - 0.575, anchor = "center")
   
def create_option_background():
    return CTkFrame(
        master   = window,
        bg_color = background_color,
        fg_color = widget_background_color,
        height   = 46,
        corner_radius = 10
    )

def place_input_output_resolution_textboxs():

    def open_info_input_resolution():
        option_list = [
            " A high value (>70%) will create high quality photos/videos but will be slower",
            " While a low value (<40%) will create good quality photos/videos but will much faster",

            " \n For example, for a 1080p (1920x1080) image/video\n" + 
            " • Input resolution 25% => input to AI 270p (480x270)\n" +
            " • Input resolution 50% => input to AI 540p (960x540)\n" + 
            " • Input resolution 75% => input to AI 810p (1440x810)\n" + 
            " • Input resolution 100% => input to AI 1080p (1920x1080) \n",
        ]

        MessageBox(
            messageType   = "info",
            title         = "Input resolution %",
            subtitle      = "This widget allows to choose the resolution input to the AI",
            default_value = None,
            option_list   = option_list
        )



    widget_row = row4_y

    background = create_option_background()
    background.place(relx = 0.75, rely = widget_row, relwidth = 0.48, anchor = "center")

    # Input resolution %
    info_button = create_info_button(open_info_input_resolution, "Input resolution")
    option_menu = create_text_box(selected_input_resize_factor, width = little_textbox_width) 

    info_button.place(relx = column_info1, rely = widget_row - 0.003, anchor = "center")
    option_menu.place(relx = column_1_5,   rely = widget_row,         anchor = "center")



    info_button.place(relx = column_info2, rely = widget_row - 0.003, anchor = "center")
    option_menu.place(relx = column_3,     rely = widget_row,         anchor = "center")


global youtube_progress_var
def place_youtube_download_menu():
    global youtube_link_entry, youtube_output_path_entry
    bg_image = Image.open("./Assets/111.jpg").resize((500, 150))  
    bg_image_tk = CTkImage(bg_image, size=(500, 150))  

    youtube_frame = CTkFrame(
        master=window,
        fg_color=dark_color,
        width=500,
        height=150,
        corner_radius=10
    )
    youtube_frame.place(relx=0.3295, rely=0.493, anchor="center")


    bg_label = CTkLabel(
        master=youtube_frame,
        image=bg_image_tk,
        width=500,
        height=150
    )
    bg_label.place(relx=0, rely=0)  
    bg_label.image = bg_image_tk



    progress_label =CTkLabel(
        master=youtube_frame,
        textvariable=youtube_progress_var,
        font=bold12,
        text_color="#00FF00"
    )
    progress_label.place(relx=0.95, rely=0.3, anchor="center")


    #input for the youtubelink
    CTkLabel(
        master=youtube_frame,
        text="YouTube URL:",
        font=bold12,
        text_color="#C0C0C0",
    ).place(relx=0.18, rely=0.2, anchor="w")

    youtube_link_entry = CTkEntry(
        master=youtube_frame,
        width=300,
        height=25,
        corner_radius=5,
        font=bold11
    ).place(relx=0.18, rely=0.45, anchor="w")

    CTkLabel(
        master=youtube_frame,
        text="Save to:",
        font=bold12,
        text_color="#C0C0C0",
    ).place(relx=0.18, rely=0.65, anchor="w")

    youtube_output_path_entry = CTkEntry(
        master=youtube_frame,
        width=200,
        height=25,
        corner_radius=5,
        font=bold11
    )
    youtube_output_path_entry.place(relx=0.18, rely=0.8, anchor="w")
    youtube_output_path_entry.insert(0,DOCUMENT_PATH)

    CTkButton(
        master=youtube_frame,
        text="Choose path",
        width=80,
        height=25,
        font=bold11,
        command=lambda: select_youtube_output_path()
    ).place(relx=0.8, rely=0.83, anchor="w")


    CTkButton(
        master=youtube_frame,
        text="Download",
        width=80,
        height=30,
        font=bold11,
        command=lambda: start_youtube_download(),
        fg_color="#282828",
        border_color="#0096FF",
        border_width=1
    ).place(relx=0.96, rely=0.45, anchor="e")

def select_youtube_output_path():
    path= filedialog.askdirectory()
    if path:
        youtube_output_path_entry.delete(0,'end')
        youtube_output_path_entry.insert(0,path)




####YOUTUBE DOWNLOADING####
def download_youtube_link(youtube_url,output_path, progress_callback=None):
    ydl_opts ={
        "outtmpl": f'{output_path}/%(title)s.%(ext)s',
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
        'progress_hooks': [progress_callback] if progress_callback else [],
        'noprogress': True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
             ydl.download([youtube_url])
        return "Download Complete!"
    except Exception as e:
        return f"Error: {str(e)}"
    
def update_progress(d):
    if d['status'] == 'downloading':
        percent = d.get('_percent_str', '0%')
        window.after(0, lambda: youtube_progress_var.set(percent))

def download_thread(youtube_url, output_path):
    try:
        info_message.set("Downloading....")
        success, message = download_youtube_link(youtube_url, output_path, update_progress)
        if success:
            info_message.set(message)
        else: info_message.set(message)
    except Exception as e:
        info_message.set(f"Error: {str(e)}")
    finally:
        youtube_progress_var.set("")

def start_youtube_download():
    url=youtube_link_entry.get()
    output_path = youtube_output_path_entry.get()

    if not url or 'youtube.com' not in url and 'youtube.be' not in url:
        info_message.set("Invalid YouTube URL!")
        return
    
    if not output_path:
        info_message.set("Choose a folder for saving!")
        return
    
    youtube_progress_var.set("0%")
    Thread(target=download_thread, args=(url, output_path)).start()

        




# Main functions ---------------------------
def on_app_close() -> None:
    window.grab_release()
    window.destroy()

    global selected_AI_model
    global selected_AI_multithreading
    global selected_gpu
    global selected_interpolation_factor
    global selected_image_extension
    global selected_video_extension
    global tiles_resolution
    global input_resize_factor
    global cpu_number
    global selected_audio_mode 

    AI_model_to_save          = f"{selected_AI_model}"
    AI_multithreading_to_save = f"{selected_AI_multithreading} threads"
    gpu_to_save               = selected_gpu
    keep_frames_to_save = "Enabled" if selected_keep_frames == True else "Disabled"
    image_extension_to_save   = selected_image_extension
    video_extension_to_save   = selected_video_extension
    
    interpolation_to_save= {
        0: "Disabled",
        0.3: "Low",
        0.5: "Medium",
        0.7: "High",
    }.get(selected_interpolation_factor)
    
    Audio_option_to_save = {
        0: "Disabled",
        1: "Vocal Isolation",
        2: "Audio Enchancement",
    }.get(selected_audio_mode)

    user_preference = {
        "default_AI_model":          AI_model_to_save,
        "default_AI_multithreading": AI_multithreading_to_save,
        "default_gpu":               gpu_to_save,
        "default_keep_frames":       keep_frames_to_save,
        "default_image_extension":   image_extension_to_save,
        "default_video_extension":   video_extension_to_save,
        "default_interpolation":     interpolation_to_save,
        "default_audio_mode":         Audio_option_to_save,
        "default_output_path":       selected_output_path.get(),
        "default_resize_factor":     str(selected_input_resize_factor.get()),
        "default_VRAM_limiter":      str(selected_VRAM_limiter.get()),
        "default_cpu_number":        str(selected_cpu_number.get()),
    }
    user_preference_json = json_dumps(user_preference)
    with open(USER_PREFERENCE_PATH, "w") as preference_file:
        preference_file.write(user_preference_json)

    stop_upscale_process()
    
    

    
    
    
class App():
    def __init__(self, Master):
        self.toplevel_window = None
        Master.protocol("WM_DELETE_WINDOW", on_app_close)
        Master.title('LearnReflect Video Enchancer')
        Master.geometry("1920x1080")
        Master.resizable(False, False)
        Master.iconbitmap(find_by_relative_path("Assets" + os_separator + "logo.ico"))
        self.bg_image = CTkImage(Image.open("Assets" + os_separator + "321.png"),size=(1920, 1080))
        self.background_label = CTkLabel(Master, image=self.bg_image, fg_color="black")
        self.background_label.place(relx=0  , rely=0, relwidth=1, relheight=1.5) 
        self.background_label.lower() 
      

        place_youtube_download_menu()
        place_loadFile_section(Master)
        place_output_path_textbox()
        place_AI_menu()
        place_AI_multithreading_menu()
        place_AI_interpolation_menu()
        place_Audio_Selection_menu()
        place_gpu_menu()
        place_vram_textbox()
        place_cpu_textbox()
        place_input_resolution_textbox()
        place_image_output_menu()
        place_video_extension_menu()
        place_message_label()
        place_upscale_button()
    

        
        
if __name__ == "__main__":
    

    multiprocessing_freeze_support()
    set_appearance_mode("Dark")
    set_default_color_theme("dark-blue")
    

    window = CTk() 
    # Set background color to black

    youtube_progress_var = StringVar()
    processing_queue = multiprocessing_Queue(maxsize=1)
    info_message            = StringVar()
    selected_output_path    = StringVar()
    selected_input_resize_factor  = StringVar()
    selected_VRAM_limiter   = StringVar()
    selected_cpu_number     = StringVar()


    global selected_file_list
    global selected_AI_model
    global selected_gpu
    global selected_keep_frames
    global selected_AI_multithreading
    global selected_image_extension
    global selected_video_extension
    global selected_interpolation_factor
    global tiles_resolution
    global input_resize_factor
    global cpu_number

    selected_file_list = []

    selected_AI_model          = default_AI_model
    selected_gpu               = default_gpu
    selected_image_extension   = default_image_extension
    selected_video_extension   = default_video_extension
    selected_AI_multithreading = int(default_AI_multithreading.split()[0])
    
    selected_keep_frames = True if default_keep_frames == "Enabled" else False

    selected_interpolation_factor = {
        "Disabled": 0,
        "Low": 0.3,
        "Medium": 0.5,
        "High": 0.7,
    }.get(default_interpolation)
    

    selected_input_resize_factor.set(default_resize_factor)
    selected_VRAM_limiter.set(default_VRAM_limiter)
    selected_cpu_number.set(default_cpu_number)
    selected_output_path.set(default_output_path)

    info_message.set("AI upscaling Ready")
    selected_input_resize_factor.trace_add('write', update_file_widget)


    font   = "Segoe UI"    
    bold8  = CTkFont(family = font, size = 8, weight = "bold")
    bold9  = CTkFont(family = font, size = 9, weight = "bold")
    bold10 = CTkFont(family = font, size = 10, weight = "bold")
    bold11 = CTkFont(family = font, size = 11, weight = "bold")
    bold12 = CTkFont(family = font, size = 12, weight = "bold")
    bold13 = CTkFont(family = font, size = 13, weight = "bold")
    bold14 = CTkFont(family = font, size = 14, weight = "bold")
    bold16 = CTkFont(family = font, size = 16, weight = "bold")
    bold17 = CTkFont(family = font, size = 17, weight = "bold")
    bold18 = CTkFont(family = font, size = 18, weight = "bold")
    bold19 = CTkFont(family = font, size = 19, weight = "bold")
    bold20 = CTkFont(family = font, size = 20, weight = "bold")
    bold21 = CTkFont(family = font, size = 21, weight = "bold")
    bold22 = CTkFont(family = font, size = 22, weight = "bold")
    bold23 = CTkFont(family = font, size = 23, weight = "bold")
    bold24 = CTkFont(family = font, size = 24, weight = "bold")
    stop_icon      = CTkImage(pillow_image_open(find_by_relative_path(f"Assets{os_separator}stop_icon.png")),      size=(15, 15))
    upscale_icon   = CTkImage(pillow_image_open(find_by_relative_path(f"Assets{os_separator}upscale_iconLR.png")),   size=(15, 15))
    clear_icon     = CTkImage(pillow_image_open(find_by_relative_path(f"Assets{os_separator}clear_icon.png")),     size=(15, 15))
    info_icon      = CTkImage(pillow_image_open(find_by_relative_path(f"Assets{os_separator}info_icon.png")),      size=(17, 17))
    
    
    
    app = App(window)#Creates an instance of the App class. Passes the window object (the main GUI window) to the App class so it can set it up.
    window.update()#Refreshes the window to ensure that all updates (like layouts and text) are visible.
    window.mainloop()#Starts the GUI's event loop, which keeps the window open and responsive. This is where the program "waits" for the user to interact with the window (like clicking a button).
