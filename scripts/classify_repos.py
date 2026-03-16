import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.classification.industry_classifier import classify_repositories

if __name__ == "__main__":
    print("Starting AI classification...")
    classify_repositories()
