#!/usr/bin/env python

import sys

notelength=1
scantimemodifier=50

scaletype=33
ASMMode=1 		#0=using defualt VIC registers 1=using 10-OFR ASM code for pitches

content = []

#test
#test test
#test test test
test=1

with open(sys.argv[1], 'r') as my_file:
	count = len(my_file.readlines(  ))
	
with open(sys.argv[1], 'r') as f:
	lines = f.read().splitlines()

PlaybackSpeedStrRaw=lines[1]
PlaybackSpeedStr=PlaybackSpeedStrRaw.replace("PlaybackSpeed=","")
PlaybackSpeed=float(PlaybackSpeedStr)
print "Playback Speed is ",PlaybackSpeed
timemultiplier=350/PlaybackSpeed

print "Total Lines in the MBC is",count
countadj=count-12
totalnotes=countadj/6
totalnotesadj=totalnotes-1
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

if (scaletype==30) and (ASMMode==0):

	s1notes=[195,201,215,219,223,225,228,231,232,233,235,236,237,238,239,240,241,0]
	s2notes=[135,147,175,183,191,195,201,207,209,212,215,217,219,221,223,225,227,228,229,231,232,233,235,236,237,238,239,240,0]
	s3notes=[135,147,159,163,167,175,179,183,187,191,195,199,201,203,207,209,212,215,217,219,221,223,225,228,231,0]

	s1offset=0
	s2offset=0
	s3offset=5

	s1low=0
	s1high=16
	s2low=0
	s2high=27
	s3low=5
	s3high=29

	voiceIndexSize=1

if (scaletype==33) and (ASMMode==0):
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

	voiceIndexSize=2

t=0
LastNoteTime=0
vicdata=[]

while t<>-1:
	CurrentTime=notelist[t][0]
	noteoccurrences=0

	while 1==1:
		tnext=t+1
		print "tnext is ",tnext

		noteoccurrences=noteoccurrences+1

		if tnext==notelistlength:
			CurrentTimeNext=CurrentTime+0.5
		else:
			CurrentTimeNext=notelist[tnext][0]

		if CurrentTime<>CurrentTimeNext:
			#print noteoccurrences," instances of a note at position ",CurrentTime
			t=t+1

			print "LastNoteTime is ",LastNoteTime
			print "CurrentTime is ",CurrentTime




			if noteoccurrences==3:

				print "detected 3 notes"
				s1used=0
				s2used=0
				s3used=0
				s1val=0
				s1val2=0
				s2val=0
				s2val2=0
				s3val=0
				s3val2=0
				tlow=t-3
				tmid=t-2
				thigh=t-1
				#print "Current Time is:",CurrentTime
				nlow=int(notelist[tlow][1])
				nmid=int(notelist[tmid][1])
				nhigh=int(notelist[thigh][1])

				print "Lowest Note is:",nlow," Middle Note is:",nmid," Highest Note is:",nhigh

				#Attempt to set lowest note in the beat
				if s1low<=nlow<=s1high and s1used==0:
					s1val=s1notes[(nlow-s1offset)*voiceIndexSize]
					s1val2=s1notes[(nlow-s1offset)*voiceIndexSize+1]
					s1used=1
					print "nlow set in S3, value:",s3val

				elif s2low<=nlow<=s2high and s2used==0:
					s2val=s2notes[(nlow-s2offset)*voiceIndexSize]
					s2val2=s2notes[(nlow-s2offset)*voiceIndexSize+1]
					s2used=1
					print "nlow set in S2, value:",s2val

				elif s3low<=nlow<=s3high and s3used==0:
					s3val=s3notes[(nlow-s3offset)*voiceIndexSize]
					s3val2=s3notes[(nlow-s3offset)*voiceIndexSize+1]
					s3used=1
					print "nlow set in S1, value:",s1val

				else:
					print "unable to set low note in any channel"

				#Attempt to set the middle note in the beat
				if s1low<=nmid<=s1high and s1used==0:
					s1val=s1notes[(nmid-s1offset)*voiceIndexSize]
					s1val2=s1notes[(nmid-s1offset)*voiceIndexSize+1]
					s1used=1
					print "nlow set in S1, value:",s3val

				elif s2low<=nmid<=s2high and s2used==0:
					s2val=s2notes[(nmid-s2offset)*voiceIndexSize]
					s2val2=s2notes[(nmid-s2offset)*voiceIndexSize+1]
					s2used=1
					print "nlow set in S2, value:",s2val

				elif s3low<=nmid<=s3high and s3used==0:
					s3val=s3notes[(nmid-s3offset)*voiceIndexSize]
					s3val2=s3notes[(nmid-s3offset)*voiceIndexSize+1]
					s3used=1
					print "nlow set in S3, value:",s1val

				else:
					print "unable to set low note in any channel"

				#Attempt to set the middle note in the beat
				if s1low<=nhigh<=s1high and s1used==0:
					s1val=s1notes[(nhigh-s1offset)*voiceIndexSize]
					s1val2=s1notes[(nhigh-s1offset)*voiceIndexSize+1]
					s1used=1
					print "nlow set in S1, value:",s3val

				elif s2low<=nhigh<=s2high and s2used==0:
					s2val=s2notes[(nhigh-s2offset)*voiceIndexSize]
					s2val2=s2notes[(nhigh-s2offset)*voiceIndexSize+1]
					s2used=1
					print "nlow set in S2, value:",s2val

				elif s3low<=nhigh<=s3high and s3used==0:
					s3val=s3notes[(nhigh-s3offset)*voiceIndexSize]
					s3val2=s3notes[(nhigh-s3offset)*voiceIndexSize+1]
					s3used=1
					print "nlow set in S3, value:",s1val

				else:
					print "unable to set low note in any channel"



				print "all voices for beat number ",CurrentTime," set."
				NoteTime=int((CurrentTimeNext-CurrentTime)*timemultiplier-notelength)

				if NoteTime<=scantimemodifier:
					NoteTime=scantimemodifier

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

				print "detected 2 notes"
				s1used=0
				s2used=0
				s3used=0
				s1val=0
				s1val2=0
				s2val=0
				s2val2=0
				s3val=0
				s3val2=0
				tmid=t-2
				thigh=t-1
				#print "Current Time is:",CurrentTime
				nmid=int(notelist[tmid][1])
				nhigh=int(notelist[thigh][1])

				print "Middle Note is:",nmid," Highest Note is:",nhigh

				#Attempt to set the middle note in the beat
				if s1low<=nmid<=s1high and s1used==0:
					s1val=s1notes[(nmid-s1offset)*voiceIndexSize]
					s1val2=s1notes[(nmid-s1offset)*voiceIndexSize+1]
					s1used=1
					print "nlow set in S1, value:",s3val

				elif s2low<=nmid<=s2high and s2used==0:
					s2val=s2notes[(nmid-s2offset)*voiceIndexSize]
					s2val2=s2notes[(nmid-s2offset)*voiceIndexSize+1]
					s2used=1
					print "nlow set in S2, value:",s2val

				elif s3low<=nmid<=s3high and s3used==0:
					s3val=s3notes[(nmid-s3offset)*voiceIndexSize]
					s3val2=s3notes[(nmid-s3offset)*voiceIndexSize+1]
					s3used=1
					print "nlow set in S3, value:",s1val

				else:
					print "unable to set low note in any channel"

				#Attempt to set the middle note in the beat
				if s1low<=nhigh<=s1high and s1used==0:
					s1val=s1notes[(nhigh-s1offset)*voiceIndexSize]
					s1val2=s1notes[(nhigh-s1offset)*voiceIndexSize+1]
					s1used=1
					print "nlow set in S1, value:",s3val

				elif s2low<=nhigh<=s2high and s2used==0:
					s2val=s2notes[(nhigh-s2offset)*voiceIndexSize]
					s2val2=s2notes[(nhigh-s2offset)*voiceIndexSize+1]
					s2used=1
					print "nlow set in S2, value:",s2val

				elif s3low<=nhigh<=s3high and s3used==0:
					s3val=s3notes[(nhigh-s3offset)*voiceIndexSize]
					s3val2=s3notes[(nhigh-s3offset)*voiceIndexSize+1]
					s3used=1
					print "nlow set in S3, value:",s1val

				else:
					print "unable to set low note in any channel"



				print "all voices for beat number ",CurrentTime," set."

				NoteTime=int((CurrentTimeNext-CurrentTime)*timemultiplier-notelength)

				if NoteTime<=scantimemodifier:
					NoteTime=scantimemodifier

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

				print "detected 1 note"
				s1used=0
				s2used=0
				s3used=0
				s1val=0
				s1val2=0
				s2val=0
				s2val2=0
				s3val=0
				s3val2=0
				tmid=t-2
				thigh=t-1
				#print "Current Time is:",CurrentTime
				nhigh=int(notelist[thigh][1])

				print "Highest Note is:",nhigh

				#Attempt to set the middle note in the beat
				if s1low<=nhigh<=s1high and s1used==0:
					s1val=s1notes[(nhigh-s1offset)*voiceIndexSize]
					s1val2=s1notes[(nhigh-s1offset)*voiceIndexSize+1]
					s1used=1
					print "nlow set in S1, value:",s3val

				elif s2low<=nhigh<=s2high and s2used==0:
					s2val=s2notes[(nhigh-s2offset)*voiceIndexSize]
					s2val2=s2notes[(nhigh-s2offset)*voiceIndexSize+1]
					s2used=1
					print "nlow set in S2, value:",s2val

				elif s3low<=nhigh<=s3high and s3used==0:
					s3val=s3notes[(nhigh-s3offset)*voiceIndexSize]
					s3val2=s3notes[(nhigh-s3offset)*voiceIndexSize+1]
					s3used=1
					print "nlow set in S3, value:",s1val

				else:
					print "unable to set low note in any channel"



				print "all voices for beat number ",CurrentTime," set."

				NoteTime=int((CurrentTimeNext-CurrentTime)*timemultiplier-notelength)

				if NoteTime<=scantimemodifier:
					NoteTime=scantimemodifier
	
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

vicdata.append(-1)
vicdata.append(0)
vicdata.append(0)
vicdata.append(0)
vicdata.append(0)
vicdata.append(0)
vicdata.append(0)
vicdata.append(0)
vicdata.append(0)
vicdata.append(0)
vicdata.append(0)
vicdata.append(0)
vicdata.append(0)
vicdata.append(0)
vicdata.append(0)

vicdatalen=len(vicdata)

#Pad an extra 4 bytes to the end of the array if it consists of an odd number of beats
if (vicdatalen % 2) == 0:
	vicdata.append(0)
	vicdata.append(0)
	vicdata.append(0)
	vicdata.append(0)

print vicdata
print "Total length is:",vicdatalen

with open("VICMusicBasic_ASM", 'r') as f:
	program_out = f.read().splitlines()


viclineindex=0
v=0
viclineoffset=300

vicdatanotes=int(vicdatalen/8)

for v in range(vicdatanotes):
	vicline=v*10+300
	#pull each element out of the array
	el0=vicdata[v*8+0]
	el1=vicdata[v*8+1]
	el2=vicdata[v*8+2]
	el3=vicdata[v*8+3]
	el4=vicdata[v*8+4]
	el5=vicdata[v*8+5]
	el6=vicdata[v*8+6]
	el7=vicdata[v*8+7]

	datastring=str(vicline) + "data" + str(el0) + "," + str(el1) + "," + str(el2) + "," + str(el3) + "," + str(el4) + "," + str(el5) + "," + str(el6) + "," + str(el7)
	datastring.replace(",0,",",,")

	print datastring
	program_out.append(datastring)

#print program_out

with open('program_out.txt', 'w') as f:
    for item in program_out:
        print >> f, item






