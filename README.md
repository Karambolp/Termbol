# Termbol AI Terminal

An advanced AI terminal assistant powered by Google's Gemini AI. Engage in natural conversations, ask questions, and get intelligent responses right from your terminal. With support for code highlighting, conversation history, and response saving.

## 🌟 Features

- **Interactive Mode**: Have natural conversations with AI
- **Quick Question Mode**: Get instant answers without starting a chat
- **Chat Mode**: Focused discussions on specific topics
- **Code Highlighting**: Automatic syntax highlighting for code snippets
- **Conversation History**: AI remembers the context of your chat
- **Save Responses**: Save AI responses to files for later reference
- **Beautiful UI**: Clean and modern terminal interface with colors
- **Cross-platform**: Works on any Linux system

## 💫 Installation

```bash
# Clone the repository
git clone https://github.com/Karambolp/termbol

# Navigate to directory
cd termbol

# Install the program
sudo ./install.sh
```

## 🚀 Usage

### Basic Commands
```bash
# Interactive mode - Start a general conversation
termbol

# Quick question mode - Get a quick answer
termbol -q "your question"

# Chat mode - Start a focused conversation on a topic
termbol -m

# Update save directory
termbol -sd

# Show help
termbol --help

# Uninstall
sudo ./uninstall.sh
```

### Interactive Mode Commands
- `q` - Quit the program
- `save` - Save the last AI response
- Just type your message to chat with AI

### Chat Mode Commands
- `q` - Quit chat mode
- `new` - Start a new topic
- `save` - Save the last AI response

### Save Directory
By default, responses are saved to:
```
~/Documents/termbol_saves/
```
You can change this using the `-sd` command.

## 🔑 API Key Setup
1. Visit [Google AI Studio](https://aistudio.google.com)
2. Sign in with your Google account
3. Click 'Get API Key'
4. Create a new API key
5. During installation, paste your API key when prompted

## 🎨 Features in Detail

### Code Highlighting
The program automatically detects and highlights code blocks in responses:
- Supports multiple programming languages
- Uses distinct colors for better readability
- Preserves code formatting

### Conversation History
- AI remembers previous messages in the conversation
- Provides context-aware responses
- History is maintained until you quit or start a new topic

### Response Saving
- Responses are saved with timestamps
- Files are saved in plain text format
- Easy to access and read later

### Error Handling
- Graceful handling of network issues
- Clear error messages
- Automatic recovery from interruptions

## 🛠️ Technical Details

### System Requirements
- Python 3.6 or higher
- Linux-based operating system
- Internet connection for API access

### Dependencies
- google.generativeai - Google's Gemini AI API
- python-dotenv - Environment variable management
- pyperclip - Clipboard operations
- colorama - Terminal colors

### Installation Details
- Creates installation directory at `/opt/termbol`
- Installs executable to `/usr/local/bin`
- Stores configuration in `.env` file
- Sets appropriate file permissions

### Security
- API key stored securely in `.env` file
- File permissions set to protect sensitive data
- No data sent to third parties

## 💻 Tech Stack
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Shell Script](https://img.shields.io/badge/shell_script-%23121011.svg?style=for-the-badge&logo=gnu-bash&logoColor=white)
![Google Cloud](https://img.shields.io/badge/Google%20Cloud-%234285F4.svg?style=for-the-badge&logo=google-cloud&logoColor=white)
![LINUX](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)

## 📊 GitHub Stats
![](https://github-readme-stats.vercel.app/api?username=karambolp&theme=dark&hide_border=false&include_all_commits=false&count_private=false)<br/>
![](https://github-readme-streak-stats.herokuapp.com/?user=karambolp&theme=dark&hide_border=false)<br/>
![](https://github-readme-stats.vercel.app/api/top-langs/?username=karambolp&theme=dark&hide_border=false&include_all_commits=false&count_private=false&layout=compact)

## 🏆 GitHub Trophies
![](https://github-profile-trophy.vercel.app/?username=karambolp&theme=radical&no-frame=false&no-bg=true&margin-w=4)

---
[![](https://visitcount.itsvg.in/api?id=karambolp&icon=0&color=0)](https://visitcount.itsvg.in)

<!-- Proudly created with GPRM ( https://gprm.itsvg.in ) --> 