from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
import pickle
from sqlalchemy.orm import Session
from . import schemas, models, token_1, oauth2
from .database import engine, SessionLocal
from .hashing import Hash

models.Base.metadata.create_all(engine)

books_songs_data = pickle.load(open('src/books_songs_data.pkl', 'rb'))
similarity_score = pickle.load(open('src/cosine_similarity.pkl', 'rb'))

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post('/register')
def register_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(username=request.username, email=request.email, password= Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()

    db.refresh(new_user)
    return new_user


@app.post('/login')
def login(request:OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid Credentials")
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Incorrect password")

    access_token = token_1.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get('/all_books')
def get_all_books (db : Session = Depends(get_db), get_current_user:schemas.User = Depends(oauth2.get_current_user)):
    books = db.query(models.Books).all()
    return books


@app.get('/all_songs')
def get_all_songs (db : Session = Depends(get_db), get_current_user:schemas.User = Depends(oauth2.get_current_user)):
    songs = db.query(models.Songs).all()
    return songs


@app.post("/recommend_books/{song}")
def recommend(song):
    track_id = books_songs_data[books_songs_data['Track-Name'] == song]['Id'].values[0]
    similar_items = sorted(list(enumerate(similarity_score[track_id])), key=lambda x:x[1], reverse=True)[1:6]
    
    data = []
    items = []
    for item in similar_items:
        book_title = books_songs_data[books_songs_data['Id'] == item[0]]['Book-Title'].values[0]
        temp_df = books_songs_data[books_songs_data['Book-Title'] == book_title]
        items.append(temp_df.drop_duplicates('Book-Title')['Book-Title'].values[0])
        items.append(temp_df.drop_duplicates('Book-Title')['Book-Author'].values[0])
        
    for i in range (5):
        dict = {'name' : items[i], 'author' : items[i+1]}
        data.append(dict)
        
    return data

