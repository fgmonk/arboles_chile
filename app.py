import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from data import trees as initial_trees

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trees.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)

# --- Models ---
class Species(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    scientific_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(200), nullable=False)
    
    # Relationship: A species can appear in many log entries
    logs = db.relationship('LogEntry', backref='species', lazy=True)

class LogEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    species_id = db.Column(db.Integer, db.ForeignKey('species.id'), nullable=False)
    user_image_path = db.Column(db.String(200), nullable=False) # Path to uploaded drawing
    notes = db.Column(db.Text, nullable=True)
    
    # Ideally we'd store a date, but for simplicity we rely on ID order or add later

# --- Helpers ---
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def init_db():
    with app.app_context():
        db.create_all()
        # Seed Species if empty
        if not Species.query.first():
            for tree_data in initial_trees:
                new_species = Species(
                    name=tree_data['name'],
                    scientific_name=tree_data['scientific_name'],
                    description=tree_data['description'],
                    image_url=tree_data['image_url']
                )
                db.session.add(new_species)
            db.session.commit()
            print("Database initialized with default species.")

# Initialize DB on start
init_db()

@app.route('/')
def home():
    # Home is now the "Bitacora" - showing user discoveries
    entries = LogEntry.query.all()
    # If no entries, show a welcome message or empty state in template
    return render_template('index.html', entries=entries)

@app.route('/catalog')
def catalog():
    # List of all reference species
    all_species = Species.query.all()
    return render_template('catalog.html', species=all_species)

@app.route('/log/new', methods=['GET', 'POST'])
def log_discovery():
    if request.method == 'POST':
        species_id = request.form.get('species_id')
        notes = request.form.get('notes')
        file = request.files.get('file')
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            new_entry = LogEntry(
                species_id=species_id,
                user_image_path=filename,
                notes=notes
            )
            db.session.add(new_entry)
            db.session.commit()
            return redirect(url_for('home'))
            
    all_species = Species.query.all()
    return render_template('log_entry.html', species=all_species)

@app.route('/entry/<int:entry_id>')
def entry_detail(entry_id):
    entry = LogEntry.query.get_or_404(entry_id)
    return render_template('detail.html', entry=entry)

if __name__ == '__main__':
    app.run(debug=True)

