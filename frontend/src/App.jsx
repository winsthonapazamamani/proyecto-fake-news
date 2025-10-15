import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

const API_BASE_URL = 'http://localhost:5000/api';

function App() {
  const [newsText, setNewsText] = useState('');
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handlePredict = async () => {
    if (!newsText.trim()) {
      setError('Please enter news text');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await axios.post(`${API_BASE_URL}/prediction/predict`, {
        text: newsText
      });
      
      setPrediction(response.data);
    } catch (err) {
      setError('Error making prediction: ' + (err.response?.data?.message || err.message));
    } finally {
      setLoading(false);
    }
  };

  const getPredictionColor = (prediction) => {
    return prediction === 1 ? 'green' : 'red';
  };

  const getPredictionText = (prediction) => {
    return prediction === 1 ? 'Positive' : 'Negative';
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>News Sentiment Predictor</h1>
        <p>Analyze the sentiment of news articles</p>
      </header>

      <main className="main-content">
        <div className="input-section">
          <textarea
            value={newsText}
            onChange={(e) => setNewsText(e.target.value)}
            placeholder="Paste news article text here..."
            rows="8"
            className="news-textarea"
          />
          
          <button 
            onClick={handlePredict} 
            disabled={loading}
            className="predict-button"
          >
            {loading ? 'Analyzing...' : 'Analyze Sentiment'}
          </button>
        </div>

        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

        {prediction && (
          <div className="result-section">
            <h2>Analysis Result</h2>
            <div className="prediction-card">
              <div className="prediction-header">
                <span 
                  className="prediction-badge"
                  style={{ backgroundColor: getPredictionColor(prediction.data.prediction) }}
                >
                  {getPredictionText(prediction.data.prediction)}
                </span>
                <span className="confidence">
                  Confidence: {(prediction.data.confidence * 100).toFixed(2)}%
                </span>
              </div>
              
              <div className="probability-breakdown">
                <h4>Probability Breakdown:</h4>
                <div className="probability-bars">
                  <div className="probability-item">
                    <span>Negative: </span>
                    <div className="probability-bar">
                      <div 
                        className="probability-fill negative"
                        style={{ width: `${prediction.data.probabilities.class_0 * 100}%` }}
                      >
                        {(prediction.data.probabilities.class_0 * 100).toFixed(1)}%
                      </div>
                    </div>
                  </div>
                  <div className="probability-item">
                    <span>Positive: </span>
                    <div className="probability-bar">
                      <div 
                        className="probability-fill positive"
                        style={{ width: `${prediction.data.probabilities.class_1 * 100}%` }}
                      >
                        {(prediction.data.probabilities.class_1 * 100).toFixed(1)}%
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;