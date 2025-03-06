# Chain of Prompts and Memories in Large Language Models: Augmented Symbolic Legal Reasoning for Accessibility

This repository contains the support material for the paper *Chain of Prompts and Memories in Large Language Models: Augmented Symbolic Legal Reasoning for Accessibility*.

This guide provides instructions for setting up and running a [Cheshire Cat AI](https://cheshirecat.ai/) instance using Docker Compose, as well as accessing Jupyter Notebooks included in this repository.

## Prerequisites  

Ensure you have the following installed on your system:  

- **Docker**: [Installation Instructions](https://docs.docker.com/get-docker/)  
- **Docker Compose**: [Installation Instructions](https://docs.docker.com/compose/install/)

## Setup Instructions  

### 1. Clone This Repository  

```bash
git clone https://github.com/copmAI/AISOC25.git
cd AISOC25
```

### 2. Start the services

Run the following command in the project directory to start the services using Docker Compose:  

```bash
docker compose up -d
```  

### 3. Install Cheshire Cat Plugins

Once the services are running, install these plugins in the **Cheshire Cat Admin Panel** (`http://localhost:1865/admin/plugins`):

1. **Rabbithole Segmentation** – Allows segmentation of documents and URLs for multi-user environments.
2. **Cheshire Cat Prompt Settings** – Enables customization of default prompt settings.

### 4. Run the Notebooks  

Open JupyterLab in your browser:

```
http://localhost:8888
```

 Open either `stipula.ipynb` or `crossjustice.ipynb`. These notebooks contain the prompts and details for the two case studies presented in the paper.

Locate the `KEY` variable inside the notebook. Replace its value with your own OpenAI API key:  

```python
KEY = "your-openai-api-key-here"
```

   Without this key, the notebook will not be able to interact with the OpenAI API.  

Execute all cells sequentially to explore the case studies.

### 5. Stop the services

To stop the running services, use:  

```bash
docker compose down
```

This will stop and remove the containers without deleting volumes or stored data.

