#!/usr/bin/env python
import numpy
import os
import LofarCtl

##### ##### #####
##### This script will trigger the LOFAR Chilbolton station upon receiver a Swift alert that meets
##### some basic criteria.
##### ##### #####


##### ####
##### Defining the observational parameters
obsfreq = 55.
antennaset = "LBA_INNER"
rcumode = 4



##### #####
##### In principle we would get coordinates from the VOEvent handler
## Using rubbish for now
ra = 45.
dec = 60.



##### #####
##### Setting up the station control script

### Creating the Obs instance
obs = LofarCtl.Observation.Observation(antennaset=antennaset, rcumode=rcumode)

### Beam setup
nsubs = 244
nrefs = 3
nsubs_primary = nsubs - nrefs*3

### Creating the science beams
obs.Add_beam_frequency(obsfreq,  nsubs_primary, ra, dec, coordsys='J2000', inradians=False, position='center')

### Gathering info about the science beam subbands
lowsub = obs.beams[0].subbands[0]
midsub = obs.beams[0].subbands[obs.beams[0].subbands.size/2]
highsub = obs.beams[0].subbands[-1]

### Determining the reference beam pointing directions
## Using rubbish for now
ra_ref = [0., 120., 240.]
dec_ref = [70., 70., 70.]
for i in xrange(nrefs):
    obs.Add_beam([lowsub,midsub,highsub], ra_ref[i], dec_ref[i], coordsys='AZELGEO', inradians=False)



##### #####
##### Dumping the information into a file
fout = open('fire_chilbolton.sh', 'w')
fout.write( obs.obsctl )
fout.close()



##### #####
##### Firing Chilbolton: scp the script and running it
print( "scp fire_chilbolton.sh lofar_soton@chilbolton.ac.uk:." )
print( "ssh lofar_soton@chilbolton.ac.uk sh fire_chilbolton.sh" )



##### #####
##### Cleaning things up
os.remove('fire_chilbolton.sh')


