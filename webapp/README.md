# Cambridge AI Professor - Web Application

This directory contains the source code for the web-based frontend and backend of the Cambridge AI Professor.

## Running the Application

To run the application, you will need to start both the backend API server and the frontend development server.

### 1. Running the Backend (FastAPI)

The backend server provides the API that the frontend communicates with.

1.  **Navigate to the backend directory**:
    ```bash
    cd webapp/backend
    ```

2.  **Start the Uvicorn server**:
    Make sure your virtual environment from the root directory is activated (`source ../../venv/bin/activate`).
    ```bash
    uvicorn app.main:app --reload
    ```
    The backend server will be running at `http://127.0.0.1:8000`.

### 2. Running the Frontend (Next.js)

The frontend is a Next.js application that provides the user interface.

1.  **Navigate to the frontend directory**:
    ```bash
    cd webapp/frontend
    ```

2.  **Install dependencies**:
    ```bash
    npm install
    ```

3.  **Start the development server**:
    ```bash
    npm run dev
    ```
    The frontend application will be accessible at `http://localhost:3000`.

Open your browser to `http://localhost:3000` to use the application.
