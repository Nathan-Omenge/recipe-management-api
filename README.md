# Recipe Management API

A complete Django REST Framework API for managing personal recipe collections with ingredients, categories, and user authentication.

## Features

### Core Functionality
- **User Authentication** - Token-based and session authentication
- **Recipe CRUD** - Create, read, update, delete recipes with full details
- **Recipe-Ingredient Management** - Add ingredients with quantities and units
- **Category Organization** - Organize recipes by meal type (Breakfast, Lunch, Dinner, etc.)
- **User Isolation** - Users can only access and manage their own recipes
- **Search & Filtering** - Find recipes by ingredient or category

### API Capabilities
- RESTful API design with proper HTTP methods
- JSON serialization with nested ingredient data
- Browsable API interface for development and testing
- Comprehensive error handling and validation
- Pagination support for large datasets

## API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login (returns auth token)
- `POST /api/auth/logout/` - User logout
- `GET /api/auth/profile/` - Get user profile
- `PUT /api/auth/profile/` - Update user profile

### Recipe Management
- `GET /api/recipes/` - List user's recipes (with filtering)
- `POST /api/recipes/` - Create new recipe
- `GET /api/recipes/{id}/` - Get recipe details with ingredients
- `PUT /api/recipes/{id}/` - Update recipe
- `DELETE /api/recipes/{id}/` - Delete recipe
- `GET /api/recipes/my-recipes/` - Explicit user recipes endpoint
- `GET /api/recipes/search_by_ingredient/?ingredient={name}` - Search recipes by ingredient

### Recipe-Ingredient Management
- `GET /api/recipes/{id}/ingredients/` - Get recipe ingredients
- `POST /api/recipes/{id}/ingredients/` - Add ingredient to recipe
- `DELETE /api/recipes/{id}/ingredients/` - Remove ingredient from recipe

### Categories & Ingredients
- `GET /api/categories/` - List all categories
- `GET /api/ingredients/` - List all ingredients
- `POST /api/ingredients/` - Add new ingredient

## Quick Start

### Prerequisites
- Python 3.9+
- pip
- Virtual environment (recommended)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/recipe-management-api.git
   cd recipe-management-api
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv recipe_env
   source recipe_env/bin/activate  # On Windows: recipe_env\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser (optional, for admin access):**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start development server:**
   ```bash
   python manage.py runserver
   ```

## Usage Examples
### API Root Page
http://127.0.0.1:8000/api/


### 1. User Registration
http://127.0.0.1:8000/api/auth/register/

```json
{
    "username": "demouser",
    "email": "demo@example.com",
    "password": "demopass123",
    "password_confirm": "demopass123",
    "first_name": "Demo",
    "last_name": "User"
}
```

### 2. User Login
http://127.0.0.1:8000/api/auth/login/

```json
{
    "username": "demouser",
    "password": "demopass123"
}
```

### 2. Create Recipe
http://127.0.0.1:8000/api/recipes/

```json
{
    "name": "Chocolate Chip Cookies",
    "description": "Classic homemade cookies",
    "instructions": "1. Mix dry ingredients\n2. Cream butter and sugar\n3. Combine everything\n4. Bake at 350°F for 10 minutes",
    "category": 1,
    "prep_time": 15,
    "cook_time": 10,
    "servings": 24,
    "difficulty": "easy",
    "ingredients": []
}
```

### 3. Add Ingredients to Recipe
http://127.0.0.1:8000/api/recipes/2/ingredients/

```json
{
    "ingredient": 1,
    "quantity": "2.5",
    "unit": "cups"
}
```

```json
{
    "ingredient": 2,
    "quantity": "2",
    "unit": "pieces"
}
```
viewing complete recipe: http://127.0.0.1:8000/api/recipes/2/

### Search by Ingredient
http://127.0.0.1:8000/api/recipes/search_by_ingredient/?ingredient=flour

http://127.0.0.1:8000/api/recipes/search_by_ingredient/?ingredient=eggs

### Category Filtering
http://127.0.0.1:8000/api/categories/

http://127.0.0.1:8000/api/recipes/?category=1

## Database Schema

- **User** - Django's built-in user model with profiles
- **Category** - Recipe categories (Breakfast, Lunch, Dinner, etc.)
- **Recipe** - Recipe details with timing, difficulty, and instructions
- **Ingredient** - Master ingredient database
- **RecipeIngredient** - Junction table linking recipes to ingredients with quantities

## Development Status

-  Django project setup and structure
-  Database models and relationships
-  Django admin interface
-  REST API endpoints with DRF
-  User authentication (token + session)
-  Recipe CRUD operations
-  Recipe-ingredient integration
-  User isolation and permissions
-  Nested serialization
-  Search and filtering (in progress)

## Tech Stack

- **Framework:** Django 4.2+ with Django REST Framework
- **Database:** SQLite (development), PostgreSQL (production ready)
- **Authentication:** DRF Token Authentication + Session Authentication
- **API Documentation:** DRF Browsable API
- **Dependencies:** django-filter for advanced filtering

## Testing

Access the browsable API interface at `http://127.0.0.1:8000/api/` to test all endpoints interactively.

**Test Authentication:**
1. Register a new user at `/api/auth/register/`
2. Login at `/api/auth/login/` 
3. Access protected endpoints with authentication

**Test Recipe Management:**
1. Create recipes with full details
2. Add ingredients with quantities
3. Retrieve complete recipes with nested ingredient data
4. Search recipes by ingredient names

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request



## Project Architecture

```
recipe_management_api/
├── apps/
│   ├── users/          # User authentication and profiles
│   ├── recipes/        # Recipe management and CRUD
│   ├── categories/     # Recipe categorization
│   └── ingredients/    # Ingredient management
├── recipe_project/     # Main project settings
├── recipe_env/         # Virtual environment
└── manage.py
```
