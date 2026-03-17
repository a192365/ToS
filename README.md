# ToS Semantic Search & Clause Classification

## Objective

This project was developed as part of a technical assessment focused on analyzing **Terms of Service (ToS)** using machine learning techniques.

The objective is to build a system capable of:

- retrieving clauses similar to a user’s concern
- identifying potentially unfair clauses

The dataset is associated with the Unfair Terms of Service (ToS) dataset and the related article provided in the assessment. It contains clauses extracted from real companies' ToS documents.

For this implementation, the data is organized as follows:

```text
data/ToS/Sentences/
data/ToS/Labels/
```

- each file represents a company
- sentences and labels are aligned line by line
- the same filename in both folders corresponds to the same company

The final tool includes two main components:

1. **Semantic Search**  
   Retrieves clauses similar to a given query.

2. **Clause Classification**  
   Estimates whether a clause may be potentially unfair.

---

## Architecture

```text
                ┌──────────────────────┐
                │       Dataset        │
                │  Sentences + Labels  │
                └──────────┬───────────┘
                           │
                           ▼
                  ┌────────────────┐
                  │  Data Loader   │
                  └───────┬────────┘
                          │
                          ▼
           ┌────────────────────────────────┐
           │     Sentence Embeddings        │
           │  (SentenceTransformers model)  │
           └───────────────┬────────────────┘
                           │
                           ▼
                  ┌────────────────┐
                  │  FAISS Index   │
                  └───────┬────────┘
                          │
          ┌───────────────┴───────────────┐
          ▼                               ▼
┌────────────────────┐         ┌──────────────────────┐
│   Semantic Search  │         │  Clause Classifier   │
│ similarity search  │         │ Logistic Regression  │
└──────────┬─────────┘         └──────────┬───────────┘
           │                              │
           └──────────────┬───────────────┘
                          ▼
                 ┌────────────────┐
                 │    FastAPI     │
                 │   API layer    │
                 └───────┬────────┘
                         │
                         ▼
                 ┌────────────────┐
                 │   Streamlit    │
                 │      UI        │
                 └────────────────┘
```

---

## Project Structure

```text
tos_simple_project/
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── loader.py
│   ├── embedder.py
│   ├── search_engine.py
│   ├── classifier.py
│   ├── schemas.py
│   └── streamlit_app.py
├── scripts/
│   ├── build_index.py
│   └── train_classifier.py
├── notebooks/
│   └── eda_validation.ipynb
├── data/
│   └── ToS/
│       ├── Sentences/
│       └── Labels/
├── models/
│   ├── faiss.index
│   ├── metadata.pkl
│   └── classifier.pkl
├── .streamlit/
│   └── config.toml
├── Dockerfile
├── Dockerfile_ui
├── docker-compose.yml
├── .dockerignore
├── requirements.txt
└── README.md
```

---

## Dataset Setup

The dataset must be placed under:

```text
data/ToS/Sentences/
data/ToS/Labels/
```

For this version of the project, only these two folders are used.

- `Sentences/` contains the clauses
- `Labels/` contains the corresponding labels

Each file corresponds to a company, and sentences are aligned with labels by index.

---

## Run

### Run locally

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Build the vector index and train the classifier:

```bash
python -m scripts.build_index
python -m scripts.train_classifier
```

Run the API:

```bash
python -m uvicorn src.main:app --reload
```

Open:

- `http://127.0.0.1:8000/docs`

In another terminal, activate the environment again and run the UI:

```bash
source venv/bin/activate
python -m streamlit run src/streamlit_app.py
```

Open:

- `http://localhost:8501`

### Run with Docker

Build the images:

```bash
docker build -t tos-api-test -f Dockerfile .
docker build -t tos-ui-test -f Dockerfile_ui .
```

Run the API container:

```bash
docker run -p 8000:8000 tos-api-test
```

Run the UI container:

```bash
docker run -p 8501:8501 -e API_URL=http://host.docker.internal:8000 tos-ui-test
```

Open:

- `http://localhost:8000/docs`
- `http://localhost:8501`

---

## API Endpoints

### `POST /search`

Semantic search over clauses.

Example request:

```json
{
  "query": "we may terminate your account without notice",
  "top_k": 5
}
```

### `POST /classify`

Clause classification.

Example request:

```json
{
  "text": "we may terminate your account without notice"
}
```

---

## User Interface

### What this tool does? 

This tool helps users explore Terms of Service clauses in two ways:

1. **Semantic Search**  
   Retrieves clauses from Terms of Service documents that are semantically similar to a user’s query. Each result includes the originating company, a similarity score indicating how closely the clause matches the query, and a classification indicating whether the clause is potentially unfair based on the annotated dataset.

2. **Clause Classification**  
   Estimates whether a clause may be potentially unfair and provides the probability of it being unfair.

Further explanations are available in the UI and in the user manual (PDF).

---

## Notebook

The project includes an exploratory notebook:

```text
notebooks/eda_validation.ipynb
```

It contains:

- dataset analysis
- label distribution
- company-level insights
- validation experiments
- retrieval examples

### User Manual — Clause Risk Detector

Clause Risk Detector is a tool designed to analyze Terms of Service (ToS) clauses through two main functionalities: **Semantic Search** and **Clause Classification**. Semantic Search allows users to input a clause or concern and retrieve similar clauses from real companies, including their source, similarity score, and dataset label. The score indicates how close the result is to the query (**lower score = more similar**). Clause Classification allows users to input a clause and receive a prediction (potentially unfair or not) along with a probability indicating how likely the clause is to be unfair (**higher percentage = higher risk**). The tool is intended for exploratory analysis and does not replace legal review.

In practice, users can first use Semantic Search to explore how similar clauses appear across different companies, and then use Clause Classification to assess the potential risk of a specific clause. The two components complement each other: search provides context and comparison, while classification provides a risk estimate. Results should be interpreted as guidance, especially in borderline cases where the model may show uncertainty.