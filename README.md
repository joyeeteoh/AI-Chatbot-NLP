# 🚀 AI-Chatbot-NLP

AI-Chatbot-NLP is a customer-support chatbot powered by natural language processing, Qwen large language models, and retrieval-augmented generation (RAG). The system combines a vector-based FAQ knowledge base derived from official Touch 'n Go (TnG) FAQ content—compiled into an Excel file (`en_faq.xlsx`)—with a conversational interface built using Gradio. FAQ entries are embedded using the BGE-M3 embedding model via Ollama and stored in ChromaDB, enabling cosine-similarity retrieval of the most relevant knowledge to support accurate and context-aware responses.

---

## 🛠️ Tech Stack

* **Python**
* **Qwen-Turbo** (DashScope API) for real-time production responses
* **Qwen2.5-7B** (Ollama) for offline development, evaluation, and testing
* **ChromaDB** for vector storage and similarity search
* **BGE-M3 embeddings** (via Ollama)
* **Gradio** for the chatbot web interface
* **Pandas** for FAQ dataset processing
* **JSON-based knowledge representation**
* **Excel/CSV** for FAQ ingestion

---

## 📦 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/joyeeteoh/AI-Chatbot-NLP.git
cd AI-Chatbot-NLP
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API keys

Create a `.env` file in the project root:

```
ALIYUN_API_KEY=Bearer <your-dashscope-api-key>
```

Get your API key from: [https://dashscope.aliyun.com/apiKey](https://dashscope.aliyun.com/apiKey)

### 4. Start ChromaDB

Open a second terminal and run:

```bash
chroma run --path ./chroma_storage --port 8899
```

### 5. Build the vector knowledge base (run once)

Ensure the FAQ file `knowledge_base/data/en_faq.xlsx` exists, then execute:

```bash
python knowledge_base/vector_db.py
```

This step loads the FAQ data, generates BGE-M3 embeddings, and stores them in ChromaDB.

### 6. Launch the chatbot

```bash
python gradio_app.py
```

Open the Gradio URL printed in the terminal (e.g., `http://127.0.0.1:7860`).

---

## 💬 Usage

Users can enter questions related to Touch 'n Go services via the Gradio interface. The chatbot follows this workflow:

1. **Input Safety Filtering** – User input is first evaluated by Qwen-Turbo to detect malicious or inappropriate content.
2. **Knowledge Retrieval** – The system retrieves the top-5 most relevant FAQ entries from ChromaDB using cosine similarity over BGE-M3 embeddings.
3. **Response Generation** – The retrieved knowledge is injected as context into the language model to generate an accurate, grounded response.
4. **Response Display** – The final answer is displayed in the Gradio chat interface.

Example queries:

* *"How do I reset my TNG eWallet password?"*
* *"Why is my RFID not working?"*
* *"How can I check my transaction history?"*

---

## 📁 Project Structure

```
AI-Chatbot-NLP/
├── agent/
│   └── chatbot.py            # Core chatbot workflow and RAG logic
│
├── knowledge_base/
│   ├── data/                 # FAQ datasets (en_faq.xlsx)
│   ├── vector_db.py          # Vector DB creation and ingestion pipeline
│   └── embeddings/           # Embedding configuration (BGE-M3 via Ollama)
│
├── assets/                   # Images and UI assets
├── gradio_app.py             # Gradio web interface
├── requirements.txt
└── README.md
```
