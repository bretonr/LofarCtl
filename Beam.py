#!/usr/bin/env python
import numpy
from Beamlet import BeamletHBA, BeamletLBA



##### ##### #####
##### class Beam
##### ##### #####
class Beam(object):
    """class Beam
    The Beam class manages the creation of a beam.
    Provided a list of instantiation parameters, the class will generate a
    list of beamlets.
    
    Methods:
        __init__(bids, subbands, ra, dec, antennaset="HBA_JOINED", rcumode=7, coordsys="J2000")
    
    Properties:
        antennaset (str): Antenna set selection.
            {"HBA_JOINED",
            "LBA_INNER"}
        beamctl (str): Telescope control sequence string for each beamlet
            contained in the beam.
        beamlets (list[Beamlet]): List of Beamlet instances.
        bids (list[int]): List of unique beamlet IDs.
        coordsys (str): Coordinate system.
            {"AZELGEO",
            "J2000"}
        dec (float): Declination in radians (or elevation analogue in other
            coordinate system).
        nbeamlets (int): Number of beamlets formed.
        ra (float): Right ascension in radians (or azimuth analogue in other
            coordinate system).
        rcumode (int): Receiver mode selection. (0...7)
            See Table 7 of Station Data Cookbook.
        subbands (list[int]): List of subbands. Each subband forms a beamlet.
    """
    def __init__(self, bids, subbands, ra, dec, antennaset="HBA_JOINED", rcumode=7, coordsys="J2000"):
        """__init__(bids, subbands, ra, dec, antennaset="HBA_JOINED", rcumode=7, coordsys="J2000")
        
        bids (list[int]): List of unique beamlet IDs.
        subbands (list[int]): List of subbands. Each subband forms a beamlet.
        ra (float): Right ascension in radians (or azimuth analogue in other
            coordinate system).
        dec (float): Declination in radians (or elevation analogue in other
            coordinate system).
        antennaset (str): Antenna set selection.
            {"HBA_JOINED",
            "LBA_INNER"}
        rcumode (int): Receiver mode selection. (0...7)
            See Table 7 of Station Data Cookbook.
        coordsys (str): Coordinate system.
            {"AZELGEO",
            "J2000"}
        """
        if numpy.min(subbands) < 0 or numpy.max(subbands) > 511:
            raise RuntimeError( "The subbands do not fit within the allowed range (0-511)" )
        if len(bids) != len(subbands):
            raise RuntimeError( "Number of bids ({}) does not match the number of subbands ({})".format(len(bids), len(subbands)) )
        self._bids = bids
        self._subbands = subbands
        self._nbeamlets = len(self._subbands)
        self._beamlets = []
        self._ra = ra
        self._dec = dec
        self._antennaset = antennaset.upper()
        self._rcumode = rcumode
        self._coordsys = coordsys
        self._lofar_HBA = 1 if self.antennaset.find('HBA') >= 0 else 0
        self._Make_beam()

    def __str__(self):
        return self.beamctl

    @property
    def antennaset(self):
        """antennaset (str): Antenna set selection.
            {"HBA_JOINED",
            "LBA_INNER"}
        """
        return self._antennaset

    @property
    def beamctl(self):
        """beamctl (str): Telescope control sequence string for each beamlet
            contained in the beam.
        """
        return "\n".join( beamlet.beamletctl for beamlet in self.beamlets )

    @property
    def beamlets(self):
        """beamlets (list[Beamlet]): List of Beamlet objects contained in the beam.
        """
        return self._beamlets

    @property
    def bids(self):
        """bids (list[int]): List of unique beamlet IDs.
        """
        return self._bids

    @property
    def coordsys(self):
        """coordsys (str): Coordinate system.
            {"AZELGEO",
            "J2000"}
        """
        return self._coordsys

    @property
    def dec(self):
        """dec (float): Declination in radians (or elevation analogue in other
            coordinate system).
        """
        return self._dec

    @property
    def nbeamlets(self):
        """nbeamlets (int): Number of beamlets formed.
        """
        return self._nbeamlets

    @property
    def ra(self):
        """ra (float): Right ascension in radians (or azimuth analogue in other
            coordinate system).
        """
        return self._ra

    @property
    def rcumode(self):
        """rcumode (int): Receiver mode selection. (0...7)
            See Table 7 of Station Data Cookbook.
        """
        return self._rcumode

    @property
    def subbands(self):
        """subbands (list[int]): List of subbands. Each subband forms a beamlet.
        """
        return self._subbands

    def _Make_beam(self):
        """_Make_beam
        Generate the list of beamlets using the paramters passed at
        initialization.
        """
        for bid, subband in zip(self._bids, self._subbands):
            if self._lofar_HBA == 1:
                self._beamlets.append( BeamletHBA(self.ra, self, dec, bid, subband, self.ra, self.dec, antennaset=self.antennaset, rcumode=self.rcumode, coordsys=self.coordsys) )
            else:
                self._beamlets.append( BeamletLBA(bid, subband, self.ra, self.dec, antennaset=self.antennaset, rcumode=self.rcumode, coordsys=self.coordsys) )


