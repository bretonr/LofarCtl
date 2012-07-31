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
        __init__(bids, subbands, ra, dec, antennaset="HBA_DUAL", rcumode=5, coordsys="J2000")
    
    Properties:
        antennaset (str): Antenna set selection.
        beamctl (str): Telescope control sequence string for each beamlet
            contained in the beam.
        beamlets (list[Beamlet]): List of Beamlet instances.
        bids (list[int]): List of unique beamlet IDs.
        coordsys (str): Coordinate system.
        dec (float): Declination in radians (or elevation analogue in other
            coordinate system).
        nbeamlets (int): Number of beamlets formed.
        ra (float): Right ascension in radians (or azimuth analogue in other
            coordinate system).
        rcumode (int): Receiver mode selection.
            See Table 7 of Station Data Cookbook.
        subbands (list[int]): List of subbands. Each subband forms a beamlet.

        See LofarCtl.config for the list of possible antennaset, coordsys and
        rcumode.
    """
    def __init__(self, bids, subbands, ra, dec, antennaset="HBA_DUAL", rcumode=5, coordsys="J2000"):
        """__init__(bids, subbands, ra, dec, antennaset="HBA_DUAL", rcumode=5, coordsys="J2000")
        
        bids (list[int]): List of unique beamlet IDs.
        subbands (list[int]): List of subbands. Each subband forms a beamlet.
        ra (float): Right ascension in radians (or azimuth analogue in other
            coordinate system).
        dec (float): Declination in radians (or elevation analogue in other
            coordinate system).
        antennaset (str): Antenna set selection.
        rcumode (int): Receiver mode selection.
            See Table 7 of Station Data Cookbook.
        coordsys (str): Coordinate system.

        See LofarCtl.config for the list of possible antennaset, coordsys and
        rcumode.
        """
        if numpy.min(subbands) < 0 or numpy.max(subbands) > 511:
            raise RuntimeError( "The subbands do not fit within the allowed range (0-511)" )
        if len(bids) != len(subbands):
            raise RuntimeError( "Number of bids ({0}) does not match the number of subbands ({1})".format(len(bids), len(subbands)) )
        self._bids = numpy.array(bids)
        self._subbands = numpy.array(subbands)
        self._nbeamlets = len(self._subbands)
        ### Check if the subbands are contiguous. If they are, they will be merged into a single telescope call in order to accelerate the configuration
        self._contiguous = False
        if  self._nbeamlets > 1:
            sep_bids = self._bids[1:] - self._bids[:-1]
            sep_subbands = self._subbands[1:] - self._subbands[:-1]
            if (sep_bids == 1).all() and (sep_subbands == 1).all():
                self._contiguous = True
        self._beamlets = []
        self._ra = ra
        self._dec = dec
        self._antennaset = antennaset.upper()
        self._rcumode = rcumode
        self._coordsys = coordsys
        self._lofar_HBA = 1 if self._antennaset.find('HBA') >= 0 else 1
        self._Make_beam()

    def __str__(self):
        return self.beamctl

    @property
    def antennaset(self):
        """antennaset (str): Antenna set selection.
        """
        return self._antennaset

    @property
    def beamctl(self):
        """beamctl (str): Telescope control sequence string for each beamlet
            contained in the beam.
        """
        return "\n".join( beamlet.beamletctl for beamlet in self._beamlets )

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
        """rcumode (int): Receiver mode selection.
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
        ### In the case of contiguous beamlets we merge them into a single telescope call
        if self._contiguous:
            if self._lofar_HBA == 1:
                self._beamlets.append( BeamletHBA(self._ra, self._dec, self._bids[[0,-1]], self._subbands[[0,-1]], self._ra, self._dec, antennaset=self._antennaset, rcumode=self._rcumode, coordsys=self._coordsys) )
            else:
                self._beamlets.append( BeamletLBA(self._bids[[0,-1]], self._subbands[[0,-1]], self._ra, self._dec, antennaset=self._antennaset, rcumode=self._rcumode, coordsys=self._coordsys) )
        else:
            for bid, subband in zip(self._bids, self._subbands):
                if self._lofar_HBA == 1:
                    self._beamlets.append( BeamletHBA(self._ra, self._dec, bid, subband, self._ra, self._dec, antennaset=self._antennaset, rcumode=self._rcumode, coordsys=self._coordsys) )
                else:
                    self._beamlets.append( BeamletLBA(bid, subband, self._ra, self._dec, antennaset=self._antennaset, rcumode=self._rcumode, coordsys=self._coordsys) )


