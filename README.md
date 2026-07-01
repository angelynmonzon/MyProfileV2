# User Management - Django + Vue + Supabase

A full-stack application with Django backend, Vue.js admin panel, and Supabase integration for user management with role-based access control.

## Features

- **User Management**: Create, Read, Update, Delete users
- **Role-Based Access Control**:
  - **SuperAdmin**: Full CRUD access to all users
  - **Editor**: Read-only access to users
- **Authentication**: Token-based authentication with Supabase integration
- **Modern Admin Panel**: Vue.js frontend with beautiful UI

## Project Structure

```
user_management/
├── manage.py                          # Django management script
├── user_management/                   # Django project configuration
│   ├── __init__.py
│   ├── settings.py                    # Django settings
│   ├── urls.py                        # Main URL configuration
│   ├── wsgi.py                        # WSGI configuration
│   └── asgi.py                        # ASGI configuration
├── users/                             # Users Django app
│   ├── __init__.py
│   ├── models.py                      # User model with roles
│   ├── serializers.py                 # DRF serializers
│   ├── views.py                       # API views
│   ├── urls.py                        # Users URL routes
│   ├── permissions.py                 # Custom permissions
│   ├── admin.py                       # Django admin configuration
│   ├── apps.py                        # App configuration
│   ├── supabase_utils.py              # Supabase integration utilities
│   └── signals.py                     # Django signals
├── admin/                             # Vue.js admin panel
│   ├── package.json                   # Node dependencies
│   ├── vite.config.js                 # Vite configuration
│   ├── index.html                     # Entry HTML
│   └── src/
│       ├── main.js                    # Vue entry point
│       ├── App.vue                    # Root component
│       ├── router/
│       │   └── index.js               # Vue Router configuration
│       ├── stores/
│       │   ├── auth.js                # Authentication store
│       │   └── users.js               # Users store
│       └── views/
│           ├── Login.vue              # Login page
│           ├── Users.vue              # Users list page
│           ├── UserForm.vue           # User create/edit form
│           └── Profile.vue            # User profile page
└── requirements.txt                   # Python dependencies
```

## Setup Instructions

### Backend Setup (Django)

1. **Create a virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**:
Create a `.env` file in the project root:
```env
DJANGO_SECRET_KEY=your-secret-key-here
DEBUG=True
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-supabase-service-role-key

# Supabase PostgreSQL Database
DB_NAME=postgres
DB_USER=postgres.your-project-ref
DB_PASSWORD=your-database-password
DB_HOST=aws-0-region.pooler.supabase.com
DB_PORT=5432
```

The database connection string is available in your Supabase dashboard under **Project Settings > Database > Connection string**. Use the transaction or session pooler host.

4. **Run migrations**:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Create a superadmin user**:
```bash
python manage.py createsuperuser
```

6. **Run the Django server**:
```bash
python manage.py runserver
```

The Django API will be available at `http://localhost:8000`

### Frontend Setup (Vue.js)

1. **Navigate to admin folder**:
```bash
cd admin
```

2. **Install dependencies**:
```bash
npm install
```

3. **Set up environment variables**:
Create a `.env` file in the `admin` folder:
```env
VITE_SUPABASE_URL=your-supabase-url
VITE_SUPABASE_KEY=your-supabase-anon-key
```

4. **Run the development server**:
```bash
npm run dev
```

The Vue admin panel will be available at `http://localhost:8080`

## API Endpoints

### Users API

- `GET /api/users/` - List all users (authenticated)
- `POST /api/users/` - Create user (SuperAdmin only)
- `GET /api/users/{id}/` - Get user details (authenticated)
- `PUT /api/users/{id}/` - Update user (SuperAdmin only)
- `PATCH /api/users/{id}/` - Partial update user (SuperAdmin only)
- `DELETE /api/users/{id}/` - Delete user (SuperAdmin only)
- `GET /api/users/me/` - Get current user (authenticated)
- `GET /api/users/editors/` - List all editors (SuperAdmin only)
- `GET /api/users/superadmins/` - List all superadmins (SuperAdmin only)

## User Roles

### SuperAdmin
- Full CRUD access to all users
- Can create, update, and delete users
- Can change user roles
- Can view all users

### Editor
- Read-only access to users
- Can view user list and details
- Cannot create, update, or delete users
- Cannot change user roles

## Authentication

The application uses token-based authentication. When logging in:
1. The frontend attempts Supabase authentication first
2. If Supabase auth fails, it falls back to Django authentication
3. A token is returned and stored in localStorage
4. All subsequent API requests include the token in the Authorization header

## Supabase Integration

The application integrates with Supabase for:
- User authentication (optional, with Django fallback)
- User data synchronization
- Additional backend services

When a user is created in Django, they are automatically synced to Supabase (if configured).

## Development

### Adding New Features

1. **Backend**: Add new models, views, and serializers in the `users` app or create new Django apps
2. **Frontend**: Add new Vue components in `admin/src/views/` and update the router

### Testing

Run Django tests:
```bash
python manage.py test
```

## Migrate from SQLite to Supabase PostgreSQL

If you have existing data in `db.sqlite3`, follow these steps to migrate it to Supabase:

1. **Ensure your `.env` has real Supabase database credentials**:
   - `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`

2. **Dump all data from SQLite**:
```bash
python manage.py dumpdata --natural-primary --natural-foreign --all --indent 2 > data_dump.json
```

3. **Install the PostgreSQL driver**:
```bash
pip install psycopg2-binary==2.9.9
```

4. **Run migrations on Supabase PostgreSQL**:
```bash
python manage.py migrate
```

5. **Load data into Supabase PostgreSQL**:
```bash
python manage.py loaddata data_dump.json
```

6. **Create a new superuser if needed**:
```bash
python manage.py createsuperuser
```

## Production Deployment

1. Set `DEBUG=False` in Django settings
2. Use environment variables for sensitive data
3. Configure Supabase PostgreSQL (already configured via environment variables)
4. Set up proper CORS origins
5. Build the Vue frontend: `npm run build`
6. Serve static files through Django or a CDN
7. Use a production WSGI server (Gunicorn, uWSGI)

## License

This project is provided as-is for educational and development purposes.
