import numpy as np
from sklearn.preprocessing import StandardScaler

def get_ideal_vector(risk_profile: str) -> np.ndarray:
    # based on benchmark data
    ideal = np.array([
        1.40390454e+02, 1.33685147e-02, 4.58329545e+06, 2.52951460e+01, 
        1.95996390e+01, 1.81372682e+11, 1.86500000e+00, 1.08250000e+00, 
        6.37114930e+00, 1.26920000e-01
    ])
    
    if risk_profile == 'high-risk':
        high_risk = ideal.copy()
        high_risk[1] *= 1.45   # volatility
        high_risk[4] *= 1.2   # forwardPE
        high_risk[6] *= 0.7   # dividendYield
        high_risk[7] *= 1.4   # beta
        return high_risk
    elif risk_profile == 'low-risk':
        low_risk = ideal.copy()
        low_risk[1] *= 0.6    # volatility
        low_risk[4] *= 0.7    # forwardPE
        low_risk[6] *= 1.4    # dividendYield
        low_risk[7] *= 0.6    # beta
        return low_risk
    else:
        return ideal

def cosine_similarity(vec_a: np.ndarray, vec_b: np.ndarray) -> float:
    norm_a = np.linalg.norm(vec_a)
    norm_b = np.linalg.norm(vec_b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return np.dot(vec_a, vec_b) / (norm_a * norm_b)

def simulate_candidate_vectors() -> dict:
    return {
        "IBM":  np.array([100.0, 0.02, 500000, 33, 27, 3e12, 0.8, 0.9, 10, 0.35]),
        "AAPL": np.array([150.0, 0.03, 1000000, 25, 20, 1.8e12, 0.01, 1.0, 4, 0.20]),
        "MSFT": np.array([210.0, 0.015, 800000, 30, 28, 2e12, 0.02, 1.1, 5, 0.30]),
        "GOOG": np.array([2800.0, 0.025, 600000, 35, 29, 1e12, 0.0, 1.2, 8, 0.15]),
        "AMZN": np.array([3400.0, 0.04, 700000, 20, 18, 3.5e12, 0.005, 1.3, 9, 0.10])
    }

def recommend_stocks_by_gap(portfolio_vector: np.ndarray, 
                             candidate_vectors: dict, 
                             risk_profile: str = 'medium-risk', 
                             top_n: int = 10) -> list:
    ideal_vector = get_ideal_vector(risk_profile)
    
    candidate_keys = list(candidate_vectors.keys())
    candidate_matrix = np.array([candidate_vectors[ticker] for ticker in candidate_keys])
    combined = np.vstack([candidate_matrix, portfolio_vector, ideal_vector])
    scaler = StandardScaler()
    normalized_combined = scaler.fit_transform(combined)
    
    normalized_candidate_matrix = normalized_combined[:len(candidate_matrix)]
    normalized_portfolio_vector = normalized_combined[len(candidate_matrix)]
    normalized_ideal_vector = normalized_combined[len(candidate_matrix)+1]
    
    deficit_vector = normalized_ideal_vector - normalized_portfolio_vector
    
    recommendations = []
    for ticker, norm_vec in zip(candidate_keys, normalized_candidate_matrix):
        score = cosine_similarity(norm_vec, deficit_vector)
        recommendations.append((ticker, score))
        
    recommendations.sort(key=lambda x: x[1], reverse=True)
    return recommendations[:top_n]

if __name__ == '__main__':
    portfolio_vector = np.array([
        421.2, 0.0186, 23562757, 33.37, 27.68,
        3075883663360, 0.8, 0.895, 10.163, 0.3543
    ])
    candidate_vectors = simulate_candidate_vectors()
    
    recs_safe = recommend_stocks_by_gap(portfolio_vector, candidate_vectors, risk_profile='low-risk', top_n=3)
    print("low risk:", recs_safe)

    recs_medium = recommend_stocks_by_gap(portfolio_vector, candidate_vectors, risk_profile='medium-risk', top_n=3)
    print("medium risk:", recs_medium)
    
    recs_high = recommend_stocks_by_gap(portfolio_vector, candidate_vectors, risk_profile='high-risk', top_n=3)
    print("high risk:", recs_high)
