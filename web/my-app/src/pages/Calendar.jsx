import React from 'react';
import { Link } from 'react-router-dom';
import '../assets/styles.css';

function calendar() {
  return (
    <div className="calendar">
      <h2>Welcome to the calendar: Pictory!</h2>
      <p>This is the calendar content.</p>
    <Link to="/">Back to the Home</Link>
    </div>
  );
}

export default calendar;
