import PyPDF2
import pyttsx3

# Open the PDF file (Enter Path To Your PDF)
file = open('C:/Users/Pranam/Documents/Books/Thank_You_for_Being_Late_by_Thomas_L._Fr.pdf', 'rb')
readpdf = PyPDF2.PdfReader(file)

# Initialize text-to-speech engine
speaker = pyttsx3.init()
rate = speaker.getProperty('rate')   # Get current speaking rate
speaker.setProperty('rate', 200)

volume = speaker.getProperty('volume')
speaker.setProperty('volume', 1)  # Set volume level (0.0 to 1.0)

# Get and set a different voice
voices = speaker.getProperty('voices')
for voice in voices:
    if "english" in voice.name.lower() and "us" in voice.name.lower():
        speaker.setProperty('voice', voice.id)
        break

# Iterate over each page in the PDF
text = ""
for pagenumber in range(len(readpdf.pages)):
    # Extract text from the page
    page = readpdf.pages[pagenumber]
    print(f"{pagenumber} - {len(page.extract_text())}")
    text += page.extract_text()

    # Use the speaker to read the text
    # speaker.say(text)
    # speaker.runAndWait()

print(len(text))
# Save the last extracted text to an audio file (if needed)
speaker.save_to_file(text, 'Thank_You_for_Being_Late_by_Thomas_L.mp3')
speaker.runAndWait()

# Stop the speaker
speaker.stop()

# Close the PDF file
file.close()
