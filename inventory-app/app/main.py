from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import Optional
import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_CONTAINER"),
        port=os.getenv("POSTGRES_PORT"),
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )

class Movie(BaseModel):
    title: str
    description: str

class MovieUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/api/movies")
def get_movies(title: Optional[str] = Query(None)):
    try:
        conn = get_db_connection()
        
        cursor = conn.cursor()
        
        if title:
            cursor.execute(
                "SELECT id, title, description FROM inventory WHERE title ILIKE %s",
                (f"%{title}%",)
            )
        else:
            cursor.execute("SELECT id, title, description FROM inventory")
        
        movies = cursor.fetchall()
        result = []
        for movie in movies:
            result.append({
                "id": movie[0],
                "title": movie[1],
                "description": movie[2]
            })
        
        cursor.close()
        conn.close()
        
        return result
        
    except Exception as e:
        return {"error": str(e)}

@app.post("/api/movies")
def create_movie(movie: Movie):
    try:
        conn = get_db_connection()
        
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO inventory (title, description) VALUES (%s, %s) RETURNING id",
            (movie.title, movie.description)
        )
        
        movie_id = cursor.fetchone()[0]
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return {"id": movie_id, "title": movie.title, "description": movie.description}
        
    except Exception as e:
        return {"error": str(e)}

@app.delete("/api/movies")
def delete_all_movies():
    try:
        conn = get_db_connection()
        
        cursor = conn.cursor()
        cursor.execute("DELETE FROM inventory")
        deleted_count = cursor.rowcount
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return {"message": f"Deleted {deleted_count} movies"}
        
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/movies/{movie_id}")
def get_movie(movie_id: int):
    try:
        conn = get_db_connection()
        
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, title, description FROM inventory WHERE id = %s",
            (movie_id,)
        )
        
        movie = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if movie:
            return {"id": movie[0], "title": movie[1], "description": movie[2]}
        else:
            return {"error": "Movie not found"}
        
    except Exception as e:
        return {"error": str(e)}

@app.put("/api/movies/{movie_id}")
def update_movie(movie_id: int, movie_update: MovieUpdate):
    try:
        conn = get_db_connection()
        
        cursor = conn.cursor()
        
        # Check if the movie exists
        cursor.execute("SELECT id FROM inventory WHERE id = %s", (movie_id,))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            return {"error": "Movie not found"}
        
        update_fields = []
        update_values = []
        
        if movie_update.title:
            update_fields.append("title = %s")
            update_values.append(movie_update.title)
        
        if movie_update.description:
            update_fields.append("description = %s")
            update_values.append(movie_update.description)
        
        if not update_fields:
            cursor.close()
            conn.close()
            return {"error": "No fields to update"}
        
        update_values.append(movie_id)
        
        cursor.execute(
            f"UPDATE inventory SET {', '.join(update_fields)} WHERE id = %s RETURNING id, title, description",
            update_values
        )
        
        updated_movie = cursor.fetchone()
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return {"id": updated_movie[0], "title": updated_movie[1], "description": updated_movie[2]}
        
    except Exception as e:
        return {"error": str(e)}

@app.delete("/api/movies/{movie_id}")
def delete_movie(movie_id: int):
    try:
        conn = get_db_connection()
        
        cursor = conn.cursor()
        cursor.execute("DELETE FROM inventory WHERE id = %s", (movie_id,))
        
        if cursor.rowcount == 0:
            cursor.close()
            conn.close()
            return {"error": "Movie not found"}
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return {"message": f"Movie {movie_id} deleted"}
        
    except Exception as e:
        return {"error": str(e)}
