AI-Assisted Element Classification
This project uses a simple machine learning model to identify key parts of a news article on the Yogonet website:

- Title

- Kicker (short subtitle or category)

- Link

- Image

How It Works
Element Extraction:
The scraper uses BeautifulSoup to extract HTML elements such as <a>, <p>, <h2>, <div>, and <span>.

AI Prediction:
Each element is passed to the AIPredictor, which uses a pre-trained scikit-learn model (stored as model_assets/element_classifier.pkl) to classify the element based on its text content.

Output:
Based on the model's prediction, the element is assigned to one of the article fields (title, kicker, link, image).

Model Training (Offline Step)
The AI model was trained using a labeled dataset of HTML element text and their corresponding type. Here’s a simplified overview:

Input: Cleaned text from HTML elements.

Labels: ["title", "kicker", "link", "image", "unknown"]

Vectorization: Using TfidfVectorizer on the text content.

Model: A simple LogisticRegression classifier inside a Pipeline.

Benefits
The model adds flexibility to adapt to layout changes.

It can generalize better than hard-coded selectors (div.class > span > h2).


🧠 Note on AI Model Accuracy:
The AI-based scraper is still under development and may not yield 100% accurate results due to limited training data.
For improved reliability while the model continues to evolve, you can switch to the non-AI version by modifying the import in main.py:

Replace:

from app.scraper import scrape_yogonet

With:

from app.scraper_sin_ai import scrape_yogonet

------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------

🐳 Running the Project with Docker
This project is containerized using Docker to ensure consistent execution across environments.

🧾 Prerequisites
Before you begin, make sure you have the following installed on your system:

Docker
Docker Compose

📁 Folder Structure (Important)
bash
Copiar
Editar
.
├── Dockerfile
├── docker-compose.yml
├── main.py
├── requirements.txt
├── secrets/
│   └── bq-sa-key.json      # 🔐 Service account for BigQuery
├── .env                    # 🔐 Environment variables
├── model_assets/
│   └── element_classifier.pkl
└── app/                    # Your Python code modules (if any)

⚠️ Make sure .env and secrets/bq-sa-key.json exist and are not committed to version control.

⚙️ Step-by-Step Instructions
1. Clone the repository

git clone https://github.com/your-user/your-repo.git
cd your-repo

2. Create .env file

Example .env:

PROJECT_ID=your-gcp-project-id
BQ_DATASET=your_dataset
BQ_TABLE=your_table
These environment variables are injected into the container and used by the application.

3. Add service account key to secrets/
Place your Google Cloud service account key JSON file at:

secrets/bq-sa-key.json
This is mounted read-only inside the container at /secrets/bq-sa-key.json.

🚀 Build and Run the Container
To build the image and run the service:

docker-compose up --build

This will:

Build the Docker image defined in the Dockerfile

Mount the secrets

Run the main application (python main.py)