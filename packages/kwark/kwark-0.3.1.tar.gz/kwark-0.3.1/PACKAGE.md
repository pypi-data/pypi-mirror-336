<!-- PACKAGE file - intended to be shown when a user browses the package in a registry, incuding PyPI. Content is focused on what a _consumer_ of the application might want to know. -->

# Kwark

## Tap into AI brilliance from a simple shell command

The tool currently has one command, `doc`, which summarize the conculsions from a discussion or thread for inclusion in technical documentation. It uses the Anthropic API and requires an API key.

## Usage (MacOS)

The `doc` command processes text from standard input and returns the summary to standard output.

```bash
pbpaste | kwark doc | pbcopy
```

(Note `pbcopy` and `pbpaste` are MacOS-specific commands.)

## Quick installation (MacOS)

```bash
brew install python@3.11
python3.11 -m pip install pipx
pipx install kwark
```

## Authentication and configuration

Kwark uses Claude 3.5 Sonnet through the Antropic API, and requires an API key.

There are three options for providing the API key to Kwark:

1. Set the default `ANTHROPIC_API_KEY` environment variable before running the `kwark` command
2. Provide the API key as a `--api-key` option to the `kwark doc` command
3. Provide the API key in a configuration file using the [WizLib ConfigHandler](https://wizlib.steamwiz.io/api/config-handler) protocol

We recommend storing the key in a password manager such as 1Password, then using a config file to retrieve the key at runtime instead of storing the key itself in a file. For example, create a file at `~/.kwark.yml` with the following contents:

```yaml
kwark:
  api:
    anthropic:
      key: $(op read "op://Private/Anthropic/api-key")
```

<br/>

<a href="https://www.flaticon.com/free-icons/particles" title="particles icons">Particles icon by Freepik-Flaticon</a>
