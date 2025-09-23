import os
from typing import Dict, List, Any, Optional
from flask import Flask, jsonify, Response, request
from sqlalchemy import or_
from models import init_db, db, Dog, Breed

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
    if available == 'true':
        query = query.filter(Dog.status == 'AVAILABLE')
    
    # Add this line before pagination:
    query = query.order_by(Dog.name)
    
    # Apply pagination
    paginated_dogs = query.paginate(page=page, per_page=per_page)
    
    # Convert the result to a list of dictionaries
    dogs_list: List[Dict[str, Any]] = [
        {
            'id': dog.id,
            'name': dog.name,
            'breed': dog.breed
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
    
    # Convert the result to a dictionary
    dog: Dict[str, Any] = {
        'id': dog_query.id,
        'name': dog_query.name,
        'breed': dog_query.breed,
        'age': dog_query.age,
        'description': dog_query.description,
        'gender': dog_query.gender,
        'status': dog_query.status.name
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


# add a new endpoint for the root of flask API
@app.route('/', methods=['GET'])
def index() -> str:
    return "Welcome to the Dog Shelter API! Use /api/dogs and /api/breeds to access data."


if __name__ == '__main__':
    app.run(debug=True, port=5100) # Port 5100 to avoid macOS conflicts