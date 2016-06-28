import numpy as np
import scipy
import logging
logger = logging.getLogger(name=__name__)


def getmodel(modeltype):
    try:
        return globals()[modeltype]
    except KeyError:
        # try to find a similar model with lowercase spelling
        for k in globals():
            if k.lower() == modeltype.lower():
                return globals()[k]
        logger.error("Model %s not found in model definition file %s",
                     modeltype, __file__)


class Model(object):
    " generic model object that will make smart use of its inputs and outputs"
    export_to_parent = []

    state = {'theoretical': {},
             'experimental': {},
             'set': {}}

    def __init__(self, parent=None):
        self.logger = logging.getLogger(__name__)
        if parent is None:
            self._parent = self
        else:
            self._parent = parent
        self.inputs = self._parent.inputs
        self.outputs = self._parent.outputs
        self._config = self._parent.c.model
        self._make_slopes()

    def setup(self):
        pass

    def search(self, *args, **kwargs):
        pass

    def lock(self, *args, **kwargs):
        pass

    def _derivative(self, func, x, n=1, args=()):
        return scipy.misc.derivative(func,
                                     x,
                                     dx=1e-9,
                                     n=n,
                                     args=args,
                                     order=3)

    def _make_slopes(self):
        for inp in self.inputs:
            # test if the slope was defined in the model
            if not hasattr(self, inp._name+"_slope"):
                fn = self.__getattribute__(inp._name)
                def fn_slope(x, *args):
                    return self._derivative(fn, x, args=args)
                self.__setattr__(inp._name+"_slope", fn_slope)

class Interferometer(Model):
    """ simplest type of optical interferometer with one photodiode """

    # declare here the public functions that are exported to the Pyrpl class
    export_to_parent = ['lock', 'unlock', 'islocked', 'calibrate', 'sweep']

    # theoretical model for input signal 'port1'
    def port1(self, phase):
        """ photocurrent at port1 of an ideal interferometer vs phase (rad)"""
        amplitude = (self._parent.port1._config.max
                     - self._parent.port1._config.min) / 2
        return np.sin(phase) * amplitude

    @property
    def phase_per_m(self):
        return 2*np.pi/self._config.wavelength

    # lock algorithm
    def lock(self, phase=0, factor=1.0):
        """
        Locks the interferometer
        Parameters
        ----------
        phase: float
            phase (rad) of the quadrature to be locked at
        factor: float
            optional gain multiplier for debugging

        Returns
        -------
        True if locked successfully, else false
        """
        input = self._parent.port1
        for o in self.outputs:
            # trivial to lock: just enable all gains
            unit = o._config.calibrationunits.split("_per_V")[0]
            phase_per_unit = self.__getattribute__("phase_per_"+unit)
            o.lock(slope=self.port1_slope(phase)*phase_per_unit,
                   setpoint=self.port1(phase),
                   input=input._config.redpitaya_input,
                   offset=0,
                   factor=factor)

    # unlock algorithm
    def unlock(self):
        for o in self.outputs:
            o.off()

    # verification whether the system is locked
    @property
    def islocked(self):
        return True

    def sweep(self):
        """
        Enables the pre-configured sweep on all outputs.

        Returns
        -------
        duration: float
            The duration of one sweep period, as it is useful to setup the
            scope.
        """
        frequency = None
        for o in self.outputs:
            frequency = o.sweep()
        return 1.0/frequency

    def calibrate(self):
        self.unlock()
        duration = self.sweep()
        curves = []
        for inp in self.inputs:
            try:
                inp._config._data["trigger_source"] = "asg1"
                inp._config._data["duration"] = duration
                inp._acquire()
                # when signal: autosave is enabled, each calibration will
                # automatically save a curve
                if inp._config.autosave:
                    curve, ma, mi = inp.curve, inp.max, inp.min
                    curves.append(curve)
                else:
                    ma, mi = inp.max, inp.min
            finally:
                # make sure to reload config file here so that the modified
                # scope parameters are not written to config file
                self._parent.c._load()
            inp._config["max"] = ma
            inp._config["min"] = mi
        # turn off sweeps
        self.unlock()
        self._parent._setupscope()
        return curves

class FabryPerot(Model):
    def _lorentz(self, x):
        return 1.0/(1.0 + x**2)

    #def transmission(self, x):
    #    " relative transmission. Max transmission will be calibrated as peak"
    #    return self._lorentz(x/self.bandwidth)

    def FWHM(self):
        return self._config.linewidth / 2

    def reflection(self, x):
        " relative reflection"
        return 1.0 - (1.0-self._config.R0)*self._lorentz(x/self.FWHM)



    def reflection_slope(self):
        pass