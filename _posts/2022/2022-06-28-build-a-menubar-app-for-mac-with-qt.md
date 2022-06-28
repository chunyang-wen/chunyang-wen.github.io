---
layout: post
title: Build a menubar macos App using PyQt5 and PyInstaller
categories: [blog, python]
tags: [python, pyqt]
---

[PyQt](https://riverbankcomputing.com/software/pyqt/) is a python package that
can be used to develop GUI applications even complex applications.
In this blog, we will develop a menubar note application and package
it using `pyinstaller`.

+ toc
{:toc}

## Final application snapshot

![Penguin note](/images/python/penguin-note.png)

## PyQt code

```python
from PyQt5.QtWidgets import (
    QApplication,
    QSystemTrayIcon,
    QMainWindow,
    QTextEdit,
    QMenu,
    QAction,
)
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
import sys
import os

app = QApplication(sys.argv)

# Close window without exiting the application
app.setQuitOnLastWindowClosed(False)

# Create the icon
path = os.path.dirname(__file__)
icon = QIcon(os.path.join(path, "animal-penguin.png"))
# Create the tray
tray = QSystemTrayIcon()
tray.setIcon(icon)

tray.setVisible(True)

menu = QMenu()
quit = QAction("Quit")
quit.triggered.connect(app.quit)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        menu = self.menuBar()
        file_menu = menu.addMenu("&File")
        self.quit = QAction("&Quit")
        self.quit.triggered.connect(app.quit)
        file_menu.addAction(self.quit)
        self.editor = QTextEdit(self)
        self.load()  # Load up the text from file.

        self.setCentralWidget(self.editor)
        self.setWindowTitle("PenguinNotes")

    def load(self):
        if os.path.exists("notes.txt"):
            with open("notes.txt", "r") as f:
                text = f.read()
            self.editor.setPlainText(text)

    def save(self):
        text = self.editor.toPlainText()
        with open("notes.txt", "w") as f:
            f.write(text)

    def activate(self, reason):
        if reason == QSystemTrayIcon.Trigger:  # Icon clicked.
            self.show()

    def notes(self):
        self.show()
        self.setWindowState(QtCore.Qt.WindowState.WindowActive)
        self.raise_()

w = MainWindow()

notes_action = QAction("Notes")
menu.addAction(notes_action)
menu.addAction(quit)
notes_action.triggered.connect(w.notes)
tray.setContextMenu(menu)
# tray.activated.connect(w.activate)
app.aboutToQuit.connect(w.save)
app.setWindowIcon(QIcon("animal-penguin.png"))
app.exec()
```

+ Save the program as `penguin-note.py`
+ You can download any image and name it to `animal-penguin.png` in order to
show the icon.
+ `python penguin-note.py`

## Compile into a macos application

First, you have to install `pyinstaller`.

```bash
pip install pyinstaller --upgrade
```

```bash
pyinstaller --windowed penguin-note.py
```

By doing so, we will have two folders:

+ build
+ dist
+ penguin-note.spec:
  + Configuration file used to build our application

In the `dist` folder, there lies our app.

![penguin-note-app](/images/python/penggui-note-dist.png)

It has no icon on the menubar and a default icon in the dock.

### Menubar icon

We need to add the png file to the `penguin-note.spec`. Add to the `Analysis part`

```python
datas=[("animal-penguin.png", ".")]
```

And then run:

```bash
pyinstaller penguin-note.spec --noconfirm
```

Bingo, now we have our icon in the menubar.

+ `--noconfirm` is used to ignore the warning of overriding the files in dist

### Dock icon

Mac use icns file.

+ Use Preview to open the png
+ Duplicate
+ Save：press option, select the type icns

Sometimes you may fail to convert the png to icns, try to crop the image to
size 512 by 512.

In the `Bundle` part, instead of `icons=None`, set to the icns file generated
such as `penguin.icns`

```python
app = BUNDLE(
    coll,
    name='penguin-note.app',
    icon="penguin.icns",
    bundle_identifier=None,
)
```

### Hide the dock icon

In order to make it a pure menubar application, we need to hide the icon in dock.
That can be achieved by modifying the `Info.plist`.

```python
app = BUNDLE(
    coll,
    name='penguin-note.app',
    icon="penguin.icns",
    bundle_identifier=None,
    info_plist={
        'LSUIElement': True,
        'LSBackgroundOnly': True,
        'NSUIElement': True
    },
)
```

## Where to go from here

You can use [`create-dmg`](https://github.com/sindresorhus/create-dmg) to
create a installed instead of an application which users can
use it to install applications.

## Reference

+ [Create GUI Applications with Python & Qt5](https://www.pythonguis.com/pyqt5-book/)
+ [Packaging Python Applications](https://www.pythonguis.com/packaging-book/)
