# PC Parser Development Environment Setup

This guide will help you set up the PC Parser project on a new device.

## Prerequisites

Before starting, make sure you have the following installed:

- **Python 3.8+** - [Download here](https://www.python.org/downloads/)
- **Node.js 16+** - [Download here](https://nodejs.org/)
- **PostgreSQL 12+** - [Download here](https://www.postgresql.org/download/)
- **Git** - [Download here](https://git-scm.com/downloads/)

### Verify installations:

```bash
python --version    # Should show Python 3.8+
node --version      # Should show Node.js 16+
npm --version       # Should come with Node.js
psql --version      # Should show PostgreSQL 12+
git --version       # Should show Git version
```

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd pc_parser
```

### 2. Backend Setup (Django)

#### Create Python Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

#### Install Backend Dependencies

```bash
pip install -r requirements.txt
```

#### Database Setup

1. **Create PostgreSQL Database:**
   
Create DB named **pc_parser_db** in pgAdmin4
<be>
<br>
or
<br>

```sql
-- Connect to PostgreSQL as superuser
psql -U postgres

-- Create database and user
CREATE DATABASE pc_parser_db;
CREATE USER campuslink_user WITH PASSWORD 'your_password_here';
GRANT ALL PRIVILEGES ON DATABASE pc_parser_db TO pc_parser_user;
\q
```
2. **Create Environment Variables File:**
   Create a `.env` file in the `/backend` directory:

```bash
# Database Configuration
DB_NAME=pc_parser_db 
DB_USER=pc_parser_user (change this)
DB_PASSWORD=your_password_here (change this)
DB_HOST=localhost
DB_PORT=5432

# Django Configuration
SECRET_KEY=your-super-secret-key-here-change-this-in-production (Change this. Found in setting.py)
DEBUG=True
```

#### Run Database Migrations
```bash
cd backend
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser  # (optional, for admin access)
python manage.py runserver
```

### 3. Frontend Setup (Vue.js)

#### Navigate to Frontend Directory

```bash
cd frontend
```

#### Install Node Dependencies and Start Dev Server

```bash
npm install
npm run dev
```

#### Create Frontend Environment File

Create `.env` file in the `frontend` directory:

```bash
VITE_API_BASE_URL=http://127.0.0.1:8000/api
```

## Recommended VS Code Extensions

For the best developer experience, install these extensions in VS Code:

### Vue.js Development

- [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar)  
  _(Essential for Vue 3 syntax highlighting, IntelliSense, and type checking)_

### Django/Python Development

- [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)  
  _(Syntax highlighting, linting, and debugging for Python)_
- [Django](https://marketplace.visualstudio.com/items?itemName=batisteo.vscode-django)  
  _(Template syntax, code snippets, and navigation for Django)_

### Code Formatting & Linting

- [Prettier - Code formatter](https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode)  
  _(Automatic code formatting for JS, Vue, CSS, etc.)_
- [ESLint](https://marketplace.visualstudio.com/items?itemName=dbaeumer.vscode-eslint)  
  _(JavaScript/Vue linting and error highlighting)_

---

**After installing these extensions, enable "Format On Save" in your VS Code settings for automatic formatting.**

# Daily Development Workflow

**Follow these steps every time you pull new changes or start work. This ensures everyone’s backend, database, and environment are consistent.**

---

##  Sync Your Codebase

- Pull the latest code (and migration files) from your main branch:
    ```bash
    git checkout main   # or your project’s main branch
    git pull
    ```

---

##  Update Virtual Environment and Python Dependencies (Stay on project root)

- If your virtual environment is not active, activate it:
    ```bash
    # On Windows
    venv\Scripts\activate
    # On Mac/Linux
    source venv/bin/activate
    ```
- Install any new requirements:
    ```bash
    pip install -r requirements.txt
    ```

---


##  Run Django Migrations

- **Always run migrations after pulling code:**
    ```bash
    python manage.py migrate
    ```

---

##  Update Frontend

    ```bash
    cd frontend
    npm install
    ```

---


##  Start Your Servers

- Backend:
    ```bash
    python manage.py runserver
    ```
- Frontend :
    ```bash
    npm run dev
    ```

---
## 🛠️ Common Project Commands

### 1. Scrape Data (Startech Example)
```sh
# Run from your scraper directory:
python startech_scraper.py
```

### 2. Populate Retailer Offers Table (Backend, venv activated)
```sh
# From backend directory, venv activated:
python manage.py import_retailer_offers D:\Programming\Projects\Hackathons\pc_parser\scraper\data\startech_products.json
```
### 3. Match Scraped Data to Global Products Table
```sh
python manage.py match_products
```

### 4. Populate/Update Global Component Specs (from docyx/pc-part-dataset)
```sh
python manage.py import_pcparts data
# 'data' is the folder containing the docyx json files (cpu.json, gpu.json, etc)
```

