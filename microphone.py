from pyaudio import PyAudio, Stream, paInt16, paInt32, paFloat32

MICROPHONE_CHUNK_SIZE = 1024


class Microphone:
    def __init__(self, format: int = paInt16,  channels: int = 2,  bitrate: int = 48000) -> None:
        self._pa_obj = PyAudio()
        self._stream = self._pa_obj.open(
            format=format,
            channels=channels,
            rate=bitrate,
            input=True,
            frames_per_buffer=MICROPHONE_CHUNK_SIZE,
        )
        self.stop()

    def stream(self) -> Stream:
        return self._stream

    def read(self, size: int = MICROPHONE_CHUNK_SIZE) -> bytearray:
        return self._stream.read(size)

    def start(self):
        self._stream.start_stream()

    def stop(self):
        self._stream.stop_stream()

    def close(self):
        self.stop()
        self._pa_obj.terminate()
