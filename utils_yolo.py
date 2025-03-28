import os 
import cv2
import numpy as np
import torch 
print("CUDA is available:", torch.cuda.is_available())
import ultralytics
ultralytics.checks()
from ultralytics import YOLO

# model = YOLO("yolo11x-seg.pt")
model = YOLO("yolo11x.pt")
# Assuming `model` is your PyTorch model
model.to('cuda')

print('model on gpu' ,next(model.parameters()).is_cuda)

def inference(model, source_image):
    batch_yolo_result = model.predict(conf=0.2, source=source_image, save=False)
    for single_image_result in batch_yolo_result:
        img = np.copy(single_image_result.orig_img)
        for ci, single_object_result in enumerate(single_image_result):
            class_id = single_object_result.boxes.cls.tolist().pop()
            label = single_object_result.names[class_id]
            # get box confidence
            conf = single_object_result.boxes.conf.tolist().pop()
            # get box coordinate
            x1, y1, x2, y2 = single_object_result.boxes.xyxy.tolist()[0]
            # get crop image
            cropped_image = img[int(y1):int(y2), int(x1):int(x2)]
            
            # annotate
            cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 2)

            # Draw the stick line (vertical line pointing down)
            cv2.line(img, (int(x2), int(y2)), (int(x2), int(y2) + 40), (0, 0, 255), 2)

            # Add label text at the top of the stick
            text = label
            cv2.putText(img, text, (int(x2), int(y2) + 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (128, 0, 128), 2)
