# self_weight.py

self_weight_dict = {
    "Precast concrete solid units (100 mm)": 2.40,
    "Precast concrete hollowcore units (150 mm)": 2.40,
    "Precast concrete hollowcore units (200 mm)": 2.87,
    "Precast concrete hollowcore units (250 mm)": 3.66,
    "Precast concrete hollowcore units (300 mm)": 4.07,
    "Precast concrete hollowcore units (350 mm)": 4.45,
    "Precast concrete hollowcore units (400 mm)": 4.84,
    "Precast concrete hollowcore units (450 mm)": 5.50,
    "Ribbed slab (250 mm)": 4.00,
    "Ribbed slab (275 mm)": 4.20,
    "Ribbed slab (300 mm)": 4.30,
    "Ribbed slab (325 mm)": 4.40,
    "Ribbed slab (350 mm)": 4.70,
    "Ribbed slab (400 mm)": 5.00,
    "Ribbed slab (450 mm)": 5.30,
    "Ribbed slab (500 mm)": 5.70,
    "Waffle slab - standard moulds (325 mm)": 6.00,
    "Waffle slab - standard moulds (350 mm)": 6.40,
    "Waffle slab - standard moulds (425 mm)": 7.30,
    "Waffle slab - standard moulds (475 mm)": 7.70,
    "Waffle slab - standard moulds (525 mm)": 8.60
}

def get_self_weight(material):
    """
    Returns the self-weight of the given concrete floor material.
    
    Parameters:
    material (str): Name of the floor type
    
    Returns:
    float: Self-weight in kN/m² or None if not found
    """
    return self_weight_dict.get(material, None)
