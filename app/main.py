from typing import Union

from fastapi import FastAPI
import re
import pickle

from app.db import database, Chat

from .settings import CLASSES

app = FastAPI()

model = pickle.load(open('logreg.pkl', 'rb'))

vectorizer = pickle.load(open('log_vectorizer.pkl', 'rb'))

@app.get("/")
async def read_root():
    return await Chat.objects.all()

@app.on_event("startup")
async def startup():
    if not database.is_connected:
        await database.connect()

@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()

@app.get("/generate")
async def generate_answer(question: Union[str, None] = None, language: Union[str, None] = None):
    if question:
        qstn = vectorizer.transform([question])
        probas = sorted(list(zip(model.predict_proba(qstn)[0], model.classes_)), reverse=True)

        return {
            "question": question, 
            'answer1': CLASSES[probas[0][1]], 
            'answer2': CLASSES[probas[1][1]], 
            'answer3': CLASSES[probas[2][1]], 
            'language': language if language else ''
        } 
    else:
        return {
            "question": '', 
            'answer1': '', 
            'answer2': '', 
            'answer3': '', 
            'language': language if language else ''
        } 
    
@app.post("/answers/")
async def create_item(answers: Chat):
    
    return await Chat.objects.get_or_create(
        question=answers.question,
        answer1=answers.answer1,
        answer2=answers.answer2,
        answer3=answers.answer3,
        real_answer=answers.real_answer,
        language=answers.language
    )