import tkinter as tk
from tkinter import ttk, filedialog
from PIL import ImageTk, Image
import cv2


def conv(sec):
    sec = sec % (24 * 3600)
    hour = sec // 3600
    sec %= 3600
    min = sec // 60
    sec %= 60
    return "%02d:%02d:%02d" % (hour, min, sec)


def open_file():
    global count
    file_path = filedialog.askopenfilename(
        filetypes=[("Video files", ("*.mp4", "*.avi", "*.mkv", "*.mov", "*.flv", "*.wmv"))])
    return file_path


def update_frame():
    # Захватываем кадр из видео
    if p == True:
        ret, frame = cap.read()

        if ret:
            # Конвертируем кадр изображения OpenCV в формат, совместимый с Tkinter
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = cv2.resize(image, (1287, 724))  # нормализуем и зафиксирум размер видео
            image = Image.fromarray(image)
            image = ImageTk.PhotoImage(image)

            # Обновляем изображение на виджете
            lbl_window.config(image=image)
            lbl_window.image = image

            lbl_fps.config(text=f"FPS: {cap.get(cv2.CAP_PROP_FPS)}")
            len = conv(int(cap.get(cv2.CAP_PROP_POS_FRAMES) /
                           cap.get(cv2.CAP_PROP_FPS)))
            le = conv(int(cap.get(cv2.CAP_PROP_FRAME_COUNT) /
                          cap.get(cv2.CAP_PROP_FPS)))
            l = str(len) + '/' + str(le)
            lbl_duration.config(text=f"Продолжительность: {l}")
    # Планируем обновление следующего кадра
    lbl_window.after(10, update_frame)


def set_pause():
    global p
    if p == False:
        p = True
    else:
        p = False


def back():
    time = cap.get(cv2.CAP_PROP_POS_FRAMES)
    time = time - (cap.get(cv2.CAP_PROP_FPS) * 15)
    cap.set(cv2.CAP_PROP_POS_FRAMES, time)


def next():
    time = cap.get(cv2.CAP_PROP_POS_FRAMES)
    time = time + (cap.get(cv2.CAP_PROP_FPS)
                   * 15)
    cap.set(cv2.CAP_PROP_POS_FRAMES, time)


p = True

# Создаем главное окно Tkinter
root = tk.Tk()
root.title("Видеопроигрыватель")
root.geometry('1920x1080')

# Открываем видеофайл с помощью OpenCV
file_path = open_file()
cap = cv2.VideoCapture(file_path)

# Создаем виджет Label для отображения изображения
lbl_window = tk.Label(root)
lbl_duration = tk.Label(root, text="Продолжительность: ")
lbl_fps = tk.Label(root, text="FPS: ")
btn_back = tk.Button(root, text="<15s", command=back)
btn_pause = tk.Button(root, text='Start/Pause', command=set_pause)
btn_next = tk.Button(root, text="15s>", command=next)
btn_open = ttk.Button(root, text="Открыть файл", command=open_file)

lbl_window.place(x=120, y=13)
lbl_duration.place(x=55, y=750)
lbl_fps.place(x=55, y=770)
btn_back.place(x=700, y=758)
btn_pause.place(x=770, y=758)
btn_next.place(x=870, y=758)
btn_open.place(x=1400, y=758)

# Запускаем функцию обновления кадра
update_frame()

# Запускаем главный цикл обработки событий Tkinter
root.mainloop()
cap.release()
