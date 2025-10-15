import os
from typing import Dict, List, Any, Optional
from flask import Flask, jsonify, Response, request
from sqlalchemy import or_
from models import init_db, db, Dog, Breed, AdoptionApplication
from utils.validation import validate_email, validate_phone_us, validate_name_length

# Get the server directory path
base_dir: str = os.path.abspath(os.path.dirname(__file__))

app: Flask = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(base_dir, "dogshelter.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database with the app
init_db(app)

@app.route('/api/dogs', methods=['GET'])
def get_dogs() -> Response:
    # Get search parameters
    search_query: str = request.args.get('search', '').strip()
    page: int = max(1, int(request.args.get('page', 1)))
    per_page: int = min(50, int(request.args.get('per_page', 12)))
    breed_id: Optional[str] = request.args.get('breed_id')
    available: Optional[str] = request.args.get('available')
    unavailable: Optional[str] = request.args.get('unavailable')
    
    # Build the base query
    query = db.session.query(
        Dog.id, 
        Dog.name, 
        Breed.name.label('breed'),
        Dog.status
    ).join(Breed, Dog.breed_id == Breed.id)
    
    # Apply search filter if search query exists
    if search_query:
        query = query.filter(
            or_(
                Dog.name.ilike(f'%{search_query}%'),
                Breed.name.ilike(f'%{search_query}%'),
                Dog.description.ilike(f'%{search_query}%')
            )
        )
    if breed_id:
        try:
            breed_id_int = int(breed_id)
            query = query.filter(Dog.breed_id == breed_id_int)
        except ValueError:
            pass
    # Apply availability filtering with combined logic
    if available == 'true' and unavailable == 'true':
        # Both checked - show all dogs (no status filter)
        pass
    elif available == 'true' and unavailable != 'true':
        # Available only (existing behavior)
        query = query.filter(Dog.status == 'AVAILABLE')
    elif unavailable == 'true' and available != 'true':
        # Unavailable only (new functionality)
        query = query.filter(Dog.status != 'AVAILABLE')
    # else: neither checked - show all dogs (default behavior)
    
    # Add this line before pagination:
    query = query.order_by(Dog.name)
    
    # Apply pagination
    paginated_dogs = query.paginate(page=page, per_page=per_page)
    
    # Convert the result to a list of dictionaries
    dogs_list: List[Dict[str, Any]] = [
        {
            'id': dog.id,
            'name': dog.name,
            'breed': dog.breed,
            'status': dog.status.name if hasattr(dog.status, 'name') else str(dog.status)
        }
        for dog in paginated_dogs.items
    ]
    
    return jsonify({
        'dogs': dogs_list,
        'total': paginated_dogs.total,
        'pages': paginated_dogs.pages,
        'current_page': page
    })

@app.route('/api/dogs/<int:id>', methods=['GET'])
def get_dog(id: int) -> tuple[Response, int] | Response:
    # Query the specific dog by ID and join with breed to get breed name
    dog_query = db.session.query(
        Dog.id,
        Dog.name,
        Breed.name.label('breed'),
        Dog.age,
        Dog.description,
        Dog.gender,
        Dog.status
    ).join(Breed, Dog.breed_id == Breed.id).filter(Dog.id == id).first()
    
    # Return 404 if dog not found
    if not dog_query:
        return jsonify({"error": "Dog not found"}), 404
    
    # Check if dog has an existing application
    has_application = AdoptionApplication.query.filter_by(dog_id=id).first() is not None
    
    # Convert the result to a dictionary
    dog: Dict[str, Any] = {
        'id': dog_query.id,
        'name': dog_query.name,
        'breed': dog_query.breed,
        'age': dog_query.age,
        'description': dog_query.description,
        'gender': dog_query.gender,
        'status': dog_query.status.name if hasattr(dog_query.status, 'name') else str(dog_query.status),
        'has_application': has_application
    }
    
    return jsonify(dog)

@app.route('/api/breeds', methods=['GET'])
def get_breeds() -> Response:
    breeds_query: List[Breed] = Breed.query.all()
    
    # Convert the result to a list of dictionaries
    breeds_list: List[Dict[str, Any]] = [
        {
            'id': breed.id,
            'name': breed.name
        }
        for breed in breeds_query
    ]
    
    return jsonify(breeds_list)  # jsonify returns a Response object


@app.route('/api/dogs/<int:dog_id>/applications', methods=['POST'])
def submit_application(dog_id: int) -> tuple[Response, int]:
    """Submit adoption application for a dog."""
    # Check if dog exists
    dog = Dog.query.get(dog_id)
    if not dog:
        return jsonify({"error": "Dog not found"}), 404
    
    # Check if dog already has an application
    existing_application = AdoptionApplication.query.filter_by(dog_id=dog_id).first()
    if existing_application:
        return jsonify({"error": "This dog already has an application"}), 400
    
    # Get request data
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    # Validate required fields
    required_fields = ['applicant_name', 'applicant_email', 'applicant_phone']
    for field in required_fields:
        if not data.get(field):
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    # Validate field lengths and formats using validation utilities
    if not validate_name_length(data['applicant_name']):
        return jsonify({"error": "Name must be between 2-50 characters", "field": "applicant_name"}), 400
    
    if not validate_email(data['applicant_email']):
        return jsonify({"error": "Invalid email format", "field": "applicant_email"}), 400
    
    if not validate_phone_us(data['applicant_phone']):
        return jsonify({"error": "Invalid phone number format", "field": "applicant_phone"}), 400
    
    # Create new application
    try:
        application = AdoptionApplication(
            dog_id=dog_id,
            applicant_name=data['applicant_name'],
            applicant_email=data['applicant_email'],
            applicant_phone=data['applicant_phone']
        )
        
        db.session.add(application)
        db.session.commit()
        
        return jsonify({
            "message": "submission accepted",
            "application_id": application.id
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to submit application"}), 500


@app.route('/api/applications', methods=['GET'])
def get_applications() -> Response:
    """Get all adoption applications for staff review."""
    applications = AdoptionApplication.query.all()
    
    applications_list: List[Dict[str, Any]] = [
        app.to_dict() for app in applications
    ]
    
    return jsonify(applications_list)


# add a new endpoint for the root of flask API
@app.route('/', methods=['GET'])
def index() -> str:
    return "Welcome to the Dog Shelter API! Use /api/dogs and /api/breeds to access data."

# add a new endpoint to list all un-available dogs
@app.route('/api/dogs/unavailable', methods=['GET'])
def get_unavailable_dogs() -> Response:
    """Get all dogs that are not available for adoption."""
    unavailable_dogs = db.session.query(
        Dog.id, 
        Dog.name, 
        Breed.name.label('breed'),
        Dog.status
    ).join(Breed, Dog.breed_id == Breed.id).filter(Dog.status != 'AVAILABLE').order_by(Dog.name).all()
    
    dogs_list: List[Dict[str, Any]] = [
        {
            'id': dog.id,
            'name': dog.name,
            'breed': dog.breed,
            'status': dog.status.name if hasattr(dog.status, 'name') else str(dog.status)
        }
        for dog in unavailable_dogs
    ]
    
    return jsonify(dogs_list)

if __name__ == '__main__':
    app.run(debug=True, port=5100) # Port 5100 to avoid macOS conflicts