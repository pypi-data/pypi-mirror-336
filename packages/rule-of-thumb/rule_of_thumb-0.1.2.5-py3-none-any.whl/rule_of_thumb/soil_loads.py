# soil_loads.py

# Bulk density of different soil types (in kN/m³)
soil_bulk_density = {
    "Chalk": 22,
    "Clay": (16, 22),
    "Clay - stiff": (19, 22),
    "Clay - firm": (17, 20),
    "Clay - soft": (16, 19),
    "Granular - very loose": "<16",
    "Granular - loose": (16, 18),
    "Granular - medium dense": (18, 19),
    "Granular - dense": (19, 21),
    "Granular - very dense": 21,
    "Peat": 11,
    "Silty clay": (16, 20),
    "Sandy clay": (16, 20),
}

def get_soil_density(material: str):
    """Returns the bulk density range for a given soil type."""
    return soil_bulk_density.get(material, "No data available")
