from kokoro import KPipeline
import sounddevice as sd


# Create the Kokoro voice pipeline
pipeline = KPipeline(lang_code="a")


def speak(text):

    # Generate speech
    generator = pipeline(
        text,
        voice="af_heart"
    )

    # Kokoro can split long text into chunks
    for _, _, audio in generator:

        # Play audio
        sd.play(audio, 24000)

        # Wait until speaking finishes
        sd.wait()