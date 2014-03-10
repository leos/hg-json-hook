# Mercurial JSON validation hook

A simple pure python Mercurial [precommit](http://www.selenic.com/mercurial/hgrc.5.html#hooks) hook script to fix trailing commas in JSON files and to make sure that `json` can load up the file. It's not a JSON Lint run but generally good enough to find issues.

There's lots of other options out there, for example: [JSHint](http://www.jshint.com/) but this hook doesn't require Node or anything outside of Python.

### Installation
Clone this repo: `git clone git://github.com/leos/hg-json-hook.git`

Add the hook to your hgrc:
```
[hooks]
precommit = python:/home/leo/hg-json-hook/hgjsonhook.py:run
```
Replace `/home/leo/` with wherever you cloned it to.

The hook hasn't been tested as anything other than a `precommit`. Pull requests welcome if it works as a different type of hook.

### Usage
The hook will automatically run on commit. If there are any trailing commas detected in json files that are part of the commit, you'll be prompted to fix them. Hit `y` to correct them or `n` to ignore.

If the `json.loads` fails, you'll be given the message from that. Newer `simplejson` versions tend to be more descriptive.

### Requirements
* Python 2.4+
* Will use `simplejson` if it's installed (required on Python 2.4, 2.5)
* ANSI compatible terminal for color (Windows users need ansi.sys or equivalent - try [ansicon](https://github.com/adoxa/ansicon))
