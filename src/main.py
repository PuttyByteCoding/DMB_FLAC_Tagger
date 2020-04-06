from fastapi import FastAPI
import uvicorn
from database import engine, metadata
from routers import venues, setlists, songs, concerts, concert_dirs, guests, tapers, recording_types

metadata.create_all(engine)
conn = engine.connect()

app = FastAPI()
app.include_router(venues.router)
app.include_router(setlists.router)
app.include_router(songs.router)
app.include_router(concerts.router)
app.include_router(concert_dirs.router)
app.include_router(guests.router)
app.include_router(tapers.router)
app.include_router(recording_types.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == '__main__':
    # uvicorn.run(app, host='127.0.0.1', port=6666)
    uvicorn.run(app, port=9999)
