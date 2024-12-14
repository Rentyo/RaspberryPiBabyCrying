import RPi.GPIO as GPIO
import time
import record
import model
import asyncio
def Sensor_detect(client_socket):
    SOUND_SENSOR_PIN = 26  # 연결된 GPIO 핀 번호

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SOUND_SENSOR_PIN, GPIO.IN)


    try:
        while True:
            if GPIO.input(SOUND_SENSOR_PIN) == GPIO.HIGH:
                print("평소")
            else:
                print("소리 감지")
                client_socket.send("아이 울음 소리 감지")
                # record.record_start()
                print("녹음 끝")
                time.sleep(6)
                detection=asyncio.run(model.main())
                client_socket.send("tired")
                time.sleep(1)
                continue
            time.sleep(0.1)
    except KeyboardInterrupt:
        GPIO.cleanup()