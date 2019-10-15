import pygame
import time

pygame.mixer.init()
#pygame.mixer.music.load("effect.mp3")

effect_left = pygame.mixer.Sound("effect_left.wav")
effect_right = pygame.mixer.Sound("effect_right.wav")

while True:
#pygame.mixer.music.play()
	effect_left.play()
	time.sleep(1.0)
	effect_right.play()
	time.sleep(1.0)
