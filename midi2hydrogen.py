#!/usr/bin/env python

# midi2hydrogen.py 0.1, 19-07-2008

# http://www.dainaccio.wordpress.com
# Author: Dainaccio, superdinoz at yahoo dot it

# This software is released under GPLv3 license:
# http://www.gnu.org/licenses/gpl.html

# You're using this software at your own risk. The author shall not
# be held liable for ANY problems caused by using this software.

# THIS VERSION IS NOT USER FRIENDLY

from MidiOutStream import MidiOutStream
from MidiInFile import MidiInFile
import sys

'''
TODO:
	- Detect bpm from midi file
	- Add a GUI for the configuration of the converter
'''

class Transposer(MidiOutStream):
   

	# http://en.wikipedia.org/wiki/General_MIDI#Percussion_notes
	'''
	The midi code and the related instrument:
	
	35 Bass Drum 2
	36 Bass Drum 1
	37 Side Stick
	38 Snare Drum 1
	39 Hand Clap
	40 Snare Drum 2
	41 Low Tom 2
	42 Closed Hi-hat
	43 Low Tom 1
	44 Pedal Hi-hat
	45 Mid Tom 2
	46 Open Hi-hat
	47 Mid Tom 1
	48 High Tom 2
	49 Crash Cymbal 1
	50 High Tom 1
	51 Ride Cymbal 1
	52 Chinese Cymbal
	53 Ride Bell
	54 Tambourine
	55 Splash Cymbal
	56 Cowbell
	57 Crash Cymbal 2
	58 Vibra Slap
	59 Ride Cymbal 2
	60 High Bongo
	61 Low Bongo
	'''
	
	# the first number is the Hydrogen instrument, the second the Midi note
	# It works with YamahaVintageKit, change the values with a different drumkit
	transposerTable = {0:35, 1:38, 2:43, 3:47, 4:50, 5:42, 6:46, 7:59, 8:44, 9:49}
	
	# my drumkit is small. I need to play the same sample despite being two different Midi notes
	# Syntax: noteFound:noteToPlay
	similarInstruments = {36:35, 40:38, 41:43, 45:47, 52:59, 53:59, 55:49 , 57:49}
	
	# Midi drum channel
	drumChannel = 9
	
	
	maxHydInstr = 20
	midiRate = 960
	maxDim = 192
	
	
	def __init__(self):
		self.melodia = []

	def getMelodia(self):
		return self.melodia
	
	def note_on(self, channel=0, note=0x40, velocity=0x40):
		
 
		if channel == self.drumChannel:

			try:
				note = self.similarInstruments[note]
			except:
				pass
			
			
			self.melodia.append((self.abs_time()*self.maxDim/(10*self.midiRate), note, velocity/100.0))
	
	def size(self):
		return self.duration()/self.maxDim + 1
		
	def duration(self):
		return self.melodia[-1][0]
	
	def getSequence(self, instrument, battuta):
		# Get the sequence (time and velocity) of a specific note (=drum instrument)
		try:
			note = self.transposerTable[instrument]
			sequence = []
		
			for a in self.melodia:
				if a[1] == note:
					if a[0] >= battuta*self.maxDim and a[0] < (battuta + 1)*self.maxDim:
						sequence.append((a[0] - battuta*self.maxDim,a[2]))
			return sequence
		except:
			return None
		
	def getInstruments(self):
		# The amount of use of each note in the midi drum
		
		instruments = {}
		
		for a in self.melodia:
			try:
				instruments[a[1]] += 1
			except:
				instruments[a[1]] = 1
		
		return instruments
		
	  
	def note_off(self, channel=0, note=0x40, velocity=0x40):
		""

if len(sys.argv) != 3:
	
	print "midi2hydrogen\n\nUsage:\n\tpython midi2hydrogen.py input.mid output.h2song\n"
	exit()
	
	
event_handler = Transposer()
in_file = sys.argv[1]
midi_in = MidiInFile(event_handler, in_file)
midi_in.read()

#print event_handler.getInstruments()
#print event_handler.duration()
#print event_handler.size()
output = ""
patternList = ""

for battuta in range(event_handler.size()):
	output += '''\t\t\t<pattern>
\t\t\t\t<name>Song %i</name>
\t\t\t\t<size>%i</size>
\t\t\t\t<sequenceList>\n'''%(battuta,event_handler.maxDim)


	patternList += '''			<group>
				<patternID>Song %i</patternID>
			</group>\n'''%battuta


	for instrument in range(0,event_handler.maxHydInstr):
		output += "\t\t\t\t\t<sequence>\n\t\t\t\t\t\t<noteList>\n"
	
		if event_handler.getSequence(instrument, battuta) != None:
			for seq in event_handler.getSequence(instrument, battuta):
				output += '''							<note>
		                   <position>%i</position>
		                   <velocity>%.2f</velocity>
		                   <pan_L>1</pan_L>
		                   <pan_R>1</pan_R>
		                   <pitch>0</pitch>
		                   <length>-1</length>
		                   <instrument>%i</instrument>
		               </note>\n'''%(seq[0],seq[1],instrument)


		output += "\t\t\t\t\t\t</noteList>\n\t\t\t\t\t</sequence>\n"
	
	output += '''\t\t\t\t</sequenceList>\n
\t\t\t</pattern>\n'''
        
        
output = '''
<song>
    <version>0.9.3</version>
    <bpm>30</bpm>
    <volume>0.61</volume>
    <metronomeVolume>0.5</metronomeVolume>
    <name>Scemo chi legge</name>
    <author>Unknown</author>
    <notes>Created with midi2hydrogen</notes>
    <loopEnabled>true</loopEnabled>
    <mode>song</mode>
    <humanize_time>0</humanize_time>
    <humanize_velocity>0</humanize_velocity>
    <swing_factor>0</swing_factor>
    <delayFXEnabled>false</delayFXEnabled>
    <delayFXWetLevel>1</delayFXWetLevel>
    <delayFXFeedback>0.4</delayFXFeedback>
    <delayFXTime>48</delayFXTime>
    <instrumentList>
        <instrument>
            <id>0</id>
            <drumkit>YamahaVintageKit</drumkit>
            <name>Kick</name>
            <volume>1</volume>
            <isMuted>false</isMuted>
            <isLocked>false</isLocked>
            <pan_L>1</pan_L>
            <pan_R>1</pan_R>
            <gain>1</gain>
            <FX1Level>0</FX1Level>
            <FX2Level>0</FX2Level>
            <FX3Level>0</FX3Level>
            <FX4Level>0</FX4Level>
            <Attack>0</Attack>
            <Decay>0</Decay>
            <Sustain>1</Sustain>
            <Release>1000</Release>
            <randomPitchFactor>0</randomPitchFactor>
            <exclude />
            <layer>
                <filename>Kik_04.flac</filename>
                <min>0.760684</min>
                <max>1</max>
                <gain>1</gain>
                <pitch>0</pitch>
            </layer>
            <layer>
                <filename>Kik_02.flac</filename>
                <min>0.534188</min>
                <max>0.773504</max>
                <gain>1</gain>
                <pitch>0</pitch>
            </layer>
            <layer>
                <filename>Kik_03.flac</filename>
                <min>0.286325</min>
                <max>0.534188</max>
                <gain>1</gain>
                <pitch>0</pitch>
            </layer>
            <layer>
                <filename>Kik_04.flac</filename>
                <min>0</min>
                <max>0.286325</max>
                <gain>1</gain>
                <pitch>0</pitch>
            </layer>
        </instrument>
        <instrument>
            <id>1</id>
            <drumkit>YamahaVintageKit</drumkit>
            <name>Snare</name>
            <volume>1</volume>
            <isMuted>false</isMuted>
            <isLocked>false</isLocked>
            <pan_L>1</pan_L>
            <pan_R>1</pan_R>
            <gain>1</gain>
            <FX1Level>0</FX1Level>
            <FX2Level>0</FX2Level>
            <FX3Level>0</FX3Level>
            <FX4Level>0</FX4Level>
            <Attack>0</Attack>
            <Decay>0</Decay>
            <Sustain>1</Sustain>
            <Release>1000</Release>
            <randomPitchFactor>0</randomPitchFactor>
            <exclude />
            <layer>
                <filename>SN_B_04.flac</filename>
                <min>0.764957</min>
                <max>1</max>
                <gain>1</gain>
                <pitch>0</pitch>
            </layer>
            <layer>
                <filename>SN_B_03.flac</filename>
                <min>0.512821</min>
                <max>0.760684</max>
                <gain>1</gain>
                <pitch>0</pitch>
            </layer>
            <layer>
                <filename>SN_B_02.flac</filename>
                <min>0.311966</min>
                <max>0.512821</max>
                <gain>1</gain>
                <pitch>0</pitch>
            </layer>
            <layer>
                <filename>SN_B_01.flac</filename>
                <min>0</min>
                <max>0.311966</max>
                <gain>1</gain>
                <pitch>0</pitch>
            </layer>
        </instrument>
        <instrument>
            <id>2</id>
            <drumkit>YamahaVintageKit</drumkit>
            <name>Floor Tom</name>
            <volume>0.84</volume>
            <isMuted>false</isMuted>
            <isLocked>false</isLocked>
            <pan_L>1</pan_L>
            <pan_R>1</pan_R>
            <gain>1</gain>
            <FX1Level>0</FX1Level>
            <FX2Level>0</FX2Level>
            <FX3Level>0</FX3Level>
            <FX4Level>0</FX4Level>
            <Attack>0</Attack>
            <Decay>0</Decay>
            <Sustain>1</Sustain>
            <Release>1000</Release>
            <randomPitchFactor>0</randomPitchFactor>
            <exclude />
            <layer>
                <filename>Flr_Tom_04.flac</filename>
                <min>0.722222</min>
                <max>1</max>
                <gain>1</gain>
                <pitch>0</pitch>
            </layer>
            <layer>
                <filename>Flr_Tom_03.flac</filename>
                <min>0.512821</min>
                <max>0.726496</max>
                <gain>1</gain>
                <pitch>0</pitch>
            </layer>
            <layer>
                <filename>Flr_Tom_02.flac</filename>
                <min>0.269231</min>
                <max>0.521368</max>
                <gain>1</gain>
                <pitch>0</pitch>
            </layer>
            <layer>
                <filename>Flr_Tom_01.flac</filename>
                <min>0</min>
                <max>0.269231</max>
                <gain>1</gain>
                <pitch>0</pitch>
            </layer>
        </instrument>
        <instrument>
            <id>4</id>
            <drumkit>YamahaVintageKit</drumkit>
            <name>Mid Tom</name>
            <volume>0.79</volume>
            <isMuted>false</isMuted>
            <isLocked>false</isLocked>
            <pan_L>1</pan_L>
            <pan_R>1</pan_R>
            <gain>1</gain>
            <FX1Level>0</FX1Level>
            <FX2Level>0</FX2Level>
            <FX3Level>0</FX3Level>
            <FX4Level>0</FX4Level>
            <Attack>0</Attack>
            <Decay>0</Decay>
            <Sustain>1</Sustain>
            <Release>1000</Release>
            <randomPitchFactor>0</randomPitchFactor>
            <exclude />
            <layer>
                <filename>Mid_Tom_04.flac</filename>
                <min>0.773504</min>
                <max>1</max>
                <gain>1</gain>
                <pitch>0</pitch>
            </layer>
            <layer>
                <filename>Mid_Tom_03.flac</filename>
                <min>0.521368</min>
                <max>0.769231</max>
                <gain>1</gain>
                <pitch>0</pitch>
            </layer>
            <layer>
                <filename>Mid_Tom_02.flac</filename>
                <min>0.260684</min>
                <max>0.525641</max>
                <gain>1</gain>
                <pitch>0</pitch>
            </layer>
            <layer>
                <filename>Mid_Tom_01.flac</filename>
                <min>0</min>
                <max>0.264957</max>
                <gain>1</gain>
                <pitch>0</pitch>
            </layer>
        </instrument>
        <instrument>
            <id>5</id>
            <drumkit>YamahaVintageKit</drumkit>
            <name>High Tom</name>
            <volume>0.85</volume>
            <isMuted>false</isMuted>
            <isLocked>false</isLocked>
            <pan_L>1</pan_L>
            <pan_R>1</pan_R>
            <gain>1</gain>
            <FX1Level>0</FX1Level>
            <FX2Level>0</FX2Level>
            <FX3Level>0</FX3Level>
            <FX4Level>0</FX4Level>
            <Attack>0</Attack>
            <Decay>0</Decay>
            <Sustain>1</Sustain>
            <Release>1000</Release>
            <randomPitchFactor>0</randomPitchFactor>
            <exclude />
            <layer>
                <filename>Hi_Tom_04.flac</filename>
                <min>0.764957</min>
                <max>1</max>
                <gain>1</gain>
                <pitch>0</pitch>
            </layer>
            <layer>
                <filename>Hi_Tom_03.flac</filename>
                <min>0.482906</min>
                <max>0.764957</max>
                <gain>1</gain>
                <pitch>0</pitch>
            </layer>
            <layer>
                <filename>Hi_Tom_02.flac</filename>
                <min>0.200855</min>
                <max>0.482906</max>
                <gain>1</gain>
                <pitch>0</pitch>
            </layer>
            <layer>
                <filename>Hi_Tom_01.flac</filename>
                <min>0</min>
                <max>0.205128</max>
                <gain>1</gain>
                <pitch>0</pitch>
            </layer>
        </instrument>
        <instrument>
            <id>6</id>
            <drumkit>YamahaVintageKit</drumkit>
            <name>Closed Hat</name>
            <volume>0.45</volume>
            <isMuted>false</isMuted>
            <isLocked>false</isLocked>
            <pan_L>0.96</pan_L>
            <pan_R>1</pan_R>
            <gain>1</gain>
            <FX1Level>0</FX1Level>
            <FX2Level>0</FX2Level>
            <FX3Level>0</FX3Level>
            <FX4Level>0</FX4Level>
            <Attack>0</Attack>
            <Decay>0</Decay>
            <Sustain>1</Sustain>
            <Release>1000</Release>
            <randomPitchFactor>0</randomPitchFactor>
            <exclude />
            <layer>
                <filename>Cl_HH_03.flac</filename>
                <min>0.649573</min>
                <max>1</max>
                <gain>1</gain>
                <pitch>0</pitch>
            </layer>
            <layer>
                <filename>Cl_HH_02.flac</filename>
                <min>0.307692</min>
                <max>0.649573</max>
                <gain>1</gain>
                <pitch>0</pitch>
            </layer>
            <layer>
                <filename>Cl_HH_01.flac</filename>
                <min>0</min>
                <max>0.307692</max>
                <gain>1</gain>
                <pitch>0</pitch>
            </layer>
        </instrument>
        <instrument>
            <id>7</id>
            <drumkit>YamahaVintageKit</drumkit>
            <name>Open Hat</name>
            <volume>0.37</volume>
            <isMuted>false</isMuted>
            <isLocked>false</isLocked>
            <pan_L>1</pan_L>
            <pan_R>1</pan_R>
            <gain>1</gain>
            <FX1Level>0</FX1Level>
            <FX2Level>0</FX2Level>
            <FX3Level>0</FX3Level>
            <FX4Level>0</FX4Level>
            <Attack>0</Attack>
            <Decay>0</Decay>
            <Sustain>1</Sustain>
            <Release>1000</Release>
            <randomPitchFactor>0</randomPitchFactor>
            <exclude />
            <layer>
                <filename>Op_HH_04.flac</filename>
                <min>0.75641</min>
                <max>1</max>
                <gain>1</gain>
                <pitch>0</pitch>
            </layer>
            <layer>
                <filename>Op_HH_03.flac</filename>
                <min>0.487179</min>
                <max>0.752137</max>
                <gain>1</gain>
                <pitch>0</pitch>
            </layer>
            <layer>
                <filename>Op_HH_02.flac</filename>
                <min>0.24359</min>
                <max>0.482906</max>
                <gain>1</gain>
                <pitch>0</pitch>
            </layer>
            <layer>
                <filename>Op_HH_01.flac</filename>
                <min>0</min>
                <max>0.24359</max>
                <gain>1</gain>
                <pitch>0</pitch>
            </layer>
        </instrument>
        <instrument>
            <id>8</id>
            <drumkit>YamahaVintageKit</drumkit>
            <name>Ride Cymbal</name>
            <volume>0.6</volume>
            <isMuted>false</isMuted>
            <isLocked>false</isLocked>
            <pan_L>1</pan_L>
            <pan_R>0.94</pan_R>
            <gain>1</gain>
            <FX1Level>0</FX1Level>
            <FX2Level>0</FX2Level>
            <FX3Level>0</FX3Level>
            <FX4Level>0</FX4Level>
            <Attack>0</Attack>
            <Decay>0</Decay>
            <Sustain>1</Sustain>
            <Release>1000</Release>
            <randomPitchFactor>0</randomPitchFactor>
            <exclude />
            <layer>
                <filename>Rd_Cymb_04_bell.flac</filename>
                <min>0.760684</min>
                <max>1</max>
                <gain>1</gain>
                <pitch>0</pitch>
            </layer>
            <layer>
                <filename>Rd_Cymb_03.flac</filename>
                <min>0.517094</min>
                <max>0.764957</max>
                <gain>1</gain>
                <pitch>0</pitch>
            </layer>
            <layer>
                <filename>Rd_Cymb_02.flac</filename>
                <min>0.235043</min>
                <max>0.525641</max>
                <gain>1</gain>
                <pitch>0</pitch>
            </layer>
            <layer>
                <filename>Rd_Cymb_01.flac</filename>
                <min>0</min>
                <max>0.235043</max>
                <gain>1</gain>
                <pitch>0</pitch>
            </layer>
        </instrument>
        <instrument>
            <id>9</id>
            <drumkit>YamahaVintageKit</drumkit>
            <name>Sizzle Cymbal</name>
            <volume>0.67</volume>
            <isMuted>false</isMuted>
            <isLocked>false</isLocked>
            <pan_L>1</pan_L>
            <pan_R>1</pan_R>
            <gain>1</gain>
            <FX1Level>0</FX1Level>
            <FX2Level>0</FX2Level>
            <FX3Level>0</FX3Level>
            <FX4Level>0</FX4Level>
            <Attack>0</Attack>
            <Decay>0</Decay>
            <Sustain>1</Sustain>
            <Release>1000</Release>
            <randomPitchFactor>0</randomPitchFactor>
            <exclude />
            <layer>
                <filename>Szl_Cym_03_bell.flac</filename>
                <min>0.739316</min>
                <max>1</max>
                <gain>1</gain>
                <pitch>0</pitch>
            </layer>
            <layer>
                <filename>Szl_Cym_02.flac</filename>
                <min>0.358974</min>
                <max>0.735043</max>
                <gain>1</gain>
                <pitch>0</pitch>
            </layer>
            <layer>
                <filename>Szl_Cym_01.flac</filename>
                <min>0</min>
                <max>0.354701</max>
                <gain>1</gain>
                <pitch>0</pitch>
            </layer>
        </instrument>
        <instrument>
            <id>10</id>
            <drumkit>YamahaVintageKit</drumkit>
            <name>Crash Cymbal</name>
            <volume>0.43</volume>
            <isMuted>false</isMuted>
            <isLocked>false</isLocked>
            <pan_L>1</pan_L>
            <pan_R>1</pan_R>
            <gain>1</gain>
            <FX1Level>0</FX1Level>
            <FX2Level>0</FX2Level>
            <FX3Level>0</FX3Level>
            <FX4Level>0</FX4Level>
            <Attack>0</Attack>
            <Decay>0</Decay>
            <Sustain>1</Sustain>
            <Release>1000</Release>
            <randomPitchFactor>0</randomPitchFactor>
            <exclude />
            <layer>
                <filename>Crsh_Cym_02.flac</filename>
                <min>0.57265</min>
                <max>1</max>
                <gain>1</gain>
                <pitch>0</pitch>
            </layer>
            <layer>
                <filename>Crsh_Cym_01.flac</filename>
                <min>0</min>
                <max>0.57265</max>
                <gain>1</gain>
                <pitch>0</pitch>
            </layer>
        </instrument>
        <instrument>
            <id>11</id>
            <drumkit>YamahaVintageKit</drumkit>
            <name>11</name>
            <volume>0.88</volume>
            <isMuted>true</isMuted>
            <isLocked>false</isLocked>
            <pan_L>1</pan_L>
            <pan_R>1</pan_R>
            <gain>1</gain>
            <FX1Level>0</FX1Level>
            <FX2Level>0</FX2Level>
            <FX3Level>0</FX3Level>
            <FX4Level>0</FX4Level>
            <Attack>0</Attack>
            <Decay>0</Decay>
            <Sustain>1</Sustain>
            <Release>1000</Release>
            <randomPitchFactor>0</randomPitchFactor>
            <exclude />
        </instrument>
        <instrument>
            <id>12</id>
            <drumkit>YamahaVintageKit</drumkit>
            <name>12</name>
            <volume>0.82</volume>
            <isMuted>true</isMuted>
            <isLocked>false</isLocked>
            <pan_L>1</pan_L>
            <pan_R>1</pan_R>
            <gain>1</gain>
            <FX1Level>0</FX1Level>
            <FX2Level>0</FX2Level>
            <FX3Level>0</FX3Level>
            <FX4Level>0</FX4Level>
            <Attack>0</Attack>
            <Decay>0</Decay>
            <Sustain>1</Sustain>
            <Release>1000</Release>
            <randomPitchFactor>0</randomPitchFactor>
            <exclude />
        </instrument>
        <instrument>
            <id>13</id>
            <drumkit>YamahaVintageKit</drumkit>
            <name>13</name>
            <volume>0.84</volume>
            <isMuted>true</isMuted>
            <isLocked>false</isLocked>
            <pan_L>1</pan_L>
            <pan_R>1</pan_R>
            <gain>1</gain>
            <FX1Level>0</FX1Level>
            <FX2Level>0</FX2Level>
            <FX3Level>0</FX3Level>
            <FX4Level>0</FX4Level>
            <Attack>0</Attack>
            <Decay>0</Decay>
            <Sustain>1</Sustain>
            <Release>1000</Release>
            <randomPitchFactor>0</randomPitchFactor>
            <exclude />
        </instrument>
        <instrument>
            <id>14</id>
            <drumkit>YamahaVintageKit</drumkit>
            <name>14</name>
            <volume>0.88</volume>
            <isMuted>true</isMuted>
            <isLocked>false</isLocked>
            <pan_L>0.9</pan_L>
            <pan_R>1</pan_R>
            <gain>1</gain>
            <FX1Level>0</FX1Level>
            <FX2Level>0</FX2Level>
            <FX3Level>0</FX3Level>
            <FX4Level>0</FX4Level>
            <Attack>0</Attack>
            <Decay>0</Decay>
            <Sustain>1</Sustain>
            <Release>1000</Release>
            <randomPitchFactor>0</randomPitchFactor>
            <exclude />
        </instrument>
        <instrument>
            <id>3</id>
            <drumkit>YamahaVintageKit</drumkit>
            <name>15</name>
            <volume>0.84</volume>
            <isMuted>true</isMuted>
            <isLocked>false</isLocked>
            <pan_L>0.96</pan_L>
            <pan_R>1</pan_R>
            <gain>1</gain>
            <FX1Level>0</FX1Level>
            <FX2Level>0</FX2Level>
            <FX3Level>0</FX3Level>
            <FX4Level>0</FX4Level>
            <Attack>0</Attack>
            <Decay>0</Decay>
            <Sustain>1</Sustain>
            <Release>1000</Release>
            <randomPitchFactor>0</randomPitchFactor>
            <exclude />
        </instrument>
        <instrument>
            <id>15</id>
            <drumkit>YamahaVintageKit</drumkit>
            <name>16</name>
            <volume>0.85</volume>
            <isMuted>true</isMuted>
            <isLocked>false</isLocked>
            <pan_L>0.96</pan_L>
            <pan_R>1</pan_R>
            <gain>1</gain>
            <FX1Level>0</FX1Level>
            <FX2Level>0</FX2Level>
            <FX3Level>0</FX3Level>
            <FX4Level>0</FX4Level>
            <Attack>0</Attack>
            <Decay>0</Decay>
            <Sustain>1</Sustain>
            <Release>1000</Release>
            <randomPitchFactor>0</randomPitchFactor>
            <exclude />
        </instrument>
        <instrument>
            <id>16</id>
            <drumkit>YamahaVintageKit</drumkit>
            <name>17</name>
            <volume>0.8</volume>
            <isMuted>true</isMuted>
            <isLocked>false</isLocked>
            <pan_L>1</pan_L>
            <pan_R>1</pan_R>
            <gain>1</gain>
            <FX1Level>0</FX1Level>
            <FX2Level>0</FX2Level>
            <FX3Level>0</FX3Level>
            <FX4Level>0</FX4Level>
            <Attack>0</Attack>
            <Decay>0</Decay>
            <Sustain>1</Sustain>
            <Release>1000</Release>
            <randomPitchFactor>0</randomPitchFactor>
            <exclude />
        </instrument>
        <instrument>
            <id>17</id>
            <drumkit>YamahaVintageKit</drumkit>
            <name>18</name>
            <volume>0.8</volume>
            <isMuted>true</isMuted>
            <isLocked>false</isLocked>
            <pan_L>1</pan_L>
            <pan_R>1</pan_R>
            <gain>1</gain>
            <FX1Level>0</FX1Level>
            <FX2Level>0</FX2Level>
            <FX3Level>0</FX3Level>
            <FX4Level>0</FX4Level>
            <Attack>0</Attack>
            <Decay>0</Decay>
            <Sustain>1</Sustain>
            <Release>1000</Release>
            <randomPitchFactor>0</randomPitchFactor>
            <exclude />
        </instrument>
        <instrument>
            <id>18</id>
            <drumkit>YamahaVintageKit</drumkit>
            <name>19</name>
            <volume>0.8</volume>
            <isMuted>true</isMuted>
            <isLocked>false</isLocked>
            <pan_L>1</pan_L>
            <pan_R>1</pan_R>
            <gain>1</gain>
            <FX1Level>0</FX1Level>
            <FX2Level>0</FX2Level>
            <FX3Level>0</FX3Level>
            <FX4Level>0</FX4Level>
            <Attack>0</Attack>
            <Decay>0</Decay>
            <Sustain>1</Sustain>
            <Release>1000</Release>
            <randomPitchFactor>0</randomPitchFactor>
            <exclude />
        </instrument>
        <instrument>
            <id>19</id>
            <drumkit>YamahaVintageKit</drumkit>
            <name>20</name>
            <volume>0.8</volume>
            <isMuted>true</isMuted>
            <isLocked>false</isLocked>
            <pan_L>1</pan_L>
            <pan_R>1</pan_R>
            <gain>1</gain>
            <FX1Level>0</FX1Level>
            <FX2Level>0</FX2Level>
            <FX3Level>0</FX3Level>
            <FX4Level>0</FX4Level>
            <Attack>0</Attack>
            <Decay>0</Decay>
            <Sustain>1</Sustain>
            <Release>1000</Release>
            <randomPitchFactor>0</randomPitchFactor>
            <exclude />
        </instrument>
        <instrument>
            <id>20</id>
            <drumkit>YamahaVintageKit</drumkit>
            <name>21</name>
            <volume>0.8</volume>
            <isMuted>true</isMuted>
            <isLocked>false</isLocked>
            <pan_L>1</pan_L>
            <pan_R>1</pan_R>
            <gain>1</gain>
            <FX1Level>0</FX1Level>
            <FX2Level>0</FX2Level>
            <FX3Level>0</FX3Level>
            <FX4Level>0</FX4Level>
            <Attack>0</Attack>
            <Decay>0</Decay>
            <Sustain>1</Sustain>
            <Release>1000</Release>
            <randomPitchFactor>0</randomPitchFactor>
            <exclude />
        </instrument>
        <instrument>
            <id>21</id>
            <drumkit>YamahaVintageKit</drumkit>
            <name>22</name>
            <volume>0.8</volume>
            <isMuted>true</isMuted>
            <isLocked>false</isLocked>
            <pan_L>1</pan_L>
            <pan_R>1</pan_R>
            <gain>1</gain>
            <FX1Level>0</FX1Level>
            <FX2Level>0</FX2Level>
            <FX3Level>0</FX3Level>
            <FX4Level>0</FX4Level>
            <Attack>0</Attack>
            <Decay>0</Decay>
            <Sustain>1</Sustain>
            <Release>1000</Release>
            <randomPitchFactor>0</randomPitchFactor>
            <exclude />
        </instrument>
        <instrument>
            <id>22</id>
            <drumkit>YamahaVintageKit</drumkit>
            <name>23</name>
            <volume>0.8</volume>
            <isMuted>true</isMuted>
            <isLocked>false</isLocked>
            <pan_L>1</pan_L>
            <pan_R>1</pan_R>
            <gain>1</gain>
            <FX1Level>0</FX1Level>
            <FX2Level>0</FX2Level>
            <FX3Level>0</FX3Level>
            <FX4Level>0</FX4Level>
            <Attack>0</Attack>
            <Decay>0</Decay>
            <Sustain>1</Sustain>
            <Release>1000</Release>
            <randomPitchFactor>0</randomPitchFactor>
            <exclude />
        </instrument>
        <instrument>
            <id>23</id>
            <drumkit>YamahaVintageKit</drumkit>
            <name>24</name>
            <volume>0.8</volume>
            <isMuted>true</isMuted>
            <isLocked>false</isLocked>
            <pan_L>1</pan_L>
            <pan_R>1</pan_R>
            <gain>1</gain>
            <FX1Level>0</FX1Level>
            <FX2Level>0</FX2Level>
            <FX3Level>0</FX3Level>
            <FX4Level>0</FX4Level>
            <Attack>0</Attack>
            <Decay>0</Decay>
            <Sustain>1</Sustain>
            <Release>1000</Release>
            <randomPitchFactor>0</randomPitchFactor>
            <exclude />
        </instrument>
        <instrument>
            <id>24</id>
            <drumkit>YamahaVintageKit</drumkit>
            <name>25</name>
            <volume>0.8</volume>
            <isMuted>true</isMuted>
            <isLocked>false</isLocked>
            <pan_L>1</pan_L>
            <pan_R>1</pan_R>
            <gain>1</gain>
            <FX1Level>0</FX1Level>
            <FX2Level>0</FX2Level>
            <FX3Level>0</FX3Level>
            <FX4Level>0</FX4Level>
            <Attack>0</Attack>
            <Decay>0</Decay>
            <Sustain>1</Sustain>
            <Release>1000</Release>
            <randomPitchFactor>0</randomPitchFactor>
            <exclude />
        </instrument>
        <instrument>
            <id>25</id>
            <drumkit>YamahaVintageKit</drumkit>
            <name>26</name>
            <volume>0.8</volume>
            <isMuted>true</isMuted>
            <isLocked>false</isLocked>
            <pan_L>1</pan_L>
            <pan_R>1</pan_R>
            <gain>1</gain>
            <FX1Level>0</FX1Level>
            <FX2Level>0</FX2Level>
            <FX3Level>0</FX3Level>
            <FX4Level>0</FX4Level>
            <Attack>0</Attack>
            <Decay>0</Decay>
            <Sustain>1</Sustain>
            <Release>1000</Release>
            <randomPitchFactor>0</randomPitchFactor>
            <exclude />
        </instrument>
        <instrument>
            <id>26</id>
            <drumkit>YamahaVintageKit</drumkit>
            <name>27</name>
            <volume>0.8</volume>
            <isMuted>true</isMuted>
            <isLocked>false</isLocked>
            <pan_L>1</pan_L>
            <pan_R>1</pan_R>
            <gain>1</gain>
            <FX1Level>0</FX1Level>
            <FX2Level>0</FX2Level>
            <FX3Level>0</FX3Level>
            <FX4Level>0</FX4Level>
            <Attack>0</Attack>
            <Decay>0</Decay>
            <Sustain>1</Sustain>
            <Release>1000</Release>
            <randomPitchFactor>0</randomPitchFactor>
            <exclude />
        </instrument>
        <instrument>
            <id>27</id>
            <drumkit>YamahaVintageKit</drumkit>
            <name>28</name>
            <volume>0.8</volume>
            <isMuted>true</isMuted>
            <isLocked>false</isLocked>
            <pan_L>1</pan_L>
            <pan_R>1</pan_R>
            <gain>1</gain>
            <FX1Level>0</FX1Level>
            <FX2Level>0</FX2Level>
            <FX3Level>0</FX3Level>
            <FX4Level>0</FX4Level>
            <Attack>0</Attack>
            <Decay>0</Decay>
            <Sustain>1</Sustain>
            <Release>1000</Release>
            <randomPitchFactor>0</randomPitchFactor>
            <exclude />
        </instrument>
        <instrument>
            <id>28</id>
            <drumkit>YamahaVintageKit</drumkit>
            <name>29</name>
            <volume>0.8</volume>
            <isMuted>true</isMuted>
            <isLocked>false</isLocked>
            <pan_L>1</pan_L>
            <pan_R>1</pan_R>
            <gain>1</gain>
            <FX1Level>0</FX1Level>
            <FX2Level>0</FX2Level>
            <FX3Level>0</FX3Level>
            <FX4Level>0</FX4Level>
            <Attack>0</Attack>
            <Decay>0</Decay>
            <Sustain>1</Sustain>
            <Release>1000</Release>
            <randomPitchFactor>0</randomPitchFactor>
            <exclude />
        </instrument>
        <instrument>
            <id>29</id>
            <drumkit>YamahaVintageKit</drumkit>
            <name>30</name>
            <volume>0.8</volume>
            <isMuted>true</isMuted>
            <isLocked>false</isLocked>
            <pan_L>1</pan_L>
            <pan_R>1</pan_R>
            <gain>1</gain>
            <FX1Level>0</FX1Level>
            <FX2Level>0</FX2Level>
            <FX3Level>0</FX3Level>
            <FX4Level>0</FX4Level>
            <Attack>0</Attack>
            <Decay>0</Decay>
            <Sustain>1</Sustain>
            <Release>1000</Release>
            <randomPitchFactor>0</randomPitchFactor>
            <exclude />
        </instrument>
        <instrument>
            <id>30</id>
            <drumkit>YamahaVintageKit</drumkit>
            <name>31</name>
            <volume>0.8</volume>
            <isMuted>true</isMuted>
            <isLocked>false</isLocked>
            <pan_L>1</pan_L>
            <pan_R>1</pan_R>
            <gain>1</gain>
            <FX1Level>0</FX1Level>
            <FX2Level>0</FX2Level>
            <FX3Level>0</FX3Level>
            <FX4Level>0</FX4Level>
            <Attack>0</Attack>
            <Decay>0</Decay>
            <Sustain>1</Sustain>
            <Release>1000</Release>
            <randomPitchFactor>0</randomPitchFactor>
            <exclude />
        </instrument>
        <instrument>
            <id>31</id>
            <drumkit>YamahaVintageKit</drumkit>
            <name>32</name>
            <volume>0.8</volume>
            <isMuted>true</isMuted>
            <isLocked>false</isLocked>
            <pan_L>1</pan_L>
            <pan_R>1</pan_R>
            <gain>1</gain>
            <FX1Level>0</FX1Level>
            <FX2Level>0</FX2Level>
            <FX3Level>0</FX3Level>
            <FX4Level>0</FX4Level>
            <Attack>0</Attack>
            <Decay>0</Decay>
            <Sustain>1</Sustain>
            <Release>1000</Release>
            <randomPitchFactor>0</randomPitchFactor>
            <exclude />
        </instrument>
    </instrumentList>
    <patternList>
        %s
    </patternList>
    <patternSequence>
        %s
    </patternSequence>
    <ladspa>
        <fx>
            <name>no plugin</name>
            <filename>-</filename>
            <enabled>false</enabled>
            <volume>0</volume>
        </fx>
        <fx>
            <name>no plugin</name>
            <filename>-</filename>
            <enabled>false</enabled>
            <volume>0</volume>
        </fx>
        <fx>
            <name>no plugin</name>
            <filename>-</filename>
            <enabled>false</enabled>
            <volume>0</volume>
        </fx>
        <fx>
            <name>no plugin</name>
            <filename>-</filename>
            <enabled>false</enabled>
            <volume>0</volume>
        </fx>
    </ladspa>
</song>'''%(output, patternList)

fileObj = open(sys.argv[2],"w")
fileObj.write(output)
fileObj.close()

print "Done !"

