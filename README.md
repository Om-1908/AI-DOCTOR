# AI Doctor - Disease Prediction System

AI Doctor is a machine learning-powered web application that helps users identify potential diseases based on their symptoms. The system uses a trained model to predict possible illnesses and provides relevant health recommendations.

## Features

- **Symptom Analysis**: Input your symptoms and get a list of possible diseases
- **Disease Information**: Get detailed information about predicted diseases
- **Prevention Tips**: Learn how to prevent and manage health conditions
- **Responsive Design**: Works on desktop and mobile devices

## Hugging Face Spaces Deployment

This application is deployed on Hugging Face Spaces. You can access it [here](https://huggingface.co/spaces/your-username/ai-doctor).

## Local Development

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Installation

1. Clone the repository:
   ```bash
   git clone https://huggingface.co/spaces/your-username/ai-doctor
   cd ai-doctor
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

Start the development server:
```bash
uvicorn app:app --reload --host 0.0.0.0 --port 7860
```

The application will be available at `http://localhost:7860`

## API Endpoints

- `GET /`: Home page
- `GET /api/health`: Health check endpoint
- `POST /api/predict`: Submit symptoms and get disease prediction
- `GET /api/predict/symptoms`: Get list of all available symptoms
- `GET /api/predict/diseases`: Get list of all available diseases

## Project Structure

```
.
├── app.py                # Main application entry point
├── requirements.txt      # Python dependencies
├── .gitignore           # Git ignore file
├── backend/             # Backend source code
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py      # FastAPI application
│   │   ├── core/        # Core configurations
│   │   ├── models/      # Data models
│   │   ├── routers/     # API routes
│   │   ├── schemas/     # Pydantic models
│   │   └── services/    # Business logic
├── static/              # Static files (CSS, JS, images)
└── template/            # HTML templates
```

## Model Information

The prediction model is trained on a dataset of symptoms and diseases using a Support Vector Classifier (SVC). The model is saved in the `Models` directory.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Dataset provided by [Source Name]
- Built with FastAPI and scikit-learn
