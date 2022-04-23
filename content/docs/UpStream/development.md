# Developers guide for UpStream

## Scripts

UpStream provides some scripts. They´re written for Windows (.bat), but the commands should be the same for Linux/MacOS.

- updateCss.bat

updates the Tailwind CSS and DaisyUI code from main.css  
Note: Make sure you have both NPM packages installed or run `yarn install`.

- installAndRun.bat

pip-installs UpStream and runs it in the current direcory  
Note: Linux/MacOS users may have to use `python3` instead of only `python`.

## Editor setup

Tailwind CSS has a VSCode IntelliSense plugin. For the best experience, you should have it enabled.  
To install the plugin, go to your command palette (Ctrl + P on Windows and Linux, Cmd + P on MacOS) and type `ext install bradlc.vscode-tailwindcss`.