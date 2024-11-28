import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
import os
from PIL import Image, ImageTk
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='tkinter')

class ImageProcessingApp(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.image1_path = None
        self.image2_path = None

    def create_widgets(self):
        self.top_frame = tk.Frame(self, bg="#f0f0f0")
        self.top_frame.pack(fill="x")
        self.open_image1_button = tk.Button(self.top_frame, text="Изображение 1", bg="#ffffff", width=20, height=3, command=self.open_image1)
        self.open_image1_button.pack(side="left", padx=10, pady=10)
        self.open_image2_button = tk.Button(self.top_frame, text="Изображение 2", bg="#ffffff", width=20, height=3, command=self.open_image2)
        self.open_image2_button.pack(side="left", padx=10, pady=10)
        self.process_button = tk.Button(self.top_frame, text="Алгоритм работы", bg="#ffffff", width=20, height=3, command=self.process)
        self.process_button.pack(side="left", padx=10, pady=10)

    def open_image1(self):
        self.image1_path = filedialog.askopenfilename(filetypes=[("Image Files", ".jpg .jpeg .png .bmp")])
        if self.image1_path:
            self.open_image1_button.config(text=os.path.basename(self.image1_path))

    def open_image2(self):
        self.image2_path = filedialog.askopenfilename(filetypes=[("Image Files", ".jpg .jpeg .png .bmp")])
        if self.image2_path:
            self.open_image2_button.config(text=os.path.basename(self.image2_path))

    def process(self):
        if self.image1_path and self.image2_path:
            output_filename = os.path.basename(self.image1_path).split('.')[0] + '_output.jpg'
            output_path = os.path.join(os.getcwd(), output_filename)
            self.process_images(self.image1_path, self.image2_path, output_path)

    def process_images(self, image1_path, image2_path, output_path):
        image1 = cv2.imread(image1_path)
        image2 = cv2.imread(image2_path)

        max_height = max(image1.shape[0], image2.shape[0])
        max_width = max(image1.shape[1], image2.shape[1])

        image1 = cv2.resize(image1, (max_width, max_height))
        image2 = cv2.resize(image2, (max_width, max_height))

        gray_image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
        _, threshold_image1 = cv2.threshold(gray_image1, 75, 255, cv2.THRESH_BINARY)

        result_image = np.zeros_like(image1)
        for y in range(image1.shape[0]):
            for x in range(image1.shape[1]):
                if threshold_image1[y, x] == 255:
                    result_image[y, x] = image1[y, x]
                else:
                    result_image[y, x] = np.clip(image1[y, x] + image2[y, x] - 1, 0, 255)

        cv2.imwrite(output_path, result_image)

root = tk.Tk()
root.title("Image Processing")
app = ImageProcessingApp(master=root)
app.mainloop()