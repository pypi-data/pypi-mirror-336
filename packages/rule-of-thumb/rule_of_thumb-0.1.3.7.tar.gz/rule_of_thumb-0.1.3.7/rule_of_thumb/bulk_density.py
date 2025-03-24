# Define a dictionary with bulk densities of materials
bulk_density_dict = {
    "Aluminium": 27.2,
    "Asphalt": 22.5,
    "Blocks - aerated concrete (min)": 5.0,
    "Blocks - aerated concrete (max)": 9.0,
    "Blocks - dense aggregate": 20.0,
    "Blocks - lightweight": 14.0,
    "Blocks - bulk storage": 8.0,
    "Books on shelves": 7.0,
    "Brass - cast": 85.0,
    "Brickwork - blue": 24.0,
    "Brickwork - engineering": 22.0,
    "Brickwork - fletton": 18.0,
    "Brickwork - London stock": 19.0,
    "Brickwork - sand lime": 21.0,
    "Bronze - cast": 83.0,
    "Chipboard": 6.9,
    "Coal": 9.0,
    "Concrete - aerated": 10.0,
    "Concrete - lightweight": 18.0,
    "Concrete - normal": 24.0,
    "Copper": 87.0,
    "Glass": 25.6,
    "Gold": 194.0,
    "Granite": 27.3,
    "Hardcore": 19.0,
    "Iron": 77.0,
    "Lead": 111.1,
    "Limestone (Bathstone - lightweight)": 20.4,
    "Limestone (Portland stone - med weight)": 22.0,
    "Limestone (marble - heavyweight)": 26.7,
    "Macadam paving": 21.0,
    "MDF": 8.0,
    "Plaster": 14.1,
    "Plywood": 6.3,
    "Sandstone": 23.5,
    "Screed - sand/cement": 22.0,
    "Steel": 77.0,
    "Terracotta": 20.7,
    "Timber - Douglas fir": 5.2,
    "Timber - European beech/oak": 7.1,
    "Timber - Grade C16": 3.6,
    "Timber - Grade C24": 4.1,
    "Timber - Iroko/teak": 6.4
}

# Function to get bulk density of a material
def get_bulk_density(material):
    """
    Returns the bulk density of the given material.
    
    Parameters:
    material (str): Name of the material
    
    Returns:
    float: Bulk density in kN/m³ or None if material is not found
    """
    # Convert input to title case to match keys in the dictionary
    material = material.title()
    
    # Retrieve the density or return None if material is not found
    return bulk_density_dict.get(material, None)

# Example usage of the function
material_name = "Steel"
density = get_bulk_density(material_name)

if density:
    print(f"The bulk density of {material_name} is {density} kN/m³.")
else:
    print(f"Material '{material_name}' not found in the database.")
