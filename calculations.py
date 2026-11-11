"""Configurable, prototype-level carbon emission calculations."""
import json
from pathlib import Path

FACTORS_FILE = Path(__file__).parent / "data" / "emission_factors.json"

def get_factors():
    with FACTORS_FILE.open(encoding="utf-8") as file:
        return json.load(file)
    
def calculate_electricity_emission(kwh, factors):
    return round(kwh * factors["electricity"]["kg_co2e_per_kwh"], 2)

def calculate_transport_emission(entries, factors):
    calculated = []
    total = 0.0
    for entry in entries:
        kind, distance = entry["transport_type"], entry["distance_km"]
        factor = factors["transport"][kind]["kg_co2e_per_km"]
        emission = round(distance * factor, 2)
        calculated.append({**entry, "emission": emission, "factor": factor})
        total += emission
    return round(total, 2), calculated

def calculate_waste_emission(waste_kg, factors):
    return round(waste_kg * factors["waste"]["kg_co2e_per_kg"], 2)

def calculate_total_emission(electricity, transport, waste):
    return round(electricity + transport + waste, 2)

def calculate_assessment(electricity_kwh, entries, waste_kg):
    factors = get_factors()
    electricity = calculate_electricity_emission(electricity_kwh, factors)
    transport, calculated_entries = calculate_transport_emission(entries, factors)
    waste = calculate_waste_emission(waste_kg, factors)
    total = calculate_total_emission(electricity, transport, waste)
    return {"electricity_emission": electricity, "transport_emission": transport,
            "waste_emission": waste, "total_emission": total,
            "transport_entries": calculated_entries, "factors": factors}

def insight_for(results):
    categories = {"Electricity": results["electricity_emission"], "Transportation": results["transport_emission"], "Waste": results["waste_emission"]}
    highest = max(categories, key=categories.get)
    suggestions = {
        "Electricity": "Consider reducing unnecessary electricity use and choosing efficient appliances where practical.",
        "Transportation": "Consider public transport, walking, cycling, or combining trips where practical.",
        "Waste": "Consider reducing waste generation and increasing recycling where appropriate."
    }
    return highest, suggestions[highest]
