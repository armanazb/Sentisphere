import React from 'react';
import {useNavigate, Link} from 'react-router-dom';
import logo1 from './logo.png';
import './App.css';

const Home = () => {
  const navigate = useNavigate();
  const handleNavigate = () => {
    navigate('/results');
  };
  return (
    <div className="App">
       <Link to="/">
          <button className="header1">Home</button>
        </Link>
        <Link to="/about">
          <button className="header2">About</button>
        </Link>

    <img src={logo1} className="imgsmall" alt="logo" />
    <img src={logo1} className="imgbig" alt="logo" />
    <h1 className="companyname">SENTISPHERE</h1>

    <h2 className="Intro2">About Us</h2>
    <p className="betterline">Sentisphere was developed as a submission for HawkHacks 2024, a hackathon at Wilfred Laurier University. It was created by Andrew Sasmito, Fiona Verzivolli, Belal Armanazi, and Advaith
    Thakur. Sentisphere utilizes webscraping, AI sentiment analysis, and data visualization,
    to give an overall connotation towards the future of a stock for a certain company. Specifically, depending on an overall summary from multiple news articles, a percentage will be provided on the positivity or negativity of the stock. We have also provided a visualization of the stock's past month trends.
    We hope you benefit from our service!
    </p>

  </div>
  );
};

export default Home;