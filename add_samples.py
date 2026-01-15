"""
Script to populate the database with sample log entries
"""
from app import app, db, LogEntry, Species

with app.app_context():
    # Check if we already have sample entries
    if LogEntry.query.count() > 0:
        print("Sample entries already exist. Skipping.")
    else:
        # Get species from database
        araucaria = Species.query.filter_by(name="Araucaria").first()
        palma = Species.query.filter_by(name="Palma Chilena").first()
        alerce = Species.query.filter_by(name="Alerce").first()
        
        # Create sample entries
        samples = [
            LogEntry(
                species_id=araucaria.id,
                user_image_path="araucaria_dibujo.png",
                notes="¡Lo encontramos en el parque! Tiene ramas muy puntiagudas como un dinosaurio. Leo, 7 años."
            ),
            LogEntry(
                species_id=palma.id,
                user_image_path="palma_dibujo.png",
                notes="Esta palma está cerca de la casa de la abuela. Es súper alta y tiene frutos naranjos. Leo, 9 años."
            ),
            LogEntry(
                species_id=alerce.id,
                user_image_path="alerce_dibujo.png",
                notes="Vimos este árbol gigante en el sur. Papá dice que es más viejo que los dinosaurios. Leo, 9 años."
            )
        ]
        
        for entry in samples:
            db.session.add(entry)
        
        db.session.commit()
        print(f"Created {len(samples)} sample log entries!")
