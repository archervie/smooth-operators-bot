# Smooth Operators

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.14%2B-blue)](#)

A security-focused Discord application developed specifically for use in the Jojodoss Discord server.

[Join the Server](https://discord.gg/nGWnJsj58q)

---

## Overview

Smooth Operators, developed through `discord.py`, is a Discord application that is inspired by the stand Smooth Operators from the Jojo's Bizarre Adventure series. It is primarily made for server security and safety.

> **Note:** You are free to use this repository as a template for your own server, but keep in mind that several features are tailored specifically for the Jojodoss server and may require modification for your own server. Additionally, this bot is primarily built for *ONE* server, not for many at once. This affects the behavior of certain cogs, such as spam prevention and logging automation.

**Key Features**

- Account Age Gate: Automatically times out accounts less than four months old.
- Verification: Accompanied by the age gate, a timed out user can verify their account at any time.
- Automation: Automates logging, member joins/leaves, and moderation.
- Spam Prevention: Automated message checking that detects spam across many channels in close intervals.

---

## Prerequisites

If you wish to use this application as a template for your own server, you must have the following set up:

- Python 3.14+
- Git
- A Discord application set up through the [Discord developer portal](https://discord.com/developers/applications)

 :warning: This bot will need privileged gateway intents (Server Members & Message Content) enabled to function.

## Installation

You can set this bot up easily after following the prerequisites.

1. Clone this repo & change directories: `git clone https://github.com/archervie/smooth-operators-bot.git && cd smooth-operators-bot/`
2. Create a virtual environment: `python3 -m venv .venv/ && source .venv/bin/activate` OR `.venv\Scripts\activate` on Windows.
3. Install all libraries: `pip install .`
4. Edit config.toml to suit your server's needs. You can look at `src/example_config.toml` for guidance.
5. Create a .env file to store your bot token: `TOKEN=my.token.here`
6. Run src/main.py: `python3 src/main.py`
