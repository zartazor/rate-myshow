# Deployment (Render + Supabase)

This guide is optional for now. The project is ready for localhost, and you can use these steps later when you want to deploy.

## Supabase (PostgreSQL)
1. Create a Supabase project and copy the connection string.
2. Set `DATABASE_URL` in Render to the Supabase connection string.
3. Ensure the database user has permissions to create tables.

## Render
1. Create a new Web Service and connect your GitHub repo.
2. Use the Render blueprint by adding `render.yaml` to the repo.
3. Add environment variables:
   - `DJANGO_SECRET_KEY`
   - `DJANGO_DEBUG=false`
   - `DATABASE_URL`
   - `OMDB_API_KEY`
4. Run migrations from the Render shell:
   - `python manage.py migrate`
5. Create a superuser:
   - `python manage.py createsuperuser`

## Static/Media
- Configure a storage provider if you want persistent media storage.
- For a basic setup, use local storage and `whitenoise` for static files.
