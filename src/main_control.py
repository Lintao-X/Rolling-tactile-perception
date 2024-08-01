from recording_contours import process_frames
from camera_capture import capture_frames
import os
import time
from multiprocessing import Process, Queue

import stitching_auto
from predict import predict_image


def clear_directory(directory):
    # clear
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.remove(file_path)
    print(f"Cleared directory: {directory}")

def main():
    save_dir = 'your_dir'
    frame_queue = Queue(maxsize=10)


    clear_directory(save_dir)

    # run camera recording and contour detection
    capture_process = Process(target=capture_frames, args=(frame_queue,))
    process_process = Process(target=process_frames, args=(frame_queue, save_dir))

    capture_process.start()
    process_process.start()

    # terminate after 10s
    time.sleep(10)

    capture_process.terminate()
    process_process.terminate()

    capture_process.join()
    process_process.join()

    # run stitching_auto.py and record consuming time
    start_stitch_time = time.time()

    stitching_auto.stitch_images(save_dir)

    end_stitch_time = time.time()
    stitch_duration = end_stitch_time - start_stitch_time
    print(f"Stitching images took {stitch_duration:.2f} seconds")

    # run predict.py and record consuming time
    start_predict_time = time.time()

    predict_image()

    end_predict_time = time.time()
    predict_duration = end_predict_time - start_predict_time
    print(f"Prediction took {predict_duration:.2f} seconds")

if __name__ == '__main__':
    main()