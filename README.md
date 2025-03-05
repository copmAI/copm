# Chain of Prompts and Memories in Large Language Models: Augmented Symbolic Legal Reasoning for Accessibility

This repository contains the support material for the paper *Chain of Prompts and Memories in Large Language Models: Augmented Symbolic Legal Reasoning for Accessibility*.

This guide provides instructions for setting up and running a [Cheshire Cat AI](https://cheshirecat.ai/) instance using Docker Compose, as well as accessing Jupyter Notebooks included in this repository.

## Prerequisites  

Ensure you have the following installed on your system:  

- **Docker**: [Installation Instructions](https://docs.docker.com/get-docker/)  
- **Docker Compose**: [Installation Instructions](https://docs.docker.com/compose/install/)
- **Python (3.8+)**: [Installation Instructions](https://www.python.org/downloads/)

## Setup Instructions  

### 1. Clone This Repository  

```bash
git clone https://github.com/copmAI/AISOC25.git
cd AISOC25
```

### 2. Start the Cheshire Cat AI Service  

Run the following command in the project directory to start the service using Docker Compose:  

```bash
docker compose up -d
```

To view logs:  

```bash
docker compose logs -f
```

To stop the running Cheshire Cat AI, use:  

```bash
docker compose down
```

This will stop and remove the containers without deleting volumes or stored data.  

### 3. Access the Cheshire Cat Admin Panel  

Once the service is running, open your browser and go to:  

```
http://localhost:1865/admin
```

Here, you can configure language models, embeddings, and other settings.  

### 4. Configure the Embedder  

To use `intfloat/multilingual-e5-large` as the embedder:  

1. Open the **Admin Panel** (`http://localhost:1865/admin`).  
2. Navigate to **Settings** → **Embedder**.  
3. Select **Qdrant FastEmbed (Local)** as the embedder type.  
4. Enter the following model name:  

   ```
   intfloat/multilingual-e5-large
   ```

5. Save the settings and restart the service if needed.

### 5. Install and Configure Plugins  

To optimize Cheshire Cat AI, install these plugins in the **Admin Panel** (`http://localhost:1865/admin/plugins`):

1. **Core CCat** – (Pre-installed, no action needed)
2. **Rabbithole Segmentation** – Allows segmentation of documents and URLs for multi-user environments.
3. **Cheshire Cat Prompt Settings** – Enables customization of default prompt settings.
4. **Dietician** – Prevents redundant document ingestion and supports declarative memory updates.

### 5. Run Jupyter Notebooks  

To run the provided Jupyter Notebooks locally inside a virtual environment:  

### **Install JupyterLab and Setup a Virtual Environment**  

1. Install `pipx` (required to manage Python tools):  

   ```bash
   sudo apt install pipx
   pipx ensurepath
   ```

2. Install JupyterLab using `pipx`:  

   ```bash
   pipx install jupyterlab
   ```

3. Create and activate a virtual environment:  

   ```bash
   python -m venv my-env
   source my-env/bin/activate
   ```

4. Install `ipykernel` and required dependencies:  

   ```bash
   pip install ipykernel
   ```

5. Create a Jupyter kernel for the virtual environment:  

   ```bash
   python -m ipykernel install --user --name=my-env
   ```

6. Launch JupyterLab:  

   ```bash
   jupyter-lab
   ```

Here's the updated **Run the Notebooks** section with more details about setting the OpenAI key and the available notebooks:  

---

### **Run the Notebooks**  

1. **Launch JupyterLab**  
   - Open JupyterLab in your browser. 

2. **Open a Notebook**  
   - Open either `stipula.ipynb` or `crossjustice.ipynb`.  
   - These notebooks contain the prompts and details for the two case studies presented in the paper.

3. **Set Up the OpenAI API Key**  
   - Locate the `KEY` variable inside the notebook.  
   - Replace its value with your own OpenAI API key:  

     ```python
     KEY = "your-openai-api-key-here"
     ```

   - Without this key, the notebook will not be able to interact with the OpenAI API.  

4. **Select the Correct Kernel**  
   - From the **Kernel** menu, choose **Change Kernel**.  
   - Select `my-env` to ensure the correct virtual environment is used.  

5. **Run the Notebook**  
   - Execute all cells sequentially to interact with Cheshire Cat AI and explore the case studies.  
