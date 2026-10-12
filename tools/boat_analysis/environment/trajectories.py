"""Seeded coherent weather histories for sensitivity studies, not forecasts."""
from dataclasses import dataclass
import math

import numpy as np


@dataclass(frozen=True)
class Weather:
    wind_from_deg: float
    wind_mps: float
    current_mps: float
    solar_fraction: float


class WeatherHistory:
    def __init__(self, parameters, hours, seed, stochastic=True, departure_hour=None):
        (direction, speed, current, regime_hours, east_probability, persistence, innovation,
         cloud_min, cloud_nominal, cloud_coefficient, current_coefficient, sunrise, sunset, departure) = parameters
        departure_hour = departure if departure_hour is None else departure_hour
        if not 0 <= sunrise < sunset <= 24 or not 0 <= cloud_min <= cloud_nominal <= 1:
            raise ValueError('Invalid daylight or cloud hypothesis')
        if hours <= 0 or regime_hours <= 0 or not 0 <= east_probability <= 1 or not 0 <= persistence < 1:
            raise ValueError('Invalid weather hypothesis')
        rng = np.random.default_rng(seed)
        self.rows = []
        disturbance = 0.
        for hour in range(math.ceil(hours) + 1):
            if stochastic:
                if hour and rng.random() < 1 - math.exp(-1 / regime_hours):
                    direction = 90. if rng.random() < east_probability else 270.
                disturbance = persistence * disturbance + innovation * rng.normal()
            wind = max(0., speed + disturbance)
            # Common weather state couples stronger disturbances with cloud and
            # discharge sensitivity. Coefficients are illustrative, not fitted.
            cloud = max(cloud_min, min(1., cloud_nominal - cloud_coefficient * abs(disturbance)))
            local_hour = (departure_hour + hour) % 24
            solar = max(0., math.sin(math.pi * (local_hour - sunrise) / (sunset-sunrise))) if sunrise <= local_hour <= sunset else 0.
            self.rows.append(Weather(direction, wind, max(0., current + current_coefficient * disturbance), solar * cloud))

    def at(self, seconds):
        if seconds < 0 or seconds / 3600 > len(self.rows) - 1:
            raise ValueError('Weather requested outside generated history')
        index = min(int(seconds // 3600), len(self.rows) - 1)
        return self.rows[index]
