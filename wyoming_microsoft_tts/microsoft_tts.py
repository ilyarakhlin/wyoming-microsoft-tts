"""Microsoft TTS."""
import logging
import tempfile
import time
from pathlib import Path

import azure.cognitiveservices.speech as speechsdk
from azure.cognitiveservices.speech.enums import SpeechSynthesisOutputFormat
from .download import get_voices

_LOGGER = logging.getLogger(__name__)


class MicrosoftTTS:
    """Class to handle Microsoft TTS."""

    def __init__(self, args) -> None:
        """Initialize."""
        _LOGGER.debug("Initialize Microsoft TTS")
        self.args = args
        self.speech_config = speechsdk.SpeechConfig(
            subscription=args.subscription_key, region=args.service_region
        )
        if args.endpoint_id:
            self.speech_config.endpoint_id = args.endpoint_id
            
        if args.custom_voice:
            self.speech_config.speech_synthesis_voice_name = args.custom_voice
        else:
            self.speech_config.speech_synthesis_voice_name = ""

        if not args.audio_format:
            self.speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Riff44100Hz16BitMonoPcm)
        else:
            _format = SpeechSynthesisOutputFormat(args.audio_format)
            self.speech_config.set_speech_synthesis_output_format(_format)
        
        output_dir = str(tempfile.TemporaryDirectory())
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir = output_dir

        self.voices = get_voices(args.download_dir)

    def synthesize(self, text, voice=None):
        """Synthesize text to speech."""
        _LOGGER.debug(f"Requested TTS for [{text}]")
        if voice is None and not self.speech_config.speech_synthesis_voice_name:
            voice = self.args.voice

        # Convert the requested voice to the key microsoft use.
        if not self.speech_config.speech_synthesis_voice_name:
            self.speech_config.speech_synthesis_voice_name = self.voices[voice]["key"]

        file_name = self.output_dir / f"{time.monotonic_ns()}.wav"
        audio_config = speechsdk.audio.AudioOutputConfig(filename=str(file_name))

        speech_synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=self.speech_config, audio_config=audio_config
        )

        speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()

        if (
            speech_synthesis_result.reason
            == speechsdk.ResultReason.SynthesizingAudioCompleted
        ):
            _LOGGER.debug(f"Speech synthesized for text [{text}]")
            return str(file_name)

        elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = speech_synthesis_result.cancellation_details
            _LOGGER.warning(f"Speech synthesis canceled: {cancellation_details.reason}")
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                _LOGGER.warning(f"Error details: {cancellation_details.error_details}")
