# Face-Recognition-service-using-email
The project aims to provide person identification as a service in a limited setting like a university or company. This allows the people to get some basic details about their colleagues. Any image for recognition will be sent as an atachment to a specified email. The python script will then extract the attached image from the specified email and reply with the closest match present in the known people images.

The project relies heavily on Adam Geitgey's library for Face recognition. [See here](https://github.com/ageitgey/face_recognition)

## Setup Instructions
1. To install the face_recognition library follow these instructions:
   - [Install face_recognition library](https://github.com/ageitgey/face_recognition#installation)  
2. Change the path in gmail.py to the directory in which the images are to be downloaded.(currently its the attachments folder)
3. Change the path in main.py to the directory which contains known people images.(currently its the db folder)
4. Change gmail settings to allow python script to access inbox. [See here](https://support.google.com/a/answer/6260879)

## Usage
Run main.py and provide the email id to which the recognition requests will be sent.


