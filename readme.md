# 🐍 Serverless Task API (Python + AWS Lambda)

This is a Serverless API project written in Python, designed to run on AWS Lambda, using MongoDB as a database and JWT for authentication. For local development, it uses the `serverless-offline` plugin.

---

## 🚀 How to run the project locally

### 🔧 Requirements

- Python 3.11 or higher  
- Node.js 16 or higher  
- MongoDB (local or Atlas)  
- Serverless Framework globally installed:
  ```bash
  npm install -g serverless
  ```

---

### 📆 Installation

1. Create a virtual environment and install Python dependencies:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Install Node.js dependencies:

   ```bash
   npm install
   npm install serverless-offline --save-dev
   ```

3. Create a `.env` file with your environment variables:

   ```env
   JWT_SECRET=supersecrettoken
   MONGODB_URI=mongodb://localhost:27017/your-database
   ```

---

## ▶️ Run in local mode

Run the following command:

```bash
sls offline start
```

This will start the service at `http://localhost:3000`.

---

## 🔐 Authentication

Task-related endpoints require authentication.  
You must obtain a JWT token from `/auth/login` or `/auth/register` and include it in your requests:

```
Authorization: Bearer <your_token>
```

---

## 📚 Available Endpoints

### 🤝 Auth

#### `POST /auth/register`
Registers a new user.

**Body:**
```json
{
  "email": "a@gmail.com",
  "password": "123456"
}
```

**Responses:**
- `201 Created`: User registered and JWT token returned.
- `400 Bad Request`: Email already registered or invalid data.

---

#### `POST /auth/login`
Authenticates a user and returns a JWT token.

**Body:**
```json
{
  "email": "a@gmail.com",
  "password": "123456"
}
```

**Responses:**
- `200 OK`: Valid JWT token.
- `400 Bad Request`: Invalid credentials.

---

### ✅ Tasks (JWT required)

#### `POST /tasks`
Creates a new task.

**Body:**
```json
{
  "title": "My Task",
  "description": "Something important",
  "status": "todo"
}
```

**Response:** `201 Created`

---

#### `GET /tasks`
Returns a paginated list of tasks.

**Optional query parameters:**
```
?page=1&limit=5
```

**Response:** `200 OK` with list of tasks and pagination metadata.

---

#### `GET /tasks/{id}`
Returns details of a task by ID.

**Response:**
- `200 OK`: Task found.
- `404 Not Found`: Task not found.

---

#### `PUT /tasks/{id}`
Updates an existing task.

**Body:**
```json
{
  "title": "New title",
  "status": "done"
}
```

**Response:**
- `200 OK`: Task updated.
- `404 Not Found`: Task not found.

---

#### `DELETE /tasks/{id}`
Deletes a task.

**Response:**
- `200 OK`: Task deleted.
- `404 Not Found`: Task not found.

---

#### `GET /tasks/stats`
Returns statistics of tasks by status.

**Response:**
```json
[
  { "status": "todo", "count": 5 },
  { "status": "done", "count": 3 }
]
```

---

## 🔮 Tests

To run tests:

```bash
pytest
```

Ensure your environment and database are properly set up before testing.

---

## 🌍 Technologies Used

- Python 3.11
- Serverless Framework
- AWS Lambda (via serverless-offline)
- MongoDB
- JWT (PyJWT)
- pytest

---

## ✉️ Contact

If you have questions or suggestions, feel free to open an issue or contact me.

