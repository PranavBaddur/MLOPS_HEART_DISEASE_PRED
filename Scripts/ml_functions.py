import pickle
import os
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from helper_functions import log_info, log_error

# Define paths dynamically
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR) if os.path.basename(BASE_DIR) == 'src' else BASE_DIR
ARTIFACTS_PATH = os.path.join(PROJECT_ROOT, "artifacts")

MODEL_PATH = os.path.join(ARTIFACTS_PATH, "heart_model.pkl")
LABEL_ENCODER_PATH = os.path.join(ARTIFACTS_PATH, "heart_label_encoder.pkl")

def train_model(X_train, y_train):
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)
    with open(MODEL_PATH, 'wb') as f:
        pickle.dump(model, f)
    log_info(f"Model trained and saved at {MODEL_PATH}")
    return model

def predict(X_val):
    try:
        with open(MODEL_PATH, 'rb') as f:
            model = pickle.load(f)
        with open(LABEL_ENCODER_PATH, 'rb') as f:
            le = pickle.load(f)
        preds = model.predict(X_val)
        return le.inverse_transform(preds)
    except FileNotFoundError as e:
        log_error(f"Model or label encoder file not found: {str(e)}")
        return None
    except Exception as e:
        log_error(f"Error during prediction: {str(e)}")
        return None

def evaluate(X_val, y_val):
    try:
        preds = predict(X_val)
        if preds is None:
            return None, None, None
            
        with open(LABEL_ENCODER_PATH, 'rb') as f:
            le = pickle.load(f)
        y_val_decoded = le.inverse_transform(y_val)
        acc = accuracy_score(y_val_decoded, preds)
        cm = confusion_matrix(y_val_decoded, preds)
        report = classification_report(y_val_decoded, preds)
        log_info("Evaluation complete.")
        return cm, acc, report
    except Exception as e:
        log_error(f"Error during evaluation: {str(e)}")
        return None, None, None

# ==============================================================================
# CONFIG.PY - New configuration file for centralized path management
# ==============================================================================

import os
from pathlib import Path

class Config:
    """Configuration class for dynamic path management"""
    
    def __init__(self):
        # Get the current file's directory and project root
        self.BASE_DIR = Path(__file__).parent.absolute()
        self.PROJECT_ROOT = self.BASE_DIR.parent if self.BASE_DIR.name == 'src' else self.BASE_DIR
        
        # Define all project paths
        self.ARTIFACTS_PATH = self.PROJECT_ROOT / "artifacts"
        self.DATA_PATH = self.PROJECT_ROOT / "data"
        self.RAW_DATA_PATH = self.DATA_PATH / "raw"
        self.OUTPUT_DATA_PATH = self.DATA_PATH / "output"
        self.LOGS_PATH = self.PROJECT_ROOT / "logs"
        
        # Model-specific paths
        self.MODEL_PATH = self.ARTIFACTS_PATH / "heart_model.pkl"
        self.PIPELINE_PATH = self.ARTIFACTS_PATH / "heart_pipeline.pkl"
        self.LABEL_ENCODER_PATH = self.ARTIFACTS_PATH / "heart_label_encoder.pkl"
        
        # Data file paths
        self.PREDICTION_DATA_PATH = self.RAW_DATA_PATH / "prediction.csv"
        
        # Create directories if they don't exist
        self.create_directories()
    
    def create_directories(self):
        """Create all necessary directories"""
        directories = [
            self.ARTIFACTS_PATH,
            self.RAW_DATA_PATH,
            self.OUTPUT_DATA_PATH,
            self.LOGS_PATH
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    def get_log_file_path(self):
        """Get the current log file path with timestamp"""
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y%m%d')
        return self.LOGS_PATH / f"heart_app_log_{timestamp}.log"

# Create a global config instance
config = Config()

# ==============================================================================
# USAGE EXAMPLE - How to use the new dynamic configuration
# ==============================================================================

# In any of your modules, you can now import and use:
# from config import config
# 
# # Access paths like this:
# model_path = config.MODEL_PATH
# data_path = config.PREDICTION_DATA_PATH
# artifacts_dir = config.ARTIFACTS_PATH
