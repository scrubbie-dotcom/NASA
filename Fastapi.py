from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware  # CORS Middleware for cross-origin requests
from pymongo import MongoClient
from bson.objectid import ObjectId
from pydantic import BaseModel
from typing import List, Optional

# Initialize FastAPI application
app = FastAPI()

# Configure CORS to allow requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

# Connect to your Remote MongoDB database
client = MongoClient("mongodb://username:password@192.168.1.100:27017/space_pod_db")
db = client["space_pod_db"]  # Replace with your database name
collection = db["planets"]   # Replace with your collection name

# Define Pydantic model for structured responses
class Planet(BaseModel):
    _id: str
    Planet_Name: str
    Type: Optional[str]
    Distance_from_Sun_AU: Optional[float]
    Diameter_km: Optional[float]
    Rotation_Period_days: Optional[float]
    Orbital_Period_years: Optional[float]
    Moons: Optional[int]
    Rings: Optional[bool]
    Temperature_Range_C: Optional[str]
    Atmosphere_Composition: Optional[dict]
    Surface_Characteristics: Optional[str]
    Interesting_Facts: Optional[str]
    Mass: Optional[str]
    Escape_velocity: Optional[str]

@app.get('/planets', response_model=List[Planet])
def get_all_planets():
    """Retrieve details of all planets."""
    planets = []
    for planet in collection.find():
        planet["_id"] = str(planet["_id"])  # Convert MongoDB ObjectId to string
        planets.append(planet)
    return planets

@app.get('/planet/{planet_id}', response_model=Planet)
def get_planet_by_id(planet_id: str):
    """Retrieve a specific planet's details by its _id."""
    try:
        planet = collection.find_one({"_id": ObjectId(planet_id)})
        if planet:
            planet["_id"] = str(planet["_id"])  # Convert ObjectId to string
            return planet
        else:
            raise HTTPException(status_code=404, detail="Planet not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid ObjectId: {e}")

@app.get('/planet/name/{planet_name}', response_model=Planet)
def get_planet_by_name(planet_name: str):
    """Retrieve a specific planet's details by its name."""
    planet = collection.find_one({"Planet_Name": planet_name})
    if planet:
        planet["_id"] = str(planet["_id"])  # Convert ObjectId to string
        return planet
    else:
        raise HTTPException(status_code=404, detail="Planet not found")

# Vercel will look for an 'app' instance inside `main.py` in the 'api' directory
