# Ging's Profile - Django + Vue + Supabase

A full-stack portfolio website with Django backend, Vue.js frontend, and Supabase integration for image storage. Includes a public portfolio site and an admin panel for content management.

## Features

### Public Portfolio Site

- **Hero Section**: Professional introduction with profile image
- **About Section**: Personal bio and about image
- **Services Section**: Display offered services with icons
- **Skills Section**: Categorized skills with visibility toggles
- **Experience Section**: Work experience timeline
- **Education Section**: Education history
- **Portfolio Projects**: Project showcase with images and videos
- **Contact Section**: Contact information and social links
- **Search**: Filter projects by title and description
- **Video Support**: YouTube and Vimeo video thumbnails with lightbox playback
- **Section Visibility**: Toggle sections on/off via admin panel

### Admin Panel

- **User Management**: Create, Read, Update, Delete users
- **Role-Based Access Control**:
  - **SuperAdmin**: Full CRUD access to all users and profile management
  - **Editor**: Profile management only
- **Profile Management**: Edit all profile information, services, skills, experience, education, and projects
- **Section Visibility**: Toggle portfolio sections on/off
- **Authentication**: Token-based authentication
- **Modern UI**: Clean, responsive Vue.js interface

## Project Structure

```
ging_profile_v2/
├── manage.py                          # Django management script
├── ging_profile_v2/                   # Django project configuration
│   ├── __init__.py
│   ├── settings.py                    # Django settings
│   ├── urls.py                        # Main URL configuration
│   ├── wsgi.py                        # WSGI configuration
│   └── asgi.py                        # ASGI configuration
├── users/                             # Users Django app
│   ├── __init__.py
│   ├── models.py                      # User, Profile, Experience, Education, PortfolioProject models
│   ├── serializers.py                 # DRF serializers
│   ├── views.py                       # API views
│   ├── urls.py                        # Users URL routes
│   ├── permissions.py                 # Custom permissions
│   ├── admin.py                       # Django admin configuration
│   ├── apps.py                        # App configuration
│   ├── storage.py                     # Supabase storage backend
│   └── management/                    # Django management commands
│       └── commands/
│           └── migrate_to_supabase.py # Migration script
├── portfolio/                         # Vue.js frontend (combined portfolio + admin)
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
│       │   ├── profile.js            # Profile store
│       │   └── users.js               # Users store
│       ├── api/
│       │   └── profile.js            # Profile API calls
│       ├── components/
│       │   ├── NavBar.vue            # Navigation bar
│       │   ├── HeroSection.vue        # Hero section
│       │   ├── AboutSection.vue       # About section
│       │   ├── ServicesSection.vue    # Services section
│       │   ├── SkillsSection.vue      # Skills section
│       │   ├── ExperienceSection.vue  # Experience section
│       │   ├── EducationSection.vue   # Education section
│       │   ├── PortfolioSection.vue   # Portfolio section with search
│       │   ├── ContactSection.vue     # Contact section
│       │   ├── FooterSection.vue      # Footer
│       │   └── admin/                 # Admin components
│       │       ├── ExperienceList.vue
│       │       ├── EducationList.vue
│       │       └── ProjectList.vue
│       └── views/
│           ├── Home.vue               # Portfolio home page
│           └── admin/                 # Admin views
│               ├── Login.vue          # Login page
│               ├── ProfileCMS.vue     # Profile management
│               ├── Users.vue          # Users list
│               ├── UserForm.vue       # User create/edit
│               └── Profile.vue        # User profile
├── requirements.txt                   # Python dependencies
└── start-all.ps1                      # PowerShell script to run all servers
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
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-supabase-service-role-key
SUPABASE_STORAGE_BUCKET=images

# Supabase PostgreSQL Database (optional locally; SQLite is used if omitted)
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

1. **Navigate to portfolio folder**:

```bash
cd portfolio
```

2. **Install dependencies**:

```bash
npm install
```

3. **Run the development server**:

```bash
npm run dev
```

The Vue application will be available at `http://localhost:5174`

### Quick Start (All Servers)

On Windows, you can use the provided PowerShell script to run all servers simultaneously:

```powershell
.\start-all.ps1
```

This will start:

- Django API on http://localhost:8000
- Vue frontend on http://localhost:5174

## Application Routes

### Public Portfolio Site

- `/` - Portfolio home page (public)

### Admin Panel

- `/admin` - Redirects to login
- `/admin/login` - Login page
- `/admin/profile-cms` - Profile management (requires authentication)
- `/admin/users` - User management (requires SuperAdmin)
- `/admin/users/create` - Create new user (requires SuperAdmin)
- `/admin/users/:id/edit` - Edit user (requires SuperAdmin)
- `/admin/profile` - View user profile (requires authentication)

## API Endpoints

### Authentication

- `POST /api/auth/login/` - Login with username/password

### Users API

- `GET /api/users/` - List all users (authenticated)
- `POST /api/users/` - Create user (SuperAdmin only)
- `GET /api/users/{id}/` - Get user details (authenticated)
- `PUT /api/users/{id}/` - Update user (SuperAdmin only)
- `PATCH /api/users/{id}/` - Partial update user (SuperAdmin only)
- `DELETE /api/users/{id}/` - Delete user (SuperAdmin only)

### Profile API

- `GET /api/profiles/public/` - Get public profile (no auth required)
- `GET /api/profiles/my_profile/` - Get current user's profile (authenticated)
- `POST /api/profiles/` - Create profile (authenticated)
- `PATCH /api/profiles/{id}/` - Update profile (authenticated)

### Experience API

- `GET /api/experiences/` - List experiences (authenticated)
- `POST /api/experiences/` - Create experience (authenticated)
- `PATCH /api/experiences/{id}/` - Update experience (authenticated)
- `DELETE /api/experiences/{id}/` - Delete experience (authenticated)

### Education API

- `GET /api/education/` - List education (authenticated)
- `POST /api/education/` - Create education (authenticated)
- `PATCH /api/education/{id}/` - Update education (authenticated)
- `DELETE /api/education/{id}/` - Delete education (authenticated)

### Portfolio Projects API

- `GET /api/projects/` - List projects (authenticated)
- `POST /api/projects/` - Create project (authenticated)
- `PATCH /api/projects/{id}/` - Update project (authenticated)
- `DELETE /api/projects/{id}/` - Delete project (authenticated)

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

1. The frontend sends username and password to Django API
2. Django validates credentials and returns a token
3. The token is stored in localStorage
4. All subsequent API requests include the token in the Authorization header

## Supabase Integration

The application integrates with Supabase for:

- **Image Storage**: Profile images, project images, and other media files are stored in Supabase Storage
- **PostgreSQL Database**: Optional - can use Supabase PostgreSQL instead of local SQLite
- **Storage Backend**: Custom Django storage backend (`SupabaseStorage`) handles file uploads to Supabase

### Migrating Images to Supabase

If you have local images and want to migrate them to Supabase Storage:

```bash
python manage.py migrate_to_supabase
```

This command will:

1. Find all images in local media directories
2. Upload them to Supabase Storage bucket
3. Update database records to use Supabase URLs

## Development

### Adding New Features

1. **Backend**: Add new models, views, and serializers in the `users` app or create new Django apps
2. **Frontend**: Add new Vue components in `portfolio/src/components/` or `portfolio/src/views/` and update the router

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

### Deploy to Render.com

This project is configured for easy deployment to Render.com. The following files have been added:

- `Procfile` - Defines the web process for Render
- `render.yaml` - Render configuration file (optional but recommended)
- `requirements.txt` - Updated with gunicorn for production
- `settings.py` - Updated to support dynamic Render domains
- `portfolio/vite.config.js` - Updated with build configuration
- `portfolio/src/api/profile.js` - Updated to support environment variable for API URL

#### Deployment Architecture

You can choose between two deployment approaches:

**Option 1: Single Service (Recommended for simplicity)**

- Django backend serves both the API and the Vue frontend
- Vue frontend is built during the build process (`npm run build`)
- Built static files are served by Django
- API endpoints remain at `/api/`
- Frontend is served at the root path `/`

**Option 2: Separate Services (If already deployed separately)**

- Django backend deployed as one service
- Vue frontend deployed as separate service
- Frontend communicates with backend via environment variable
- More complex setup but allows independent scaling

#### Deployment Steps

**Option 1: Using render.yaml (Recommended)**

1. Push your code to GitHub
2. Go to [render.com](https://render.com) and sign up/login
3. Click "New +" → "Web Service"
4. Connect your GitHub repository
5. Render will detect the `render.yaml` and auto-configure
6. Set the following environment variables in Render dashboard:
   - `SECRET_KEY` - Generate a secure secret key (or let Render auto-generate)
   - `DEBUG` - Set to `False`
   - `ALLOWED_HOSTS` - Set to `*.onrender.com`
   - `SUPABASE_URL` - Your Supabase project URL
   - `SUPABASE_KEY` - Your Supabase anon key
   - `SUPABASE_SERVICE_ROLE_KEY` - Your Supabase service role key
   - `SUPABASE_STORAGE_BUCKET` - Your Supabase storage bucket name (default: images)
   - `DB_NAME` - Database name (postgres)
   - `DB_USER` - Database user (e.g., postgres.your-project-ref)
   - `DB_PASSWORD` - Database password
   - `DB_HOST` - Database host (Supabase pooler URL, e.g., aws-0-region.pooler.supabase.com)
   - `DB_PORT` - Database port (5432)

**Option 2: Separate Services (Vue Frontend)**

1. Push to GitHub
2. Create new Web Service on Render for the frontend
3. Configure:
   - **Root Directory**: `portfolio`
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `dist`
   - **Node Version**: 18 or later (required for Vite 5)
4. Add environment variable:
   - `VITE_API_BASE_URL`: Your Django backend URL (e.g., `https://your-backend-name.onrender.com/api`)
   - `VITE_ADMIN_URL`: Admin CMS URL, if it differs from `/admin`
5. Deploy the service

**Option 2: Manual Configuration (Django Backend)**

1. Push to GitHub
2. Create new Web Service on Render for the backend
3. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn ging_profile_v2.wsgi:application --bind 0.0.0.0:$PORT`
   - **Python Version**: 3.11 or later
4. Add the same environment variables as above
5. Add a post-deploy command: `python manage.py migrate --noinput && python manage.py collectstatic --noinput`

#### Important Notes

**For Single Service:**

- The `SECRET_KEY` will be auto-generated by Render if using render.yaml
- `DEBUG` is set to `False` in production
- Your Supabase credentials must be configured in Render environment variables
- The app will automatically run migrations and collect static files on deployment
- The `ALLOWED_HOSTS` setting automatically includes your Render domain
- The Vue frontend is built during the build process and served by Django
- No need for separate frontend deployment - everything is in one service

**For Separate Services:**

- Deploy Django backend first and get its URL
- Use the backend URL for `VITE_API_BASE_URL` in frontend
- Both services need to be deployed separately
- Frontend will communicate with backend via the configured URLs

#### Getting Supabase Credentials

1. Go to your Supabase project dashboard
2. **Supabase URL**: Available in Project Settings > API
3. **Supabase Keys**: Available in Project Settings > API (anon key and service role key)
4. **Database Credentials**: Available in Project Settings > Database > Connection string
   - Use the "Transaction pooler" or "Session pooler" connection details
   - The pooler URL format: `aws-0-region.pooler.supabase.com`

### General Production Checklist

1. Set `DEBUG=False` in Django settings
2. Use environment variables for sensitive data
3. Configure Supabase PostgreSQL (already configured via environment variables)
4. Set up proper CORS origins
5. Build the Vue frontend: `npm run build`
6. Serve static files through Django or a CDN
7. Use a production WSGI server (Gunicorn, uWSGI)

## License

This project is provided as-is for educational and development purposes.
