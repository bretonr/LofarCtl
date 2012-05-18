#!/usr/bin/env python
import numpy
from Beam import Beam
from Receiver import Receiver



##### ##### #####
##### class Observation
##### ##### #####
class Observation(object):
    """class Observation
    The Observation class manages and generates an observation sequence sequence.
    Once instantiated with the basic parameters, one can add beams. Then, the
    observation sequence (a string of command sequences) can be returned.
    
    Methods:
        __init__(antennaset, rcumode)
        Add_beam(subbands, ra, dec, coordsys='J2000', inradians=True)
        Add_beam(frequency, nsubbands, ra, dec, coordsys='J2000',
            inradians=True, position='center')
    
    Properties:
        antennaset (str): Antenna set selection.
            {"HBA_JOINED",
            "LBA_INNER"}
        beams (list[Beam]): List of Beam instances.
        nbeams (int): Number of beams formed.
        nbeamlets (int): Number of beamlets formed.
        obsctl (str): Telescope control sequence string for each beam
            contained in the observation.
        rcumode (int): Receiver mode selection. (0...7)
            See Table 7 of Station Data Cookbook.
    """
    def __init__(self, antennaset="HBA_JOINED", rcumode=7):
        """__init__(antennaset="HBA_JOINED", rcumode=7)
        
        antennaset (str): Antenna set selection.
            {"HBA_JOINED",
            "LBA_INNER"}
        rcumode (int): Receiver mode selection. (0...7)
            See Table 7 of Station Data Cookbook.
        """
        self._antennaset = antennaset
        self._rcumode = rcumode
        self._max_beamlets = 244
        self._nbeamlets = 0
        self._nbeams = 0
        self._bids = []
        self._beams = []
        self.Receiver = Receiver(rcumode)
        self.Beam = Beam

    def __str__(self):
        return self.obsctl

    @property
    def antennaset(self):
        """antennaset(str): Antenna set selection.
            {"HBA_JOINED",
            "LBA_INNER"}
        """
        return self._antennaset

    @property
    def beams(self):
        """beams (list[Beam]): List of Beams objects contained in the observation.
        """
        return self._beams

    @property
    def obsctl(self):
        """obsctl (str): Telescope control sequence string for each beamlet
            contained in the beam.
        """
        return "\n".join( beam.beamctl for beam in self.beams )

    @property
    def nbeams(self):
        """nbeams (int): Number of beams formed.
        """
        return self._nbeams

    @property
    def nbeamlets(self):
        """nbeamlets (int): Number of beamlets formed.
        """
        return self._nbeamlets

    @property
    def rcumode(self):
        """rcumode (int): Receiver mode selection. (0...7)
            See Table 7 of Station Data Cookbook.
        """
        return self._rcumode

    def Add_beam(self, subbands, ra, dec, coordsys='J2000', inradians=True):
        """Add_beam(subbands, ra, dec, coordsys='J2000', inradians=True)
        Adds another beam to the current list of beams using a list of subbands.
        
        subbands (list[int]): List of subbands to add to the beam.
        ra (float): RA of the beam center.
        dec (float): Dec of the beam center.
        coordsys (str): Coordinate system to use. If not J2000, the
            ra and dec parameters are their equivalent in the other system.
            {"AZELGEO", "J2000"}
        inradiands (bool): If True, the coordinates are in radians. If False,
            degrees are assumed.
        """
        # Making sure subbands is array type
        subbands = numpy.atleast_1d(subbands)
        # Check that the subbands fall within the passband
        valid_passband = self.Receiver.Check_subband(subbands)
        # Converting ra/dec to radians if needed
        if not inradians:
            ra = ra*numpy.pi/180
            dec = dec*numpy.pi/180
        # Getting a list of unique beamlet IDs for the requested subbands
        try:
            bids = self._Bid_manager(subbands.size)
        except RuntimeError as inst:
            print( inst )
            print( 'The beam could not be added.' )
            return
        # Creating the new beam
        try:
            self._beams.append( Beam(bids, subbands, ra, dec, antennaset=self.antennaset, rcumode=self.rcumode, coordsys=coordsys) )
            # Updating the count of beams and beamlets
            self._nbeamlets = self._bids.size
            self._nbeams += 1
        except Exception as inst:
            print( inst )
            print( "A problem occured while adding the beam. No beam added." )
        return

    def Add_beam_frequency(self, frequency, nsubbands, ra, dec, coordsys='J2000', inradians=True, position='center'):
        """Add_beam(frequency, nsubbands, ra, dec, coordsys='J2000', inradians=True, position='center')
        Adds another beam to the current list of beams using a specified
        frequency and a number of subbands.
        
        frequency (float): Reference frequency for the creation of the beam.
        nsubbands (int): Number of subbands to create in the beam.
        ra (float): RA of the beam center.
        dec (float): Dec of the beam center.
        coordsys (str): Coordinate system to use. If not J2000, the
            ra and dec parameters are their equivalent in the other system.
            {"AZELGEO", "J2000"}
        inradiands (bool): If True, the coordinates are in radians. If False,
            degrees are assumed.
        position (str): Position of the specified frequency in the list of
            subbands. 'center' implies that the reference frequency is at
            the center of the list of subbands. In the case of an even
            nsubbands, there will be one more subbands below than above
            the reference frequency.
            Note that if the upper or lower end of the subbands falls of the
            range of allowed subbands, the subbands will automatically be
            shifted to fit in.
            {'center', 'lower', 'upper'}
        """
        # Determining the subband that is closest to the selected frequency
        subband0 = self.Receiver.Subband(frequency)
        if position.lower() == 'lower':
            subbands = numpy.arange(subband0, subband0+nsubbands)
        elif position.upper() == 'upper':
            subbands = numpy.arange(subband0-nsubbands+1, subband0+1)
        else:
            half = int(nsubbands)/2
            plusone = int(nsubbands%2)
            subbands = numpy.arange(subband0-half, subband0+half+plusone)
        # Safe testing the subbands to make sure that they fit within the allowed range
        sub_min = subbands.min()
        sub_max = subbands.max()
        if sub_min < 0:
            subbands -= sub_min
        elif sub_max > 511:
            subbands -= sub_max-511
        # Now that we have a list of subbands we can generate the beam
        self.Add_beam(subbands, ra, dec, coordsys=coordsys, inradians=inradians)
        return

    def _Bid_manager(self, nbids):
        """_Bid_manager(nbids)
        Verifies that the proposed beam to be added respects the basic
        constraints imposed by the telescope. Returns a list of beamlet IDs.
        
        nbids (int): number of requested beam IDs.
        
        Note:
            The total number of beamlets must be less than the maximum number
            of beamlets, which is currently 244.        
        """
        # Retrieving a list of unique integers between 0 and self._max_beamlets-1
        new_bids = numpy.lib.arraysetops.setdiff1d(numpy.arange(self._max_beamlets),  self._bids, assume_unique=True)[:nbids]
        if new_bids.size != nbids:
            print( new_bids )
            raise RuntimeError( 'The total number of beamlets requested exceeds the maximum number permitted ({}).'.format(self._max_beamlets) )
        self._bids = numpy.r_[self._bids, new_bids]
        return new_bids

