# Zebra Printer Daily

Do you miss getting a newspaper daily? I don't know why you would, but now instead you can print out your own tiny newspaper every day!

This project grabs a few things from public APIs and puts it on a cute little print.
Currently, it'll tell you the time, weather, and have a image of a cat, saying a hopefully helpful quote

You'll need a zebra printer with 4" x 6" labels or thermal paper for this to work out of the box. 
Zebra printers are very simple label printers, so it'll only cost you like $800 to buy one. 
[<img alt="example label" src="https://github.com/timeglitch/Zebra-Printer-Daily/blob/main/zebralable.webp?raw=true">]

AI Disclosure: Asked AI for help occasionally, but wrote all the code myself. 
You can tell b/c there are no useless tests, those are for cowards.

# Installation Guide

1. Clone the repo to your computer. The python part should work on Mac and Windows as well, but I've only set up the timer for Linux.
2. Set the env settings, then run `uv run zebra-printer-daily`. It should create a print.
3. If you're on Mac or Windows, you're done!!!
4. On linux, edit the paths for Execstart and WorkingDirectory in zebra_printer_daily.service so it points to where you downloaded the project.
5. Install them to systemd with these commands:
```
sudo cp zebra_printer_daily.service zebra_printer_daily.timer /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now zebra_printer_daily.timer
```
6. Test print a label and check with these commands:
```
sudo systemctl start zebra_printer_daily.service
journalctl -u zebra_printer_daily.service -n 30
systemctl list-timers zebra_printer_daily.timer
```

## TODO:

- make fonts better
- use an alternative image creation system, and get higher quality cat photos