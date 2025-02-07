# Ghanili
Arabic Lyrics Search Egnine

# Building Locally
```bash
docker build -t ghanili .
docker run -p 8080:8080 ghanili
```

# Docker Image
```bash
docker pull abdulrahmantabaza/ghanili:latest
docker run -p 8080:8080 abdulrahmantabaza/ghanili:latest
```

Then headover to `http://localhost:8080/`

# Development Context
1. Lyrics are scraped from `http://fnanen.com/`, they contain over 18K songs, while the site does a tremendous effort curating lyrics, songs and metadata, I would like a more complete collection, with options to add songs and make them searchable.
2. The search is a simple [BM25](https://github.com/xhluca/bm25s) baseline, with lucene default parameters, and [Tashaphyne](https://github.com/linuxscout/tashaphyne) as the stemmer, I also use this [stopword list](https://github.com/linuxscout/arabicstopwords), the preprocessing pipeline is simple enough, and can be reviewed in `notebooks/eda.ipynb`.
3. I would like some sort of click data streaming, and eventually, an LTR model, and semantic search, to experiment with preprocessing and more search methodologies other than lexical.
4. The frontend for this is a static HTML file, with Tailwind CSS and htmx, the backend is a FastAPI endpoint, with Jinja templating.
5. The system is static, it loads both search index and the indexed raw data from files on disk. You can't add new data to the system, although that's always the end goal.
6. The system has realtime search as you type, and the docker image is optimized at around ~500mbs, making it extremely lightweight overall.
7. I will open source the scraper as well, once I clear that what I did wasn't illegal or unethical, I actually respect the effort that went into the site I scraped.
8. I would eventually like to have multiple modality search options, such as similar songs by audio, similar songs by lyrical themes, but right now I'm focusing on lyrics search.
