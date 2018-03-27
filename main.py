from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from matplotlib import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
from tomograf import *

def calculate():
  #img = filedialog.askopenfilename(initialdir = os.path.dirname(os.path.realpath(__file__)), title = "Select file",filetypes = (("png files", "*.png"), ("bmp files","*.bmp"),("all files","*.*")))
  #img = img[img.rfind("/")+1:]
  filename = filedialog.askopenfilename()
  #print(filename)
  image, height, width = load(filename)
  mse_before, mse_after = main(image, detectors_range.get(), detectors.get(), steps.get(), animation_speed.get(), fig, canvas)
  mse_text.set("\nBłąd przed filtracją: "+ str( mse_before) +"\n\nBłąd po filtracji: "+ str( mse_after))

root = Tk()
root.title("Symulacja tomografu komputerowego")

# ramki
info_frame = Frame(root)
info_frame.pack(side=RIGHT)

results_frame = Frame(root)
results_frame.pack(side=BOTTOM)

detector_frame = Frame(info_frame)
detector_frame.pack(side=TOP)

detector_angle_frame = Frame(info_frame)
detector_angle_frame.pack(side=TOP)

alpha_frame = Frame(info_frame)
alpha_frame.pack(side=TOP)

animation_frame = Frame(info_frame)
animation_frame.pack(side=TOP)

mse_frame = Frame(info_frame)
mse_frame.pack(side=TOP)

# detektory
label = Label(detector_frame, text="Liczba\ndetektorów:")
label.pack()
detectors = Scale(detector_frame, from_=2, to=500, orient=HORIZONTAL)
detectors.set(150)
detectors.pack(side=LEFT)

# rozpiętość detektorów
label = Label(detector_angle_frame, text="Rozpiętość\ndetektorów:")
label.pack()
detectors_range = Scale(detector_angle_frame, from_=1, to=180, orient=HORIZONTAL)
detectors_range.set(200)
detectors_range.pack(side=LEFT)

# ilość kroków
label = Label(alpha_frame, text="Liczba kroków emitera:")
label.pack()
steps = Scale(alpha_frame, from_=1, to=360, orient=HORIZONTAL)
steps.set(90)
steps.pack(side=LEFT)

# szybkość animacji
label = Label(animation_frame, text="Szybkość animacji:")
label.pack()
animation_speed = Scale(animation_frame, from_=1, to=10, orient=HORIZONTAL)
animation_speed.set(5)
animation_speed.pack(side=LEFT)

# błąd średniokwadratowy
mse_text = StringVar()
mse_text.set("\nBłąd przed filtracją: \n\nBłąd po filtracji: ")
mse_label = Label(mse_frame, textvariable = mse_text)
mse_label.pack()


# wywołanie obliczeń
button = Button(info_frame, text="Symulacja", command=calculate)
button.pack(side=BOTTOM)

# utworzenie canvasa
fig = Figure(figsize=(20, 20))
canvas = FigureCanvasTkAgg(fig, master=results_frame)
canvas.get_tk_widget().pack()


root.mainloop()
