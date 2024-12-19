//index.js
import React from 'react';
import ReactDOM from 'react-dom/client';
//import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

// App.js
function App() {
  return (
    <div>
      <h1>Welcome back!</h1>
    </div>
  );
}

export default App;