from llama_index.tools import FunctionTool
import os
from datetime import datetime

note_file = os.path.join("data", "notes.txt")

def save_note_with_timestamp(note):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    note_with_timestamp = f"{timestamp} - {note}"

    if not os.path.exists(note_file):
        open(note_file, "w").close()

    with open(note_file, "a") as f:
        f.write(note_with_timestamp + "\n")

    return f"Note saved at {timestamp}"

def list_notes():
    if not os.path.exists(note_file):
        return "No notes found."

    with open(note_file, "r") as f:
        notes = f.readlines()

    if not notes:
        return "No notes found."

    formatted_notes = "".join(notes)
    return f"Here are your notes:\n{formatted_notes}"

note_saver_tool = FunctionTool.from_defaults(
    fn=save_note_with_timestamp,
    name="note_saver",
    description="This tool can save a text-based note with a timestamp to a file for the user",
)

note_reader_tool = FunctionTool.from_defaults(
    fn=list_notes,
    name="note_reader",
    description="This tool can read and list all the saved notes for the user",
)
