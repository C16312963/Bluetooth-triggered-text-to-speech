from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import sys
import subprocess
from tempfile import gettempdir
import bluetooth

# Create a client using the credentials and region defined in the [default]
# section of the AWS credentials file (~/.aws/credentials).
session = Session(profile_name="default")
polly = session.client("polly")
try:
  # Request speech synthesis
  response = polly.synthesize_speech(Text="Hello World!", OutputFormat="mp3", VoiceId="Joanna")
except (BotoCoreError, ClientError) as error:
  # The service returned an error, exit gracefully
  print(error)
  sys.exit(-1)

# Access the audio stream from the response
if "AudioStream" in response:
  # Note: Closing the stream is important because the service throttles on the
  # number of parallel connections. Here we are using contextlib.closing to
  # ensure the close method of the stream object will be called automatically
  # at the end of the with statement's scope.
  with closing(response["AudioStream"]) as stream:
    output = os.path.join(gettempdir(), "speech.mp3")

    try:
      # Open a file for writing the output as a binary stream
        with open(output, "wb") as file:
          file.write(stream.read())
    except IOError as error:
      # Could not write to file, exit gracefully
      print(error)
      sys.exit(-2)
else:
  # The response didn't contain audio data, exit gracefully
  print("Could not stream audio")
  sys.exit(-3)

target_name = "Galaxy S5 Neo" # Name of Bluetooth device to search for
target_address = None

nearby_devices = bluetooth.discover_devices()

for bdaddr in nearby_devices:
    if target_name == bluetooth.lookup_name( bdaddr ):
        target_address = bdaddr # If the bluetooth device is found set the target_address to its ID 
        print(bdaddr)
    else:
        target_address = "none" #If not then set target_address to none

if target_address is not "none":
    # Play the audio using the platform's default player
    os.startfile(output)
else:
    print("could not find target bluetooth device nearby")
