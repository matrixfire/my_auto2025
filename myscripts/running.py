from elevenlabs import play
from elevenlabs.client import ElevenLabs
from pydub import AudioSegment
from pydub.playback import play
import pyttsx3 # audio
import os
from collections import defaultdict


def generate_and_save_audio(api_key, text, voice="Brian", model="eleven_multilingual_v2", save_path="G:\\temp\\test_message.mp3"):
    """
    Generates speech from text, saves it as an MP3 file, and optionally plays the audio.

    Parameters:
        api_key (str): The ElevenLabs API key.
        text (str): The text to convert to speech.
        voice (str): The voice to use (default is "Brian").
        model (str): The model to use for speech generation (default is "eleven_multilingual_v2").
        save_path (str): Path to save the generated MP3 file (default is "G:\\temp\\test_message.mp3").

    Returns:
        str: Path to the saved MP3 file.
    """
    # Create a client instance
    client = ElevenLabs(api_key=api_key)

    # Generate speech
    audio = client.generate(
        text=text,
        voice=voice,
        model=model
    )

    # Convert generator to bytes
    audio_content = b''.join(audio)

    # Save the audio as an MP3 file
    with open(save_path, "wb") as f:
        f.write(audio_content)

    print(f"Audio saved to {save_path}")
    return save_path


def create_narration_ai(text, output_file, api_key='sk_712c4a61f017d43b924d59e0df6653b01c2d27d77657895a'):
    """
    Generate narration audio using ElevenLabs API and save it as a WAV file.

    Args:
        text (str): The narration text.
        output_file (str): The file path to save the narration as WAV.
        api_key (str): ElevenLabs API key.
    """
    try:
        # Generate MP3 using the ElevenLabs API
        temp_mp3_path = "temp_audio.mp3"
        generate_and_save_audio(api_key, text, save_path=temp_mp3_path)

        # Convert MP3 to WAV
        audio = AudioSegment.from_file(temp_mp3_path, format="mp3")
        audio.export(output_file, format="wav")

        print(f"Narration successfully saved to {output_file}")
        # Clean up temporary file
        os.remove(temp_mp3_path)
    except Exception as e:
        print(f"Failed to generate narration: {e}")


# Function to generate a break narration
def generate_break_narration(start_time, break_duration, pre_break_message, countdown_message="Back to running in", break_number=None):
    """
    Generate narrations for a break, including a pre-break message and a countdown.
    :param start_time: When the break starts in seconds.
    :param break_duration: Duration of the break in seconds.
    :param pre_break_message: What to say before the break starts.
    :param countdown_message: What to say during the countdown (default message).
    :param break_number: Number of the break for labeling (optional).
    :return: A list of narration dictionaries.
    """
    group_label = f"break_{break_number}" if break_number else "break"
    narrations = [{"start_time": start_time, "text": pre_break_message, "group": group_label}]
    countdown_start = start_time + break_duration - 10
    countdown_narrations = generate_countdown_narration(
        countdown_start, 10, countdown_message, show_message_once=True, group=group_label
    )
    return narrations + countdown_narrations


# Function to generate countdown narrations
def generate_countdown_narration(start_time, count, message, show_message_once=False, group=None):
    """
    Generate a countdown narration.
    :param start_time: When the countdown starts in seconds.
    :param count: How many seconds to count down.
    :param message: Message to prefix before each countdown number.
    :param show_message_once: Whether to show the full message only on the first second.
    :param group: Group label for these narrations (optional).
    :return: A list of narration dictionaries.
    """
    narrations = []
    for i in range(count, 0, -1):
        narration_text = f"{message} {i}..." if (show_message_once and i == count) else f"{i}..."
        narrations.append({"start_time": start_time + (count - i), "text": narration_text, "group": group})
    return narrations


# Function to generate exercise-specific narrations
def generate_running_narrations(music_duration, break_intervals, break_duration, final_message):
    """
    Generate narrations for a running exercise.
    :param music_duration: Total duration of the music in seconds.
    :param break_intervals: List of times (in seconds) for breaks.
    :param break_duration: Duration of each break in seconds.
    :param final_message: Message at the end of the exercise.
    :return: A list of narration dictionaries.
    """
    narrations = [{"start_time": 0, "text": "Welcome to your running workout! Let's get moving and have some fun!", "group": "intro"}]
    narrations.append({"start_time": 5, "text": "Keep a steady pace and enjoy the music. You've got this!", "group": "intro"})
    
    for idx, start_time in enumerate(break_intervals, start=1):
        narrations += generate_break_narration(
            start_time=start_time,
            break_duration=break_duration,
            pre_break_message=f"Time for break #{idx}! Slow down and catch your breath.",
            countdown_message="Back to running in",
            break_number=idx
        )
    
    if music_duration - 10 > 0:
        narrations += generate_countdown_narration(music_duration - 10, 10, "Almost done! Wrapping up in", show_message_once=True, group="outro")
    
    narrations.append({"start_time": music_duration, "text": final_message, "group": "outro"})
    return narrations



# Function to create narration from text
def create_narration(text, output_path):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    # Set the voice to an English voice
    engine.setProperty('voice', voices[1].id)  # For example, voices[1] could be an English voice
    engine.save_to_file(text, output_path)
    engine.runAndWait()




def overlay_narration_with_music(music_path, narrations, output_file):
    from collections import defaultdict
    
    # Load the background music (MP3)
    music = AudioSegment.from_mp3(music_path)
    music_duration = len(music) / 1000  # Convert milliseconds to seconds
    
    # Print the total length of the music in seconds
    print(f"Total music duration: {music_duration:.2f} seconds")
    
    # Append a final custom narration (example usage)
    narrations.append({
        "start_time": music_duration - 7,
        "text": "This is Bill Zou, who just wanna say thanks for your following me, good bye, hahaha!",
        "group": "final_message"
    })
    
    # Group narrations by their group label
    grouped_narrations = defaultdict(list)
    for narration in narrations:
        group = narration.get("group", "default")
        grouped_narrations[group].append(narration)
    
    # Initialize the final audio as the music
    final_audio = music
    
    # Process each group
    for group, group_narrations in grouped_narrations.items():
        # Determine the start and end time for the group
        group_start_time = min(n["start_time"] for n in group_narrations) * 1000  # Convert to milliseconds
        group_end_time = max(n["start_time"] for n in group_narrations) * 1000 + 1000  # Add 1 second buffer
        
        # Reduce background music volume for the entire group duration
        music_during_narration = (
            final_audio[:group_start_time]
            + final_audio[group_start_time:group_end_time].apply_gain(-30)
            + final_audio[group_end_time:]
        )
        
        # Overlay each narration in the group
        for narration in group_narrations:
            start_time = narration["start_time"] * 1000  # Convert seconds to milliseconds
            text = narration["text"]
            
            # Generate the narration audio
            narration_file = "narration.wav"
            create_narration(text, narration_file)
            # create_narration_ai(text, narration_file)
            narration_audio = AudioSegment.from_wav(narration_file)
            
            # Overlay the narration onto the reduced-volume music
            music_during_narration = music_during_narration.overlay(narration_audio, position=start_time)
            
            # Clean up the temporary narration file
            os.remove(narration_file)
        
        # Update the final audio with the processed group
        final_audio = music_during_narration

    # Export the final audio with all narrations
    final_audio.export(output_file, format="mp3")
    print(f"Audio successfully created and saved to {output_file}")
    return output_file



# Main function to run the process
def create_custom_mp3(music_path, narrations, output_file="output.mp3"):
    # Create the customized MP3 with narration
    final_output = overlay_narration_with_music(music_path, narrations, output_file)
    print(f"Audio successfully created and saved to {final_output}")


# Configuration
total_music_duration = 1800  # Total duration in seconds
break_duration = 60
units = [3, 5, 7,7,5,3]
total_units = sum(units)
seconds_per_unit = total_music_duration / total_units

break_intervals = []
cumulative_time = 0
for unit in units:
    cumulative_time += unit * seconds_per_unit
    break_intervals.append(int(cumulative_time))

final_message = "Great workout! You've done an amazing job. See you next time!"

narrations = generate_running_narrations(total_music_duration, break_intervals, break_duration, final_message)

print(narrations)
music_path = r"C:\Users\recur\Desktop\WORK\Virtual Running Videos For Treadmill With Music  30 Minute Virtual Run.mp3"
output_path = r"C:\Users\recur\Desktop\WORK\Modified_Music_with_Narrations.mp3"

create_custom_mp3(music_path, narrations, output_file=output_path)
