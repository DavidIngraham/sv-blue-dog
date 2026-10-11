package MarineCourse {
    private import ScalarValues::*;
    calc def TackAverage {
        in a : Real; in b : Real; in lateralA : Real; in lateralB : Real;
        return vmg : Real;
        (a*RealFunctions::abs(lateralB)+b*RealFunctions::abs(lateralA))/(RealFunctions::abs(lateralA)+RealFunctions::abs(lateralB))
    }
    calc def Route {
        in water : Real [8] ordered nonunique;
        in states : Real [48] ordered nonunique;
        in policy : Real [7] ordered nonunique;
        doc /* Cases ordered by wind 5 then 8 m/s, windward then leeward, tack + then -.
         * Each state contains speed, heading, incidence, leeway, rudder and heel.
         * Tack times cancel crosswind displacement. Equal time fractions per wind
         * and 0.5/1.0 m/s downstream current are illustrative, not weather evidence.
         * policy#7 is 1 for easterly (upstream windward), 0 for westerly. */
        attribute cross0 : Real = states#(1)*TrigFunctions::sin(TrigFunctions::rad(states#(2)+states#(4)));
        attribute cross1 : Real = states#(7)*TrigFunctions::sin(TrigFunctions::rad(states#(8)+states#(10)));
        attribute cross2 : Real = states#(13)*TrigFunctions::sin(TrigFunctions::rad(states#(14)+states#(16)));
        attribute cross3 : Real = states#(19)*TrigFunctions::sin(TrigFunctions::rad(states#(20)+states#(22)));
        attribute cross4 : Real = states#(25)*TrigFunctions::sin(TrigFunctions::rad(states#(26)+states#(28)));
        attribute cross5 : Real = states#(31)*TrigFunctions::sin(TrigFunctions::rad(states#(32)+states#(34)));
        attribute cross6 : Real = states#(37)*TrigFunctions::sin(TrigFunctions::rad(states#(38)+states#(40)));
        attribute cross7 : Real = states#(43)*TrigFunctions::sin(TrigFunctions::rad(states#(44)+states#(46)));
        attribute vmg0 : Real = TackAverage(water#(1),water#(2),cross0,cross1);
        attribute vmg1 : Real = TackAverage(water#(3),water#(4),cross2,cross3);
        attribute vmg2 : Real = TackAverage(water#(5),water#(6),cross4,cross5);
        attribute vmg3 : Real = TackAverage(water#(7),water#(8),cross6,cross7);
        attribute windwardMean : Real = (vmg0+vmg2)/2;
        attribute leewardMean : Real = (vmg1+vmg3)/2;
        attribute downstream : Real = policy#(1)*(if policy#(7)>0.5 ? leewardMean else windwardMean)+(policy#(2)+policy#(3))/2;
        attribute upstream : Real = policy#(1)*(if policy#(7)>0.5 ? windwardMean else leewardMean)-(policy#(2)+policy#(3))/2;
        attribute duration : Real = if downstream>0 and upstream>0 ? policy#(4)/3600*(1/downstream+1/upstream) else 1000000.0;
        return result : Real [6] ordered nonunique;
        (downstream/policy#(6)-1,upstream/policy#(6)-1,1-duration/policy#(5),downstream,upstream,duration)
    }
}
