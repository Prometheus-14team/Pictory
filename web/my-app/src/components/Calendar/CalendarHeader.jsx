import React from 'react';

function CalendarHeader({ currentMonth, onPrevMonth, onNextMonth }) {
  return (
    <div className="calendar-header">
      <button onClick={onPrevMonth}>Prev</button>
      <h2>{currentMonth}</h2>
      <button onClick={onNextMonth}>Next</button>
    </div>
  );
}

export default CalendarHeader;
