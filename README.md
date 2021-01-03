# Kerbal Space Program Autopilot

## Setting up the environment
- Install kRPC: https://krpc.github.io/krpc/getting-started.html
  - Download the package
  - Unzip the files
  - Move the files into the GameData folder in your local KSP installation.
- Clone this repo
- Set up a Python virtual environment
  - Must be Python 3.x
  - Install krpc with pip
- Copy the .craft files from this repo to the VAB folder in your local KSP installation.

## Running the autopilot
- Start KSP and load a game
- Load one of the spacecraft from this repo
- Start the kRPC server
- From a terminal, run the .py file that corresponds to the spacecraft you loaded.