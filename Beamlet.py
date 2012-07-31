#!/usr/bin/env python
import numpy
import config



##### ##### #####
##### class _Beamlet
##### ##### #####
class _Beamlet(object):
    """class _Beamlet
    The _Beamlet class manages the creation of a beamlet.
    Provided a list of instantiation parameters, the class will generate a
    beamlet. A beamlet corresponds to the smallest observing 'element'
    at a LOFAR station. Each of them represents one subband.
    
    Methods:
        __init__(bid, subband, ra, dec, antennaset="HBA_DUAL", rcumode=5, coordsys="J2000")
    
    Properties:
        antennaset (str): Antenna set selection.
        beamletctl (str): Takes the initialization parameters and returns the
            telescope control sequence string.
        bid (int): Unique beamlet ID. (0...243)
        coordsys (str): Coordinate system.
        dec (float): Declination in radians (or elevation analogue in other
            coordinate system).
        ra (float): Right ascension in radians (or azimuth analogue in other
            coordinate system).
        rcumode (int): Receiver mode selection.
            See Table 7 of Station Data Cookbook.
        subband (int): Subband number. (0...511)

        See LofarCtl.config for the list of possible antennaset, coordsys and
        rcumode.
    """
    def __init__(self, bid, subband, ra, dec, antennaset="HBA_DUAL", rcumode=5, coordsys="J2000"):
        """__init__(bid, subband, ra, dec, antennaset="HBA_DUAL", rcumode=5, coordsys="J2000")

        bid (int): Unique beamlet ID. (0...243)
        subband (int): Subband number. (0...511)
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
        # The list of defined antenna sets
        _antennaset = config.antennaset
        # The list of available rcu modes
        _rcumode = config.rcumode
        # The list of available coordinate systems
        _coordsys = config.coordsys

        self._bid = bid
        self._subband = subband
        self._ra = ra
        self._dec = dec
        # Check that the antenna set is valid
        if antennaset.upper() in _antennaset:
            self._antennaset = antennaset.upper()
        else:
            raise RuntimeError( "The requested antenna set ({0}) does not match any of the available antenna sets.".format(antennaset.upper()) )
        # Check that the receiver mode is valid
        if rcumode in _rcumode:
            self._rcumode = rcumode
        else:
            raise RuntimeError( "The requested rcu mode ({0}) does not match any of the possible rcu modes.".format(rcumode) )
        # Check that the coordinate system is valid
        if coordsys in _coordsys:
            self._coordsys = coordsys
        else:
            raise RuntimeError( "The requested coordinate system ({0}) does not match any of the possible coordinate system.".format(coordsys) )
        # Check that the antenna set and receiver mode are compatible
        if self._antennaset.find('HBA') != -1 and self._rcumode in [5,6,7]:
            pass
        elif  self._antennaset.find('LBA') != -1 and self._rcumode in [3,4]:
            pass
        else:
            raise RuntimeError( "The antenna set ({0}) is not compatible with the receiver mode ({1})".format(self._antennaset, self._rcumode) )

    def __str__(self):
        return self.beamletctl

    @property
    def antennaset(self):
        """antennaset (str): Antenna set selection.
        """
        return self._antennaset

    @property
    def beamletctl(self):
        """beamletctl (str): Takes the initialization parameters and returns the
            telescope control sequence string.
        """
        ctl = "beamctl " + self._Beamlet_options() + " &"
        return ctl

    @property
    def bid(self):
        """bid (int): Unique beamlet ID. (0...243)
        """
        return self._bid

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
    def subband(self):
        """subband (int): Subband number. (0...511)
        """
        return self._subband

    def _Beamlet_options(self):
        """_Beamlet_options()
        Construct the set of optional parameters to a beamlet control
        sequence.
        """
        if isinstance(self._bid, (list, numpy.ndarray, tuple)):
            ctl = "--antennaset={0} --rcus=0:191 --rcumode={1} --subbands={2[0]}:{2[1]} --beamlets={3[0]}:{3[1]} --digdir={4},{5},{6}".format(self._antennaset, self._rcumode, self._subband, self._bid, self._ra, self._dec, self._coordsys)
        else:
            ctl = "--antennaset={0} --rcus=0:191 --rcumode={1} --subbands={2} --beamlets={3} --digdir={4},{5},{6}".format(self._antennaset, self._rcumode, self._subband, self._bid, self._ra, self._dec, self._coordsys)
        return ctl


##### ##### #####
##### class BeamletLBA
##### ##### #####
class BeamletLBA(_Beamlet):
    """class BeamletLBA(_Beamlet)
    The BeamletLBA class is derived from the _Beamlet class.
    The BeamletLBA class manages the creation of an LBA beamlet.
    Provided a list of instantiation parameters, the class will generate a
    beamlet. A beamlet corresponds to the smallest observing 'element'
    at a LOFAR station. Each of them represents one subband.
    
    Methods:
        __init__(bid, subband, ra, dec, antennaset="HBA_DUAL", rcumode=5, coordsys="J2000")
    
    Properties:
        antennaset (str): Antenna set selection.
        beamletctl (str): Takes the initialization parameters and returns the
            telescope control sequence string.
        bid (int): Unique beamlet ID. (0...243)
        coordsys (str): Coordinate system.
        dec (float): Declination in radians (or elevation analogue in other
            coordinate system).
        ra (float): Right ascension in radians (or azimuth analogue in other
            coordinate system).
        rcumode (int): Receiver mode selection.
            See Table 7 of Station Data Cookbook.
        subband (int): Subband number. (0...511)
        
        See LofarCtl.config for the list of possible antennaset, coordsys and
        rcumode.
    """
    def __init__(self, *args, **kwargs):
        """__init__(bid, subband, ra, dec, antennaset="HBA_DUAL", rcumode=5, coordsys="J2000")

        bid (int): Unique beamlet ID. (0...243)
        subband (int): Subband number. (0...511)
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
        _Beamlet.__init__(self, *args, **kwargs)


##### ##### #####
##### class BeamletHBA
##### ##### #####
class BeamletHBA(_Beamlet):
    """class BeamletHBA(_Beamlet)
    The BeamletHBA class is derived from the _Beamlet class.
    The BeamletHBA class manages the creation of an HBA beamlet.
    Provided a list of instantiation parameters, the class will generate a
    beamlet. A beamlet corresponds to the smallest observing 'element'
    at a LOFAR station. Each of them represents one subband.
    
    Methods:
        __init__(anara, anadec, bid, subband, ra, dec, antennaset="HBA_DUAL", rcumode=5, coordsys="J2000")
    
    Properties:
        anadec (float): Declination in radians of the HBA analogue beam
            former (or elevation analogue in other coordinate system).
        anara (float): Right ascension in radians of the HBA analogue beam
            former (or azimuth analogue in other coordinate system).
        antennaset (str): Antenna set selection.
        beamletctl (str): Takes the initialization parameters and returns the
            telescope control sequence string.
        bid (int): Unique beamlet ID. (0...243)
        coordsys (str): Coordinate system.
        dec (float): Declination in radians (or elevation analogue in other
            coordinate system).
        ra (float): Right ascension in radians (or azimuth analogue in other
            coordinate system).
        rcumode (int): Receiver mode selection.
            See Table 7 of Station Data Cookbook.
        subband (int): Subband number. (0...511)

        See LofarCtl.config for the list of possible antennaset, coordsys and
        rcumode.
    """
    def __init__(self, anara, anadec, *args, **kwargs):
        """__init__(anara, anadec, bid, subband, ra, dec, antennaset="HBA_DUAL", rcumode=5, coordsys="J2000")

        anara (float): Right ascension in radians of the HBA analogue beam
            former (or azimuth analogue in other coordinate system).
        anadec (float): Declination in radians of the HBA analogue beam
            former (or elevation analogue in other coordinate system).
        bid (int): Unique beamlet ID. (0...243)
        subband (int): Subband number. (0...511)
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
        _Beamlet.__init__(self, *args, **kwargs)
        self._anara = anara
        self._anadec = anadec

    @property
    def anadec(self):
        """anadec (float): Declination in radians of the HBA analogue beam
            former (or elevation analogue in other coordinate system).
        """
        return self._anadec

    @property
    def anara(self):
        """anara (float): Right ascension in radians of the HBA analogue beam
            former (or azimuth analogue in other coordinate system).
        """
        return self._anara

    def _Beamlet_options(self):
        """_Beamlet_options()
        Construct the set of optional parameters to a beamlet control
        sequence.
        """
        cmd = _Beamlet._Beamlet_options(self) + " --anadir={0},{1},{2}".format(self._anara, self._anadec, self._coordsys)
        return cmd


