#!/usr/bin/env python
import numpy



##### ##### #####
##### class Receiver
##### ##### #####
class Receiver(object):
    """class Receiver
    The Receiver class manages the relationship between subbands and
    frequencies.
    
    Methods:
        __init__(rcumode)
        Check_subband(subband)
        Frequency_from_subband(subband)
        Subband_from_frequency(frequency)
    
    Properties:
        band(list[float]): Receiver band [lower, upper] (MHz).
        passband(list[float]): Passband [lower, upper] (MHz).
        width (float): Subband channel width (MHz).
    """
    def __init__(self, rcumode):
        """__init__()
        
        rcumode (int): Receiver mode.
            {0, 1, 2, 3, 4, 5, 6, 7}
        """
        # We select the right clock sampling frequency depending on the rcumode
        if rcumode == 6:
            clock = 160.
        else:
            clock = 200.
        # Calculating the subband channel width
        self._width = clock/1024
        # Determining the receiver band
        if rcumode == 0:
            self._band = [0.,0.]
            self._passband = [0.,0.]
            self._direction = 1
        elif rcumode == 1:
            self._band = [0.,100.]
            self._passband = [10.,90.]
            self._direction = 1
        elif rcumode == 2:
            self._band = [0.,100.]
            self._passband = [30.,80.]
            self._direction = 1
        elif rcumode == 3:
            self._band = [0.,100.]
            self._passband = [10.,80.]
            self._direction = 1
        elif rcumode == 4:
            self._band = [0.,100.]
            self._passband = [30.,80.]
            self._direction = 1
        elif rcumode == 5:
            #self._band = [200.,100.]
            self._band = [100.,200.]
            self._passband = [110.,190.]
            #self._direction = -1
            self._direction = 1
        elif rcumode == 6:
            self._band = [160.,240.]
            self._passband = [170.,230.]
            self._direction = 1
        elif rcumode == 7:
            self._band = [200.,300.]
            self._passband = [210.,270.]
            self._direction = 1
        else:
            raise RuntimeError( "The selected rcumode is invalid." )

    @property
    def band(self):
        """band(list[float]): Receiver band [lower, upper] (MHz).
        """
        return self._band

    @property
    def passband(self):
        """passband(list[float]): Passband [lower, upper] (MHz).
        """
        return self._passband

    @property
    def width(self):
        """width(float): Subband channel width (MHz).
        """
        return self._width

    def Check_frequency(self, frequency):
        """Check_frequency(frequency)
        Verifies that the frequency falls within the passband.
        Returns True if it does, otherwise False.
        
        frequency (float, array): frequency to check.
        """
        if numpy.any(numpy.array(frequency) < self._passband[0]):
            print( 'Warning: frequency falling below the lower limit of the passband.' )
            return False
        elif numpy.any(numpy.array(frequency) > self._passband[1]):
            print( 'Warning: frequency falling above the upper limit of the passband.' )
            return False
        else:
            return True

    def Check_subband(self, subband):
        """Check_subband(subband)
        Verifies that the subband falls within the passband.
        Returns True if it does, otherwise False.
        
        subband (int, array): subband to check.
        """
        return_val = True
        frequency = self.Frequency_from_subband(subband)
        if numpy.any(frequency < self._passband[0]):
            print( 'Warning: frequency ({0}) falling below the lower limit ({1}) of the passband.'.format(frequency.min(), self._passband[0]) )
            return_val = False
        if numpy.any(frequency > self._passband[1]):
            print( 'Warning: frequency ({0}) falling above the upper limit ({1}) of the passband.'.format(frequency.max(), self._passband[1]) )
            return_val = False
        return return_val

    def Frequency_from_subband(self, subband):
        """Frequency_from_subband(subband)
        Returns the frequency associated to the subband.
        
        subband (float, array): subband number (0-511).
            Values outside (0-511) are clipped to that range.
        """
        return numpy.array(subband).clip(0, 511)*self._width*self._direction + self._band[0]

    def Subband_from_frequency(self, frequency):
        """Subband_from_frequency(frequency)
        Returns the nearest subband index corresponding to the
        frequency.
        
        frequency (float, array): frequency
            Values outside the receiver band range are clipped to the
            range.
        """
        return numpy.round(self._direction*(frequency - self._band[0])/self._width).astype(int).clip(0, 511)


