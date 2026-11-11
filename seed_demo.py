"""Optional demo data generator. Normal app startup never invokes this file."""
from database import init_db, save_assessment
from calculations import calculate_assessment

init_db()
for electricity, trips, waste in [(210,[{"transport_type":"petrol_car","distance_km":420}],28),(180,[{"transport_type":"train","distance_km":180},{"transport_type":"bus","distance_km":90}],22)]:
    results=calculate_assessment(electricity,trips,waste)
    save_assessment({"electricity_kwh":electricity,"waste_kg":waste,"entries":trips},results)
print("Created clearly labeled prototype demo assessments.")
