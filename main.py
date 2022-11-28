from fastapi import FastAPI, Depends, HTTPException
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from typing import List

import schemas
import models
import uvicorn

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# refresh databasenya
def migrate_table():
    return models.Base.metadata.create_all(bind=engine)

@app.post('/user')
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(username=request.username, password=request.password, email=request.email)
    db.add(new_user)
    db.commit()

    db.refresh(new_user)
    return new_user


@app.get('/user', response_model = List[schemas.UserView])
def get_user(db: Session = Depends(get_db)):
    return db.query(models.User).all()

# Delete
# Use 204 when do something to database but no content to be returned
@app.delete('/blog/{id}', status_code=204, tags=['Blogs'])
def destroy(id, db: Session = Depends(get_db)):
	blog = db.query(models.Blog).filter(models.Blog.id == id)
	if not blog.first():
		raise HTTPException(status_code=404, detail=f'Blog with ID {id} not found.')
	blog.delete(synchronize_session=False)
	db.commit()
	# Note: If the status_code is 204, it is fine to not return anything
	# return f'Blog with ID {id} h

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)