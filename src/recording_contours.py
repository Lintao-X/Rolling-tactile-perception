import cv2
import numpy as np
from multiprocessing import Process, Queue
import os

def process_frames(frame_queue, save_dir):
    prev_hsv = None
    contour_count = 0


    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    while True:
        if not frame_queue.empty():
            frame = frame_queue.get()

            # convert to HSV
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            # split
            h, s, v = cv2.split(hsv)

            # make difference
            if prev_hsv is not None:
                prev_v = cv2.split(prev_hsv)[2]
                diff_v = cv2.absdiff(v, prev_v)

                # binarization
                _, thresh = cv2.threshold(diff_v, 40, 255, cv2.THRESH_BINARY)

                # find contours
                contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                # contour count
                contour_count = len(contours)

                # set threshold for keyframe
                if contour_count > 100:
                    frame_count = len(os.listdir(save_dir))  # 获取当前保存的图像数量
                    filename = os.path.join(save_dir, f'frame_{frame_count:05d}.jpg')
                    cv2.imwrite(filename, frame)  # 保存图像
                    print("Recording begin.")
                else:
                    print("No Recording.")



                cv2.namedWindow('V Channel Diff with Contours', cv2.WINDOW_NORMAL)
                cv2.imshow('V Channel Diff with Contours', diff_v)


                print(f"Contour count: {contour_count}")

            # refresh prev_hsv
            prev_hsv = hsv


            cv2.namedWindow('Original Frame', cv2.WINDOW_NORMAL)
            cv2.imshow('Original Frame', frame)

            # 退出条件
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cv2.destroyAllWindows()

if __name__ == '__main__':
    save_dir = 'your_dir'
    frame_queue = Queue(maxsize=10)
    process_process = Process(target=process_frames, args=(frame_queue, save_dir))
    process_process.start()

