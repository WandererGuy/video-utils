import cv2
import os

# Open the video stream
vcap = cv2.VideoCapture("rtsp://admin:TriNam@@@192.168.100.15:554/Streaming/Channels/101")

# Check if the stream is opened
if not vcap.isOpened():
    print("Error: Could not open the video stream.")
    exit()

# Create a directory to store the frames
output_dir = "frames"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

frame_count = 0  # Counter to name the files uniquely
import time 
while True:
    try:
        ret, frame = vcap.read()
    except:
        continue 
    
    if not ret:
        print("Error: Could not read the frame.")
        break

    # Show the video frame
    cv2.imshow('VIDEO', frame)

    # Save the frame as an image
    frame_filename = os.path.join(output_dir, f"frame_{frame_count}.jpg")
    if frame_count % 60 == 0:
        cv2.imwrite(frame_filename, frame)

    # Increment the frame counter
    frame_count += 1
    
    # Break on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close the display window
vcap.release()
cv2.destroyAllWindows()
