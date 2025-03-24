import pygame

class AudioPlayer:
    def __init__(self, file_path):
        pygame.mixer.init()
        self.file_path = file_path
        self.is_playing = False
        self.is_paused = False

    def play(self):
        if not self.is_playing:
            pygame.mixer.music.load(self.file_path)
            pygame.mixer.music.play()
            self.is_playing = True
            self.is_paused = False
            print("Playing audio...")
        elif self.is_paused:
            pygame.mixer.music.unpause()
            self.is_paused = False
            print("Resumed audio.")

    def pause(self):
        if self.is_playing and not self.is_paused:
            pygame.mixer.music.pause()
            self.is_paused = True
            print("Paused audio.")

    def stop(self):
        if self.is_playing:
            pygame.mixer.music.stop()
            self.is_playing = False
            self.is_paused = False
            print("Stopped audio.")
