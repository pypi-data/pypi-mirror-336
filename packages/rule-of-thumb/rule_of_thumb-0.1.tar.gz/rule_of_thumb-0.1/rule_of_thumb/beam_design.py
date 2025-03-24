# Define a dictionary with bulk densities of materials
dictionary_test = {
    "Aluminium": 27.2,
    "Asphalt": 22.5,
    "Blocks - aerated concrete (min)": 5.0,
    "Blocks - aerated concrete (max)": 9.0,
   
  
}

# Function to get bulk density of a material
def dsg_transfer_beam(fck,fyk,g_k,q_k,b):
    """
    Returns the bulk density of the given material.
    
    Parameters:
    material (str): Name of the material
    
    Returns:
    float: Bulk density in kN/m³ or None if material is not found
    """
    ultimate_load = 1.4 * g_k + 1.6 * q_k
    d = ultimate_load/(4 * b)   
    # Retrieve the density or return None if material is not found
    return dsg_transfer_beam.get(d, None)

# Example usage of the function
material_name = "Steel"
density = get_bulk_density(material_name)

if density:
    print(f"The bulk density of {material_name} is {density} kN/m³.")
else:
    print(f"Material '{material_name}' not found in the database.")
