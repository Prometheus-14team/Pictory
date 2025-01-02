import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import CalendarPage from './pages/Calendar';
import Home from './pages/Home';
import './assets/styles.css';


function App() {
  return (
    <Router>
      <div className="app">
        {/* 전역 네비게이션 바 */}
        <header>
          <h1>My Website</h1>
        </header>

        {/* 페이지 라우팅 */}
        <main>
          <Routes>
          
            <Route path = "/" element = {<Home />} />
            <Route path = "./pages/Calendar" element = {<CalendarPage />} />
              
          </Routes>
        </main>

        {/* 전역 푸터 */}
        <footer>
          <p>&copy; 2025 My Website</p>
        </footer>
      </div>
    </Router>
  );
}

export default App;
