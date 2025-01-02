import React from 'react';

function CalendarDay({ date, isToday, events }) {
  return (
    <div className={`calendar-day ${isToday ? 'today' : ''}`}>
      <p>{date}</p>
      <div className="events">
        {events.map((event, index) => (
          <div key={index} className="event">
            {event}
          </div>
        ))}
      </div>
    </div>
  );
}

export default CalendarDay;
