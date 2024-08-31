import logo from './logo.svg';
import './App.css';
import Login from './pages/Login';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import Dashboard from './pages/Dashboard';

function App() {
  return (
    <div>
      {/* <Credentials/> */}
      <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login/>}/>
        <Route path="/dashboard" element={<Dashboard/>}/>
      </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
