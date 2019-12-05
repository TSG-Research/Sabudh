import numpy as np
import pandas as pd
import time
import cv2
# import argparse
import numpy as np
import matplotlib.pyplot as plt
import imutils
import argparse


def get_output_layers(net):
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    return output_layers

def draw_prediction(img, class_id, confidence, x, y, x_plus_w, y_plus_h):
    label = str(classes[class_id])
    color = COLORS[class_id]
    cv2.rectangle(img, (x,y), (x_plus_w,y_plus_h), color, 2)
    cv2.putText(img, label, (x-5,y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)
def get_output_layers(net):
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    return output_layers

def draw_prediction(img, class_id, confidence, x, y, x_plus_w, y_plus_h):
    label = str(classes[class_id])
    color = COLORS[class_id]
    cv2.rectangle(img, (x,y), (x_plus_w,y_plus_h), color, 2)
    cv2.putText(img, label, (x-5,y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)

a=0
start_time = time.time()

Width = image.shape[1]
Height = image.shape[0]
scale = 0.00392
   
classes = None

with open('/content/gdrive/My Drive/Yolo/coco.names', 'r') as f:
    classes = [line.strip() for line in f.readlines()]

COLORS = np.random.uniform(0, 255, size=(len(classes), 3))

net = cv2.dnn.readNet("/content/gdrive/My Drive/Yolo/yolov3.weights", "/content/gdrive/My Drive/Yolo/cfg/yolov3.cfg")

vs = cv2.VideoCapture('/content/gdrive/My Drive/Yolo/traffic.mkv')
writer = None
(W, H) = (None, None)
frameIndex = 0
try:
	# Uska
	prop = cv2.cv.CV_CAP_PROP_FRAME_COUNT if imutils.is_cv2() \
		else cv2.CAP_PROP_FRAME_COUNT
	total = int(vs.get(prop))
	print("[INFO] {} total frames in video".format(total))

# an error occurred while trying to determine the total
# number of frames in the video file
except:
	print("[INFO] could not determine # of frames in video")
	print("[INFO] no approx. completion time can be provided")
	total = -1

#_______________________________________________________________-

while True:
	# read the next frame from the file
	(grabbed, frame) = vs.read()

	# if the frame was not grabbed, then we have reached the end
	# of the stream
	if not grabbed:
		break

	# if the frame dimensions are empty, grab them
	if W is None or H is None:
		(H, W) = frame.shape[:2]
  # construct a blob from the input frame and then perform a forward
  blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416,416), (0,0,0), swapRB = True, crop =False)
  net.setInput(blob)
  outs = net.forward(get_output_layers(net))

  class_ids = []
  confidences = []
  boxes = []
  conf_threshold = 0.3
  nms_threshold = 0.3

  ncars=0
  for out in outs:
      for detection in out:
          scores = detection[5:]
          class_id = np.argmax(scores)
          confidence = scores[class_id]
            
          if confidence > 0.56:
              center_x = int(detection[0] * Width)
              center_y = int(detection[1] * Height)
              w = int(detection[2] * Width)
              h = int(detection[3] * Height)
              x = center_x - w / 2
              y = center_y - h / 2
              class_ids.append(class_id)
              confidences.append(float(confidence))
              boxes.append([x, y, w, h])
              ncars=ncars + 1

  idxs = cv2.dnn.NMSBoxes(boxes, confidences, args["confidence"], args["threshold"])
    
    dets = []
    if len(idxs) > 0:
      # loop over the indexes we are keeping
      for i in idxs.flatten():
        (x, y) = (boxes[i][0], boxes[i][1])
        (w, h) = (boxes[i][2], boxes[i][3])
        dets.append([x, y, x+w, y+h, confidences[i]])

    np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})
    dets = np.asarray(dets)
    tracks = tracker.update(dets)

    boxes = []
    indexIDs = []
    c = []
    previous = memory.copy()
    memory = {}

    for track in tracks:
      boxes.append([track[0], track[1], track[2], track[3]])
      indexIDs.append(int(track[4]))
      memory[indexIDs[-1]] = boxes[-1]

    if len(boxes) > 0:
      i = int(0)
      for box in boxes:
        # extract the bounding box coordinates
        (x, y) = (int(box[0]), int(box[1]))
        (w, h) = (int(box[2]), int(box[3]))

        # draw a bounding box rectangle and label on the image
        color = [int(c) for c in COLORS[classIDs[i]]]
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

        # color = [int(c) for c in COLORS[indexIDs[i] % len(COLORS)]]
        # cv2.rectangle(frame, (x, y), (w, h), color, 2)

  cv2.line(frame, line[0], line[1], (0, 255, 255), 5)

	if writer is None:
		# initialize our video writer
		fourcc = cv2.VideoWriter_fourcc(*"MJPG")
		writer = cv2.VideoWriter(args["output"], fourcc, 30,
			(frame.shape[1], frame.shape[0]), True)

		# some information on processing single frame
		if total > 0:
			elap = (end - start)
			print("[INFO] single frame took {:.4f} seconds".format(elap))
			print("[INFO] estimated total time to finish: {:.4f}".format(
				elap * total))

	# write the output frame to disk
	writer.write(frame)

	# increase frame index
	frameIndex += 1

print("--- %s number of objects in image---" %ncars)
print("--- %s seconds ---" % (time.time() - start_time))
# release the file pointers
print("[INFO] cleaning up...")
writer.release()
vs.release()
