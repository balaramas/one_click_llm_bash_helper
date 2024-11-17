import pyperclip
import subprocess
import threading
import ollama
from pynput import keyboard

class CommandAssistant:
    def __init__(self):
        # Start listening for key events
        self.listener = keyboard.Listener(on_press=self.on_key_press)
        self.listener.start()

    def on_key_press(self, key):
        try:
            if key == keyboard.Key.f6:
                # Trigger command generation on F6
                print("Processing task description...")
                self.process_task_description()
        except AttributeError:
            pass

    def process_task_description(self):
        # Step 1: Copy the selected text using Ctrl+Shift+C
        subprocess.run(['xdotool', 'key', '--clearmodifiers', 'ctrl+shift+c'])

        # Get the selected text from clipboard
        task_description = pyperclip.paste()

        # Set up the command-generation prompt
        prompt = (
            "You are a Linux terminal assistant. Convert the following description of a task "
            "into a single Linux command that accomplishes it. Provide only the command, "
            "without any additional text or surrounding quotes:\n\n"
            f"Task description: {task_description}"
        )

        # Step 2: Run command generation in a separate thread
        threading.Thread(target=self.generate_command, args=(prompt,)).start()

    def generate_command(self, prompt):
        try:
            # Query the Llama model for the command
            response = ollama.generate(model='llama3.1', prompt=prompt)
            generated_command = response['response'].strip()

            # Remove any surrounding quotes (if present)
            if generated_command.startswith("'") and generated_command.endswith("'"):
                generated_command = generated_command[1:-1]
            elif generated_command.startswith('"') and generated_command.endswith('"'):
                generated_command = generated_command[1:-1]
            
            # Step 3: Replace the selected text with the generated command
            self.replace_with_command(generated_command)
        except Exception as e:
            print(f"Command generation error: {str(e)}")

    def replace_with_command(self, command):
        # Copy the generated command to the clipboard
        pyperclip.copy(command)

        # Step 4: Clear the current input using Ctrl+C
        subprocess.run(['xdotool', 'key', '--clearmodifiers', 'ctrl+c'])

        subprocess.run(['xdotool', 'key', '--clearmodifiers', 'ctrl+l'])

        # Step 5: Paste the generated command using Ctrl+Shift+V
        subprocess.run(['xdotool', 'key', '--clearmodifiers', 'ctrl+shift+v'])

if __name__ == "__main__":
    app = CommandAssistant()
    # Keep the script running to listen for key presses
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Exiting Command Assistant.")
