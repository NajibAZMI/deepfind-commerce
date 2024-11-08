import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [message, setMessage] = useState('');

  useEffect(() => {
    // Appel à l'API Flask
    axios.get('http://localhost:5000/api/greet')
      .then(response => {
        setMessage(response.data.message);
      })
      .catch(error => {
        console.error('Error fetching data', error);
      });
  }, []);

  return (
    <div className="App">
      <h1>React + Python (Flask)</h1>
      <p>{message}</p>
    </div>
  );
}

export default App;

