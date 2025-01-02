import React, { useState } from 'react';
import CalendarHeader from './CalendarHeader';
import CalendarBody from './CalendarBody';

function Calendar() {
  const [currentMonth, setCurrentMonth] = useState("January 2025");
  const days = [
    { date: "1", isToday: false },
    { date: "2", isToday: false },
    { date: "3", isToday: true }, // 오늘 날짜
    { date: "4", isToday: false },
    { date: "5", isToday: false },
  ];
  const events = {
    "1": ["Event A"],
    "3": ["Event B"],
  };

  const handlePrevMonth = () => {
    console.log("Prev Month");
  };

  const handleNextMonth = () => {
    console.log("Next Month");
  };

  return (
    <div className="calendar">
      <CalendarHeader
        currentMonth={currentMonth}
        onPrevMonth={handlePrevMonth}
        onNextMonth={handleNextMonth}
      />
      <CalendarBody days={days} events={events} />
    </div>
  );
}

export default Calendar;
