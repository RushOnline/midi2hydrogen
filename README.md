# midi2hydrogen: ready to rock ?

[Posted on 21 July 2008 by Dainaccio](http://dainaccio.wordpress.com/2008/07/21/midi2hydrogen-ready-to-rock/)

Midi files are good and small but I don’t like their sound…
Hydrogen is powerful and perfect to use as drum machine while playing guitar but I’m too lazy to write down the rhythm of the famous songs that I want to play…

The solution ? midi2hydrogen


It’s a small python script that creates a Hydrogen file from the drum channel of a MIDI file.
It’s designed to work “out of the box” with Hydrogen YamahaVintageKit (I like its sound). You can find it in the Hydrogen website (for free).

Other drumkits are not supported (yet). That means that you’ll find all the patterns messed up (ex. the rhythm of the crash in the row of the snare… and so on).


## How to use

First of all, you have to install python. Then you can open a terminal and start to use the script.

The syntax to use is:

python midi2hydrogen.py input.mid output.h2song

That’s all.

### Bugs

The Tempo will certain be wrong and notes can be not aligned with Hydrogen’s grid.
It’s very far from layout perfection…

### Future plans

I’m preparing a GUI, for the configuration and the file selections.

### Thank to

The creator of Python Midi Package

This script is not recomended by any famous rock star. :-P
