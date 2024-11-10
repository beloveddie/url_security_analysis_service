# Create a new file: server.py
from fastapi import FastAPI
from main import URLFeatureExtractor, URLSecurityModel
import uvicorn

app = FastAPI()
feature_extractor = URLFeatureExtractor()
model = URLSecurityModel(feature_extractor)
model.load("./models/custom_model_domain_reps.joblib")

@app.get("/")
def read_root():
    return {"message": "URL Security Analyzer API"}

@app.post("/analyze")
async def analyze_url(url: str):
    features = feature_extractor.extract_features(url)
    feature_vector = [[features[name] for name in model.feature_names]]
    risk_score = float(model.model.predict_proba(feature_vector)[0][1])
    
    return {
        "url": url,
        "risk_score": risk_score,
        "features": features
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)