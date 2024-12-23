from pydub import AudioSegment
from pydub.playback import play
import pyttsx3
import os




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


# Main Configuration
total_music_duration = 60  # 60 minutes

# Units for each interval
units = [1,]

# Calculate total units
total_units = sum(units)

# Calculate seconds per unit
seconds_per_unit = total_music_duration / total_units

# Generate break intervals by calculating cumulative time
break_intervals = []
cumulative_time = 0

for unit in units:
    cumulative_time += unit * seconds_per_unit
    break_intervals.append(int(cumulative_time))

# Customize exercise settings
music_duration = total_music_duration
break_duration = 10
final_message = "Great workout! You've done an amazing job. See you next time!"

# Generate the narrations dynamically
narrations = generate_running_narrations(music_duration, break_intervals, break_duration, final_message)

# Print the narrations for review
for narration in narrations:
    print(narration)


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
            # create_narration(text, narration_file)
            create_narration_ai(text, narration_file)
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

# music_path = "C:/Users/recur/Desktop/WORK/Running Mix 2020 - Cropped.mp3"
music_path = r"C:\Users\recur\Desktop\WORK\Running Mix 2020 - Cropped.mp3"
output_path = "C:/Users/recur/Desktop/WORK/Modified_Music_with_Narrations_124_1.mp3"

# Create the customized MP3
create_custom_mp3(music_path, narrations, output_file=output_path)

















from elevenlabs.client import ElevenLabs

def create_narration_ai(
    text,
    save_path="narration.wav",
    api_key="sk_712c4a61f017d43b924d59e0df6653b01c2d27d77657895a",
    voice="Brian",
    model="eleven_multilingual_v2"
):
    """
    Generates high-quality narration using ElevenLabs AI and saves it as a WAV file.

    Parameters:
        text (str): The text to convert to speech.
        save_path (str): Path to save the generated WAV file.
        api_key (str): The ElevenLabs API key (default provided).
        voice (str): The AI voice to use (default is "Brian").
        model (str): The speech generation model to use (default is "eleven_multilingual_v2").

    Returns:
        str: Path to the saved WAV file.
    """
    try:
        # Initialize the ElevenLabs client
        client = ElevenLabs(api_key=api_key)

        # Generate the audio content
        audio = client.generate(
            text=text,
            voice=voice,
            model=model
        )

        # Combine audio content into bytes
        audio_content = b''.join(audio)

        # Save the audio content as a WAV file
        with open(save_path, "wb") as f:
            f.write(audio_content)

        print(f"Audio saved to {save_path}")
        return save_path

    except Exception as e:
        print(f"Error generating narration: {e}")
        return None















# old code
# Function to create narration from text
def create_narration(text, output_path):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    # Set the voice to an English voice
    engine.setProperty('voice', voices[1].id)  # For example, voices[1] could be an English voice
    engine.save_to_file(text, output_path)
    engine.runAndWait()


# Function to overlay narration with background music
def overlay_narration_with_music(music_path, narrations, output_file):
    # Load the background music (MP3)
    music = AudioSegment.from_mp3(music_path)
    music_duration = len(music) / 1000  # Convert milliseconds to seconds
    
    # Print the total length of the music in seconds
    print(f"Total music duration: {music_duration:.2f} seconds")
    
    # Append the custom narration at the end of the music
    narrations.append({
        "start_time": music_duration - 7,  # Add the narration 7 seconds before the music ends
        "text": "This is Bill Zou, who just wanna say thanks for your following me, good bye, hahaha!"
    })
    
    # Initialize the final audio as the music
    final_audio = music
    
    # Process each narration and insert it into the music at specified times
    for narration in narrations:
        start_time = narration["start_time"] * 1000  # Convert seconds to milliseconds
        text = narration["text"]
        
        # Generate the narration audio
        narration_file = "narration.wav"
        create_narration(text, narration_file)
        narration_audio = AudioSegment.from_wav(narration_file)
        
        # Reduce background music volume temporarily during narration
        music_during_narration = (
            final_audio[:start_time]
            + final_audio[start_time:start_time + len(narration_audio)].apply_gain(-30)
            + final_audio[start_time + len(narration_audio):]
        )
        
        # Overlay the narration onto the music at the specified time
        final_audio = music_during_narration.overlay(narration_audio, position=start_time)

        # Clean up the temporary narration file
        os.remove(narration_file)

    # Export the final audio with all narrations
    final_audio.export(output_file, format="mp3")
    return output_file



# Main function to run the process
def create_custom_mp3(music_path, narrations, output_file="output.mp3"):
    # Create the customized MP3 with narration
    final_output = overlay_narration_with_music(music_path, narrations, output_file)
    print(f"Audio successfully created and saved to {final_output}")
    
    # Optional: Play the final output (after it's created)
    # final_audio = AudioSegment.from_mp3(final_output)
    # play(final_audio)

# Example usage:
narrations = [
    {"start_time": 3, "text": "Starting countdown from 10. Here we go!"},
    {"start_time": 4, "text": "Ten..."},
    {"start_time": 5, "text": "Nine..."},
    {"start_time": 6, "text": "Eight..."},
    {"start_time": 7, "text": "Seven..."},
    {"start_time": 8, "text": "Six..."},
    {"start_time": 9, "text": "Five..."},
    {"start_time": 10, "text": "Four..."},
    {"start_time": 11, "text": "Three..."},
    {"start_time": 12, "text": "Two..."},
    {"start_time": 13, "text": "One..."},
    {"start_time": 14, "text": "Lift off! Let's go!"},
    {"start_time": 20, "text": "Are you still here? The fun's just getting started!"}
]

# music_path = "C:/Users/recur/Desktop/WORK/Running Mix 2020 - Cropped.mp3"
music_path = r"C:\Users\recur\Desktop\WORK\Running Mix 2020 _ 135 - 160 BPM _ Best Running Music.mp3"
output_path = "C:/Users/recur/Desktop/WORK/Modified_Music_with_Narrations.mp3"

# Create the customized MP3
create_custom_mp3(music_path, narrations, output_file=output_path)


















### below is another project...



'''

ffmpeg -protocol_whitelist "file,http,https,tcp,tls,crypto" -i "C:\Users\Administrator\Downloads\m.m3u8" -c copy "output.mp4"

ffmpeg -protocol_whitelist "file,http,https,tcp,tls,crypto" -i "C:\Users\Administrator\Downloads\m.m3u8" -vn -acodec libmp3lame "output.mp3"



'''
import subprocess
import os
import re
import pyperclip

def download_m3u8(m3u8_source, output_file, format="mp4"):
    """
    Downloads and converts an m3u8 file to mp4 or mp3.
    
    Parameters:
    - m3u8_source (str): The URL or local path to the .m3u8 file.
    - output_file (str): The desired output file name (e.g., 'output.mp4' or 'output.mp3').
    - format (str): Output format ('mp4' for video, 'mp3' for audio).
    
    Returns:
    - str: The path to the downloaded file or an error message.
    """
    # Validate format
    if format not in ["mp4", "mp3"]:
        return "Invalid format! Use 'mp4' or 'mp3'."
    
    # Build the ffmpeg command
    protocol_whitelist = "file,http,https,tcp,tls,crypto"
    ffmpeg_cmd = [
        "ffmpeg",
        "-protocol_whitelist", protocol_whitelist,
        "-i", m3u8_source
    ]
    
    if format == "mp4":
        # Video output: Copy streams without re-encoding
        ffmpeg_cmd.extend(["-c", "copy", output_file])
    elif format == "mp3":
        # Audio output: Extract audio and convert to MP3
        ffmpeg_cmd.extend(["-vn", "-acodec", "libmp3lame", output_file])
    
    # Run the command
    try:
        subprocess.run(ffmpeg_cmd, check=True)
        return f"Successfully downloaded and converted to {output_file}"
    except subprocess.CalledProcessError as e:
        return f"Error during conversion: {e}"

def is_url(source):
    """
    Checks if the given source is a URL.
    """
    return source.startswith("http://") or source.startswith("https://")

def get_next_file_name(base_folder, course_name, format="mp4"):
    """
    Determines the next available file name for the course series.
    
    Parameters:
    - base_folder (str): The directory to save the files.
    - course_name (str): The base name for the course (e.g., 'CourseName').
    - format (str): Desired output format ('mp4' or 'mp3').
    
    Returns:
    - str: The next available file name with full path.
    """
    # File extension
    ext = "mp4" if format == "mp4" else "mp3"
    
    # Regex to find existing files matching the pattern
    pattern = re.compile(rf"{re.escape(course_name)}\((\d+)\)\.{ext}$")
    existing_files = os.listdir(base_folder)
    numbers = []

    for file_name in existing_files:
        match = pattern.match(file_name)
        if match:
            numbers.append(int(match.group(1)))
    
    # Determine the next number
    next_number = max(numbers, default=-1) + 1
    return os.path.join(base_folder, f"{course_name}({next_number}).{ext}")

def handle_m3u8(m3u8_source, base_folder, course_name, format="mp4"):
    """
    Handles both local and URL m3u8 sources for downloading and converting.
    
    Parameters:
    - m3u8_source (str): The path or URL of the m3u8 file.
    - base_folder (str): The directory to save the downloaded files.
    - course_name (str): The base name for the course series.
    - format (str): Desired output format ('mp4' or 'mp3').
    
    Returns:
    - str: The result message.
    """
    # Ensure the output directory exists
    os.makedirs(base_folder, exist_ok=True)

    # Generate the next available file name
    output_file = get_next_file_name(base_folder, course_name, format)

    # Handle local files or URLs
    if is_url(m3u8_source):
        print(f"Processing URL: {m3u8_source}")
    elif os.path.exists(m3u8_source):
        print(f"Processing local file: {m3u8_source}")
        m3u8_source = os.path.abspath(m3u8_source)  # Get absolute path
    else:
        return "Invalid source! Provide a valid URL or local file path."
    
    # Download and convert
    return download_m3u8(m3u8_source, output_file, format)

def bootstrap_from_clipboard(course_name, format="mp4"):
    """
    Boots up the process by reading the URL from the clipboard and initiating the download.
    
    This function will extract the m3u8 URL from the clipboard and start the download process.
    """
    # Get the URL from the clipboard
    m3u8_source = pyperclip.paste()
    
    # Ensure the clipboard contains a valid URL
    if not is_url(m3u8_source):
        print("The clipboard does not contain a valid URL.")
        return
    
    # Define other parameters
    base_folder = r"C:\Users\Administrator\dwhelper"  # Folder to save downloads
    format = "mp4"  # 'mp4' for video or 'mp3' for audio
    
    # Call the handle_m3u8 function to process the URL
    result = handle_m3u8(m3u8_source, base_folder, course_name, format)
    print(result)

# Example usage
if __name__ == "__main__":
    bootstrap_from_clipboard("Statistics")
    bootstrap_from_clipboard("Probability")
    bootstrap_from_clipboard("GPT")



'''

刘嘉
跟杜国楹学创业
前沿课·吴军讲GPT
'''


from moviepy.editor import AudioFileClip, concatenate_audioclips
import os

# Helper function to extract audio as MP3
def extract_audio(file_path):
    """
    Extracts audio from an MP4 file and saves it as an MP3 file.
    """
    try:
        print(f"Extracting audio from: {file_path}")
        audio = AudioFileClip(file_path)
        mp3_path = file_path.replace(".mp4", ".mp3")
        audio.write_audiofile(mp3_path)
        print(f"Audio extracted: {mp3_path}")
        return mp3_path
    except Exception as e:
        print(f"Error extracting audio from {file_path}: {e}")
        return None

# Combine audio files into a single MP3 using moviepy
def combine_audio_files(audio_files, output_path):
    """
    Combines multiple MP3 files into a single MP3 file using moviepy.
    """
    print(f"Combining audio files into: {output_path}")
    try:
        audio_clips = [AudioFileClip(file) for file in audio_files]
        combined_audio = concatenate_audioclips(audio_clips)
        combined_audio.write_audiofile(output_path)
        print(f"Combined audio saved to: {output_path}")
    except Exception as e:
        print(f"Error combining audio files: {e}")

# Main script logic
if __name__ == "__main__":
    folder_path = r"G:\courses"  # Path to the folder containing MP4 files

    # Lists for storing audio files
    gpt_files = []
    probability_files = []

    # Populate the file lists with MP4 files
    for file in sorted(os.listdir(folder_path)):
        if file.startswith("GPT") and file.endswith(".mp4"):
            gpt_files.append(os.path.join(folder_path, file))
        elif file.startswith("Probability") and file.endswith(".mp4"):
            probability_files.append(os.path.join(folder_path, file))

    # Interleave the files
    combined_files = []
    max_length = max(len(gpt_files), len(probability_files))
    for i in range(max_length):
        if i < len(probability_files):
            combined_files.append(probability_files[i])
        if i < len(gpt_files):
            combined_files.append(gpt_files[i])

    # Extract audio and prepare MP3 list
    valid_audio_files = []
    for file in combined_files:
        mp3_file = extract_audio(file)
        if mp3_file:
            valid_audio_files.append(mp3_file)

    # Check if valid MP3 files exist
    if valid_audio_files:
        # Combine the audio files into one
        output_audio_path = os.path.join(folder_path, "Combined_Audio.mp3")
        combine_audio_files(valid_audio_files, output_audio_path)
    else:
        print("No valid audio files found. Exiting.")











from moviepy.editor import AudioFileClip, concatenate_audioclips
import os


# Function to extract audio as MP3 from MP4 files
def extract_audio_from_mp4(folder_path):
    """
    Extracts audio from all MP4 files in the folder and saves them as MP3 files.
    """
    print("Converting MP4 files to MP3...")
    mp3_files = []
    for file in sorted(os.listdir(folder_path)):
        if file.endswith(".mp4"):
            file_path = os.path.join(folder_path, file)
            try:
                print(f"Extracting audio from: {file_path}")
                audio = AudioFileClip(file_path)
                mp3_path = file_path.replace(".mp4", ".mp3")
                audio.write_audiofile(mp3_path)
                print(f"Audio extracted: {mp3_path}")
                mp3_files.append(mp3_path)
            except Exception as e:
                print(f"Error extracting audio from {file_path}: {e}")
    print(f"MP4 to MP3 conversion completed. {len(mp3_files)} files converted.")
    return mp3_files


# Function to combine MP3 files into one
def combine_audio_files(audio_files, output_path):
    """
    Combines multiple MP3 files into a single MP3 file using moviepy.
    """
    print(f"Combining audio files into: {output_path}")
    try:
        audio_clips = [AudioFileClip(file) for file in audio_files]
        combined_audio = concatenate_audioclips(audio_clips)
        combined_audio.write_audiofile(output_path)
        print(f"Combined audio saved to: {output_path}")
    except Exception as e:
        print(f"Error combining audio files: {e}")


# Function to interleave two lists of files
def interleave_files(list1, list2):
    """
    Interleaves two lists of files and returns the combined list.
    """
    interleaved_list = []
    max_length = max(len(list1), len(list2))
    for i in range(max_length):
        if i < len(list1):
            interleaved_list.append(list1[i])
        if i < len(list2):
            interleaved_list.append(list2[i])
    return interleaved_list


# Helper function to format time in hh:mm:ss or mm:ss
def format_time(seconds):
    """
    Formats time in seconds into hh:mm:ss or mm:ss format.
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)

    if hours > 0:
        return f"{hours:02}:{minutes:02}:{seconds:02}"
    else:
        return f"{minutes:02}:{seconds:02}"


# Function to display interleaved file order with time frames
def display_interleaved_order(audio_files):
    """
    Displays the interleaved order of files with their time frames in hh:mm:ss or mm:ss format.
    """
    print("\nInterleaved File Order with Time Frames:")
    cumulative_time = 0  # Track cumulative duration
    for index, file in enumerate(audio_files, start=1):
        try:
            with AudioFileClip(file) as audio:
                duration = audio.duration
                start_time = cumulative_time
                end_time = cumulative_time + duration
                print(f"{index}: {os.path.basename(file)} "
                      f"({format_time(start_time)} to {format_time(end_time)})")
                cumulative_time = end_time
        except Exception as e:
            print(f"Error reading duration for {file}: {e}")


# Main function
def main(folder_path, output_file, convert_mp4=True):
    """
    Main logic for extracting MP3s, interleaving files, and combining them.
    """
    if convert_mp4:
        # Extract MP3 files from MP4s
        extract_audio_from_mp4(folder_path)

    # Gather MP3 files
    gpt_files = []
    probability_files = []
    for file in sorted(os.listdir(folder_path)):
        if file.startswith("GPT") and file.endswith(".mp3"):
            gpt_files.append(os.path.join(folder_path, file))
        elif file.startswith("Probability") and file.endswith(".mp3"):
            probability_files.append(os.path.join(folder_path, file))

    # Interleave files
    combined_files = interleave_files(probability_files, gpt_files)

    # Display interleaved order with time frames
    if combined_files:
        display_interleaved_order(combined_files)

    # Combine MP3 files
    if combined_files:
        combine_audio_files(combined_files, output_file)
    else:
        print("No valid MP3 files found to combine.")


if __name__ == "__main__":
    # Folder containing the MP4/MP3 files
    folder_path = r"G:\courses"
    # Output file for the combined MP3
    output_audio_path = os.path.join(folder_path, "Combined_Audio1.mp3")
    # Call the main function with the folder path and output file
    main(folder_path, output_audio_path, convert_mp4=True)







kk = 'sk_712c4a61f017d43b924d59e0df6653b01c2d27d77657895a'


from elevenlabs import play
from elevenlabs.client import ElevenLabs

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

    # Optionally play the audio
    play(audio_content)

    print(f"Audio saved to {save_path}")
    
    return save_path

# Example usage:
# api_key = input("Please enter your ElevenLabs API key: ")
api_key = kk
text_to_speech = "A few days ago, I saw on TikTok that some guys are trying to copy our products. They bought some of our building block sets—the ones I told you about—and this guy made some cool videos using AI-generated voices as the narrator. Then he even built a website and tried to sell our products without our permission."
# text_to_speech = "几天前，我在TikTok上看到有些人在尝试抄袭我们的产品。他们买了我们的一些积木套装——就是我告诉过你的那些——然后这个人用AI生成的声音做旁白，制作了一些很酷的视频。然后他甚至建立了一个网站，试图未经我们允许销售我们的产品。"
save_path = r"C:\Users\recur\Desktop\WORK\my_auto\myscripts\custom_test_message.mp3"
generate_and_save_audio(api_key, text_to_speech, voice="Alice", model="eleven_multilingual_v2", save_path=save_path)












from moviepy.editor import VideoFileClip, concatenate_videoclips
import os

class VideoHandler:
    def concatenate_videos(self, video_paths, output_path):
        """
        Concatenates multiple video files into one.

        :param video_paths: List of file paths to the videos to be concatenated.
        :param output_path: Path to save the concatenated video.
        """
        try:
            clips = [VideoFileClip(path) for path in video_paths]
            final_clip = concatenate_videoclips(clips, method="compose")
            final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
            print(f"Concatenated video saved to {output_path}")
        except Exception as e:
            print(f"Error while concatenating videos: {e}")
        finally:
            for clip in clips:
                clip.close()

# Instantiate VideoHandler
handler = VideoHandler()

# Paths to your videos
video_list = [
    r"C:\Users\Administrator\Downloads\314547623-1-192.mp4",
    r"C:\Users\Administrator\Downloads\【浙江大学】博弈论｜可爱的老师又来了.mp4",
    r"C:\Users\Administrator\Downloads\【浙江大学】博弈论｜可爱的老师又来了 (1).mp4"
]

# Output directory and file
output_dir = r"G:\temp"
output_file = os.path.join(output_dir, "concatenated_video.mp4")

# Concatenate videos
handler.concatenate_videos(video_list, output_file)














def interleave_lists(*lists):
    """
    Interleaves multiple lists, handling varying lengths.
    :param lists: Multiple lists to interleave
    :return: A single list with interleaved elements
    """
    interleaved = []
    max_length = max(len(lst) for lst in lists)
    for i in range(max_length):
        for lst in lists:
            if i < len(lst):
                interleaved.append(lst[i])
    return interleaved

# Example usage
lt1 = ['a', 'b', 'c']
lt2 = [1, 2, 3, 4]
result = interleave_lists(lt1, lt2)
print(result)  # Output: ['a', 1, 'b', 2, 'c', 3, 4]







import os
import math
from moviepy.video.io.VideoFileClip import VideoFileClip
from tqdm import tqdm

class VideoProcessor:
    def __init__(self, video_path):
        """Initialize the VideoProcessor object with a video file path."""
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"The file {video_path} does not exist.")
        
        self.video_path = video_path
        self.video_name = os.path.splitext(os.path.basename(video_path))[0]
        self.video_dir = os.path.dirname(video_path)

    def split_video(self, snippet_duration):
        """Split the video into snippets of the specified duration.

        Args:
            snippet_duration (int): Duration of each snippet in seconds.

        Returns:
            list: List of file paths for the generated video snippets.
        """
        if snippet_duration <= 0:
            raise ValueError("Snippet duration must be greater than 0.")

        with VideoFileClip(self.video_path) as video:
            total_duration = math.ceil(video.duration)  # Total duration in seconds

            snippet_paths = []
            total_snippets = math.ceil(total_duration / snippet_duration)

            print("Splitting video...")
            for i, start_time in enumerate(
                tqdm(range(0, total_duration, snippet_duration), desc="Processing", unit="snippet")
            ):
                end_time = min(start_time + snippet_duration, total_duration)
                
                # Check if the snippet range is valid
                if start_time >= total_duration:
                    break

                snippet_filename = f"{self.video_name}_part_{i + 1}.mp4"
                snippet_path = os.path.join(self.video_dir, snippet_filename)

                # Prevent overwriting
                if os.path.exists(snippet_path):
                    print(f"Skipping existing file: {snippet_path}")
                    snippet_paths.append(snippet_path)
                    continue

                try:
                    snippet = video.subclip(start_time, end_time)
                    snippet.write_videofile(
                        snippet_path, codec="libx264", audio_codec="aac", logger="bar"
                    )
                    snippet_paths.append(snippet_path)
                except Exception as e:
                    print(f"Error processing snippet {i + 1}: {e}")
                    continue

            print(f"Successfully split video into {total_snippets} snippets.")

        return snippet_paths


# Example usage:
if __name__ == "__main__":
    video_a_path = r"C:\Users\recur\dwhelper\linear_al2.mp4"

    snippet_duration = 300  # 5 minutes

    video_a_processor = VideoProcessor(video_a_path)

    try:
        video_a_snippets = video_a_processor.split_video(snippet_duration)
        print("Video A snippets:", video_a_snippets)
    except Exception as e:
        print(f"Error occurred: {e}")









from moviepy.editor import VideoFileClip, concatenate_videoclips
from pathlib import Path

# Paths to video files
video_files = [
    "C:\\Users\\recur\\dwhelper\\ai_1_part_1.mp4",
    "C:\\Users\\recur\\dwhelper\\linear_al_part_1.mp4",
    "C:\\Users\\recur\\dwhelper\\ai_1_part_2.mp4",
    "C:\\Users\\recur\\dwhelper\\linear_al_part_2.mp4",
    "C:\\Users\\recur\\dwhelper\\ai_1_part_3.mp4",
    "C:\\Users\\recur\\dwhelper\\linear_al_part_3.mp4",
    "C:\\Users\\recur\\dwhelper\\ai_1_part_4.mp4",
    "C:\\Users\\recur\\dwhelper\\linear_al_part_4.mp4",
    "C:\\Users\\recur\\dwhelper\\ai_1_part_5.mp4",
    "C:\\Users\\recur\\dwhelper\\linear_al_part_5.mp4",
    "C:\\Users\\recur\\dwhelper\\ai_1_part_6.mp4",
    "C:\\Users\\recur\\dwhelper\\linear_al_part_6.mp4",
]

output_file = "C:\\Users\\recur\\dwhelper\\concatenated_video3.mp4"

# Check if all files exist
for video in video_files:
    if not Path(video).exists():
        raise FileNotFoundError(f"File not found: {video}")

# Load video clips
clips = []
for video in video_files:
    print(f"Loading video: {video}")
    clip = VideoFileClip(video)
    clips.append(clip)

# Concatenate video clips
print("Concatenating videos...")
final_clip = concatenate_videoclips(clips, method="compose")

# Write the final video
print("Saving the concatenated video...")
final_clip.write_videofile(output_file, codec="libx264", audio_codec="aac", fps=30, preset="ultrafast")

# Close all clips
for clip in clips:
    clip.close()

print(f"Concatenated video saved as: {output_file}")














import pyttsx3
import pyperclip

def save_clipboard_to_audio(file_name="output.mp3", language="zh", rate_increase=50):
    # Initialize the pyttsx3 engine
    engine = pyttsx3.init()
    
    # Get text from clipboard
    clipboard_text = pyperclip.paste()
    
    if not clipboard_text.strip():
        print("Clipboard is empty. Please copy some text first.")
        return
    
    # Set properties for the voice engine
    voices = engine.getProperty('voices')
    chinese_voice = None

    # Find a Chinese-compatible voice
    for voice in voices:
        if voice.languages and language in voice.languages[0].decode("utf-8"):
            chinese_voice = voice
            break

    if chinese_voice:
        engine.setProperty('voice', chinese_voice.id)
    else:
        print("No Chinese-compatible voice found. Using default voice.")
    
    # Increase the voice speed (rate)
    current_rate = engine.getProperty('rate')  # Default speed
    engine.setProperty('rate', current_rate + rate_increase)  # Faster speed
    
    # Save audio to file
    engine.save_to_file(clipboard_text, file_name)
    engine.runAndWait()
    
    print(f"Audio saved to {file_name} with faster voice speed.")

if __name__ == "__main__":
    # Save audio with a faster speed (increase rate by 50)
    save_clipboard_to_audio(rate_increase=100)  # Change the number for different speeds



from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import pyperclip

def save_clipboard_to_audio(file_name="output.mp3", language="zh", speed_factor=1.5):
    # Get text from clipboard
    clipboard_text = pyperclip.paste()
    
    if not clipboard_text.strip():
        print("Clipboard is empty. Please copy some text first.")
        return
    
    # Convert text to audio and save as MP3
    tts = gTTS(text=clipboard_text, lang=language)
    tts.save(file_name)
    print(f"Audio saved to {file_name}. Now adjusting speed...")

    # Adjust playback speed using pydub
    audio = AudioSegment.from_file(file_name)
    faster_audio = audio._spawn(audio.raw_data, overrides={
        "frame_rate": int(audio.frame_rate * speed_factor)
    }).set_frame_rate(audio.frame_rate)
    
    # Save the modified audio
    faster_file_name = f"faster_{file_name}"
    faster_audio.export(faster_file_name, format="mp3")
    print(f"Faster audio saved to {faster_file_name}")

if __name__ == "__main__":
    # Save audio with faster speed (1.5x)
    save_clipboard_to_audio(speed_factor=2.0)







