# TuxDroid
This repo contains TuxDroid Python API examples and scripts to install Tuxbox (app to work with the TuxDroid) on modern Linux (my system is Ubuntu 22.04).

## Usage
(1) Clone this repository:
```
git clone https://github.com/BowlOfSoup/tuxdroid.git
```

(2) Install dependencies needed, run `sudo bin/dependencies`.

(3) Run `sudo bin/install`. You can always uninstall all files by running: `sudo bin/uninstall`.

There should be an application installed in your app menu called "TuxBox 2.0", this is the webbased control panel for the droid.

You can use the following scripts:
* `/usr/bin/tuxbox`: this will start the Tuxbox HTTP server and will open a browser window to the webbased control panel.
* `/usr/bin/tuxhttpserver`: you can start the HTTP server manually with `tuxhttpserver --start`. (See also: `--restart` and `--stop`)
* `/usr/bin/tuxsh`: You can use Python to give commands to the droid (see examples)

There are some Python files in this repo (`main.py` etc.) that serve as entrypoint for my own droid 'scripts'. It's basic, but still fun to use as commit hook to entertain your colleagues.

**Example usage trough shell script: `./tux.sh alert`**

### What is not included, does not work?
* Text To Speech. Can't get it to work. Files are **not** included in this repo.
* Have Tux play .wav files. Can't get it to work.

### Uninstall dependencies
Tuxbox needs some special dependencies, also because it's a quite old. Hereby the commands to remove the deps For my installaton (Ubuntu 22.04):

```
sudo apt remove gcc-11-multilib gcc-multilib lib32asan6 lib32atomic1 lib32gcc-11-dev lib32gcc-s1 lib32gomp1 lib32itm1 lib32quadmath0 lib32stdc++6 lib32ubsan1 libc6-dev-i386 libc6-dev-x32 libc6-i386 libc6-x32 libx32asan6 libx32atomic1 libx32gcc-11-dev libx32gcc-s1 libx32gomp1 libx32itm1 libx32quadmath0 libx32stdc++6 libx32ubsan1 

sudo apt remove lib32z1 lib32z1-dev

sudo apt remove ca-certificates-java default-jre default-jre-headless fonts-dejavu-extra java-common libatk-wrapper-java libatk-wrapper-java-jni openjdk-11-jre openjdk-11-jre-headless
```

### Special thanks
Shoutout to http://tuxdroid.tounepi.com/. Thanks to the work this person did I was able to set up this repo and get my TuxDroid to work. Lots of other resources can be found on this website.