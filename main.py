import math
from tkinter import *
import pygame
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
# work_sound_file = "work_sound.wav"
short_break_sound_file = "short_break_sound.mp3"
long_break_sound_file = "long_break_sound.mp3"
WORK_MIN = 2
SHORT_BREAK_MIN = 1
LONG_BREAK_MIN = 2
reps = 0
timer = None

# Initialize pygame mixer
pygame.mixer.init()

# ---------------------------- TIMER RESET ------------------------------- #
def reset():
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00")
    title_lable.config(text="Timer")
    check_marks.config(text="")
    global reps
    reps = 0

# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    global reps
    reps += 1
    work_sec = WORK_MIN * 60
    short_brack_sec = SHORT_BREAK_MIN * 60
    long_breack_sec = LONG_BREAK_MIN * 60

    if reps % 8 == 0:
        count_down(long_breack_sec)
        title_lable.config(text="Breack", fg=RED)
        play_sound(long_break_sound_file)
    elif reps % 2 == 0:
        count_down(short_brack_sec)
        title_lable.config(text="Breack", fg=PINK)
        play_sound(short_break_sound_file)
    else:
        count_down(work_sec)
        title_lable.config(text="Work", fg=GREEN)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    count_min = math.floor(count / 60)
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"
    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        global timer
        timer =  window.after(1000, count_down, count -1)
    else:
        start_timer()
        marks = ""
        work_sessions = math.floor(reps / 2)
        for _ in range(work_sessions):
            marks += "✅"
        check_marks.config(text=marks)

def play_sound(sound_file):
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50)


title_lable = Label(text="Timer", fg=GREEN, font=(FONT_NAME, 50))
title_lable.grid(column=1, row=0)

canvas = Canvas(width=200, height=224, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="00:00", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)

start_button = Button(text="Start", command=start_timer)
start_button.grid(column=0, row=2)

reset_button = Button(text="Reset", command=reset)
reset_button.grid(column=2, row=2)

check_marks = Label(fg=GREEN, font=(FONT_NAME, 30))
check_marks.grid(column=1, row=3)

window.mainloop()
