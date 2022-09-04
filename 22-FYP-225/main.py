
from re import S


wait_after_sample = 5
try:
    # For audio
    import pyaudio
    import wave
    import datetime

    # For classifier
    import tensorflow as tf
    from tensorflow.keras import models
    import numpy as np

    from functions import thres
    import os
    import threading
    import time

    Model_realtime_testing = True
    # Sample rate: 48 kHz. Resolution: 16 bits. Channel: 1
    chunk = 100
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 48000

    # num_max: number of wav files to record.
    record_seconds = 4.064
    # 50 min of recordings with 4 seconds
    num_max = 1000
    times = 0

    condition = False
    # LOAD PRE-TRAINED MODEL
    model = tf.keras.models.load_model('models/no10_model.h5')

    parent_dir = 'audio'
    sub_dirs= ['input']

    def name_matching():
        # import name_called
        import speech_recognition as sr 
        from speech_recognition import UnknownValueError

        rec = sr.Recognizer()

        my_micro = sr.Microphone(device_index=1)

        with my_micro as source:

            # print("Say Something...")
            # audio = rec.listen(source, 3)

            harvard = sr.AudioFile('audio\input\live_audio.wav')
            
            with harvard as source:
                audio = rec.record(source)
            try:
                to_text = rec.recognize_google(audio)
                print("**************"+to_text+"***************")

                if "Luqman" in to_text or "Lukman" in to_text or 'lukma' in to_text:
                    print("your name is called.")
                    print("Vibrator is on now for 2seconds")
                    return True 
                else:
                    print("unknown name")
                    return False

            except UnknownValueError:
                print("Unable to recognize")
                return False

    def empty_dir():
        try:
            path = r"audio\\input\\"
            for file_name in os.listdir(path):
                # construct full file path
                file = path + file_name
                if os.path.isfile(file):
                    print('Deleting file:', file)
                    os.remove(file)
        except Exception as e:
            print(e)

    while times < num_max:
        if Model_realtime_testing:
            empty_dir()
            print("Taking audio Sample now")
            start_rec = datetime.datetime.now()

            p = pyaudio.PyAudio()
            stream = p.open(format=FORMAT,
                            channels=CHANNELS,
                            rate=RATE,
                            input=True,
                            output=True,
                            frames_per_buffer=chunk)
        
            frames = []
            # print(" times = %i" % times)

            for i in range(0, int(RATE / chunk * record_seconds)):
                data = stream.read(chunk)
                frames.append(data)

            stop_rec =  datetime.datetime.now() - start_rec
            print('Recording time: ', stop_rec)


            start_save = datetime.datetime.now()
            
            todaydate = datetime.date.today()
            today = todaydate.strftime("%d_%m_%Y")
            file_name_with_extension = "live_audio.wav"

            stream.stop_stream()
            stream.close()
            p.terminate()

            wf = wave.open("audio/input/" + file_name_with_extension, 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(2)
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
            wf.close()
            print("Audio Sample taken. Processing now.")

            stop_save =  datetime.datetime.now() - start_save
            print('Saving time: ', stop_save)
        

        #checking name in parallel
        match_name = name_matching()
        time.sleep(wait_after_sample)

        if match_name == False:
            thres(parent_dir=parent_dir,sub_dirs=sub_dirs,model=model)

        print("Process completed successfully")
        if Model_realtime_testing==False:
            print("GET ready")
            time.sleep(wait_after_sample)
            break
except Exception as e:
    print(e)
    try:
        import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
        from time import sleep # Import the sleep function from the time module
        GPIO.setwarnings(False) # Ignore warning for now
        GPIO.setmode(GPIO.BOARD) # Use physical pin numbering

        def voice_callback():
            sleep(2)
            print("Sound Detected")
            GPIO.output(11, GPIO.HIGH) # Turn on
            GPIO.output(13, GPIO.HIGH) # Turn on
            print("Vibrator and led on")
            sleep(1) # Sleep for 1 second
            
            GPIO.output(11, GPIO.LOW) # Turn off
            GPIO.output(13, GPIO.LOW) # Turn off
            print("Vibrator and led off")
            sleep(10) # Sleep for 1 secon

        
        GPIO.setup(11, GPIO.OUT, initial=GPIO.LOW) # Set pin 8 to be an output pin and set initial value to low (off)
        GPIO.setup(13, GPIO.OUT, initial=GPIO.LOW) # Set pin 8 to be an output pin and set initial value to low (off)
        GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        #GPIO.add_event_detect(15,GPIO.RISING,callback=voice_callback)

        while True: # Run forever
            Sound_matched = GPIO.input(15)
            if Sound_matched == True:
                voice_callback()
            else:
                print("no sound matched")
                time.sleep(1)
    except:
        pass
