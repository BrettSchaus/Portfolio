from pypdf import PdfReader
import boto3
import os

# creating a pdf reader object
reader = PdfReader('/home/brett/Downloads/TextToSpeechTest.pdf')  # Will need to update path

text = ""

for page in reader.pages:
    text += page.extract_text()

polly = boto3.client("polly", region_name="eu-west-1")

response = polly.synthesize_speech(
    Text=text,
    OutputFormat="mp3",
    VoiceId="Joanna"
)

downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")

with open(os.path.join(downloads_folder, "speech.mp3"), "wb") as file:
    file.write(response["AudioStream"].read())
    print("Successfully created mp3 file.")

