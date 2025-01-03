import React from "react";

function CalendarList({events}) {
    if (!events) {
        return <div>Loading..</div>
    }

    return (
    <div>
      <ul>
        {events && events.length > 0 ? (
          events.map((event, index) => (
            <li key={index}>{event.name}</li>  // 전달된 이벤트를 리스트로 출력
          ))
        ) : (
          <li>No events available</li> // 이벤트가 없을 경우 메시지 출력
        )}
      </ul>
    </div>
      );
    }

export default CalendarList;