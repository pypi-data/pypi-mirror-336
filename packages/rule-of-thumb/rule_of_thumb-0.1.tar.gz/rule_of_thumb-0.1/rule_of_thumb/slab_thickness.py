# slab_thickness.py

# Recommended slab thickness (in mm) based on span (in meters)
slab_thickness_recommendations = {
    2.0: 100,   # Span 2m -> Thickness 100mm
    3.0: 120,   # Span 3m -> Thickness 120mm
    4.0: 150,   # Span 4m -> Thickness 150mm
    5.0: 180,   # Span 5m -> Thickness 180mm
}

def get_slab_thickness(span: float) -> int:
    """Returns the recommended slab thickness for a given span."""
    return slab_thickness_recommendations.get(span, "No recommendation available")
