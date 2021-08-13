from .AISayListen import AISayListen as AISL
from .AISayListenException import AISayListenAttributeTypeError, AISayListenAttributeValueError, AISayListenMicrophoneError, AISayListenSpeakEnablingError, AISayListenGttsError
import pytest
from sys import stderr
import speech_recognition as sr

class TestAISayListen:

    def test_init(self):
        try:
            AISL(can_speak=False)
        except:
            pytest.fail("It should not have failed")
        with pytest.raises(AISayListenAttributeTypeError):
            AISL(LANG=42, can_speak=False)
        with pytest.raises(AISayListenAttributeValueError):
            AISL(SAMPLE_RATE=-1000, can_speak=False)
        with pytest.raises(AISayListenAttributeValueError):
            AISL(CHUNK_SIZE=-200, can_speak=False)
        with pytest.raises(AISayListenSpeakEnablingError):
            AISL(can_speak="toto")

    def test_change_mic(self):
        try:
            ai = AISL(can_speak=True)
        except AISayListenSpeakEnablingError:
            print("Unsure of test suite change_mic as it may occure because of no mics are aviable", stderr)
            print("Aborting test suite: test_change_mic", stderr)
            pytest.fail("Cannot test change_mic")
        with pytest.raises(AISayListenMicrophoneError):
            ai.change_microphone("surely unexisting microphone")
        with pytest.raises(AISayListenAttributeTypeError):
            ai.change_microphone(5)
        try:
            if len(sr.Microphone.list_microphone_names()):
                ai.change_microphone(sr.Microphone.list_microphone_names()[0])
        except Exception as e:
            pytest.fail(f'Device had a microphone but could not change it - Exception: {e}')

    def test_set_get_language_canspeak(self):
        ai = AISL(can_speak=False)
        assert ai.get_canspeak_status() is False
        ai.set_canspeak_status(True)
        assert ai.get_canspeak_status() is True
        assert ai.get_language() == "fr"
        ai.set_language("en")
        assert ai.get_language() == "en"

    def test_listen(self):
        ai = AISL(can_speak=False)
        with pytest.raises(AISayListenSpeakEnablingError):
            ai.listen()

    def test_say(self):
        ai = AISL(can_speak=False)
        with pytest.raises(AISayListenAttributeTypeError):
            ai.say(50)
        ai.say(None)
        try:
            ai.say("test vocal de l'ia")
        except AISayListenGttsError:
            pass
