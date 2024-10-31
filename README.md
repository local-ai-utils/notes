# Local AI Utils - Notes
A plugin for [local-ai-utils](https://github.com/local-ai-utils/core) to interact with a small SQLite notes database. In all reality this doesn't utilize any AI utilities, but it is a simple example tool chain that is greatly enhanced by other AI utilities.

## Example Use Case
This plugin was made with an imagination of a local utility that can quickly take notes via a voice interface. You can use a few Local AI Utils Plugins to achieve this.

- [**listen**](https://github.com/local-ai-utils/listen) to quickly capture audio from the microphone, and transcibe it
- [**assist**](https://github.com/local-ai-utils/assist) to call out to an LLM recognize when the user is making a note, categorize it, and then make a tool call to...
- **notes** exposes the assist tool for creation, so there is no extra configuration needed.

A simple bash script could tie all of these tools together into a seamless experience, or use an automation tool like [Hammerspoon](https://www.hammerspoon.org/) to bind a hotkey for even quicker note taking!

## Installation
Currently installation is only supported via the GitHub remote.
```
pip install git+https://github.com/local-ai-utils/notes
```

## Configuration
All you need to do is load the plugin, so that other LAUI Plugins can utilize it.

`~/.config/ai-utils.yaml`
```
plugins:
    notes:
```

### Usage
## Assist Tool
A note creation function is configured, if you have the [local-ai-utils-assist](https://github.com/local-ai-utils/assist) plugin installed. You can see the definition for the function in `/src/notes/plugin.py`. Note creation is currently the only tool exposed for Assist, there is no listing or editing or injecting notes into context for the LLM.

## CLI Usage
You can also interact with notes directly from the CLI.

```
$ notes "I need to call Joe" # create a new note
Note added successfully with ID: 1

$ notes "Research Anthropic tool support" -c research -c AI # create notes with categories
Note added successfully with ID: 2

$ notes # List all of your notes
1 10/24/24 I need to call Joe
2 10/27/24 Research Anthropic tool support
3 10/27/24 I took my medicine at 12:30 today
4 10/27/24 Jen has a big presentation next Thursday


# Notes are automatically added to 
$ notes -n 2 # Lists all the notes in a category

2 -- 10/27/24

Research Anthropic tool support
Categories: research, AI
```

A window will pop up indicating that recording has started. Press the `Enter` key to stop recording and receive the transcription.