import React from 'react';
import { Link } from 'react-router-dom';
import '../assets/styles.css';
import group1 from "../assets/images/group-1.png";
import group2 from "../assets/images/group-2.png";
import group13 from "../assets/images/group-13.png";
import group15 from "../assets/images/group-15.png";
import group11 from "../assets/images/group-11.png";
import group12 from "../assets/images/group-12.png";
import vector306 from "../assets/images/vector-306.svg";
import vector316 from "../assets/images/vector-316.svg";

const Home = () => {
  return (
    <div className="intro">
      <div className='jung'>
        <div className="rectangle" />
        <div className="ellipse" />
        <img className="group" alt="Group" src={group1} />
        <img className="group-2" alt="Group" src={group15} />
        <img className="vector" alt="Vector" src={vector316} />
        <div className="flexcontainer">
          <p className="text">
            <span className="span">
              PICTORY, 당신의 내면 이야기를 그림으로 펼쳐내는 마법 같은 공간
              <br />
            </span>
          </p>
          <p className="text">
            <span className="span">
              <br />
            </span>
          </p>
          <p className="text">
            <span className="span">
              <br />
            </span>
          </p>
          <p className="text">
            <span className="span">
              동심의 순수함과 AI의 첨단 기술이 만나 탄생한 픽토리는 <br /><br />
              단순한 그림일기 플랫폼을 넘어섭니다. 
            </span>
          </p>
          <p className="text">
            <span className="span">
              <br />
            </span>
          </p>
          <p className="text">
            <span className="span">
              글로 적은 당신의 내밀한 이야기를 AI가 섬세하게 읽어내고, <br /><br />
              마치 어린 시절 상상 속 그림책처럼 생생하게 시각화합니다.
            </span>
          </p>
        </div>
        <div className="box">
          <img alt="Group" src={group11} />
        </div>
        <div className="pencil">
          <img className="vector" alt="Group" src={group13} />
        </div>
        <div className="smile">
          <img className="vector" alt="Group" src={group12} />
        </div>
        <div className="div">
          <p className="text">
              <span className="span">
                <br />
              </span>
          </p>
          <p className="text">
              <span className="span">
                <br />
              </span>
          </p>
          <p className="text">
            <span className="span">
              매 순간의 이야기를 고유한 화풍으로 담아내는 당신만의
              일기장&nbsp;&nbsp;Pictory,
              <br />
            </span>
          </p>
          <p className="text">
            <span className="span">
              창의적 대화를 통해 매일의 기억을 예술로 탄생시키는 특별한 여정에
              여러분을 초대합니다!
            </span>
          </p>
        </div>
        <div className="text-wrapper"><Link to="/calendar">Start here</Link></div>
        <img className="group-5" alt="Group" src={group2} />
        <img className="vector-2" alt="Vector" src={vector306} />
      </div>
      <div className="text-wrapper-2">Ai drawing diary</div>
      <img className="group-6" alt="Group" src={group2} />
    </div>
  );
};

export default Home;
