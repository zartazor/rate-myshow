# RateMyShow

RateMyShow is a movie and TV show rating platform built with Django 5.x. It uses the OMDB API for title data, provides a modern dark UI, and supports ratings, reviews, watchlists, and personalized recommendations.

## Features
- Email-based authentication with verification
- Trending, popular, top lists, and personalized recommendations
- Global search with live results
- Title detail pages with reviews and ratings
- Watchlist, watched history, and activity feed
- Hybrid recommendations (content-based + collaborative)
- Responsive, mobile-first UI with dark mode

## Local Setup
1. Create a virtual environment and install dependencies:
   - `python -m venv .venv`
   - `./.venv/Scripts/activate`
   - `pip install -r requirements.txt`
2. Copy the example env file:
   - `copy .env.example .env`
3. Set `DATABASE_URL` to your local Postgres or Supabase connection string.
4. Run migrations and create a superuser:
   - `python manage.py migrate`
   - `python manage.py createsuperuser`
5. Start the dev server:
   - `python manage.py runserver`

## Screenshots
- Home page: (add screenshot)
- Title detail: (add screenshot)
- Profile: (add screenshot)

## Notes
- The default OMDB key is included for local testing. Replace it for production.
- The deployment guide is provided in deployment.md, but you can focus on localhost until ready.
