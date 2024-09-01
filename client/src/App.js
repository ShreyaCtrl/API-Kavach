import logo from './logo.svg';
import './App.css';
import Login from './pages/Login';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import { Toaster } from 'sonner';
import PrivateRoute from './components/PrivateRoute';
import Sidebar from './components/Sidebar';
import ApiList from './components/ApiList';

function App() {
  return (
    <div>
      {/* <Credentials/> */}
      {/* <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login/>}/>
        <Route path="/dashboard" element={<PrivateRoute element={Dashboard} />} />
      </Routes>
      </BrowserRouter> */}
      {/* <Sidebar/> */}
      {/* <Dashboard/> */}
<ApiList/>
    </div>
  );
}

export default App;
