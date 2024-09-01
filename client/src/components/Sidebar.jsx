import React from 'react'
import ProfileCard from './Profile'

function Sidebar() {
  return (
    <div className='h-screen w-1/4 shadow-md shadow-violet-300 bg-gradient-to-l from-violet-900 to-violet-300'>
        <div className='flex-col justify-center items-center'>
            <ProfileCard/>
        </div>
    </div>
  )
}

export default Sidebar
