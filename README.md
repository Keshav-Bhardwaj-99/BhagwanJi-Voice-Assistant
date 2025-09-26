# Bhagwan Ji Spiritual Voice Assistant

A powerful voice-controlled assistant built with Python that can perform various tasks through voice commands while embodying the persona of "Bhagwan Ji".

## Features

### Core Features
- **Voice Recognition**: Uses Google Speech Recognition for accurate voice-to-text conversion
- **Text-to-Speech**: Natural voice responses using pyttsx3 (automatically speaks in Hindi when you converse in Hindi)
- **Music Playback**: Play songs on YouTube
- **Time & Date**: Get current time
- **Wikipedia Search**: Get information about people, places, and topics
- **Jokes**: Tell random jokes

### Advanced Features
- **Weather Information**: Get current weather for any city (requires API key)
- **Web Search**: Search Google for any query
- **Website Opening**: Open websites in your default browser
- **Application Launch**: Open common Windows applications (Notepad, Calculator, etc.)
- **Calculator**: Perform basic mathematical calculations
- **News Headlines**: Get top news headlines (requires API key)
- **Reminders**: Set timed reminders
- **Conversational**: Responds to greetings and basic conversation (English & Hindi)

## Installation

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up API Keys** (Optional but recommended for full functionality):
   - **OpenWeather API**: Get from https://openweathermap.org/api (free tier available)
   - **News API**: Get from https://newsapi.org/ (free tier available)

   Replace the placeholder values in `BhagwanJi.py`:
   ```python
   OPENWEATHER_API_KEY = "your_openweather_api_key_here"
   NEWS_API_KEY = "your_news_api_key_here"
   ```

## Usage

### Running the Assistant
```bash
python BhagwanJi.py
```

### Voice Commands

Bhagwan Ji understands English and Hindi. Speak naturally in either language—commands are translated on the fly.

#### Basic Commands
- **"Bhagwan Ji play [song name]"** - Play music on YouTube
- **"Bhagwan Ji time"** - Get current time
- **"Bhagwan Ji joke"** - Tell a random joke
- **"Bhagwan Ji who is [person/topic]"** - Get Wikipedia information
- **"Bhagwan Ji what is [topic]"** - Get Wikipedia information
- **"Bhagwan Ji tell me about [topic]"** - Get Wikipedia information

#### Advanced Commands
- **"Bhagwan Ji weather in [city]"** - Get weather information
- **"Bhagwan Ji search [query]"** - Search Google
- **"Bhagwan Ji open website [url]"** - Open a website
- **"Bhagwan Ji open [application]"** - Open applications (notepad, calculator, cmd, explorer)
- **"Bhagwan Ji calculate [expression]"** - Perform calculations
- **"Bhagwan Ji news"** - Get top news headlines
- **"Bhagwan Ji remind me to [message] in [time]"** - Set a reminder

#### Conversational Commands
- **"Bhagwan Ji hello/hi/hey"** (or the Hindi equivalents) - Greeting
- **"Bhagwan Ji how are you"** (or "Bhagwan Ji aap kaise ho") - Check status
- **"Bhagwan Ji thank you/thanks"** (or "Bhagwan Ji dhanyavaad") - Gratitude response
- **"Bhagwan Ji goodbye/bye/stop"** (or "Bhagwan Ji alvida") - Exit the assistant

## Requirements

- Python 3.7+
- Microphone for voice input
- Speakers/headphones for voice output
- Internet connection for web-based features

## Dependencies

- `speech_recognition` - Voice recognition
- `pywhatkit` - YouTube playback and WhatsApp integration
- `pyttsx3` - Text-to-speech
- `googletrans` - Translate and detect Hindi/English commands
- `wikipedia` - Wikipedia API
- `pyjokes` - Joke generation
- `requests` - HTTP requests for APIs
- `webbrowser` - Web browser control
- `subprocess` - System application launching

## Troubleshooting

### Common Issues

1. **"Could not understand audio"**
   - Check your microphone is working
   - Ensure you're in a quiet environment
   - Speak clearly and close to the microphone

2. **API-related errors**
   - Verify your API keys are correct
   - Check your internet connection
   - Ensure API services are available

3. **Application opening fails**
   - Some applications may not be installed on your system
   - Windows-specific commands may not work on other operating systems

4. **Speech recognition errors**
   - Ensure you have a stable internet connection
   - Google Speech Recognition requires internet access

## Customization

### Adding New Features
The assistant is modular and easy to extend. Add new command handlers in the `run_bhagwanji()` function following this pattern:

```python
elif "your_command" in command:
    # Your logic here
    talk("Your response")
```

### Voice Settings
You can customize the voice by modifying the pyttsx3 settings:

```python
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)  # Change index for different voices
```

## Limitations

- Requires internet connection for most features
- Speech recognition accuracy depends on audio quality
- Some features require API keys
- Windows-specific application commands
- Basic reminder system (no persistence across restarts)

## License

This project is open-source and available under the MIT License.

## Contributing

Feel free to contribute by:
- Adding new features
- Improving speech recognition
- Adding support for other platforms
- Fixing bugs and issues

---

**Enjoy your spiritual guide: Bhagwan Ji!** 🎤🕉️