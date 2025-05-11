import os
import shutil
import re
import platform
from pathlib import Path
import spacy

class FileSystemAgent:
    def _init_(self):
        # Load the spaCy NLP model
        print("Loading NLP model...")
        self.nlp = spacy.load("en_core_web_sm")
        
        # Get user home directory
        self.home_dir = str(Path.home())
        
        # Common locations dictionary
        self.locations = {
            "desktop": os.path.join(self.home_dir, "Desktop"),
            "downloads": os.path.join(self.home_dir, "Downloads"),
            "documents": os.path.join(self.home_dir, "Documents"),
            "pictures": os.path.join(self.home_dir, "Pictures"),
            "music": os.path.join(self.home_dir, "Music"),
            "videos": os.path.join(self.home_dir, "Videos"),
            "home": self.home_dir
        }
        
        # Available actions
        self.actions = {
            "move": self.move_item,
            "copy": self.copy_item,
            "delete": self.delete_item,
            "rename": self.rename_item,
            "create": self.create_item,
            "list": self.list_items
        }
        
        print(f"File System Agent initialized for {platform.system()}")
        print(f"Home directory: {self.home_dir}")
    
    def process_command(self, command):
        """Process a natural language command"""
        print(f"\nProcessing command: '{command}'")
        
        # Parse the command using spaCy
        doc = self.nlp(command.lower())
        
        # Extract action, source, and destination
        action = None
        item_name = None
        source_location = None
        destination_location = None
        new_name = None
        
        # First, identify the action
        for token in doc:
            if token.lemma_ in self.actions:
                action = token.lemma_
                break
        
        # Fall back to regex pattern matching for actions
        if not action:
            action_patterns = {
                r"\bmove\b|\btransfer\b|\bput\b": "move",
                r"\bcopy\b|\bduplicate\b": "copy",
                r"\bdelete\b|\bremove\b|\btrash\b": "delete",
                r"\brename\b|\bchange name\b": "rename",
                r"\bcreate\b|\bmake\b|\bnew\b": "create",
                r"\blist\b|\bshow\b|\bdisplay\b": "list"
            }
            
            for pattern, act in action_patterns.items():
                if re.search(pattern, command.lower()):
                    action = act
                    break
        
        # Extract locations and item names
        if action:
            # Look for source location
            for loc_name, loc_path in self.locations.items():
                if loc_name in command.lower():
                    if not source_location:
                        source_location = loc_path
                    elif not destination_location and action in ["move", "copy"]:
                        destination_location = loc_path
            
            # Extract "from X to Y" pattern
            from_to_match = re.search(r"from\s+(\w+)\s+to\s+(\w+)", command.lower())
            if from_to_match:
                source_keyword, dest_keyword = from_to_match.groups()
                # Try to match these keywords to known locations
                for loc_name, loc_path in self.locations.items():
                    if source_keyword in loc_name:
                        source_location = loc_path
                    if dest_keyword in loc_name:
                        destination_location = loc_path
            
            # Extract item name - look for patterns like "folder named X" or just "X folder"
            name_match = re.search(r"(?:folder|file|directory)(?:\s+named|\s+called)?\s+[\"']?([^\"']+)[\"']?", command.lower())
            if name_match:
                item_name = name_match.group(1).strip()
            else:
                # Try to extract just the filename/foldername
                words = command.lower().split()
                folder_index = -1
                
                for i, word in enumerate(words):
                    if word in ["folder", "file", "directory"]:
                        folder_index = i
                        break
                
                if folder_index > 0 and folder_index < len(words) - 1:
                    item_name = words[folder_index - 1]
                
                # Last resort - look for quotes
                if not item_name:
                    quote_match = re.search(r"[\"']([^\"']+)[\"']", command)
                    if quote_match:
                        item_name = quote_match.group(1)
            
            # For rename action, try to extract new name
            if action == "rename":
                rename_match = re.search(r"(?:to|as)\s+[\"']?([^\"']+)[\"']?", command.lower())
                if rename_match:
                    new_name = rename_match.group(1).strip()
        
        # Execute the appropriate action if we have enough information
        if action:
            if action in ["move", "copy"]:
                if item_name and source_location and destination_location:
                    return self.actions[action](item_name, source_location, destination_location)
                else:
                    missing = []
                    if not item_name: missing.append("item name")
                    if not source_location: missing.append("source location")
                    if not destination_location: missing.append("destination location")
                    return f"I need more information: {', '.join(missing)}"
            
            elif action == "delete":
                if item_name and source_location:
                    return self.actions[action](item_name, source_location)
                else:
                    missing = []
                    if not item_name: missing.append("item name")
                    if not source_location: missing.append("source location")
                    return f"I need more information: {', '.join(missing)}"
            
            elif action == "rename":
                if item_name and source_location and new_name:
                    return self.actions[action](item_name, source_location, new_name)
                else:
                    missing = []
                    if not item_name: missing.append("current item name")
                    if not source_location: missing.append("location")
                    if not new_name: missing.append("new name")
                    return f"I need more information: {', '.join(missing)}"
            
            elif action == "create":
                if item_name and source_location:
                    return self.actions[action](item_name, source_location)
                else:
                    missing = []
                    if not item_name: missing.append("item name")
                    if not source_location: missing.append("location")
                    return f"I need more information: {', '.join(missing)}"
            
            elif action == "list":
                location = source_location or self.home_dir
                return self.actions[action](location)
        
        return "I couldn't understand the command. Please try providing more details or rephrase your request."
    
    def move_item(self, item_name, source_location, destination_location):
        """Move a file or folder from source to destination"""
        source_path = os.path.join(source_location, item_name)
        dest_path = os.path.join(destination_location, item_name)
        
        if not os.path.exists(source_path):
            return f"Error: '{item_name}' not found in {source_location}"
        
        try:
            shutil.move(source_path, dest_path)
            return f"Successfully moved '{item_name}' from {source_location} to {destination_location}"
        except Exception as e:
            return f"Error moving '{item_name}': {str(e)}"
    
    def copy_item(self, item_name, source_location, destination_location):
        """Copy a file or folder from source to destination"""
        source_path = os.path.join(source_location, item_name)
        dest_path = os.path.join(destination_location, item_name)
        
        if not os.path.exists(source_path):
            return f"Error: '{item_name}' not found in {source_location}"
        
        try:
            if os.path.isdir(source_path):
                shutil.copytree(source_path, dest_path)
            else:
                shutil.copy2(source_path, dest_path)
            return f"Successfully copied '{item_name}' from {source_location} to {destination_location}"
        except Exception as e:
            return f"Error copying '{item_name}': {str(e)}"
    
    def delete_item(self, item_name, source_location):
        """Delete a file or folder"""
        item_path = os.path.join(source_location, item_name)
        
        if not os.path.exists(item_path):
            return f"Error: '{item_name}' not found in {source_location}"
        
        try:
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
            else:
                os.remove(item_path)
            return f"Successfully deleted '{item_name}' from {source_location}"
        except Exception as e:
            return f"Error deleting '{item_name}': {str(e)}"
    
    def rename_item(self, item_name, source_location, new_name):
        """Rename a file or folder"""
        old_path = os.path.join(source_location, item_name)
        new_path = os.path.join(source_location, new_name)
        
        if not os.path.exists(old_path):
            return f"Error: '{item_name}' not found in {source_location}"
        
        try:
            os.rename(old_path, new_path)
            return f"Successfully renamed '{item_name}' to '{new_name}'"
        except Exception as e:
            return f"Error renaming '{item_name}': {str(e)}"
    
    def create_item(self, item_name, location, folder=True):
        """Create a new folder or file"""
        new_path = os.path.join(location, item_name)
        
        if os.path.exists(new_path):
            return f"Error: '{item_name}' already exists in {location}"
        
        try:
            if folder:
                os.makedirs(new_path)
                return f"Successfully created folder '{item_name}' in {location}"
            else:
                with open(new_path, 'w') as f:
                    pass
                return f"Successfully created file '{item_name}' in {location}"
        except Exception as e:
            return f"Error creating '{item_name}': {str(e)}"
    
    def list_items(self, location):
        """List files and folders in a location"""
        try:
            items = os.listdir(location)
            if not items:
                return f"No items found in {location}"
            
            result = f"Items in {location}:\n"
            for item in items:
                item_path = os.path.join(location, item)
                item_type = "📁 " if os.path.isdir(item_path) else "📄 "
                result += f"{item_type}{item}\n"
            
            return result
        except Exception as e:
            return f"Error listing items in {location}: {str(e)}"


# Example of a main program to use the agent
def main():
    # Install required packages if needed
    try:
        import spacy
        # Check if the English model is downloaded
        try:
            nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("Downloading spaCy language model...")
            import subprocess
            subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
    except ImportError:
        print("Installing required packages...")
        import subprocess
        import sys
        subprocess.check_call([sys.executable, "-m", "pip", "install", "spacy"])
        subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
    
    agent = FileSystemAgent()
    print("File System Agent is ready!")
    print("You can now use natural language commands like:")
    print("- 'move folder projects from desktop to documents'")
    print("- 'copy file report.pdf from downloads to desktop'")
    print("- 'create folder new_project in documents'")
    print("- 'delete file temp.txt from downloads'")
    print("- 'list files in downloads'")
    print("Type 'exit' to quit.\n")
    
    while True:
        command = input("What would you like me to do? > ")
        if command.lower() in ['exit', 'quit', 'bye']:
            print("Goodbye!")
            break
        
        result = agent.process_command(command)
        print(result)


if _name_ == "_main_":
    main()