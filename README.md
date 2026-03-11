# Address Mapping Application

A full-stack application to calculate the distance between two addresses using geolocation services.

## Prerequisites

- **Python 3.9+** - [Download](https://www.python.org/downloads/)
- **Node.js 16+ and npm** - [Download](https://nodejs.org/)
- **Git** - [Download](https://git-scm.com/downloads)

## Installation

### 1. Clone the Repository
```bash
git clone <your-repository-url>
cd Address_Mapping
```

### 2. Backend Setup

**Windows:**
```cmd
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**macOS/Linux:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Frontend Setup

Open a new terminal window:

```bash
cd frontend
npm install
```

## Running the Application

### Start Backend Server

**Windows:**
```cmd
cd backend
venv\Scripts\activate
fastapi run
```

**macOS/Linux:**
```bash
cd backend
source venv/bin/activate
fastapi run
```

Backend runs at: `http://localhost:8000`

### Start Frontend Server

In a separate terminal:

```bash
cd frontend
npm run dev
```

Frontend runs at: `http://localhost:5173`

### Access the Application

- **Application:** http://localhost:5173
- **API Docs:** http://localhost:8000/docs
