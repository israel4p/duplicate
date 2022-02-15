#!/bin/bash

pyinstaller --onefile --noconsole --clean src/main.py

mv dist/main dist/duplicate
