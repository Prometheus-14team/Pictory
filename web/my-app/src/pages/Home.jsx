import React from 'react';
import { Link } from 'react-router-dom';
import '../assets/styles.css';
import Group17Image from '../assets/images/Group 17.png';
import Group18Image from '../assets/images/Group 18.png';
import Group19Image from '../assets/images/Group 19.png';

function Home() {
  return (
    <div className="home-container">
      <div className="home-section">
        <img className="header-img" src={Group17Image} alt="Header Image" />
        <img className="intro-img" src={Group18Image} alt="Introduction Image" />
        <div className="text1">
          PICTORY, 당신의 내면 이야기를 그림으로 펼쳐내는 마법 같은 공간<br /><br /><br /><br /><br /><br /><br />
          동심의 순수함과 AI의 첨단 기술이 만나 탄생한 픽토리는<br />
          단순한 그림일기 플랫폼을 넘어섭니다.
        </div>
      </div>
      <div className="home-section">
        <div className="text2">
          글로 적은 당신의 내밀한 이야기를 AI가 섬세하게 읽어내고,<br />
          마치 어린 시절 상상 속 그림책처럼 생생하게 시작합니다.
        </div>
      </div>
      <div className="home-section">
        <img className="invitation-img" src={Group19Image} alt="Invitation Image" />
        <div className="text3">
          매 순간의 이야기를 고유한 작품으로 담아내는 당신만의 일기장 Pictory,<br /><br /><br />
          창의적 대화를 통해 매일의 기억을 예술로 탄생시키는 특별한 여정에 여러분을 초대합니다!
          <div className="label">
        <div className="text-wrapper"><Link to="/calendar">Start here</Link></div>
        </div>
        </div>
      </div>
    </div>
  );}


export default Home;
