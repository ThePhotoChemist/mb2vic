# mb2vic

This python script will pull out all the note data from a MusicBoxComposer (.mbc) file, and spit out a BASIC program, ready to be played on a VIC-20.  The programs tend to be fairly large, so you will likely need a memory expansion of at least 8k for songs with any appreciable amount of notes.  "Out of the box" this script only supports 33-note mbc files, currnetly.  

To Use:  in a command line prompt, run:
  python mb2vic.py "path/to/your/file.mbc"

This will spit out the BAISC program into a file called "program_out.txt", the contents of which can be pasted into VICE or another program to be converted to a runnable .prg file.  
