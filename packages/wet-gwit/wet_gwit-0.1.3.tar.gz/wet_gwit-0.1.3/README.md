# Wet

Wet is Gwit's Wget.

Wet is a bare-bones POC client implementation for [Gwit protocol](https://gwit.site/).
It serves as a development target for libGwit.

Wet assumes that you are on a UNIX system. To my knowledge it has only been tested on a Linux Mint.

## Installation

We recomment installing wet through Pypi : `python3 -m pip install wet-gwit`

Otherwise, just `git clone --recursive https://framagit.org/matograine/wet.git`.
Don't forget the `--recursive` flag since it will also clone the `libgwit` repo.

### Dependencies

You should have installed on your system :
- Git
- python-gnupg `pip install python-gnupg`
- GitPython `pip install GitPython`

You can install them by running `python3 -m pip install -r requirements.txt`

If you want to run tests, you need to have `pytest` available.

You can install it by running `python3 -m pip install -r requirements_dev.txt`

## Interface

You can use `./wet.py -h` to see available options.

A quick tutorial is available in [USAGE.md](USAGE.md).

Available and planned features are described in [FEATURES.md](FEATURES.md).

### Limitations

Petnames will be stored in plain text format, allowing for manual update.
Updating and exporting petnames informations from CLI is not a goal for now.

wet only displays the content retrieved. No formatting nor interactivity is intended.

If the gwitsite contains blobs, such as images, wet does not know how to handle it.

## Data storage

All content will be stored in a unique dir. This dir can be provided by option --data-dir, but will default to `$XDG_DATA_PATH/gwit` or `~/.local/share/gwit` if no `$XDG_DATA_PATH`.

This is the file hierarchy:
```
- data_dir
  - repos
    - 0x16c8a566bb88303c2513cf6328996d46e0440e85 -> dir containing the relevant repo
    - ...
  - petnames.yaml -> file containing all sites configs (both self and introductions)
  - 123456_context.txt -> file containing the last URL visited for each terminal session. It is used to manage relative URLS (relative paths or `self` ULRs). Cleaned if not updated since one day.
```

The petnames.yaml file contains two parts, 'locals' and 'introductions':
```yaml
locals:
  '0x16c8a566bb88303c2513cf6328996d46e0440e85':
    # informations for this locally-stored site
    #...
  '0x408198c2c363076c6b1eabe797ea3168a78cd65a':
    #...
introductions:
  '0x16c8a566bb88303c2513cf6328996d46e0440e85': {} # This gwit site does no contain any introductions
  '0x408198c2c363076c6b1eabe797ea3168a78cd65a':
    '0x16c8a566bb88303c2513cf6328996d46e0440e85':
      # informations for this introduced site site
      #...
    '0x24860d48d3abbb5ceffbc5126483fd2f7b9eaddf':
      # ...
    '0xb1f5a34aac62bfda746a3188aab4500edeaf682a':
      # ...
```

## Testing

Prepare the tests by launching `./prepare-tests.sh`. This will create a dir `testing_remote` that contains sites used in tests. If tests fail because they can't reach a dir, you may want to run it again to refresh local sites.

Then, simply run `pytest`.

NB - some tests will fetch informations remotely, tests will fail if your computer is offline.

## Attacks and mitigation

Since files will be downloaded locally and petnames will be processed locally, I see these attacks (protections not implemented yet, see [FEATURES.md](./FEATURES.md)):

### Heavy repos

An attacker may create a very heavy repo to fill the user's drive.
To avoid this, a timeout should be available (first hardcoded, then maybe configured) to avoid cloning too heavy repos

### Too many petnames

An attacker may create a large number of petnames to make the processing long.
To avoid this, a limit on the number of petnames provided by a site should be set (first hardcoded, then maybe configured).
Say 500 petnames.
The site will be cloned, but petnames above the 500 first will be discarded.

### Executable files

Git allows an attacker to define rights on the files. We certainly don't want executable files to be fetched on the local system.
`wet` will set the rights to 440, which means "redable by the current user and its group"
