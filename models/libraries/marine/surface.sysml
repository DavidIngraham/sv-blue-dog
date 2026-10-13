package MarineSurface {
    private import ScalarValues::*;
    doc /* SI magnitudes. Neutral log profile and strip quadrature are a first
     * surface-layer screen, not a stability-corrected wave boundary-layer model.
     * Wave resistance is an explicitly uncalibrated sensitivity coefficient.
     * Deep-water wave/current action transport assumes slow spatial variation;
     * a uniform river current is not itself a shoaling transition. */
    calc def WindSample {
        in x : Real [9] ordered nonunique;
        // reference wind, reference height, roughness, sample height, heading,
        // vessel speed, leeway (radians), shear enabled, minimum valid height.
        attribute height : Real = NumericalFunctions::max(x#(4),x#(9));
        attribute ratio : Real = if x#(8)>0.5 ? OpenSysMLMathFunctions::ln(height/x#(3))/OpenSysMLMathFunctions::ln(x#(2)/x#(3)) else 1;
        attribute ax : Real = x#(1)*ratio*TrigFunctions::cos(x#(5))+x#(6)*TrigFunctions::cos(x#(7));
        attribute ay : Real = x#(1)*ratio*TrigFunctions::sin(x#(5))-x#(6)*TrigFunctions::sin(x#(7));
        return result : Real [5] ordered nonunique;
        (ratio,ax,ay,RealFunctions::sqrt(ax*ax+ay*ay),x#(4)/x#(9)-1)
    }
    calc def StripLoad {
        in x : Real [10] ordered nonunique;
        // rho, strip area, apparent x/y, heel rad, height above mean water,
        // CL, CD, chord, signed mast moment coefficient.
        attribute va : Real = RealFunctions::sqrt(x#(3)*x#(3)+x#(4)*x#(4));
        attribute pressureArea : Real = 0.5*x#(1)*va*va*x#(2);
        attribute xs : Real = pressureArea*(x#(7)*TrigFunctions::cos(x#(5))*x#(4)-x#(8)*x#(3))/va;
        attribute ys : Real = pressureArea*(x#(7)*TrigFunctions::cos(x#(5))*x#(3)+x#(8)*x#(4))/va;
        return result : Real [4] ordered nonunique;
        (xs,ys,ys*x#(6),pressureArea*x#(9)*x#(10))
    }
    calc def FetchSea {
        in x : Real [3] ordered nonunique;
        // reference 10 m wind, effective fetch, gravity; SMB deep-water growth.
        attribute wind : Real = NumericalFunctions::max(x#(1),0.1);
        attribute fetch : Real = x#(3)*x#(2)/(wind*wind);
        attribute hArg : Real = 0.0125*OpenSysMLMathFunctions::exp(0.42*OpenSysMLMathFunctions::ln(fetch));
        attribute tArg : Real = 0.077*OpenSysMLMathFunctions::exp(0.25*OpenSysMLMathFunctions::ln(fetch));
        attribute hTanh : Real = (1-OpenSysMLMathFunctions::exp(-2*hArg))/(1+OpenSysMLMathFunctions::exp(-2*hArg));
        attribute tTanh : Real = (1-OpenSysMLMathFunctions::exp(-2*tArg))/(1+OpenSysMLMathFunctions::exp(-2*tArg));
        return result : Real [2] ordered nonunique;
        (if x#(1)>0 ? 0.283*wind*wind/x#(3)*hTanh else 0, NumericalFunctions::max(1,2*TrigFunctions::pi*1.2*wind/x#(3)*tTanh))
    }
    calc def SpeedRetention {
        in x : Real [2] ordered nonunique;
        // Added resistance and calm-water resistance at the solved state.
        // Local R ~ V^2 and unchanged available thrust: sensitivity, not a VPP.
        return ratio : Real [1] ordered nonunique;
        (RealFunctions::sqrt(NumericalFunctions::max(0,1-x#(1)/x#(2))))
    }
    calc def WaveScreen {
        in x : Real [13] ordered nonunique;
        // incident Hs, absolute period, current along propagation, L, B,
        // water-relative speed, cos(wave-to minus heading), resistance coeff,
        // freeboard, wing-root height, appendage-tip immersion, g, rho.
        attribute omega : Real = 2*TrigFunctions::pi/x#(2);
        attribute discriminant : Real = x#(12)+4*x#(3)*omega;
        attribute root : Real = RealFunctions::sqrt(NumericalFunctions::max(discriminant,0.000001));
        attribute sqrtK : Real = 2*omega/(root+RealFunctions::sqrt(x#(12)));
        attribute k : Real = sqrtK*sqrtK;
        attribute sigma : Real = RealFunctions::sqrt(x#(12)*k);
        attribute groupSpeed : Real = 0.5*RealFunctions::sqrt(x#(12)/k);
        attribute absoluteGroup : Real = groupSpeed+x#(3);
        attribute incidentGroup : Real = x#(12)/(2*omega);
        attribute height : Real = x#(1)*RealFunctions::sqrt(sigma*incidentGroup/(omega*NumericalFunctions::max(absoluteGroup,0.000001)));
        attribute wavelength : Real = 2*TrigFunctions::pi/k;
        attribute encounter : Real = RealFunctions::abs(sigma-k*x#(6)*x#(7));
        attribute coupling : Real = NumericalFunctions::min(1,k*k*x#(4)*x#(4));
        attribute resistance : Real = x#(8)*x#(13)*x#(12)*x#(5)*height*height/16*coupling*(0.25+0.375*(1-x#(7)));
        return result : Real [9] ordered nonunique;
        (height,wavelength,encounter,resistance,discriminant/x#(12),0.1-height/wavelength,x#(9)-height,x#(10)-height,x#(11)-height)
    }
}
