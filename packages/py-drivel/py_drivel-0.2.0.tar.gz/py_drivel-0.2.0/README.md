[![Build Status](https://github.com/dusktreader/drivel/actions/workflows/push.yaml/badge.svg)](https://github.com/dusktreader/drivel/actions/workflows/push.yaml)
[![PyPI Versions](https://img.shields.io/pypi/v/py-drivel?style=plastic&label=pypi-version)](https://img.shields.io/pypi/v/py-drivel?style=plastic&label=pypi-version)

> [!IMPORTANT]
> I'm looking for a job right now! If you know of any openings that match my skill-set,
> please let me know! You can read my resume over at my
> [cv site](https://cv.dusktreader.dev). Thanks!!

# Drivel

[//]: # (Add an asciicast)

`drivel` is a package and CLI application to provide you with
[metasyntactic](https://en.wikipedia.org/wiki/Metasyntactic_variable) name values.

It is heavily inspired by the [metasyntactic](https://github.com/ask/metasyntactic) package. However, `metasyntactic`
is quite old and it is unmaintained.

Drivel is a modern package that borrows many of the themes from `metasyntactic`, used others for inspiratoin, and adds a
few new ones.


## Quickstart

### Install `drivel`:

```bash
pip install py-drivel
```

### CLI

#### [Optional] Configure `drivel`:

Drivel may be configured to retain settings between commands. To learn more about this, see the
[Configuration](#configuration) section below.


#### Run `drivel`:

To get 10 metasyntactic names from the default theme, run:

```bash
drivel give 10
```


### Package

Just import in your code, and go!

```python
from drivel.themes import Theme

print(Theme.load().give())
```


## Using drivel

You can see all the commands available in drivel by running the main command without an subcommand or by passing the
`--help` flag:

```
drivel
```

```
 Usage: drivel [OPTIONS] COMMAND [ARGS]...

 Welcome to drivel!
 More information can be shown for each command listed below by running it with the
 --help option.

╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --verbose               --no-verbose      Enable verbose logging to the terminal [default: no-verbose]     │
│ --version               --no-version      Print the version of this app and exit [default: no-version]     │
│ --install-completion                      Install completion for the current shell.                        │
│ --show-completion                         Show completion for the current shell, to copy it or customize   │
│                                           the installation.                                                │
│ --help                                    Show this message and exit.                                      │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ─────────────────────────────────────────────────────────────────────────────────────────────────╮
│ config   Configure the app, change settings, or view how it's currently configured                         │
│ give     Give N fun metasyntactic variable names.                                                          │
│ themes   Commands to interact with themes.                                                                 │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

╭────────────────────────────────────────── Need an drivel command ──────────────────────────────────────────╮
│                                                                                                            │
│   No command provided. Please check usage                                                                  │
│                                                                                                            │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```


### Getting metasyntactic names

This is the main `drivel` sub-command. It will produce metasyntactic names for you to use from the selected theme.

To see all the options available, run this subcommand with the `--help` flag:

```
drivel give --help
```

```
Usage: drivel give [OPTIONS] [MAX_COUNT] COMMAND [ARGS]...

 Give N fun metasyntactic variable names.

╭─ Arguments ────────────────────────────────────────────────────────────────────────────────────────────────╮
│   max_count      [MAX_COUNT]  The maximum number of metasyntactic names to give [default: None]            │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --shuffle                                                   Mix the names                                  │
│ --theme                                TEXT                 The theme to use (If not provided, will use    │
│                                                             current default                                │
│                                                             [default: None]                                │
│ --kind                                 TEXT                 The kind of names to give. Use 'all' to pull   │
│                                                             from all kinds                                 │
│                                                             [default: default]                             │
│ --format                               [json|spaces|lines]  The output format to use [default: spaces]     │
│ --fancy           --no-fancy                                Enable fancy output [default: fancy]           │
│ --to-clipboard    --no-to-clipboard                         Copy output to clipboard                       │
│                                                             [default: to-clipboard]                        │
│ --help                                                      Show this message and exit.                    │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

The arguments/options will be explained below:


#### max_count

This will limit the number of items that `drivel` produces for you. If there are not as many names available as the max
that you specify, drivel will give you all that it has.

```
drivel give 3
```

```
╭────────────────────────────────────────── Fun names from foobar ───────────────────────────────────────────╮
│                                                                                                            │
│   foo bar baz                                                                                              │
│                                                                                                            │
╰─────────────────────────────────────────── Copied to clipboard! ───────────────────────────────────────────╯
```


#### --shuffle

By default, `drivel` will give you the names in the order that they are specified in the data files. If you would like a
random ordering, use this flag:

```
drivel give --shuffle 6
```

```
╭────────────────────────────────────────── Fun names from foobar ───────────────────────────────────────────╮
│                                                                                                            │
│   garply corge grault plugh fred xyzzy                                                                     │
│                                                                                                            │
╰─────────────────────────────────────────── Copied to clipboard! ───────────────────────────────────────────╯
```


#### --theme

This allows you to select the theme that you would like to pull names from:

```
drivel give --theme=star-wars 5
```

```
╭───────────────────────────────────────── Fun names from star-wars ─────────────────────────────────────────╮
│                                                                                                            │
│   jawa ewok hutt pyke bith                                                                                 │
│                                                                                                            │
╰─────────────────────────────────────────── Copied to clipboard! ───────────────────────────────────────────╯
```


#### --kind

Many of the themes have more than one "kind". That is, there are different groups that you can pull from. For example,
the "star-wars" theme has "short" names and "longer" names. By default, it's configured to use the "short" names, but
you can access other options with this flag:

```
drivel give --theme=star-wars --kind=longer 5
```

```
╭───────────────────────────────────────── Fun names from star-wars ─────────────────────────────────────────╮
│                                                                                                            │
│   aqualish besalisk bothan chiss devaronian                                                                │
│                                                                                                            │
╰─────────────────────────────────────────── Copied to clipboard! ───────────────────────────────────────────╯
```

Finally, you can provide the "all" kind to fetch all the names from every group:

```
drivel give --theme=star-wars --kind=all 20
```

```
╭───────────────────────────────────────── Fun names from star-wars ─────────────────────────────────────────╮
│                                                                                                            │
│   jawa ewok hutt pyke bith gran talz muun teek vurk aqualish besalisk bothan chiss devaronian dug duros    │
│ gamorrean geonosian gungan                                                                                 │
│                                                                                                            │
╰─────────────────────────────────────────── Copied to clipboard! ───────────────────────────────────────────╯
```

Notice that only the first 10 come from the "short" group. The rest of the 20 are filled in from the "longer" group


#### --format

This allows you to specify how you would like the results to be printed out. There are 3 options here:

- spaces: print them on a single line with spaces in between
- lines:  print each entry on its own line
- json:   print the output as a JSON-serialized string


```
drivel give --format=json
```

```
[
  "foo",
  "bar",
  "baz",
  "qux",
  "quux",
  "corge",
  "grault",
  "garply",
  "waldo",
  "fred",
  "plugh",
  "xyzzy",
  "thud"
]
```


#### --fancy

This flag controls whether "fancy" formatting is used. By default, `drivel` wraps output in `rich` panels. However, if
you want to get the raw output without decoration, you can use the `--no-fancy` flag to turn it off:

```
drivel give --no-fancy 5
```

```
foo bar baz qux quux
```

Note that for JSON format, the output will not contain any newlines (so it's ready to pipe to another command).


#### --to-clipboard

By default, `drivel` will copy the output from the commands to you clipboard (if it can). If you would like to disable
this behavior, just use the `--no-to-clipboard` flag.


### Managing Themes

The next sub-command of `drivel` allows you to interact with the available themes:

```
drivel themes
```

```
 Usage: drivel themes [OPTIONS] COMMAND [ARGS]...

 Commands to interact with themes.
 More information can be shown for each sub-command listed below by running it with the
 --help option.

╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ─────────────────────────────────────────────────────────────────────────────────────────────────╮
│ list     List all available themes.                                                                        │
│ add      Fetch all available themes.                                                                       │
│ remove   Fetch all available themes.                                                                       │
│ show     Show a theme.                                                                                     │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

╭──────────────────────────────────── Need an drivel->themes sub-command ────────────────────────────────────╮
│                                                                                                            │
│   No sub-command provided. Please check usage                                                              │
│                                                                                                            │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

There are a few useful subcommands available.


#### list

This command simply lists all the themes that are currently available. This includes all of the builtin themes as well
as any that you may have added.

```
drivel themes list
```

```
╭────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│                                                                                                            │
│   crypto star-wars stars ubuntu octothorpe smurfs zodiac swords jabberwocky drivel foobar constellations   │
│ care-bears alice batman tarot debian python bible                                                          │
│                                                                                                            │
╰─────────────────────────────────────────── Copied to clipboard! ───────────────────────────────────────────╯
```


#### add

If you would like to add your own theme to drivel, you can! You must first produce a YAML file that conforms to the
schema that `drivel` uses for its data files (see the `schema` subcommand below). Then, you import the theme into
`drivel`.

Here is an example theme that you can load:

```yaml
metadata:
  explanation: |
    Just a list of colors.

default: basic

kinds:
  basic:
  - red
  - orange
  - yellow
  - green
  - blue
  - indigo
  - violet
```

If this file was stored at `~/colors.yaml`, you could add it to `drivel` as a new theme with this command:

```
drivel themes add ~/colors.yaml
```

Now it's ready to use!

```
drivel give --theme=colors
```

```
╭─────────────────────────────────────────────────────────────── Fun names from colors ────────────────────────────────────────────────────────────────╮
│                                                                                                                                                      │
│   red orange yellow green blue indigo violet                                                                                                         │
│                                                                                                                                                      │
╰──────────────────────────────────────────────────────────────── Copied to clipboard! ────────────────────────────────────────────────────────────────╯
```

Note that if you try to replace a built-in theme, it will not work. Instead, `drivel` will not load the theme.


#### show

This command will show the theme's data. You may choose whether to show the theme in YAML (the default) or JSON. There
are also flags to control fancy display and whether or not the data is copied to the clipboard:

```
drivel themes show colors
```

```
default: basic
kinds:
  basic:
  - red
  - orange
  - yellow
  - green
  - indigo
  - violet
metadata:
  attribution: null
  explanation: 'Just a list of colors.
    '
```


#### remove

If you want to remove a theme that you have added before, just run the `remove` subcommand

```
drivel themes remove colors
```


#### schema

The final sub-command will show the schema required for new themes in the JSONSchema format:

```
drivel themes schema
```

```
{
  "$defs": {
    "ThemeMetadata": {
      "properties": {
        "attribution": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Attribution"
        },
        "explanation": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Explanation"
        }
      },
      "title": "ThemeMetadata",
      "type": "object"
    }
  },
  "properties": {
    "name": {
      "title": "Name",
      "type": "string"
    },
    "default": {
      "type": "string",
      "title": "Default"
    },
    "kinds": {
      "additionalProperties": {
        "items": {
          "type": "string"
        },
        "type": "array"
      },
      "title": "Kinds",
      "type": "object"
    },
    "metadata": {
      "$ref": "#/$defs/ThemeMetadata"
    }
  },
  "required": [
    "name",
    "default",
    "kinds",
    "metadata"
  ],
  "title": "Theme",
  "type": "object"
}
```

This may be useful to understand how to construct a new theme.


### Configuration

The `drivel` CLI stores its configuration in a file so that it can use the same settings for many runs without having a
super-cluttered command line. There are several commands that allow you to interact with the config. You can see the
options by running:

```bash
drivel config --help
```

```
 Usage: drivel config [OPTIONS] COMMAND [ARGS]...

 Configure the app, change settings, or view how it's currently configured

╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ─────────────────────────────────────────────────────────────────────────────────────────────────╮
│ bind     Bind the configuration to the app.                                                                │
│ update   Update one or more configuration settings that are bound to the app.                              │
│ unset    Remove a configuration setting that was previously bound to the app.                              │
│ show     Show the config that is currently bound to the app.                                               │
│ path     Show the path to the config file that is currently bound to the app.                              │
│ clear    Clear the config from the app.                                                                    │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

#### show

This is the most basic config command. It will show you the current config. If you have not bound a config yet, it will
show the defaults:

```
drivel config bind show
```

```
╭────────────────────────────────────────── Current Configuration ───────────────────────────────────────────╮
│                                                                                                            │
│   default-theme -> foobar                                                                                  │
│                                                                                                            │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

`foobar` is the theme that will be used as the default unless you configure `drivel` differently.


#### bind

This command will set all the configuration options that are available in your saved config. It will show you the new
config settings after it runs.

```bash
drivel config bind --default-theme=star-wars
```

```
╭────────────────────────────────────────── Current Configuration ───────────────────────────────────────────╮
│                                                                                                            │
│   default-theme -> star-wars                                                                               │
│                                                                                                            │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```


#### update

This command will update only the configuration settings that you select. At the moment `drivel` doesn't have any
required configuration options, so this is functionally the same as `bind`.

```bash
drivel config update --default-theme=care-bears
```

```
╭────────────────────────────────────────── Current Configuration ───────────────────────────────────────────╮
│                                                                                                            │
│   default-theme -> care-bears                                                                              │
│                                                                                                            │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

#### unset

This command allows you to unset one or more configuration settings so that they return to the built-in defaults:

```bash
drivel config unset --default-theme
```

```
╭────────────────────────────────────────── Current Configuration ───────────────────────────────────────────╮
│                                                                                                            │
│   default-theme -> foobar                                                                                  │
│                                                                                                            │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

Notice that the options that you pass into `unset` are _flags_. They do not take a value.


#### clear

This command will clear all settings and return them to the built-in defaults:


```bash
drivel config clear
```

```
Are you sure you want to clear the settings? [y/N]: y

╭───────────────────────────────────────────── Settings Cleared ─────────────────────────────────────────────╮
│                                                                                                            │
│   All settings have been cleared and returned to built-in defaults                                         │
│                                                                                                            │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```


#### path

This command will show you the path to the config file that stores your settings:

```
drivel config path
```
```
╭──────────────────────────────────────── Current Configuration Path ────────────────────────────────────────╮
│                                                                                                            │
│   /home/username/.local/share/drivel/settings.json                                                         │
│                                                                                                            │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```


## License

Distributed under the MIT License. See `LICENSE.md` for more information.
