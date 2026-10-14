package Thermal {
    private import ScalarValues::*;
    // SI magnitudes: current A, resistance ohm, power W.
    calc def JouleHeat {
        in current : Real;
        in resistance : Real default 10;
        return power : Real = current * current * resistance;
    }
    calc def ValidResistance {
        in resistance : Real;
        return positiveResistance : Real = if resistance>0 ? 1.0 else 0.0;
    }
}
