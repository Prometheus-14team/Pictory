import React from 'react';
import CalendarDay from './CalendarDay';

function CalendarBody({ days, events }) {
  return (
    <div className="calendar-body">
      {days.map((day, index) => (
        <CalendarDay
          key={index}
          date={day.date}
          isToday={day.isToday}
          events={events[day.date] || []}
        />
      ))}
    </div>
  );
}

export default CalendarBody;
