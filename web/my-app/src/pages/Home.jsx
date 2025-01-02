import React from 'react';
import aa from '../assets/images/aa.png';  // 이미지 불러오기

function Home() {
  return (
    <div>
      <h2>Welcome to the Home Page</h2>
      <p>This is the home page content.</p>
      <img src={'/assets/images/aa.png'} alt="My Image" className="aa" /> 
    </div>
  );
}

export default Home;
