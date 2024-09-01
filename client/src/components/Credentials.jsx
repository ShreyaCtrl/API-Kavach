import React, {useState} from 'react'
import axios from 'axios'
import { useNavigate } from 'react-router-dom';
import Notification from './Notification';
import { toast, Toaster } from 'sonner';

function Credentials() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [role, setRole] = useState('');
    const [errorMessage, setErrorMessage] = useState('');
    const [message, setMessage] = useState('');
    const [type, setType] = useState('');
    const [notification, setNotification] = useState({ message: '', type: '' });
     //registered = false;
    let navigate = useNavigate();

    const handleLogin = () => {
        // Check if entered email and password match any sample user data
        const data = {
          username: username,
          password: password,
          role: role
        };
        // const user = userData.find(u => u.email === email && u.password === password && u.role === role);

      //   if (user) {
      //     // Clear error message if authentication successful
      //     setErrorMessage('');
      //   } else {
      //     // Set error message if authentication fails
      //     setErrorMessage('Invalid email or password');
      //   }
      // };

      axios.post('http://localhost:5000/login', data)
            .then(response => {
                console.log(response.data);
                if (response.data.status === 200) {
                    setErrorMessage('');
                    // setNotification({ message: 'Login Successful!', type: 'success' });
                    // toast.success('Login Successful');
                    // navigate('/dashboard', { replace: true });
                    localStorage.setItem('token', response.data.token);
                    navigate('/dashboard', { state: { message: 'Login Successful!', type: 'success' } });
                } else {
                  setErrorMessage(response.message);
                  setNotification({ message: response.data.message, type: 'error' });

                }
            })
            .catch(error => {
                console.error('Error:', error);
                setErrorMessage('Login Failed');
                setNotification({ message: 'Login Failed', type: 'error' });
            });
    };

    const handleSignup = () => {
      // Check if entered email and password match any sample user data
      const data = {
        username: username,
        password: password,
        role: role
      };

      axios.post('http://localhost:5000/signup', data)
            .then(response => {
                console.log(response.data);
                if (response.data.status === 201) {
                    setErrorMessage('');
                    localStorage.setItem('token', response.data.token);
                    navigate('/dashboard', { state: { message: 'Signup Successful!', type: 'success' } });
                } else if (response.data.status === 400) {
                    setErrorMessage(response.message);
                    setNotification({ message: response.data.message, type: 'error' });

                }
            })
            .catch(error => {
                console.error('Error:', error);
                setErrorMessage('Sign up failed');
                setNotification({ message: 'Signup Failed', type: 'error' });
            });
    };




  return (
    <div className='flex items-center justify-center h-screen w-1/3 z-10 float-right'>
    <div className='p-6'>
      <div className='h-80 w-96 flex flex-col justify-around'>
        <div>
        <label className ='text-left text-white'>Username</label>
        <div>
            <input
                id="username"
                type="username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="form-input w-full h-10 bg-gray-100 text-black rounded-md p-2 shadow shadow-violet-200"
                placeholder="Enter your username"
                required
            />
        </div>
        </div>

        
        <div>
        <label className = 'text-left text-white'>Password</label>
        <div>
          <input
            id="password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="form-input w-full h-10 bg-gray-100 text-black rounded-md p-2 shadow shadow-violet-200"
            placeholder="Enter your password"
            required
          />
        </div>
        </div>

        <div>
            <label className='text-left font text-white'>Role</label>
            <div>
                <select
                id="dropdown"
                type="dropdown"
                value={role}
                onChange={(e) => setRole(e.target.value)}
                className="form-input w-full h-10 bg-gray-100 text-gray-600 rounded-md p-2 shadow shadow-violet-200 text-md"
                
                required>
                <option value="">Select your role</option>
                <option value="Developer">Developer</option>
                <option value="Tester">Tester</option>
                <option value="DevOps Engineer">DevOps Engineer</option>
                <option value="Administrator">Administrator</option>

                </select>
            </div>
        </div>

        <div className = 'flex justify-around'>
          <button
            onClick={handleLogin}
            className="btn text-violet-600 bg-gray-100 hover:bg-violet-600 hover:text-white hover:shadow-violet-400 mt-4 w-1/3 p-1 rounded-lg text-lg shadow shadow-violet-600 text-center">
            Login
          </button>
          <button
            onClick={handleSignup}
            className="btn text-violet-600 bg-gray-100 hover:bg-violet-600 hover:text-white hover:shadow-violet-400 mt-4 w-1/3 p-1 rounded-lg text-lg shadow shadow-violet-600 text-center">
            Sign Up
          </button>
        </div>
        
      </div>
    {errorMessage && <div className="text-red-500">{errorMessage}</div>}
    {/* <Notification message={message} type={type} />
    <Notification message={notification.message} type={notification.type} /> */}
    </div>  
    {/* <Toaster position='top-right' richColors/> */}
    </div>
  )
}

export default Credentials
