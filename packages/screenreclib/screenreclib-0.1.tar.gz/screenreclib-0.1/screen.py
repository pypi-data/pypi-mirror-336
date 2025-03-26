import pyautogui
import cv2
import numpy as np
import time
import threading

# Global variable to control recording
recording = False

def screen(fps=30.0, res=(1920, 1080), codec="XVID"):
    """
    Function to record the screen and save it as a video.

    Parameters:
        fps (float): Frames per second for the video. Default is 30.
        res (tuple): Resolution for the video. Default is (1920, 1080).
        codec (str): The codec used for video compression. Default is "XVID".
    """
    global recording
    # Specify video codec
    fourcc = cv2.VideoWriter_fourcc(*codec)

    # Name of the output file
    filename = "video.avi"

    # Creating a VideoWriter object
    out = cv2.VideoWriter(filename, fourcc, fps, res)

    # Start recording in a separate thread to avoid blocking
    def record():
        global recording
        try:
            while recording:
                # Take screenshot using PyAutoGUI
                img = pyautogui.screenshot()

                # Convert the screenshot to a numpy array
                frame = np.array(img)

                # Convert from BGR to RGB
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Write it to the output file
                out.write(frame)

                # Optional: Sleep to avoid 100% CPU usage
                time.sleep(1 / fps)
        except KeyboardInterrupt:
            print("Recording stopped.")

        # After stopping, release the VideoWriter
        out.release()
        print("Recording saved to video.avi")

    # If recording is already started, do nothing
    if recording:
        print("Recording is already in progress.")
        return

    # Set recording to True to start the recording
    recording = True

    # Run the recording in a separate thread so it doesn't block other code
    thread = threading.Thread(target=record)
    thread.start()
