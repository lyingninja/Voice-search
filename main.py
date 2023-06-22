import sounddevice as sd
import soundfile as sf
import time
import speech_recognition as sr
import pyttsx3
import openai


openai.api_key = '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';

# Initialize the recognizer
r = sr.Recognizer()
 
# Function to convert text to
# speech
def SpeakText(command):
     
    # Initialize the engine
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()
     
def async_record(filename, duration, fs, channels):
    print('recording')
    myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=channels)
    # can execute commands 
    print('Able to execute this before finishing.')
    # printstuff(30)
    # now wait until done before writing to file 
    sd.wait()
    sf.write(filename, myrecording, fs)
    print('done recording')


# Loop infinitely for user to
# speak
logs = [];
while(True):
     
    # Exception handling to handle
    # exceptions at the runtime
    try:
         
        # use the microphone as source for input.
        with sr.Microphone() as source:

            print('Listening...');
             
            # wait for a second to let the recognizer
            # adjust the energy threshold based on
            # the surrounding noise level
            r.adjust_for_ambient_noise(source, duration=0.2);
             
            #listens for the user's input
            audio2 = r.listen(source)
             
            # Using google to recognize audio
            MyText = r.recognize_google(audio2)
            MyText = MyText.lower()
 
            print("Your Query:", MyText);
            logs.append({"role": "user", "content": MyText});
            result = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=logs)["choices"][0]["message"]['content'];
            logs.append({"role": "assistant", "content": result});
            print("Answer:", result);
            # SpeakText(MyText)
             
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
         
    except sr.UnknownValueError:
        print("unknown error occurred")


# playback file 
# async_record('async_record.wav', 10, 16000, 1);
