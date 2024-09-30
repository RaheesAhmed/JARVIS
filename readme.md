# JARVIS - Your Personal AI Assistant

JARVIS (Just A Rather Very Intelligent System) is an advanced AI-powered personal assistant designed to help you with various tasks, from simple conversations to complex system operations.

## Features

- Natural language processing for casual conversations
- Voice input and output capabilities
- System operations (opening/closing applications, file management)
- Web browsing and internet searches
- Task execution using various tools
- Extensible architecture for adding custom functionalities

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.7+
- pip (Python package manager)


## Installation

1. Clone the repository:
   ```
   git clone https://github.com/RaheesAhmed/JARVIS.git
   ```

2. Navigate to the project directory:
   ```
   cd JARVIS
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the root directory and add the following:
   ```
   OPENAI_API_KEY=your_openai_api_key
   TAVILY_API_KEY=your_tavily_api_key
   ```

## Usage

To start JARVIS, run the following command:
```
python main.py
```


JARVIS will greet you and wait for your input. You can interact with JARVIS using voice commands or text input.

## Project Structure

- `main.py`: The entry point of the application
- `agents/`: Contains the AI agent implementations
- `tools/`: Includes various tools and utilities used by JARVIS
- `voice/`: Houses the speech-to-text and text-to-speech modules

## Key Components

1. **JarvisAPI**: The main interface for interacting with JARVIS
2. **BasicAgent**: Handles natural language processing and task execution
3. **SystemTools**: Provides system-level operations
4. **CustomTools**: Allows for the addition of custom functionalities
5. **STTEngine**: Converts speech to text for voice input
6. **TTSEngine**: Converts text to speech for voice output

## Extending JARVIS

You can extend JARVIS's capabilities by:

1. Adding new tools in the `tools/` directory
2. Implementing custom agents in the `agents/` directory
3. Enhancing the voice interaction capabilities in the `voice/` directory

## Contributing

Contributions to JARVIS are welcome! Please follow these steps:

1. Fork the repository
2. Create a new branch: `git checkout -b feature-branch-name`
3. Make your changes and commit them: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature-branch-name`
5. Create a pull request



## Acknowledgements

- OpenAI for the GPT model
- Tavily for internet search capabilities
- Edge-TTS for text-to-speech functionality
- Whisper for speech-to-text capabilities
- langchainfro Agnet

## Contact

If you have any questions or feedback, please open an issue on the GitHub repository.



