import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.metrics.user_metrics import calculate_user_metrics
from src.metrics.ecosystem_metrics import calculate_ecosystem_metrics

if __name__ == "__main__":
    print("Calculating User Metrics...")
    calculate_user_metrics()
    print("Calculating Ecosystem Metrics...")
    calculate_ecosystem_metrics()
    print("All metrics calculated successfully.")
