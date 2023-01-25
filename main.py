#Need to install python and VSC to path, and to install pygame, use "pip install pygame --pre"
import sys, math, wave, numpy, pygame
from pygame.locals import *
from scipy.fftpack import dct

#Switches the number, width and heights of the bars and the FPS of them

Number = 30 # number of bars
HEIGHT = 600 # HEIGHT of a bar
WIDTH = 40 #WIDTH of a bar
FPS = 10

file_name = sys.argv[0]
status = 'stopped'
fpsclock = pygame.time.Clock()

#screen init, music playback

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode([Number * WIDTH, 50 + HEIGHT])
pygame.display.set_caption('Audio Visualizer')
my_font = pygame.font.SysFont('consolas', 16)
pygame.mixer.music.load("Music.wav")
pygame.mixer.music.play()
pygame.mixer.music.set_endevent()
pygame.mixer.music.set_volume(0.2)
status = "Playing"

#reads wave data
#The wave addon allows .WAV files which are audio files to be read and played.


f = wave.open("Music.wav", 'rb')
params = f.getparams()
nchannels, sampwidth, framerate, nframes = params[:4]
str_data = f.readframes(nframes)
f.close()
wave_data = numpy.fromstring(str_data, dtype = numpy.short)
wave_data.shape = -1, 2
wave_data = wave_data.T

num = nframes

#finds frames and outputs wave data +number of revolutions p/minute
def Visualizer(nums):
    num = int(nums)
    h = abs(dct(wave_data[0][nframes - num:nframes - num + Number]))
    h = [min(HEIGHT, int(i**(1 / 2.5) * HEIGHT / 100)) for i in h]
    draw_bars(h)

def vis(status):
    global num
    if status == "stopped":
        num = nframes
        return
    elif status == "paused":
        Visualizer(num)
    else:
        num -= framerate / FPS
        if num > 0:
            Visualizer(num)

#This get_time will get the number of miliseconds that the music has been playing for

def get_time():
    seconds = max(0, pygame.mixer.music.get_pos() / 1000)
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    hms = ("%02d:%02d:%02d" % (h, m, s))
    return hms

#This controls the status in the top left of the screen with if/else statements.
def controller(key):
    global status
    if status == "stopped":
        if key == K_RETURN:
            pygame.mixer_music.play()
            status = "playing"
    elif status == "paused":
        if key == K_RETURN:
            pygame.mixer_music.stop()
            status = "stopped"
        elif key == K_SPACE:
            pygame.mixer.music.unpause()
            status = "playing"
    elif status == "playing":
        if key == K_RETURN:
            pygame.mixer.music.stop()
            status = "stopped"
        elif key == K_SPACE:
            pygame.mixer.music.pause()
            status = "paused"

#This allows the bars to be displayed

def draw_bars(h):
    bars = []
    for i in h:
        bars.append([len(bars) * WIDTH , 50 + HEIGHT - i, WIDTH - 1, i])
    for i in bars:
        pygame.draw.rect(screen, [255,255,255], i, 0)

#This statement makes it so if you close the window, it will shut down the code and stop running as well as stop playing the .wav

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == KEYDOWN:
            controller(event.key)

    if num <= 0:
        status = "stopped"

    name = my_font.render(file_name, True, (255,255,255))
    info = my_font.render(status.upper() + "" + get_time(), True, (255,255,255))
    screen.fill((0,0,0))
    screen.blit(name,(0,0))
    screen.blit(info,(0, 18))
    fpsclock.tick(FPS)
    vis(status)
    pygame.display.update()
