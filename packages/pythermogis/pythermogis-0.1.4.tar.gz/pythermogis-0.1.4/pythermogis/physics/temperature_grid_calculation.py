def calculate_temperature_from_gradient(depth, thickness, degrees_per_km, surface_temperature):
    return surface_temperature + (depth + thickness / 2) * (degrees_per_km * 0.001)