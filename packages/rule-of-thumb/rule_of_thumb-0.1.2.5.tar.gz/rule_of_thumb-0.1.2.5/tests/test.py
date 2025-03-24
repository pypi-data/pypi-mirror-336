# test.py

from slab_thickness import get_slab_thickness
from soil_loads import get_soil_density

# Test slab thickness function
span = 3.0
print(f"Recommended slab thickness for {span}m span: {get_slab_thickness(span)} mm")

# Test soil density function
soil_type = "Clay - firm"
print(f"Bulk density for {soil_type}: {get_soil_density(soil_type)} kN/m³")


# main.py

from self_weight import get_self_weight

material_name = "Ribbed slab (350 mm)"
weight = get_self_weight(material_name)

if weight:
    print(f"The self-weight of {material_name} is {weight} kN/m².")
else:
    print(f"Material '{material_name}' not found in the database.")
