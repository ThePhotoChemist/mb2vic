# mb2vic

This python script will pull out all the note data from a MusicBoxComposer (.mbc) file, and spit out a BASIC program, ready to be played on a VIC-20.  The programs tend to be fairly large, so you will likely need a memory expansion of at least 8k for songs with any appreciable amount of notes.  "Out of the box" this script only supports 33-note mbc files, currently.  

To Use:  in a command line prompt, run:
  python mb2vic.py "path/to/your/file.mbc"

This will spit out the BAISC program into a file called "program_out.txt", the contents of which can be pasted into VICE or another program to be converted to a runnable .prg file.  


Some tips:

Avoid having more than 3 notes at a time in MusicBoxComposer, since the VIC-20 only has 3 square wave voices, and probably a bunch of weird stuff will happen as the script tries to assign notes to each channel. 

If the song plays too fast or too slow, try modifying line 32, which determines playback speed, which defaults at 350.  Increasing the number will result in a slower song, and smaller numbers will cause it to play faster. 
