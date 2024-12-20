# Spy Cat Agency Management Application

**Spy Cat Agency Management Application** is a CRUD API for managing spy cats, their missions, and assigned targets. This application allows creating agents, assigning them to missions, and managing mission targets to streamline the information-gathering process.

## Features

- **Cats (Agents)**: Full CRUD operations for managing spy cats, including fields like name, breed, years of experience, and salary.
- **Missions**: CRUD operations to manage missions. Missions can be created without an agent assigned and later assigned to a cat.
- **Targets**: Each mission includes one to three targets. Targets can be updated with notes and marked as complete, which then freezes any further updates.

## Requirements

- **Python** 3.9+
- **FastAPI**
- **PostgreSQL**

## Setup and Run

1. **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/spy_cat_agency.git
    cd spy_cat_agency
    ```

2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Set up environment variables**:
   - Create a `.env` file in the root directory:
      ```env
      DATABASE_URL=postgresql+asyncpg://user:password@localhost/db_name
      ```

4. **Run the application**:
    ```bash
    uvicorn app.main:app --reload
    ```

5. **API Documentation**:
   - Access the interactive API documentation at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

## API Endpoints

### Cats

- **POST /cats/**: Create a new spy cat
- **GET /cats/**: Retrieve a list of all cats
- **GET /cats/{cat_id}**: Retrieve details of a specific cat
- **PUT /cats/{cat_id}**: Update a cat's salary
- **DELETE /cats/{cat_id}**: Remove a cat from the system

### Missions

- **POST /missions/**: Create a new mission, optionally including targets
- **GET /missions/{mission_id}**: Retrieve details of a specific mission
- **PUT /missions/{mission_id}**: Mark a mission as complete
- **DELETE /missions/{mission_id}**: Delete a mission (only if it hasn’t been assigned to a cat)
- **POST /missions/{mission_id}/assign/{cat_id}**: Assign a cat to a mission

### Targets

- **PUT /missions/{mission_id}/targets/{target_id}**: Update a target's notes or completion status

## Postman Collection

To make testing easier, a [Postman collection](https://link-to-postman-collection) is provided with all the endpoints defined above.

### Instructions for Using the Postman Collection

1. Download the Postman collection from the link provided above.
2. Import the collection into Postman:
   - Open Postman and go to **File** > **Import**.
   - Select the downloaded collection file and import it.
3. Use the imported collection to test the API endpoints with sample data.
