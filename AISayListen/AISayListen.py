import speech_recognition as sr
import gtts
from playsound import playsound
import sys
from typing import Union, Any

from .AISayListenException import AISayListenAttributeTypeError
from .AISayListenException import AISayListenAttributeValueError
from .AISayListenException import AISayListenGttsError
from .AISayListenException import AISayListenMicrophoneError
from .AISayListenException import AISayListenSpeakEnablingError

class AISayListen:

    def __check_self_attributes_types(self) -> None:
        err = "NA"
        try:
            err = "self.LANG"
            assert isinstance(self.LANG, str)
            err = "self.MIC_NAME"
            assert isinstance(self.MIC_NAME, str)
            err = "self.SAMPLE_RATE"
            assert isinstance(self.SAMPLE_RATE, int)
            err = "self.CHUNK_SIZE"
            assert isinstance(self.CHUNK_SIZE, int)
            err = "self.can_speak"
            assert isinstance(self.can_speak, bool)
            err = "self.DEVICE_ID"
            assert isinstance(self.DEVICE_ID, int)
        except:
            raise AISayListenAttributeTypeError(err, self)

    def __init__(self,
            LANG: str = "fr",
            MIC_NAME: str = "default",
            SAMPLE_RATE: int = 48000,
            CHUNK_SIZE: int = 2048,
            can_speak: bool = True):

        self.can_speak, self.LANG, self.SAMPLE_RATE, self.CHUNK_SIZE = can_speak, LANG, SAMPLE_RATE, CHUNK_SIZE
        if self.SAMPLE_RATE <= 0 or CHUNK_SIZE <= 0:
            raise AISayListenAttributeValueError("assert not(self.SAMPLE_RATE <= 0 or CHUNK_SIZE <= 0)")
        if not can_speak:
            self.DEVICE_ID = -1
            self.MIC_NAME = "N/A"
        else:
            self.change_microphone(MIC_NAME)
            self.recognizer = sr.Recognizer()
        self.__check_self_attributes_types()

    def say(self, speech: str) -> None:
        if speech is None:
            print("WARNING: Got None value for AISayListen.say", file=sys.stderr)
            return
        if isinstance(speech, str) is False:
            raise AISayListenAttributeTypeError("AISayListen.say(speech) speech was not of type str", self)
        try:
            tts = gtts.gTTS(speech, lang=self.LANG)
            tts.save("/tmp/answer.mp3")
            playsound("/tmp/answer.mp3")
        except:
            raise AISayListenGttsError(speech)

    def listen(self) -> Union[str, None]:
        if self.can_speak is not True:
            raise AISayListenSpeakEnablingError()
        try:
            with sr.Microphone(self.DEVICE_ID, self.SAMPLE_RATE, self.CHUNK_SIZE) as source:
                self.recognizer.adjust_for_ambient_noise(source)
                return self.recognizer.recognize_google(
                        self.recognizer.listen(source),
                        language=self.LANG)
        except Exception as e:
            print(f'Listen Exception: {e}', file=sys.stderr)
            return None

    def change_microphone(self, mic_name: str) -> None:
        if isinstance(mic_name, str) is False:
            raise AISayListenAttributeTypeError("AISayListen.change_microphone(mic_name) mic_name was not of type str", self)
        if self.can_speak is not True:
            raise AISayListenSpeakEnablingError()
        self.MIC_NAME = mic_name
        mic_list = sr.Microphone.list_microphone_names()
        try:
            if not len(mic_list):
                raise AISayListenMicrophoneError("No mics are aviable on this device")
            elif self.MIC_NAME not in mic_list:
                raise AISayListenMicrophoneError(f'[{self.MIC_NAME}] Microphone could not be found in: {mic_list}')
        except AISayListenMicrophoneError as e:
            self.DEVICE_ID = -1
            self.MIC_NAME = "N/A"
            raise AISayListenMicrophoneError(e)
        self.DEVICE_ID = mic_list.index(self.MIC_NAME)
        print(f'Sucessfully changed microphone to {self.MIC_NAME}:{self.DEVICE_ID}')

    def set_canspeak_status(self, status: bool) -> None:
        if isinstance(status, bool) is False:
            raise AISayListenAttributeTypeError("AISayListen.set_canspeak_status(lang) status was not of type bool", self)
        self.can_speak = status

    def get_canspeak_status(self) -> bool:
        return self.can_speak

    def set_language(self, lang: str) -> None:
        if isinstance(lang, str) is False:
            raise AISayListenAttributeTypeError("AISayListen.set_language(lang) lang was not of type str", self)
        self.LANG = lang

    def get_language(self) -> str:
        return self.LANG

    def __str__(self) -> str:
        return f'[ DeviceID: {self.DEVICE_ID}, Microphone Name: {self.MIC_NAME}, Sample Rate: {self.SAMPLE_RATE}, Chunk Size: {self.CHUNK_SIZE}, Can Speak: {self.can_speak}, Language: {self.LANG} ]'

    __repr__ = __str__

