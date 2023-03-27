import pyttsx3


def read_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content


def text_to_speech(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 170)  # Speed of speech
    engine.setProperty('volume', 1.0)  # Volume level (0.0 to 1.0)
    engine.say(text)
    engine.runAndWait()


def main():
    file_path = input("Please enter the file path: ")
    content = read_file(file_path)
    text_to_speech(content)


if __name__ == "__main__":
    main()
