# Sensing Garden Client

A Python client for interacting with the Sensing Garden API.

## Installation

```bash
pip install sensing-garden-client
```

## Usage

### Basic Usage

The modern API provides a more intuitive, object-oriented interface:

```python
import sensing_garden_client

# Initialize the client with the new interface
sgc = sensing_garden_client.SensingGardenClient(
    base_url="https://api.example.com", 
    api_key="your-api-key"  # Only needed for POST operations
)

# Working with models
models = sgc.models.fetch(limit=10)
model = sgc.models.create(
    model_id="model-123",
    name="My Plant Model",
    version="1.0.0",
    description="A model for plant classification"
)

# Working with detections
with open("plant_image.jpg", "rb") as f:
    image_data = f.read()
    
detection = sgc.detections.add(
    device_id="device-123",
    model_id="model-456",
    image_data=image_data,
    bounding_box=[0.1, 0.2, 0.3, 0.4],
    timestamp="2023-06-01T12:34:56Z"
)
detections = sgc.detections.fetch(device_id="device-123")

# Working with classifications
classification = sgc.classifications.add(
    device_id="device-123",
    model_id="model-456",
    image_data=image_data,
    family="Rosaceae",
    genus="Rosa",
    species="Rosa gallica",
    family_confidence=0.95,
    genus_confidence=0.92,
    species_confidence=0.89,
    timestamp="2023-06-01T12:34:56Z"
)
classifications = sgc.classifications.fetch(model_id="model-456")
```

### Environment Variables

The client can also be configured using environment variables:

```python
import os
import sensing_garden_client

# Set environment variables
os.environ["API_BASE_URL"] = "https://api.example.com"
os.environ["SENSING_GARDEN_API_KEY"] = "your-api-key"

# Initialize the client using environment variables
sgc = sensing_garden_client.SensingGardenClient(
    base_url=os.environ.get("API_BASE_URL"),
    api_key=os.environ.get("SENSING_GARDEN_API_KEY")
)
```

## Features

- Modern, intuitive API with domain-specific clients
- GET operations for models, detections, and classifications
- POST operations for submitting detections and classifications
- Model management operations
- Backward compatibility with previous API versions

## Dependencies

- `requests`: For API communication
