# **Question-Answering with Documents using LangChain & AWS Bedrock** 🎯📜🤖

This project is a **Question-Answering (QA) system** that leverages **LangChain**, **FAISS**, and **AWS Bedrock** to enable users to query uploaded documents (PDFs) and retrieve precise answers using **Amazon Bedrock's large language models (LLMs)**. 📄💡🧠

---

## **🚀 Key Features** ⚡📌🛠️

- **Retrieval-Augmented Generation (RAG)** powered by **FAISS**
- **Amazon Bedrock Titan Models** for embeddings and LLM responses
- **Streamlit UI** for an intuitive user experience
- **Custom prompt engineering** to enhance answer relevance
- **Automatic vector store updates** for newly uploaded documents

---

## **📂 Project Structure** 🏗️📁📜

```
LLMOPS/
│── app.py                # Streamlit-based UI for user interaction
│── QA_system/
│   │── ingestion.py       # Handles data ingestion and FAISS vector store creation
│   │── retrivalandgeneration.py  # Manages LLM interaction and response generation
│── faiss_index/          # Directory for storing FAISS index
│── README.md             # Project documentation
│── requirements.txt      # List of dependencies
```

---

## **📚 Required Libraries** 📖📦⚙️

### **Core Dependencies:**

- [LangChain](https://github.com/hwchase17/langchain) - Framework for building LLM applications
- [Amazon Bedrock](https://aws.amazon.com/bedrock/) - Serverless AI model inference service
- [FAISS](https://github.com/facebookresearch/faiss) - Efficient similarity search for vector embeddings
- [Streamlit](https://streamlit.io/) - Web-based UI framework for user interactions
- [Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) - AWS SDK for Python integration

### **Additional Dependencies:**

- Standard Python libraries: `json`, `os`, `sys`

---

## **🛠 Setup Instructions** ⚙️💻📌

### **1️⃣ Clone the Repository** 🖥️📂🔽

```sh
git clone https://github.com/your-repo/LLMOPS.git
cd LLMOPS
```

### **2️⃣ Install Dependencies** 📥📦⚙️

```sh
pip install -r requirements.txt
```

### **3️⃣ Configure AWS Credentials** 🔑🔒☁️

Ensure that you have access to **AWS Bedrock** and that your credentials are properly configured:

```sh
aws configure
```

### **4️⃣ Launch the Application** 🚀📜🖥️

```sh
streamlit run app.py
```

---

## **🔍 How to Use** 📜❓🤖

### **1️⃣ Upload Documents & Update the Vector Store** 📂📤🔄

- Click **"Vectors Update"** in the sidebar to process and index new PDFs.

### **2️⃣ Ask a Question** 📝❔🤖

- Enter a question in the text box and press Enter.
- The system retrieves relevant document snippets and generates an accurate response.

### **3️⃣ Use the Llama Model** 🦙📡💬

- Click **"Llama Model"** to generate a response using the **Titan model**.

---

## **📌 Future Enhancements** 🌟🚀🔮

✅ Expand support for multiple document formats (DOCX, TXT, etc.)\
✅ Improve prompt engineering for enhanced accuracy\
✅ Deploy the application on **AWS Lambda** or **EC2**

---

## **📜 License** 📄⚖️🔗

This project is licensed under the **MIT License**.

---

## **📧 Contact Information** 📬📩🌍

📩 **Email:** [Voona Sriraj](mailto\:srirajvoona2004@gmail.com)\
🐙 **GitHub:** [github-repo]([https://github.com/your-repo](https://github.com/VoonaSriraj/LLMOPS))

