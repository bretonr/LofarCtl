#!/usr/bin/env python
import numpy
from astropysics.coords.coordsys import FK5Coordinates
from LofarCtl import Config
import json


##### ##### #####
##### class Receiver
##### ##### #####
class Calibrator(object):
    """class Calibrator
    The Calibrator class manages the list of calibrators.
    
    Methods:
        __init__(fln=None)
        Elevation(observatory, time_up)
        Separation(*args)
    
    Properties:
        names (list[str]): List of calibrator names
        ra (list[float]): List of calibrator right ascenscion (in degrees)
        dec (list[float]): List of calibrator right declination (in degrees)
        source (list[FK5Coordinates]): List of calibrator FK5Coordinates
            objects.
        nsources (int): Number of calibrators.
    """
    def __init__(self, fln=None):
        """__init__(fln=None)
        Initiatilize the calibrator instance.
        
        fln (str): Filename to read the calibrator list from.
            If not specified will use the default configuration file in
            the package directory. Format must be:
             name ra(HH:MM:SS.S) dec(+DD:MM:SS.S)
        """
        # We load the list of calibrators
        if fln is None:
            fln = Config.calib_file
        self.names = []
        self.coords = []
        for name, source in json.load(open(fln)).items():
            self.names.append( name )
            self.coords.append( FK5Coordinates(source["ra"], source["dec"], source["epoch"]) )
        self.nsources = len(self.names)

    def Elevation(self, observatory, time_up):
        """Elevation(observatory, time_up)
        Returns the elevation in degrees of the calibrators at the
        given observatory location.
        
        observatory (Site): An observatory instance (from astropysics.obstools.site)
        time_up (datetime): A datetime.datetime object of the time to compute the
            elevation for.
        """
        elevation = numpy.empty(self.nsources)
        for i,s in enumerate(self.coords):
            apparentCoordinates = observatory.apparentCoordinates(s, time_up)[0]
            elevation[i] = apparentCoordinates.alt.degrees
        return elevation

    def Separation(self, *args):
        """Separation(*args)
        Returns the angular separation in degrees between the calibrators
        and a sky position provided in the arguments.
        
        *args: Sky position. Can be a FK5Coordinates or an input to create
            such an instance.
            * EquatorialCoordinatesBase()
            * EquatorialCoordinatesBase(:class:`EquatorialCoordinatesBase`)
            * EquatorialCoordinatesBase('rastr decstr')
            * EquatorialCoordinatesBase((ra,dec))
            * EquatorialCoordinatesBase(ra,dec)
            * EquatorialCoordinatesBase(ra,fdec,raerr,decerr)
            * EquatorialCoordinatesBase(ra,dec,raerr,decerr,epoch)
            * EquatorialCoordinatesBase(ra,dec,raerr,decerr,epoch,distancepc)
        """
        if isinstance(args[0], FK5Coordinates):
            source = args[0]
        else:
            try:
                source = FK5Coordinates(*args)
            except:
                print( 'Error with the arguments provided, not compatible to create an FK5Coordinates object' )
                return
        distance = numpy.empty(self.nsources)
        for i,s in enumerate(self.coords):
            distance[i] = (s-source).degrees
        return distance        





