from typing import Annotated

import json
import bm25s
import arabicstopwords.arabicstopwords as stp
from tashaphyne.stemming import ArabicLightStemmer
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

ArListem = ArabicLightStemmer()
stemmer = lambda x: [ArListem.light_stem(x_) for x_ in x]
stopwords = stp.stopwords_list()
lyrics = json.load(open("../data/songs_with_lyrics_no_error_message.json"))

retriever = bm25s.BM25.load("../lyrics_index", load_corpus=True)


def retrieve_bm25(query, k=5):
    query_tokens = bm25s.tokenize(
        query, stemmer=stemmer, stopwords=stopwords, show_progress=False
    )
    results, scores = retriever.retrieve(query_tokens, k=k, show_progress=False)
    scores = scores.squeeze().tolist()
    results = results.squeeze().tolist()
    filtered_results = [
        result for result, score in list(zip(results, scores)) if score > 0
    ]
    songs = [lyrics[result] for result in filtered_results]
    return songs


app = FastAPI()
app.mount("/static", StaticFiles(directory="static", html=True), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=FileResponse, tags=["home"])
async def home_page():
    return FileResponse("static/home.html")


@app.post("/lyrics", response_class=HTMLResponse)
async def read_item(request: Request, query: Annotated[str, Form()]):
    print("Query: ", query)
    print("Stemmed Query: ", ArListem.light_stem(query))
    results = retrieve_bm25(query=query, k=10)
    return templates.TemplateResponse(
        request=request,
        name="display_results.html",
        context={"request": request, "results": results},
    )
