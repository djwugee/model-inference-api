
Built by https://www.blackbox.ai

---

# Model Inference API

## Project Overview
The **Model Inference API** is a FastAPI-based backend service designed to facilitate inference operations for machine learning models. The API is set up to load a model from a specified directory and process inference requests both through HTTP and WebSocket communication. It includes mechanisms for loading, unloading, and caching inference results, ensuring efficient operation and resource management.

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Steps
1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. Install the required packages:
   ```bash
   pip install fastapi uvicorn psutil
   ```

3. Ensure you have the model file `flux1-k-dev-q2_k.gguf` located in the `ComfyUI/models/unet` directory.

## Usage

1. Start the FastAPI server by running:
   ```bash
   python model_inference_backend.py
   ```

2. The server will be accessible at `http://localhost:8000`.

3. You can interact with the API through defined endpoints:
   - **List Models**: `GET /models`
   - **Inference with HTTP**: `POST /infer` (send a JSON payload with the prompt and settings)
   - **Inference with WebSocket**: Connect to `ws://localhost:8000/ws/infer` and send a JSON payload with the prompt and settings.

## Features

- **Model Management**: Automatically loads the specified model on server startup and unpacks resources on shutdown.
- **Caching**: Results of inference are cached to optimize repeated requests.
- **Resource Monitoring**: Insights into memory and CPU usage are provided with each inference response.
- **WebSocket Support**: Real-time inference capabilities via WebSocket connections.

## Dependencies
The project depends on the following Python packages, as listed in `requirements.txt`:
```json
{
  "dependencies": {
    "fastapi": "^0.68.1",
    "uvicorn": "^0.15.0",
    "psutil": "^5.8.0"
  }
}
```

## Project Structure
```
.
├── model_inference_backend.py     # FastAPI application for model inference
├── model_inference_frontend.py    # Placeholder for frontend implementation (currently empty)
└── ComfyUI/
    └── models/
        └── unet/
            └── flux1-k-dev-q2_k.gguf # Model file used for inference
```

## License
This project is licensed under the MIT License - see the LICENSE file for details.

For any issues and feature requests, please open an issue in the GitHub repository.

---

Feel free to reach out for further questions or contributions to enhance this project!