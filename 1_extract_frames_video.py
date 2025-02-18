'''
script collect up to max_frame_count number of frame per video 
'''
import cv2
import os 
import uuid
import shutil 
import os
import time 
import yaml
import time 
from unidecode import unidecode
import yaml
from tqdm import tqdm

def find_all_video_paths(folder_path: str) -> list[str]:
    # List of common video file extensions
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv']
    video_paths = []
    # Walk through the folder to find video files
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if any(file.lower().endswith(ext) for ext in video_extensions):
                video_paths.append(os.path.join(root, file))
    return video_paths

def find_all_image_paths(folder_path: str) -> list[str]:
    # List of common video file extensions
    video_extensions = ['.jpg', '.png', '.jpeg']
    video_paths = []
    # Walk through the folder to find video files
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if any(file.lower().endswith(ext) for ext in video_extensions):
                video_paths.append(os.path.join(root, file))
    return video_paths

def start_video(video_path: str):
    video_capture = cv2.VideoCapture(video_path)
    total_frames = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
    # Check if video is opened correctly
    if not video_capture.isOpened():
        print("Error: Could not open video.")
        exit()
    return video_capture, total_frames

def calculate_capture_rate(total_frames: int, max_frame_count: int) -> int:
    num_capture_rate = int(total_frames / max_frame_count)        
    if num_capture_rate == 0:
        num_capture_rate = 1
    print ( "NUM CAPTURE RATE: " + str(num_capture_rate))
    return num_capture_rate

def create_save_video_folder(output_folder: str, video_path:str) -> str:
    t = unidecode(os.path.basename(video_path).split(".")[0]).replace('"', '').replace("'", '')
    save_video_folder_name = os.path.basename(os.path.dirname(video_path)) + '____' + str(t)
    save_video_folder = os.path.join(output_folder, save_video_folder_name)
    os.makedirs(save_video_folder, exist_ok=True)
    return save_video_folder

def process_video(video_capture, num_capture_rate: int, max_frame_count:int, save_video_folder: str) -> None:
    frame_count = 0
    extracted_frame_count = 0
    while True:
        # Read the next frame
        ret, frame = video_capture.read()
        if not ret:
            break  # Exit loop when video ends
        if frame_count % num_capture_rate == 0:  # Capture every 4th frame
            # Save the frame as an image
            cv2.imwrite(os.path.join(save_video_folder, f'{extracted_frame_count}.jpg'), frame)
            print(f"Image extracted and saved as '{extracted_frame_count}.jpg'.")
            extracted_frame_count += 1
        frame_count += 1
        if extracted_frame_count >= max_frame_count:
            break
    # Release the video capture object
    video_capture.release()

def main(data: dict, output_folder: str):
    """
    given a folder 
    get all videos in the folder/subfolder/...
    extract frame per video
    save frames of 1 video to 1 folder 
    """
    max_frame_count = data["MAX_FRAME_COUNT"]
    folder_path = data["SOURCE_FOLDER_HAVE_VIDEOS"]
    ls_video_path = find_all_video_paths(folder_path)

    for video_path in tqdm(ls_video_path, total=len(ls_video_path)):
            video_capture, total_frames = start_video(video_path)
            num_capture_rate = calculate_capture_rate(total_frames, max_frame_count)
            save_video_folder = create_save_video_folder(output_folder, video_path)
            process_video(video_capture, num_capture_rate, max_frame_count, save_video_folder)


if __name__ == "__main__":
    for folder_path in ["1_extracted_frames", "2_dest_folder", "3_AI_label"]:
        if os.path.exists(folder_path):
            # Remove the folder and its contents
            shutil.rmtree(folder_path)
            print(f"The folder {folder_path} has been removed.")

    with open("config.yaml", "r") as file:
        data = yaml.safe_load(file)
    output_folder = "1_extracted_frames"

    main(data, output_folder)




