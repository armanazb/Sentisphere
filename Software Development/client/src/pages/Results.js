import React, { useEffect, useState } from 'react';
import Plot from 'react-plotly.js';
import { useLocation } from 'react-router-dom';
import {useNavigate, Link} from 'react-router-dom';
import logo1 from './logo.png';


const Results = () => {
  const location = useLocation();
  const query = new URLSearchParams(location.search);
  const ticker = query.get('ticker');
  const [graphData, setGraphData] = useState(null);
  const [sentimentData, setSentimentData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (ticker) {
      fetch(`https://final-42ycc7ezxq-pd.a.run.app/api/graph?ticker=${ticker}`)
        .then(response => response.json())
        .then(data => setGraphData(data))
        .catch(error => setError('Failed to fetch graph data'));
    }
  }, [ticker]);

  useEffect(() => {
    if (ticker) {
      fetch(`https://final-42ycc7ezxq-pd.a.run.app/sentiment?stock_name=${ticker}`)
        .then(response => response.json())
        .then(data => setSentimentData(data))
        .catch(error => setError('Failed to fetch sentiment data'));
    }
  }, [ticker]);

  return (
    <div className="results">
        <img src={logo1} className="imgsmall" alt="logo" />

        <Link to="/">
          <button className="header1">Home</button>
        </Link>
        <Link to="/about">
          <button className="header2">About</button>
        </Link>
      {graphData && sentimentData ? (
        <div className="graph-container">
            <h2 className="graph-title">Stock Graph</h2>
            <Plot
            data={graphData.data}
            layout={{
              ...graphData.layout,
              annotations: [
                {
                  text: sentimentData.stockname,
                  x: 0,
                  y: 1,
                  xref: 'paper',
                  yref: 'paper',
                  showarrow: false,
                  font: {
                    size: 16,
                    color: 'black'
                  },
                  xanchor: 'left',
                  yanchor: 'top',
                }
              ],
            }}
            config={graphData.config}
          />
        </div>
      ) : (
        <p>Loading graph...</p>
      )}
      {sentimentData ? (
        <div className="sentiment-container">
          <h3>Sentiment Analysis</h3>
          <p>Positive: {sentimentData.positive.toFixed(2)}%</p>
          <p>Neutral: {sentimentData.neutral.toFixed(2)}%</p>
          <p>Negative: {sentimentData.negative.toFixed(2)}%</p>
        </div>
      ) : (
        <p>Loading sentiment analysis...</p>
      )}
      {error && <p>{error}</p>}
        <div className="articles-container">
        {sentimentData && sentimentData.articletitle && sentimentData.articletitle.length > 0 ? (
        sentimentData.articletitle.map((title, index) => (
            <div key={index} className="article">
            <img src={sentimentData.articlepicture[index]} alt={title} />
            <div className="article-details">
                <a href={sentimentData.articlelink[index]} target="_blank" rel="noopener noreferrer">
                <h4>{title}</h4>
                </a>
                <p>{sentimentData.articledesc[index]}</p>
            </div>
            </div>
        ))
        ) : (
        <p>No articles available yet...</p>
        )}
        </div>
        </div>
  );
};

export default Results;
