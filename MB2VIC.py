#!/usr/bin/env python

import sys

notelength=1
scantimemodifier=50

scaletype=33
ASMMode=1 		#0=using defualt VIC registers 1=using 10-OFR ASM code for pitches

content = []


with open(sys.argv[1], 'r') as my_file:
	count = len(my_file.readlines(  ))
	
with open(sys.argv[1], 'r') as f:
	lines = f.read().splitlines()
	
verbose=0
printdata=0
superverbose=1


if superverbose==1:
	verbose=1
	printdata=1

PlaybackSpeedStrRaw=lines[1]
PlaybackSpeedStr=PlaybackSpeedStrRaw.replace("PlaybackSpeed=","")
PlaybackSpeed=float(PlaybackSpeedStr)

timemultiplier=350/PlaybackSpeed

countadj=count-12
totalnotes=countadj/6
totalnotesadj=totalnotes-1


if verbose:
	print "Playback Speed is ",PlaybackSpeed
	print "Total Lines in the MBC is",count
	print "Total Notes:",totalnotes

#notelistunsorted = []

rows, cols = (5, 5) 
notelistunsorted = [[0 for i in range(2)] for j in range(totalnotes)] 

#print notelistunsorted

for n in range(totalnotes):
	with open(sys.argv[1], 'r') as my_file:
		PosLine=n*6+13
		TimeLine=n*6+14
		#print "Current Index: ",n

		CurrentPosStrRaw=lines[PosLine]
		CurrentPosStr=CurrentPosStrRaw.replace("p=","")
		CurrentPos=float(CurrentPosStr)
		notelistunsorted[n][1]=CurrentPos

		CurrentTimeStrRaw=lines[TimeLine]
		CurrentTimeStr=CurrentTimeStrRaw.replace("t=","")
		CurrentTime=float(CurrentTimeStr)
		notelistunsorted[n][0]=CurrentTime

		

notelist=sorted(notelistunsorted, key=lambda element: (element[0], element[1]))

if superverbose:
	print notelist

notelistlength=len(notelist)

print "notelist has ",notelistlength," elements"

print "checking for duplicates"

res = [] 
for i in notelist: 
    if i not in res: 
        res.append(i) 

notelist=res
notelistlength=len(notelist)
print "new notelist has ",notelistlength," elements"




########### Here's the VIC 20 DATA FORMATTING PART ###########

if (scaletype==30) and (ASMMode==0): #30 note MBC mode using values from VIC-20 manual

	s1notes=[195,201,215,219,223,225,228,231,232,233,235,236,237,238,239,240,241,0]
	s2notes=[135,147,175,183,191,195,201,207,209,212,215,217,219,221,223,225,227,228,229,231,232,233,235,236,237,238,239,240,0]
	s3notes=[135,147,159,163,167,175,179,183,187,191,195,199,201,203,207,209,212,215,217,219,221,223,225,228,231,0]

	s1offset=0 #offsets the value array for the high notes, since the lowest note in the array can't hit note position 0 from the MBC file
	s2offset=0
	s3offset=5

	s1low=0 #min / max values for the note range, since sometimes super high or super low values kinda sound shitty and should be assigned to another channel
	s1high=16
	s2low=0
	s2high=27
	s3low=5
	s3high=29

	voiceIndexSize=1

if (scaletype==33) and (ASMMode==0): #33 note mode using values from VIC-20 manual
	s1notes=[225,228,229,231,232,233,235,236,237,238,239,240,241,0]
	s2notes=[195,201,203,207,209,212,215,217,219,221,223,225,227,228,229,231,232,233,235,236,237,238,239,240,241,0]
	s3notes=[135,147,151,159,163,167,175,179,183,187,191,195,199,201,203,207,209,212,215,217,219,221,223,225,227,228,229,231,232,233,235,236,237,0]

	s1offset=0
	s2offset=0
	s3offset=0

	s1low=0
	s1high=12
	s2low=0
	s2high=24
	s3low=0
	s3high=32

	voiceIndexSize=1

if (scaletype==33) and (ASMMode==1):
	s1notes=[224,4,227,6,229,3,230,6,232,1,233,3,234,5,235,6,236,7,237,7,238,7,239,6,240,5,241,3,242,1,242,7,243,4,244,2,244,6,245,3,245,7]
	s2notes=[193,7,200,5,203,5,206,4,209,2,211,6,214,2,216,4,218,5,220,6,222,5,224,4,226,1,227,6,229,3,230,6,232,1,233,3,234,5,235,6,236,7,237,7,238,7,239,6,240,5,241,3,242,1,242,7,243,4,244,2,244,6,245,3,245,7]
	s3notes=[132,7,146,1,152,2,158,0,163,4,168,5,173,4,178,0,182,3,186,4,190,2,193,7,197,3,200,5,203,5,206,4,209,2,211,6,214,2,216,4,218,5,220,6,222,5,224,4,226,1,227,6,229,3,230,6,232,1,233,3,234,5,235,6,236,7]

	s1offset=0
	s2offset=0
	s3offset=0

	s1low=0
	s1high=20
	s2low=0
	s2high=32
	s3low=0
	s3high=32

	voiceIndexSize=2 #since the ASM sound mode uses two values for each voice, every two values is a new note now instead of every value

t=0
LastNoteTime=0
vicdata=[]

#This section looks complex but it's pretty straightforward.  It finds out how many notes are in a particular "beat" (either 1,2 or 3), and depending on how many it has, it then attempts to assign the note to a particular voice.  
#Since VIC-20 voices are all shifted apart by one octave it tries to assign the lowest note to the lowest channel first (since it's usable range is the smallest" and cycles up from there

while t<>-1:
	CurrentTime=notelist[t][0]
	noteoccurrences=0

	while 1==1:
		tnext=t+1
		
		if superverbose:
			print "tnext is ",tnext

		noteoccurrences=noteoccurrences+1

		if tnext==notelistlength:
			CurrentTimeNext=CurrentTime+0.5
		else:
			CurrentTimeNext=notelist[tnext][0]

		if CurrentTime<>CurrentTimeNext:
			#print noteoccurrences," instances of a note at position ",CurrentTime
			t=t+1
			
			if superverbose:
				print "LastNoteTime is ",LastNoteTime
				print "CurrentTime is ",CurrentTime




			if noteoccurrences==3:
				if superverbose:
					print "detected 3 notes"
				s1used=0
				s2used=0
				s3used=0
				s1val=1 #S1 S2 and S3 values are assigned default values of 1 instead of 0 because 0 is the song terminator value
				s1val2=0
				s2val=1
				s2val2=0
				s3val=1
				s3val2=0
				tlow=t-3
				tmid=t-2
				thigh=t-1
				#print "Current Time is:",CurrentTime
				nlow=int(notelist[tlow][1])
				nmid=int(notelist[tmid][1])
				nhigh=int(notelist[thigh][1])

				if superverbose:
					print "Lowest Note is:",nlow," Middle Note is:",nmid," Highest Note is:",nhigh

				#Attempt to set lowest note in the beat
				if s1low<=nlow<=s1high and s1used==0:
					s1val=s1notes[(nlow-s1offset)*voiceIndexSize]
					s1val2=s1notes[(nlow-s1offset)*voiceIndexSize+1]
					s1used=1
					if superverbose:
						print "nlow set in S3, value:",s3val

				elif s2low<=nlow<=s2high and s2used==0:
					s2val=s2notes[(nlow-s2offset)*voiceIndexSize]
					s2val2=s2notes[(nlow-s2offset)*voiceIndexSize+1]
					s2used=1
					if superverbose:
						print "nlow set in S2, value:",s2val

				elif s3low<=nlow<=s3high and s3used==0:
					s3val=s3notes[(nlow-s3offset)*voiceIndexSize]
					s3val2=s3notes[(nlow-s3offset)*voiceIndexSize+1]
					s3used=1
					if superverbose:
						print "nlow set in S1, value:",s1val

				else:
					if superverbose:
						print "unable to set low note in any channel"

				#Attempt to set the middle note in the beat
				if s1low<=nmid<=s1high and s1used==0:
					s1val=s1notes[(nmid-s1offset)*voiceIndexSize]
					s1val2=s1notes[(nmid-s1offset)*voiceIndexSize+1]
					s1used=1
					if superverbose:
						print "nlow set in S1, value:",s3val

				elif s2low<=nmid<=s2high and s2used==0:
					s2val=s2notes[(nmid-s2offset)*voiceIndexSize]
					s2val2=s2notes[(nmid-s2offset)*voiceIndexSize+1]
					s2used=1
					if superverbose:
						print "nlow set in S2, value:",s2val

				elif s3low<=nmid<=s3high and s3used==0:
					s3val=s3notes[(nmid-s3offset)*voiceIndexSize]
					s3val2=s3notes[(nmid-s3offset)*voiceIndexSize+1]
					s3used=1
					if superverbose:
						print "nlow set in S3, value:",s1val

				else:
					if superverbose:
						print "unable to set low note in any channel"

				#Attempt to set the middle note in the beat
				if s1low<=nhigh<=s1high and s1used==0:
					s1val=s1notes[(nhigh-s1offset)*voiceIndexSize]
					s1val2=s1notes[(nhigh-s1offset)*voiceIndexSize+1]
					s1used=1
					if superverbose:
						print "nlow set in S1, value:",s3val

				elif s2low<=nhigh<=s2high and s2used==0:
					s2val=s2notes[(nhigh-s2offset)*voiceIndexSize]
					s2val2=s2notes[(nhigh-s2offset)*voiceIndexSize+1]
					s2used=1
					if superverbose:
						print "nlow set in S2, value:",s2val

				elif s3low<=nhigh<=s3high and s3used==0:
					s3val=s3notes[(nhigh-s3offset)*voiceIndexSize]
					s3val2=s3notes[(nhigh-s3offset)*voiceIndexSize+1]
					s3used=1
					if superverbose:
						print "nlow set in S3, value:",s1val

				else:
					if superverbose:
						print "unable to set low note in any channel"


				if superverbose:
					print "all voices for beat number ",CurrentTime," set."
				NoteTime=int((CurrentTimeNext-CurrentTime)*timemultiplier-notelength)

				if NoteTime<=scantimemodifier:
					NoteTime=scantimemodifier
				if superverbose:
					print "NoteTime is ",NoteTime

				if ASMMode==0:
					vicdata.append(s1val)
					vicdata.append(s2val)
					vicdata.append(s3val)
					vicdata.append(NoteTime-scantimemodifier)
				else:
					vicdata.append(s1val)
					vicdata.append(s1val2)
					vicdata.append(s2val)
					vicdata.append(s2val2)
					vicdata.append(s3val)
					vicdata.append(s3val2)
					vicdata.append(NoteTime-scantimemodifier)

			if noteoccurrences==2:
				if superverbose:
					print "detected 2 notes"
				s1used=0
				s2used=0
				s3used=0
				s1val=1
				s1val2=0
				s2val=1
				s2val2=0
				s3val=1
				s3val2=0
				tmid=t-2
				thigh=t-1
				#print "Current Time is:",CurrentTime
				nmid=int(notelist[tmid][1])
				nhigh=int(notelist[thigh][1])
				if superverbose:
					print "Middle Note is:",nmid," Highest Note is:",nhigh

				#Attempt to set the middle note in the beat
				if s1low<=nmid<=s1high and s1used==0:
					s1val=s1notes[(nmid-s1offset)*voiceIndexSize]
					s1val2=s1notes[(nmid-s1offset)*voiceIndexSize+1]
					s1used=1
					if superverbose:
						print "nlow set in S1, value:",s3val

				elif s2low<=nmid<=s2high and s2used==0:
					s2val=s2notes[(nmid-s2offset)*voiceIndexSize]
					s2val2=s2notes[(nmid-s2offset)*voiceIndexSize+1]
					s2used=1
					if superverbose:
						print "nlow set in S2, value:",s2val

				elif s3low<=nmid<=s3high and s3used==0:
					s3val=s3notes[(nmid-s3offset)*voiceIndexSize]
					s3val2=s3notes[(nmid-s3offset)*voiceIndexSize+1]
					s3used=1
					if superverbose:
						print "nlow set in S3, value:",s1val

				else:
					if superverbose:
						print "unable to set low note in any channel"

				#Attempt to set the middle note in the beat
				if s1low<=nhigh<=s1high and s1used==0:
					s1val=s1notes[(nhigh-s1offset)*voiceIndexSize]
					s1val2=s1notes[(nhigh-s1offset)*voiceIndexSize+1]
					s1used=1
					if superverbose:
						print "nlow set in S1, value:",s3val

				elif s2low<=nhigh<=s2high and s2used==0:
					s2val=s2notes[(nhigh-s2offset)*voiceIndexSize]
					s2val2=s2notes[(nhigh-s2offset)*voiceIndexSize+1]
					s2used=1
					if superverbose:
						print "nlow set in S2, value:",s2val

				elif s3low<=nhigh<=s3high and s3used==0:
					s3val=s3notes[(nhigh-s3offset)*voiceIndexSize]
					s3val2=s3notes[(nhigh-s3offset)*voiceIndexSize+1]
					s3used=1
					if superverbose:
						print "nlow set in S3, value:",s1val

				else:
					if superverbose:
						print "unable to set low note in any channel"


				if superverbose:
					print "all voices for beat number ",CurrentTime," set."

				NoteTime=int((CurrentTimeNext-CurrentTime)*timemultiplier-notelength)

				if NoteTime<=scantimemodifier:
					NoteTime=scantimemodifier
				if superverbose:
					print "NoteTime is ",NoteTime

				if ASMMode==0:
					vicdata.append(s1val)
					vicdata.append(s2val)
					vicdata.append(s3val)
					vicdata.append(NoteTime-scantimemodifier)
				else:
					vicdata.append(s1val)
					vicdata.append(s1val2)
					vicdata.append(s2val)
					vicdata.append(s2val2)
					vicdata.append(s3val)
					vicdata.append(s3val2)
					vicdata.append(NoteTime-scantimemodifier)

			if noteoccurrences==1:
				if superverbose:
					print "detected 1 note"
				s1used=0
				s2used=0
				s3used=0
				s1val=1
				s1val2=0
				s2val=1
				s2val2=0
				s3val=1
				s3val2=0
				tmid=t-2
				thigh=t-1
				#print "Current Time is:",CurrentTime
				nhigh=int(notelist[thigh][1])
				if superverbose:
					print "Highest Note is:",nhigh

				#Attempt to set the middle note in the beat
				if s1low<=nhigh<=s1high and s1used==0:
					s1val=s1notes[(nhigh-s1offset)*voiceIndexSize]
					s1val2=s1notes[(nhigh-s1offset)*voiceIndexSize+1]
					s1used=1
					if superverbose:
						print "nlow set in S1, value:",s3val

				elif s2low<=nhigh<=s2high and s2used==0:
					s2val=s2notes[(nhigh-s2offset)*voiceIndexSize]
					s2val2=s2notes[(nhigh-s2offset)*voiceIndexSize+1]
					s2used=1
					if superverbose:
						print "nlow set in S2, value:",s2val

				elif s3low<=nhigh<=s3high and s3used==0:
					s3val=s3notes[(nhigh-s3offset)*voiceIndexSize]
					s3val2=s3notes[(nhigh-s3offset)*voiceIndexSize+1]
					s3used=1
					if superverbose:
						print "nlow set in S3, value:",s1val

				else:
					if superverbose:
						print "unable to set low note in any channel"


				if superverbose:
					print "all voices for beat number ",CurrentTime," set."

				NoteTime=int((CurrentTimeNext-CurrentTime)*timemultiplier-notelength)

				if NoteTime<=scantimemodifier:
					NoteTime=scantimemodifier
				if superverbose:
					print "NoteTime is ",NoteTime

				if ASMMode==0:
					vicdata.append(s1val)
					vicdata.append(s2val)
					vicdata.append(s3val)
					vicdata.append(NoteTime-scantimemodifier)
				else:
					vicdata.append(s1val)
					vicdata.append(s1val2)
					vicdata.append(s2val)
					vicdata.append(s2val2)
					vicdata.append(s3val)
					vicdata.append(s3val2)
					vicdata.append(NoteTime-scantimemodifier)

			LastNoteTime=CurrentTime

			


			print "-------"
			break
		t=t+1
	if t>=notelistlength:
		break

#Append the terminator value so the player knows to stop playing (when S1 val is a 0)
vicdata.append(0) 
vicdata.append(0)
vicdata.append(0)
vicdata.append(0)
vicdata.append(0)
vicdata.append(0)
vicdata.append(0)

#find the total number of note data we need to format into the BASIC program
vicdatalen=len(vicdata)


if superverbose:
	print""
	print "VICDATA array:"
	print vicdata
	
if verbose:
	print""
	print "Total VICDATA array length is:",vicdatalen
	print ""

with open("VICMusicBasic_ASM", 'r') as f:
	program_out = f.read().splitlines()


viclineindex=0

datalinecounter=0 #increment by one every time a line is printed
viclineoffset=300 #start datalines at the "300" line in BASIC
dataline=str(viclineoffset+datalinecounter) + "data" #set up initial data string
datalineelements=0 #tracks how many elements are in a line (basically just to avoid a comma between "data" and the first value

for v in range(vicdatalen):
	
	datalinelen=len(dataline)
	nextvaluetest=str(vicdata[v])
	nextvaluelen=len(nextvaluetest)
	
	if (datalinelen + nextvaluelen + 1) < 79:
		datalineelements=datalineelements+1
		if datalineelements>1:
		
			dataline=dataline + "," + nextvaluetest
		else:
			dataline=dataline + nextvaluetest
	else:
		if printdata:
			print dataline
			
		program_out.append(dataline)
		datalinecounter=datalinecounter+1
		datalineelements=0
		dataline=str(viclineoffset+datalinecounter) + "data" + nextvaluetest + ","
		
print dataline 
program_out.append(dataline)
		
	

with open('program_out.txt', 'w') as f:
    for item in program_out:
        print >> f, item






