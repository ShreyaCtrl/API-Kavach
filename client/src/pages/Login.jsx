import React from 'react'
import Credentials from '../components/Credentials'
import loginbg from '../images/loginbg.png'
import logo from '../images/logo.png'

function Login() {
  return (
    <div className='h-screen w-screen bg-violet-950'>
      <div
          className="h-screen w-screen bg-cover bg-no-repeat bg-center"
          style={{
            backgroundImage: `url(${loginbg})`,
            backgroundSize: '100%',
            // backgroundPosition: 'middle',
            // opacity:0.9,

          }}>

            <div className='flex w-screen items-center justify-evenly'> 
            <img src={logo} alt="Logo of API Kavach" className="h-80"/>
            <Credentials/>
            </div>
            
          </div>
      
    </div>
  )
}

export default Login
