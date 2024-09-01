import React from 'react'
// import Notification from '../components/Notification'
import { toast, Toaster } from 'sonner';
import { useLocation } from 'react-router-dom';
import ApiCountWidget from './ApiCountWidget';
import Sidebar from './Sidebar';

function Dashboard() {
  const location = useLocation();

  React.useEffect(() => {
      if (location.state && location.state.message) {
          toast[location.state.type](location.state.message);
      }
  }, [location.state]);

  

  return (
    <div>
     <ApiCountWidget/>
     <Toaster position='top-right' richColors/>
    </div>
  )
}

export default Dashboard
