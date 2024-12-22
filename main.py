import os
import sys
import re
import pyperclip
import google.generativeai as genai
from dotenv import load_dotenv
import datetime

# Colors and styles
class Style:
    PURPLE = '\033[38;5;141m'  # Lighter purple
    CYAN = '\033[38;5;51m'     # Bright cyan
    BLUE = '\033[38;5;75m'     # Light blue
    GREEN = '\033[38;5;114m'   # Soft green
    YELLOW = '\033[38;5;221m'  # Soft yellow
    RED = '\033[38;5;203m'     # Soft red
    GRAY = '\033[38;5;245m'    # Medium gray
    WHITE = '\033[38;5;255m'   # Bright white
    BOLD = '\033[1m'
    END = '\033[0m'
    BG_BLACK = '\033[48;5;233m'  # Very dark gray (near black)

def create_box(title, width=60):
    title = f" {title} "
    padding = width - len(title) - 2
    line = "─" * padding
    return f"{Style.GRAY}╭{title}{line}╮{Style.END}"

def create_bottom(width=60):
    return f"{Style.GRAY}╰{'─' * (width - 2)}╯{Style.END}"

def format_message(text, is_code=False):
    width = 60 if not is_code else 50
    
    if is_code:
        formatted = create_box("💻 Code", width)
        lines = text.split('\n')
        for line in lines:
            padding = ' ' * (width - len(line) - 2)
            formatted += f"\n{Style.GRAY}│{Style.END} {Style.YELLOW}{line}{Style.END}{padding}{Style.GRAY}│{Style.END}"
    else:
        formatted = create_box("💬 Message", width)
        words = text.split()
        lines = []
        current_line = []
        current_length = 0
        
        for word in words:
            if current_length + len(word) + 1 <= width - 4:
                current_line.append(word)
                current_length += len(word) + 1
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
                current_length = len(word)
        
        if current_line:
            lines.append(' '.join(current_line))
        
        for line in lines:
            padding = ' ' * (width - len(line) - 2)
            formatted += f"\n{Style.GRAY}│{Style.END} {Style.WHITE}{line}{Style.END}{padding}{Style.GRAY}│{Style.END}"
    
    formatted += f"\n{create_bottom(width)}"
    return formatted, text

def save_to_file(text, save_dir):
    try:
        # Create directory if it doesn't exist
        os.makedirs(save_dir, exist_ok=True)
        
        # Use timestamp for filename
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{save_dir}/termbol_{timestamp}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(text)
        
        print(f"\n{Style.GREEN}✓ Text saved to: {filename}{Style.END}")
    except Exception as e:
        print(f"\n{Style.RED}✗ Save error: {str(e)}{Style.END}")

def update_save_dir():
    install_dir = "/opt/termbol"
    env_file = f"{install_dir}/.env"
    
    print(f"\n{Style.BOLD}Termbol AI - Update Save Directory{Style.END}")
    print("=" * 40)
    print("\nEnter the directory where texts will be saved:")
    save_dir = input(f"{Style.GREEN}>{Style.END} ")
    
    if not save_dir:
        print(f"\n{Style.RED}✗ Directory path cannot be empty!{Style.END}")
        return
    
    # Expand directory (resolve ~ characters)
    save_dir = os.path.expanduser(save_dir)
    
    try:
        # Test if directory can be created
        os.makedirs(save_dir, exist_ok=True)
        
        # Read current .env file
        with open(env_file, 'r') as f:
            lines = f.readlines()
        
        # Find or add SAVE_DIR line
        save_dir_line = f"SAVE_DIR={save_dir}\n"
        save_dir_found = False
        
        for i, line in enumerate(lines):
            if line.startswith("SAVE_DIR="):
                lines[i] = save_dir_line
                save_dir_found = True
                break
        
        if not save_dir_found:
            lines.append("\n# Save Directory\n")
            lines.append("# -------------\n")
            lines.append(save_dir_line)
        
        # Update file
        with open(env_file, 'w') as f:
            f.writelines(lines)
        
        print(f"\n{Style.GREEN}✓ Save directory updated!{Style.END}")
    except Exception as e:
        print(f"\n{Style.RED}✗ Error: {str(e)}{Style.END}")
        print("Root privileges required to update directory path.")
        print("Run the command as 'sudo termbol -sd'")

def save_last_response(text, save_dir):
    try:
        # Create directory if it doesn't exist
        os.makedirs(save_dir, exist_ok=True)
        
        # Use timestamp for filename
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{save_dir}/termbol_{timestamp}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(text)
        
        print(f"\n{Style.GREEN}✓ AI response saved to: {filename}{Style.END}")
    except Exception as e:
        print(f"\n{Style.RED}✗ Save error: {str(e)}{Style.END}")

def interactive_mode():
    print(f"\n{Style.BOLD}{Style.PURPLE}╭{'─' * 58}╮{Style.END}")
    print(f"{Style.BOLD}{Style.PURPLE}│{' ' * 18}Gemini AI Terminal{' ' * 19}│{Style.END}")
    print(f"{Style.BOLD}{Style.PURPLE}╰{'─' * 58}╯{Style.END}")
    print(f"\n{Style.CYAN}Type 'q' to quit | Type 'save' to save the last response{Style.END}")
    
    chat_history = []
    last_response = None  # Store last response
    
    while True:
        user_input = input(f"\n{Style.GREEN}You:{Style.END} ")
        
        if user_input.lower() == 'q':
            print(f"\n{Style.YELLOW}Goodbye!{Style.END}")
            break
        elif user_input.lower() == 'save' and last_response:
            save_last_response(last_response, SAVE_DIR)
            continue
        elif user_input.lower() == 'save':
            print(f"\n{Style.RED}✗ No response to save yet!{Style.END}")
            continue
            
        try:
            # Keep context using chat history
            if chat_history:
                context = f"""Chat history:
{chr(10).join([f"{'Me' if msg[0] == 'user' else 'You'}: {msg[1]}" for msg in chat_history])}

Message: {user_input}"""
            else:
                context = user_input

            response = model.generate_content(context)
            last_response = response.text  # Store last response
            
            # Find and format code blocks
            text = response.text
            code_blocks = re.findall(r'```(?:\w+\n)?(.*?)```', text, re.DOTALL)
            
            if code_blocks:
                # Split code blocks and normal text
                parts = re.split(r'```(?:\w+\n)?.*?```', text, flags=re.DOTALL)
                
                # Format each part appropriately
                for i, part in enumerate(parts):
                    if part.strip():
                        formatted, raw_text = format_message(part.strip())
                        print(f"\n{Style.BLUE}AI:{Style.END}", formatted)
                    
                    if i < len(code_blocks):
                        formatted, raw_text = format_message(code_blocks[i], is_code=True)
                        print(formatted)
            else:
                # Just normal text
                formatted, raw_text = format_message(text)
                print(f"\n{Style.BLUE}AI:{Style.END}", formatted)
            
            # Update chat history
            chat_history.append(("user", user_input))
            chat_history.append(("ai", response.text))
        except Exception as e:
            print(f"{Style.RED}Error occurred: {str(e)}{Style.END}")

def chat_mode():
    print(f"\n{Style.BOLD}{Style.PURPLE}╭{'─' * 58}╮{Style.END}")
    print(f"{Style.BOLD}{Style.PURPLE}│{' ' * 18}Gemini AI Chat{' ' * 23}│{Style.END}")
    print(f"{Style.BOLD}{Style.PURPLE}╰{'─' * 58}╯{Style.END}")
    print(f"\n{Style.CYAN}Commands:{Style.END}")
    print(f"{Style.CYAN}• Type 'q' to quit{Style.END}")
    print(f"{Style.CYAN}• Type 'new' for a new topic{Style.END}")
    print(f"{Style.CYAN}• Type 'save' to save the last response{Style.END}")
    
    current_topic = ""
    chat_history = []
    last_response = None  # Store last response
    
    while True:
        if not current_topic:
            print(f"\n{Style.CYAN}📝 What topic would you like to discuss?{Style.END}")
            print(f"{Style.GRAY}(Example: Python programming, Linux commands, Artificial Intelligence...){Style.END}")
            print(f"{Style.GREEN}You:{Style.END}", end=" ")
            current_topic = input()
            
            if current_topic.lower() == 'q':
                print(f"\n{Style.YELLOW}Goodbye!{Style.END}")
                break
            elif current_topic.lower() == 'save' and last_response:
                save_last_response(last_response, SAVE_DIR)
                continue
            elif current_topic.lower() == 'save':
                print(f"\n{Style.RED}✗ No response to save yet!{Style.END}")
                continue
            elif not current_topic.strip():
                print(f"\n{Style.RED}✗ Please enter a topic!{Style.END}")
                continue
            
            print(f"\n{Style.PURPLE}✨ Let's talk about '{current_topic}'{Style.END}")
            print(f"{Style.GRAY}(Type your questions...){Style.END}")
            
            # Send first message
            try:
                response = model.generate_content(current_topic)
                last_response = response.text  # Store last response
                
                formatted, raw_text = format_message(response.text)
                print(f"\n{Style.BLUE}AI:{Style.END}", formatted)
                
                chat_history.append(("system", current_topic))
                chat_history.append(("ai", response.text))
            except Exception as e:
                print(f"\n{Style.RED}❌ Error occurred: {str(e)}{Style.END}")
            continue
            
        print(f"{Style.GREEN}You:{Style.END}", end=" ")
        user_input = input()
        
        if user_input.lower() == 'q':
            print(f"\n{Style.YELLOW}Goodbye!{Style.END}")
            break
        elif user_input.lower() == 'new':
            print(f"\n{Style.CYAN}🔄 Starting a new topic...{Style.END}")
            current_topic = ""
            chat_history = []
            continue
        elif user_input.lower() == 'save' and last_response:
            save_last_response(last_response, SAVE_DIR)
            continue
        elif user_input.lower() == 'save':
            print(f"\n{Style.RED}✗ No response to save yet!{Style.END}")
            continue
        elif not user_input.strip():
            print(f"\n{Style.RED}✗ Please type something!{Style.END}")
            continue
            
        try:
            context = f"""Chat history:
{chr(10).join([f"{'Me' if msg[0] == 'user' else 'You'}: {msg[1]}" for msg in chat_history if msg[0] in ['user', 'ai']])}

{user_input}"""

            response = model.generate_content(context)
            last_response = response.text  # Store last response
            
            # Find and format code blocks
            text = response.text
            code_blocks = re.findall(r'```(?:\w+\n)?(.*?)```', text, re.DOTALL)
            
            if code_blocks:
                # Split code blocks and normal text
                parts = re.split(r'```(?:\w+\n)?.*?```', text, flags=re.DOTALL)
                
                # Format each part appropriately
                for i, part in enumerate(parts):
                    if part.strip():
                        formatted, raw_text = format_message(part.strip())
                        print(f"\n{Style.BLUE}AI:{Style.END}", formatted)
                    
                    if i < len(code_blocks):
                        formatted, raw_text = format_message(code_blocks[i], is_code=True)
                        print(formatted)
            else:
                # Just normal text
                formatted, raw_text = format_message(text)
                print(f"\n{Style.BLUE}AI:{Style.END}", formatted)
            
            # Update chat history
            chat_history.append(("user", user_input))
            chat_history.append(("ai", response.text))
        except Exception as e:
            print(f"\n{Style.RED}❌ Error occurred: {str(e)}{Style.END}")

def quick_question(question):
    try:
        response = model.generate_content(question)
        
        # Find and format code blocks
        text = response.text
        code_blocks = re.findall(r'```(?:\w+\n)?(.*?)```', text, re.DOTALL)
        
        if code_blocks:
            # Split code blocks and normal text
            parts = re.split(r'```(?:\w+\n)?.*?```', text, flags=re.DOTALL)
            
            # Format each part appropriately
            for i, part in enumerate(parts):
                if part.strip():
                    formatted, raw_text = format_message(part.strip())
                    print(f"\n{Style.BLUE}Answer:{Style.END}", formatted)
                
                if i < len(code_blocks):
                    formatted, raw_text = format_message(code_blocks[i], is_code=True)
                    print(formatted)
        else:
            # Just normal text
            formatted, raw_text = format_message(text)
            print(f"\n{Style.BLUE}Answer:{Style.END}", formatted)
            
    except Exception as e:
        print(f"{Style.RED}Error occurred: {str(e)}{Style.END}")

def print_help():
    print(f"""
{Style.BOLD}Usage:{Style.END}
    {Style.GREEN}termbol{Style.END}              : Interactive mode
    {Style.GREEN}termbol -q "question"{Style.END}: Quick question mode
    {Style.GREEN}termbol -m{Style.END}           : Chat mode (continuous conversation on a topic)
    {Style.GREEN}termbol -sd{Style.END}          : Update save directory
    {Style.GREEN}termbol --help{Style.END}       : Help menu
    
{Style.BOLD}Examples:{Style.END}
    {Style.CYAN}termbol -q "What is the command to list files in Linux?"{Style.END}
    {Style.CYAN}termbol -m{Style.END}    # Start chat mode

{Style.BOLD}Saving Responses:{Style.END}
    Type 'save' after any response to save it to a file.
    Files are saved by default to ~/Documents/termbol_saves/
    """)

# Main program
if __name__ == "__main__":
    # Load API key and save directory from .env
    load_dotenv()
    GOOGLE_API_KEY = os.getenv('GEMINI_API_KEY')
    SAVE_DIR = os.path.expanduser(os.getenv('SAVE_DIR', '~/Documents/termbol_saves'))
    
    # Configure Gemini model
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
    
    # Process arguments
    i = 1
    while i < len(sys.argv):
        if sys.argv[i] in ['-h', '--help']:
            print_help()
            sys.exit()
        elif sys.argv[i] == '-sd':
            update_save_dir()
            sys.exit()
        elif sys.argv[i] == '-m':
            chat_mode()
            sys.exit()
        elif sys.argv[i] == '-q' and i + 1 < len(sys.argv):
            question = sys.argv[i + 1]
            quick_question(question)
            sys.exit()
        else:
            i += 1
    
    if len(sys.argv) == 1:
        interactive_mode() 