from .settings import MUSIC_PATH, sound_tracks_path
import time as t
import pygame

class SoundManager(object):
    _instance = None
    @staticmethod
    def get_instance():
        if SoundManager._instance is None:
            SoundManager()
        return SoundManager._instance

    def __init__(self):
        if SoundManager._instance is not None:
            raise Exception('only one SoundManager can exist')
        else:
            self._id = id(self)
            SoundManager._instance = self

        pygame.init() #for music
        self.bgm = pygame.mixer.music.load(MUSIC_PATH)#importing sound file
        self.sound_track = {}
        self._mute = False

        # init sound object
        for sound_track in sound_tracks_path.keys():
            self.sound_track[sound_track] = pygame.mixer.Sound(sound_tracks_path[sound_track])

    def play_sound(self, name):
        if not self._mute:
            if name in self.sound_track:
                return self.sound_track[name].play()
            else:
                return None

    def bgm_loop(self, play=True):
        if not self._mute:
            if play == True:
                if pygame.mixer.music.get_busy() != 1:
                    # continuely plays music
                    pygame.mixer.music.play(-1, 0.0)
            else:
                pygame.mixer.music.pause()

    def mute(self):
        self._mute = True