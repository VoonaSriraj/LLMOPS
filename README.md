# **QA with Documents using LangChain & AWS Bedrock**

This project implements a **Question-Answering (QA) system** using **LangChain**, **FAISS**, and **AWS Bedrock**. The system allows users to ask questions from uploaded documents (PDFs) and retrieves relevant answers using **Amazon Bedrock's LLM models**.

---

## **🚀 Features**
- **Retrieval-Augmented Generation (RAG)** using **FAISS**
- **Amazon Bedrock Titan Models** for LLM and embeddings
- **Streamlit UI** for user interaction
- **Custom prompt engineering** for better responses
- **Automatic vector store update** for new documents

---

## **📂 Project Structure**
```
LLMOPS/
│── app.py                # Streamlit-based UI for user interaction
│── QA_system/
│   │── ingestion.py       # Data ingestion and FAISS vector store creation
│   │── retrivalandgeneration.py  # LLM interaction & response generation
│── faiss_index/          # Stored FAISS index
│── README.md             # Project documentation
│── requirements.txt      # Dependencies
```

---

## **📚 Libraries Used**
### **Core Dependencies:**
- [LangChain](https://github.com/hwchase17/langchain) - Framework for LLM applications
- [Amazon Bedrock](https://aws.amazon.com/bedrock/) - Serverless AI model inference
- [FAISS](https://github.com/facebookresearch/faiss) - Efficient similarity search for vector embeddings
- [Streamlit](https://streamlit.io/) - Interactive UI for Q&A
- [Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) - AWS SDK for Python

### **Additional Dependencies:**
- `json`, `os`, `sys` - Standard Python libraries

---

## **🛠 Setup Instructions**

### **1️⃣ Clone the Repository**
```sh
git clone https://github.com/your-repo/LLMOPS.git
cd LLMOPS
```

### **2️⃣ Install Dependencies**
```sh
pip install -r requirements.txt
```

### **3️⃣ Configure AWS Credentials**
Ensure that you have access to **AWS Bedrock** and that your credentials are set up:
```sh
aws configure
```

### **4️⃣ Run the Application**
```sh
streamlit run app.py
```

---

## **🔍 Usage**
### **1️⃣ Upload Documents & Update Vector Store**
- Click **"vectors update"** in the sidebar to process new PDFs.

### **2️⃣ Ask Questions**
- Type your question in the input box and press Enter.
- The system retrieves relevant document snippets and generates an answer.

### **3️⃣ Use Llama Model**
- Click **"llama model"** to generate a response from the **Titan model**.

---

## **🛠 Troubleshooting**
### **⚠️ Common Issues**
❌ **AccessDeniedException on Bedrock** → Ensure model access is enabled in AWS Console.
❌ **FAISS Index Not Found** → Run `vectors update` before querying.
❌ **ModuleNotFoundError** → Run `pip install -r requirements.txt`.

---

## **📌 Future Enhancements**
✅ Support for multiple document formats (DOCX, TXT, etc.)
✅ Fine-tuned prompts for better accuracy
✅ Deployment on AWS Lambda or EC2

---

## **📜 License**
This project is licensed under **MIT License**.

---

## **📧 Contact**
📩 **Email:** your.email@example.com  
🐙 **GitHub:** [your-repo](https://github.com/your-repo)

