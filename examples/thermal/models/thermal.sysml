package Thermal {
    private import ScalarValues::*;
    calc def JouleHeat {
        in current : Real;
        in resistance : Real default 10;
        return power : Real = current * current * resistance;
    }
}
