# Anki Handsfree

Export audio from Anki cards into audio files and play them everywhere!

## Intro

I wrote Handsfree because I wanted to review my cards even at times when I can't interact with Anki. That could be when doing house chores, walking or cycling (only off-road!). With this addon, you can easily export cards in Anki into audio files and play them in any media player.

**For vocabulary acquisition, pairing with the [AwesomeTTS](https://ankiweb.net/shared/info/301952613) addon is recommended.**

## Features

- Export to most audio formats
- Customizable delay between answer and question
- A audible countdown before answer and repeating question and answer after answer (useful for learning vocabulary)

## Installation

### Manual Installation

Right now, Handsfree isn't as polished as some other Anki addons and requires some extra work. It shouldn't be too hard, though, and if you struggle with the process, feel free to ask in [Issues](https://github.com/angel333/handsfree/issues) or me directly.

1. **Open your Anki addons folder**<br>
    Open Anki and in the top menu choose *Tools* &raquo; *Add-ons* &raquo; *Open Add-ons Folder...*.
2. **Extract the addon**<br>
    Copy all files from `src` into your addons folder &ndash; i.e. the `handsfree.py` file and the `handsfree` folder.
3. **Install ffmpeg**<br>
    - Windows and OS X: You can download ffmpeg [here](https://ffmpeg.zeranoe.com/builds/) &ndash; choose any version, your platform, and "static linking". Open the archive and in the `bin` folder, find a file called `ffmpeg` (for OS X) or `ffmpeg.exe` (for Windows). Extract this file into the `handsfree` folder in your Anki addons folder. This file is all you need, you don't need anything else from the archive.
    - Linux: The easiest option is to install ffmpeg with your package manager. Open a terminal window and try to execute `sudo yum install ffmpeg`, `sudo aptitude install ffmpeg` or `sudo pacman install ffmpeg`. Chances are one of them will work. If not, just google how to install ffmpeg.

## How to use

Right now. most of the configuration is done in a JSON file `<Anki addons folder>/handsfree/config.json`. It looks like this:

```json
{
    "qa_delay": 5000,
    "aq_delay": 2000,
    "countdown": true,
    "repeat": true,
    "query": "deck:current",
    "output_directory": "~\\Dropbox",
    "output_format": "opus",
    "output_bitrate": "32k",
    "output_filename": "cards.opus",
    "output_individual": false,
    "output_individual_filename_pattern": "card_{:03d}.opus",
    "audio_tags": {
        "title": "Anki Handsfree Export",
        "album": "Anki Handsfree",
        "artist": "Anki Handsfree"
    }
}
```

- `qa_delay` and `aq_delay` are delays (in ms) between question and answer, and answer and question respectively.
- If `countdown` is true, a beeping countdown will be played before the answer.
- if `repeat` is true, question and answer will be repeated once again after answer, this time with only very short (500ms) delays.
- `query` determines which cards will be included. You can test this in the browser.
- `output_...` options determine where to save the audio file, how to name it, what format to use (e.g. `opus`, `mp3` or `adts` for aac), as well as the bitrate.
- If `output_individual` is true, a file will be created for each card. `output_individual_filename_pattern` should then contain a pattern for the Python `format()` function. E.g. if you set `card-{:003}.opus`, the files will be named `card_000.opus`, `card_001.opus`, `card_002.opus`, etc.
- Values from `audio_tags` will be shown in your player.

When the configuration is ready, open Anki and in the main window, choose *Tools* &raquo; *Handsfree export* and follow the prompts.

## Bugs and questions

Please don't hesitate to post bug reports or ask any questions. 

## Tips and tricks

- Save audio files in a cloud storage (e.g. Dropbox) and sync them to your phone automatically via an app, e.g. [FolderSync](https://play.google.com/store/apps/details?id=dk.tacit.android.foldersync.lite&hl=cs).
- If you don't want to clutter your cards with the extra `[sound:...]` tags (that are needed for Handsfree), just create new cards with those tags, and then use the Anki's [Deck Override](https://apps.ankiweb.net/docs/manual.html#deckoverride) feature to automatically put these cards in a different deck (to ignore them easier).

## Caveats

**My cards are omitted**

In order to process the cards, they need to contain the `[sound:...]` tag in both the question and the answer.

## License

[MIT](LICENSE)