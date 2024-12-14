import pyaudio
import wave

MIC_DEVICE_ID = 3
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 48000  # 장치에 맞는 샘플 레이트로 변경
SAMPLE_SIZE = pyaudio.get_sample_size(FORMAT)

def record(record_seconds):
    p = pyaudio.PyAudio()
    stream = None
    try:
        stream = p.open(input_device_index=MIC_DEVICE_ID,
                        format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
        print("Start to record the audio.")
        frames = []

        for i in range(0, int(RATE / CHUNK * record_seconds)):
            data = stream.read(CHUNK, exception_on_overflow=False)
            frames.append(data)

        print("Recording is finished.")

    except Exception as e:
        print(f"Recording error: {e}")
        frames = []

    finally:
        if stream is not None:  # stream이 정의된 경우에만 stop 및 close 호출
            stream.stop_stream()
            stream.close()
        p.terminate()

    return frames

# 녹음 데이터를 WAV 파일로 저장하기
def save_wav(target, frames):
    wf = wave.open(target, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(SAMPLE_SIZE)
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def record_start():
    RECORD_SECONDS = 7
    frames = record(RECORD_SECONDS)

    if frames:  # 녹음된 데이터가 있을 때만 저장
        WAVE_OUTPUT_FILENAME = "output.wav"
        save_wav(WAVE_OUTPUT_FILENAME, frames)
