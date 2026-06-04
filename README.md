# RaspberryPiBabyCrying

청각장애 보호자를 위한 **아이 울음소리 감지 및 원인 분류 시스템**의 Raspberry Pi 영역입니다.
Raspberry Pi에서 사운드 센서를 통해 소리를 감지하고, USB 마이크로 녹음한 음성 데이터를 AI 모델로 분류한 뒤 Bluetooth를 통해 Android 앱으로 감지 결과를 전송하는 구조입니다.

## 📌 프로젝트 개요

청각장애 보호자는 아이의 울음소리를 즉각적으로 인지하기 어려워 아이가 우는 상황을 놓칠 수 있습니다.
본 프로젝트는 Raspberry Pi와 Android 앱을 연동하여 아이 울음소리를 감지하고, 울음 원인을 분류하여 보호자에게 알림을 전달하는 것을 목표로 합니다.

이 저장소는 전체 시스템 중 **Raspberry Pi 기반 소리 감지, 음성 녹음, AI 추론, Bluetooth 전송** 역할을 담당합니다.

<br>

## 🎯 주요 목표

* LM393 사운드 센서를 이용한 소리 감지
* USB 마이크를 활용한 울음소리 녹음
* AST 기반 ONNX 모델을 이용한 울음 원인 분류
* Bluetooth RFCOMM 통신을 통한 Android 앱 연동
* 감지 결과를 Android 앱으로 실시간 전송

<br>

## 🛠 기술 스택

### Hardware

* Raspberry Pi
* LM393 Sound Sensor
* USB Microphone
* Bluetooth Module / Raspberry Pi Built-in Bluetooth

### Language & Runtime

* Python
* asyncio

### Audio Processing

* PyAudio
* wave
* librosa

### AI / Model Inference

* PyTorch
* Hugging Face Transformers
* AST(Audio Spectrogram Transformer)
* ONNX
* ONNX Runtime
* NumPy

### Communication

* Bluetooth RFCOMM Socket
* PyBluez

<br>

## 🏗 시스템 구조

```text
[LM393 Sound Sensor]
          ↓
[Raspberry Pi GPIO 감지]
          ↓
[USB Microphone 녹음]
          ↓
[AST 기반 ONNX 모델 추론]
          ↓
[울음 원인 분류]
          ↓
[Bluetooth RFCOMM 전송]
          ↓
[Android App 알림 표시]
```

<br>

## 📁 파일 구조

```text
RaspberryPiBabyCrying
├── blCom.py
├── detectUseSensor.py
├── model.py
├── record.py
├── README.md
└── __pycache__
```

<br>

## 🧩 주요 파일 설명

### `blCom.py`

Bluetooth RFCOMM 서버를 실행하는 파일입니다.

주요 역할은 다음과 같습니다.

* RFCOMM Bluetooth Socket 생성
* Android 앱과 Bluetooth 연결 대기
* 연결 성공 시 Android 앱으로 연결 메시지 전송
* 센서 감지 로직 실행

Android 앱과의 Bluetooth 통신에는 Serial Port Profile UUID를 사용합니다.

```python
uuid = "00001101-0000-1000-8000-00805f9b34fb"
```

<br>

### `detectUseSensor.py`

LM393 사운드 센서의 GPIO 입력을 감지하는 파일입니다.

주요 역할은 다음과 같습니다.

* GPIO BCM 모드 설정
* GPIO 26번 핀을 입력 핀으로 사용
* 센서 입력값을 반복적으로 확인
* 소리 감지 시 Android 앱으로 감지 메시지 전송
* 녹음 및 AI 모델 추론 로직 호출

센서에서 소리가 감지되면 Android 앱으로 다음 메시지를 전송합니다.

```text
아이 울음 소리 감지
```

이후 모델 추론 결과를 바탕으로 울음 유형을 Android 앱에 전달하는 구조로 확장할 수 있습니다.

<br>

### `record.py`

USB 마이크를 통해 음성 데이터를 녹음하고 WAV 파일로 저장하는 파일입니다.

주요 설정은 다음과 같습니다.

| 항목             | 값          |
| -------------- | ---------- |
| Channel        | 1          |
| Format         | 16-bit PCM |
| Rate           | 48000Hz    |
| Chunk          | 1024       |
| Recording Time | 7초         |

녹음된 파일은 기본적으로 `output.wav`로 저장됩니다.

<br>

### `model.py`

녹음된 WAV 파일을 불러와 AI 모델로 울음 원인을 분류하는 파일입니다.

주요 처리 흐름은 다음과 같습니다.

1. WAV 파일 로드
2. `librosa`를 이용한 오디오 로딩
3. Hugging Face `AutoProcessor`를 활용한 AST 입력 전처리
4. ONNX Runtime을 이용한 모델 추론
5. Softmax 적용 후 가장 높은 확률의 클래스를 예측
6. 예측 결과를 울음 유형 문자열로 반환

분류 결과는 다음과 같이 매핑됩니다.

| Class Index | Label        |
| ----------- | ------------ |
| 0           | `bellypain`  |
| 1           | `discomfort` |
| 2           | `hungry`     |
| 3           | `tired`      |

<br>

## 🔄 동작 흐름

### 1. Bluetooth 연결

```text
Raspberry Pi에서 blCom.py 실행
        ↓
Bluetooth RFCOMM 서버 시작
        ↓
Android 앱에서 Raspberry Pi 선택
        ↓
Bluetooth Socket 연결
        ↓
Android 앱으로 connected 메시지 전송
```

<br>

### 2. 소리 감지 및 분류

```text
LM393 센서 입력 감지
        ↓
소리 감지 시 Android 앱에 감지 메시지 전송
        ↓
USB 마이크로 음성 녹음
        ↓
output.wav 저장
        ↓
AST 기반 ONNX 모델 추론
        ↓
울음 유형 분류
        ↓
Bluetooth로 Android 앱에 결과 전송
```

<br>

## 📱 Android 앱과의 연동

본 Raspberry Pi 프로젝트는 Android 앱 저장소와 함께 동작합니다.

Android 앱은 Raspberry Pi에서 전송한 Bluetooth 메시지를 수신하고, 수신된 값에 따라 보호자에게 알림을 표시합니다.

Android 앱 저장소는 아래 링크에서 확인할 수 있습니다.

👉 [Capstone_BabyCrying Android App](https://github.com/Rentyo/Capstone_BabyCrying)

<br>

## 🚀 실행 방법

### 1. Repository Clone

```bash
git clone https://github.com/Rentyo/RaspberryPiBabyCrying.git
cd RaspberryPiBabyCrying
```

<br>

### 2. Python 패키지 설치

프로젝트 실행을 위해 아래 패키지가 필요합니다.

```bash
pip install pybluez
pip install RPi.GPIO
pip install pyaudio
pip install librosa
pip install torch
pip install transformers
pip install onnx
pip install onnxruntime
pip install numpy
```

환경에 따라 `pyaudio` 설치 전 PortAudio 설치가 필요할 수 있습니다.

```bash
sudo apt-get update
sudo apt-get install portaudio19-dev python3-pyaudio
```

<br>

### 3. Bluetooth 설정

Raspberry Pi에서 Bluetooth가 활성화되어 있어야 합니다.

```bash
sudo systemctl start bluetooth
sudo systemctl enable bluetooth
```

필요한 경우 Raspberry Pi를 검색 가능한 상태로 설정합니다.

```bash
sudo hciconfig hci0 piscan
```

<br>

### 4. 모델 파일 경로 설정

`model.py`에서 ONNX 모델 경로를 환경에 맞게 수정합니다.

```python
model_path = '/home/pi/capstone_python/ai/CustomASTClassifier.onnx'
```

녹음 파일 경로도 실제 환경에 맞게 확인합니다.

```python
item = "/home/pi/capstone_python/output.wav"
```

<br>

### 5. 실행

```bash
python blCom.py
```

실행 후 Android 앱에서 Raspberry Pi를 선택해 Bluetooth 연결을 진행합니다.

<br>

## ⚠️ 현재 코드 참고 사항

현재 `detectUseSensor.py`에서는 모델 추론 결과를 변수로 받은 뒤, Android 앱으로 고정된 `"tired"` 메시지를 전송하는 구조가 포함되어 있습니다.

```python
detection = asyncio.run(model.main())
client_socket.send("tired")
```

실제 추론 결과를 전송하려면 아래처럼 수정할 수 있습니다.

```python
detection = asyncio.run(model.main())
client_socket.send(detection)
```

또한 녹음 함수 호출 부분이 주석 처리되어 있다면, 실제 녹음 후 추론이 가능하도록 아래 코드를 활성화해야 합니다.

```python
record.record_start()
```

<br>

## 📊 프로젝트 성과

* Raspberry Pi와 Android 앱 간 Bluetooth RFCOMM 통신 구현
* LM393 사운드 센서를 활용한 소리 감지 구조 구현
* USB 마이크 기반 음성 녹음 기능 구현
* AST 기반 ONNX 모델 추론 구조 구현
* Android 앱과 연동해 울음 감지 알림 전달
* 전체 프로젝트 기준 울음소리 분류 정확도 45.3%에서 62.8%까지 개선

<br>

## 🧑‍💻 담당 역할

* Raspberry Pi 기반 소리 감지 환경 구성
* LM393 사운드 센서 GPIO 입력 처리
* USB 마이크 녹음 기능 구현
* AI 모델 추론 코드 연동
* Bluetooth RFCOMM 서버 구성
* Android 앱으로 감지 결과 전송
* 실제 사용 흐름을 고려한 감지 → 녹음 → 분류 → 알림 구조 설계

<br>

## 🔧 개선 방향

* 모델 추론 결과를 Android 앱에 직접 전송하도록 로직 정리
* 녹음 파일 경로와 모델 경로를 설정 파일로 분리
* 예외 처리 및 로그 구조 개선
* Bluetooth 연결 끊김 발생 시 재연결 로직 추가
* 센서 민감도 조정 및 오탐 방지 로직 개선
* Raspberry Pi 부팅 시 자동 실행을 위한 systemd 서비스 구성
* Android 앱과 메시지 프로토콜 문서화

<br>

## 🏷 Keywords

`Raspberry Pi` `Python` `Bluetooth` `PyBluez` `RPi.GPIO` `PyAudio` `AST` `ONNX Runtime` `Baby Cry Detection` `Android`
