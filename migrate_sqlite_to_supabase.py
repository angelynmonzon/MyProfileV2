"""
Helper script to migrate data from the local SQLite database to Supabase PostgreSQL.

Prerequisites:
- .env file contains real DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
- psycopg2-binary is installed: pip install psycopg2-binary==2.9.9
- The SQLite file db.sqlite3 exists in the project root

Usage:
    python migrate_sqlite_to_supabase.py
"""
import os
import subprocess
import sys
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent

# Load environment variables
load_dotenv(BASE_DIR / '.env')

REQUIRED_DB_VARS = ['DB_NAME', 'DB_USER', 'DB_PASSWORD', 'DB_HOST']
DUMP_FILE = BASE_DIR / 'data_dump.json'


def check_env():
    """Ensure Supabase database credentials are present."""
    missing = [var for var in REQUIRED_DB_VARS if not os.environ.get(var)]
    if missing:
        print(f"Error: Missing environment variables: {', '.join(missing)}")
        print("Please add the Supabase database credentials to your .env file.")
        sys.exit(1)


def sqlite_file_exists():
    """Check if the SQLite database file exists."""
    sqlite_path = BASE_DIR / 'db.sqlite3'
    if not sqlite_path.exists():
        print(f"Warning: {sqlite_path} not found. Skipping SQLite dump.")
        return False
    return True


def run_django_command(args, env=None, stdout=None):
    """Run a Django management command using the current Python interpreter."""
    cmd = [sys.executable, 'manage.py'] + args
    subprocess.run(cmd, cwd=BASE_DIR, env=env, stdout=stdout, check=True)


def dump_sqlite_data():
    """Dump all data from SQLite while ignoring PostgreSQL env variables."""
    print("Dumping data from SQLite (db.sqlite3)...")
    # Use a dedicated settings module that forces SQLite so manage.py does not
    # re-read DB_* variables from the .env file in the child process.
    env = os.environ.copy()
    for key in ['DB_NAME', 'DB_USER', 'DB_PASSWORD', 'DB_HOST', 'DB_PORT']:
        env.pop(key, None)
    env.pop('DATABASE_URL', None)

    with open(DUMP_FILE, 'w', encoding='utf-8') as f:
        run_django_command(
            [
                'dumpdata',
                '--settings=ging_profile_v2.sqlite_settings',
                '--natural-primary',
                '--natural-foreign',
                '--all',
                '--indent',
                '2',
            ],
            env=env,
            stdout=f,
        )
    print(f"SQLite data dumped to {DUMP_FILE}")


def migrate_postgres():
    """Run migrations on the Supabase PostgreSQL database."""
    print("Running migrations on Supabase PostgreSQL...")
    run_django_command(['migrate'])
    print("Migrations completed.")


def load_data_into_postgres():
    """Load dumped data into Supabase PostgreSQL."""
    print("Loading data into Supabase PostgreSQL...")
    run_django_command(['loaddata', str(DUMP_FILE)])
    print("Data loaded successfully.")


def main():
    check_env()

    if sqlite_file_exists():
        dump_sqlite_data()
    else:
        print("No SQLite dump to load.")
        return

    migrate_postgres()
    load_data_into_postgres()

    print("\nMigration complete!")
    print("You can now create a superuser if needed:")
    print("    python manage.py createsuperuser")
    print(f"\nYou may delete the dump file when finished: {DUMP_FILE}")


if __name__ == '__main__':
    main()
