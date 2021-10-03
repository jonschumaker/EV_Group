import numpy as np

def powerconsumption(Avg_slope = 0, Mass = 1250, fr = 0.011, Time = 1, Distance = 100):
    # Avg_slop (unitless), Mass (Kg), fr is rolling resistance coefficient (unitless), Time (hours), Distance (km)
    # Equations are taken from Battery consumption article page 1533
    # Calling the function with Avg_slope = 0 gives the baseline power consumed for the distance for these equations, not the total power consumed
    # From the paper a journey of 100km at 100km/hr consumes ~ 14kWh, of that ~ 3.83 kWh are from these equations. According to the paper, model is within 5% of actual
    # For reference Tesla models vary between 14.9-23.6 kWh / 100km, with masses between 1733-2668kg https://www.tesla.com/en_EU/support/european-union-energy-label
    # Stuff this function doesn't account for is drag, accleration, power train efficency loss, aux power like AC, radio, on-board computers
    g = 9.81 #(m/s^2)
    kph = Distance / Time
    mps = kph / 3.6
    F_r = fr * Mass * g * np.cos(Avg_slope) # Equation (3), rolling resistance force aka friction with the road
    F_g = Mass * g * np.sin(Avg_slope) # Equation (5), road slope force aka force from traveling up and down hill
    P_bat = (F_r + F_g) * Time * mps / 1000 #/1000 to get kilo watts instead of watts
    return P_bat # Power the battery provides for slope related activites(kWh)

def powerdifference(Avg_slope = 0, Mass = 1250, fr = 0.011, Time = 1, Distance = 100):
    baseline = powerconsumption(Mass = Mass, fr = fr, Time = Time, Distance = Distance)
    experiment = powerconsumption(Mass = Mass, fr = fr, Time = Time, Distance = Distance, Avg_slope = Avg_slope)
    return experiment - baseline
