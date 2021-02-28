#!/usr/bin/env python3

#------------------------------------------------------------------------
# SignalFlow: Euclidean rhythm example, using a global pulse
# and ClockDivider to drive a series of rhythm generators.
# Impulses are passed through resonant filters of different freqencies.
#------------------------------------------------------------------------
from signalflow import *
import random

graph = AudioGraph(start=True)

#------------------------------------------------------------------------
# Subclass Patch to create a re-usable subgraph.
# Notes:
#  - __init__() must always be called from Patch subclass constructors
#  - add_input is not required in this case, but it's good practice
#    as it is needed when serialising Patch json to provide info on
#    which component nodes should be labelled as named inputs.
#  - set_output must be called finally to label the Patch's output node
#------------------------------------------------------------------------
class EuclideanPatch (Patch):
    def __init__(self, clock, divider=1, sequence_length=24, num_events=8, cutoff=8000, resonance=0.99, pan=0.0, amp=0.5):
        super().__init__()
        self.clock = clock
        self.cutoff = self.add_input("cutoff", cutoff)
        self.resonance = self.add_input("resonance", resonance)
        self.divider = self.add_input("divider", divider)
        self.sequence_length = self.add_input("sequence_length", sequence_length)
        self.num_events = self.add_input("num_events", num_events)
        self.amp = self.add_input("amp", amp)
        self.pan = self.add_input("pan", pan)
        self.eu = Euclidean(ClockDivider(self.clock, self.divider), self.sequence_length, self.num_events)
        self.flt = SVFFilter(self.eu, "low_pass", cutoff=self.cutoff, resonance=self.resonance)
        self.panned = LinearPanner(2, self.flt * self.amp, self.pan)
        self.set_output(self.panned)

clock = Impulse(8)

#--------------------------------------------------------------------------------
# Create four parallel Euclidean rhythm lines with different parameters.
#--------------------------------------------------------------------------------
a = EuclideanPatch(clock, 2, 23, 7, 80, 0.99, 0.0, 10.0)
b = EuclideanPatch(clock, 3, 13, 9, 800, 0.98, 0.7, 0.2)
c = EuclideanPatch(clock, 4, 16, 11, 8000, 0.97, -0.7, 0.1)
d = EuclideanPatch(clock, 2, 19, 12, 480, 0.99, 0.0, 0.2)

#--------------------------------------------------------------------------------
# Sum the rhythm lines, boost and pass through a tanh soft clipper.
#--------------------------------------------------------------------------------
mix = a + b + c + d
mix = Tanh(mix * 10)

#--------------------------------------------------------------------------------
# Add ping-pong delay: two all-pass delay lines, the right delayed by 1/16s.
#--------------------------------------------------------------------------------
delay_l = AllpassDelay(ChannelMixer(1, mix), delaytime=1/8, feedback=0.7)
delay_r = OneTapDelay(AllpassDelay(ChannelMixer(1, mix), delaytime=1/8, feedback=0.7), delaytime=1/16)

#--------------------------------------------------------------------------------
# Mix the wet/dry signals and play the output.
#--------------------------------------------------------------------------------
wetdry = WetDry(mix, [ delay_l, delay_r ], 0.25)
wetdry.play()

graph.wait()
