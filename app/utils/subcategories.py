from typing import Dict, List

SUBCATEGORIES: Dict[str, List[str]] = {
    "Cleaning": ["standard", "general", "post-renovation", "window washing"],
    "Plumbing": ["installation", "repair", "maintenance", "emergency work"],
    "Electrical": ["installation", "repair", "rewiring", "equipment installation"],
    "Repairs": ["cosmetic", "major", "finishing"]
}

def get_subcategories_for_category(category_name: str) -> List[str]:
    return SUBCATEGORIES.get(category_name, [])