# 🚀 AI-Chatbot-NLP

AI-Chatbot-NLP is a customer-support chatbot powered by natural language processing, Qwen LLMs, and retrieval-augmented generation (RAG). The system combines a vector-based FAQ knowledge base with a conversational interface built using Gradio, enabling users to ask questions and receive accurate, TNG-related responses. Knowledge retrieval is handled via ChromaDB with BGE-M3 embeddings, ensuring the chatbot provides context-aware answers grounded in real FAQ data.

---

## 🛠️ Tech Stack

* **Python**
* **Qwen LLM (DashScope API)**
* **ChromaDB** for vector storage
* **BGE-M3 embeddings** (via Ollama)
* **Gradio** for the chatbot UI
* **Pandas** for FAQ dataset processing
* **JSON-based knowledge storage**
* **Excel/CSV FAQ ingestion**

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

Open a second terminal:

```bash
chroma run --path ./chroma_storage --port 8899
```

### 5. Build the vector knowledge base (only once)

```bash
python knowledge_base/vector_db.py
```

### 6. Launch the chatbot

```bash
python gradio_app.py
```

Open the Gradio URL printed in your terminal (e.g., `http://127.0.0.1:7860`).

---

## 💬 Usage

Simply enter a question related to Touch 'n Go services.
The chatbot will:

1. Check input safety
2. Retrieve the most relevant FAQ entries via ChromaDB
3. Generate a final answer using Qwen LLM
4. Display the result in the Gradio chat UI

Example queries:

* *"How do I reset my TNG eWallet password?"*
* *"Why is my RFID not working?"*
* *"How can I check my transaction history?"*

---

## 📁 Project Structure

```
AI-Chatbot-NLP/
├── agent/
│   └── chatbot.py            # Main chatbot workflow logic
│
├── knowledge_base/
│   ├── data/                 # FAQ datasets (Excel/CSV)
│   ├── vector_db.py          # Vector DB creation and ingestion
│   └── embeddings/           # Embedding configuration (BGE-M3)
│
├── assets/                   # Images and UI assets
├── gradio_app.py             # Gradio web interface
├── requirements.txt
└── README.md
```
