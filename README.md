# YouTube for Original Xbox
You can now again watch YouTube on Original Xbox!

## Table of Contents
- [Info](#info)
- [Requirements](#requirements)
- [Setup Guide](#setup-guide)
- [Running](#running)
- [Functionalities](#functionalities)
  * [Xbox functionalities](#xbox)
  * [PC funcionalities](#pc)
- [Video](#video)
- [Some images](#some-images)

## Info
This is plugin for XBMC4Xbox that aims to resurrect streaming of videos from YouTube on this dated hardware. Plugin is coded in Python and it's using Invidious for fetching data. PC application is simple backend coded in Node.js that acts like a gateway between Xbox and Invidious. Currently, this can't work without PC gateway because every public Invidious instance require TLS1.2 or higher which OpenSSL 0.9.8 doesn't support. Hovever, if someone can host Invidious instance with TLS1.0 or even unencrypted HTTP support, there is only one line in plugin that needs to be changed that will completely remove dependence for PC backend. Maybe, some day when I get free time, I'll try host my own Invidious instance.

## Requirements
- **Xbox**
    + You need softmodded or hardmodded Xbox
    + You need latest release of [XBMC4Xbox](https://www.dropbox.com/sh/8mcip8xsfe1zjap/AABSR3_toPPiFn-7OqwQY_JIa)
- **PC**
    + [Node.js](https://nodejs.org/en/download/)
    + PC with Windows, Linux or macOS

## Setup Guide
### Xbox
 - From this repo, Xbox/**plugins** to the root of XBMC4Xbox folder. In most cases it's: **E:\Apps\XBMC\**
### PC
 - Install Node.js

## Running
### Xbox
 - Open plugin from XBMC4Xbox located in Videos -> Plugins
### PC
 - Open PC/xbox-backend in terminal/console and type:
      ```bash
      npm install
      npm start
      ```
 - Open frontend on http://YOUR_IP_ADDRESS:9005 in your browser

## Support
<a href="https://www.buymeacoffee.com/antonic901" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: 41px !important;width: 174px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" ></a>

## Video
TODO
## Some images
TODO
