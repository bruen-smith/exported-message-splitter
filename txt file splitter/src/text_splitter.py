import os
import re

# Settings
INPUT_FILE = r"C:\Users\bruen\OneDrive\Downloads\large_text_file"
OUTPUT_DIR = "chunks"
OUTPUT_PREFIX = "text_chunk_"
TARGET_WORDS_PER_CHUNK = 450000  # adjust based on limit

# Helpers

# Detects lines like:
# [1/19/2023 13:59] username
MESSAGE_HEADER = re.compile(r"^\[\d{1,2}/\d{1,2}/\d{4} \d{1,2}:\d{2}\] ")


def is_message_header(line: str) -> bool:
    return bool(MESSAGE_HEADER.match(line))


def count_words(text: str) -> int:
    return len(text.split())


# Load file
os.makedirs(OUTPUT_DIR, exist_ok=True)

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Group lines into full messages
messages = []
current_message = []

for line in lines:
    if is_message_header(line):
        if current_message:
            messages.append("".join(current_message))
            current_message = []
    current_message.append(line)

# Add last message
if current_message:
    messages.append("".join(current_message))

print(f"Total messages parsed: {len(messages)}")

# Create chunks by WORD COUNT, not by lines
chunk_index = 1
current_chunk = []
current_word_total = 0

for msg in messages:
    msg_word_count = count_words(msg) # change to count_lines(msg) if lines is the goal

    # If adding this message would exceed chunk size → save file
    if current_word_total + msg_word_count > TARGET_WORDS_PER_CHUNK and current_chunk:
        filename = f"{OUTPUT_PREFIX}{chunk_index}.txt"
        filepath = os.path.join(OUTPUT_DIR, filename)

        with open(filepath, "w", encoding="utf-8") as out:
            out.write("".join(current_chunk))

        print(f"Created: {filename} (approx {current_word_total} words)")

        chunk_index += 1
        current_chunk = []
        current_word_total = 0

    # Add message to chunk
    current_chunk.append(msg)
    current_word_total += msg_word_count

# Write final chunk
if current_chunk:
    filename = f"{OUTPUT_PREFIX}{chunk_index}.txt"
    filepath = os.path.join(OUTPUT_DIR, filename)

    with open(filepath, "w", encoding="utf-8") as out:
        out.write("".join(current_chunk))

    print(f"Created: {filename} (approx {current_word_total} words)")

print("Done!")

