import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import logo1 from './logo.png';
import './App.css';

const Home = () => {
  const navigate = useNavigate();
  const [ticker, setTicker] = useState('');

  const handleNavigate = () => {
    if (ticker) {
      navigate(`/results?ticker=${ticker}`);
    } else {
      alert("Please enter a stock ticker symbol.");
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      handleNavigate();
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <Link to="/">
          <button className="header1">Home</button>
        </Link>
        <Link to="/about">
          <button className="header2">About</button>
        </Link>
      </header>

      <h2 className="Intro">Stay Ahead in the Stock Market with Sentisphere!</h2>
      <p className="line1">Whether you're a seasoned investor or just</p>
      <p className="line2">getting started, Sentisphere offers personalized</p>
      <p className="line3">news feeds and data-driven insights to help you</p>
      <p className="line4">make informed decisions and maximize your</p>
      <p className="line5">investment potential.</p>

      <div className="box"></div>
      <h3 className="join">Try Now!</h3>

      <img src={logo1} className="imgsmall" alt="logo" />
      <input
        placeholder="Input Stock Ticker Here"
        className="searchbox"
        value={ticker}
        onChange={(e) => setTicker(e.target.value)}
        onKeyDown={handleKeyDown}
      />
      <img src={logo1} className="imgbig" alt="logo" />
      <h1 className="companyname">SENTISPHERE</h1>
    </div>
  );
};

export default Home;
