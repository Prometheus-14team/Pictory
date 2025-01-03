import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { fetchEvents } from '../utils/api'
import '../assets/styles.css';
import CalendarBody from '../components/Calendar/CalendarBody';
import CalendarList from '../components/Calendar/CalendarList';
import CalendarHeader from '../components/Calendar/CalendarHeader';

function Calendar() {
    const [events, setEvents] = useState([]);

    useEffect(() => {
        fetchEvents()
        .then((data) => setEvents(data)) // 데이터 불러오기
        .catch((error) => console.error('Error fetching events:', error)); // 오류 처리
    }, []);

    return (
        <div className="calendar-page">
          {/* 캘린더 상단 헤더 */}
          <CalendarHeader />
          
          <div className="calendar-container">
            {/* 왼쪽: 캘린더 그리드 */}
            <div className="calendar-grid">
              <CalendarBody /> {/* 기본 캘린더 그리드 */}
            </div>
    
            {/* 오른쪽: 캘린더 목록 */}
            <div className="calendar-list">
            <CalendarList events={events} /> {/* 캘린더 목록 컴포넌트 */}
            </div>
          </div>
        </div>
      );
    }

export default Calendar;
