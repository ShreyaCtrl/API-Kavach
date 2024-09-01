// ProfileCard.js
import React from 'react';
import profile from '../images/profile.png'


const ProfileCard = () => {
  return (
    <div className="flex h-1/4 w-full mx-auto rounded-lg ">
      <img class="h-20 rounded-full" src={require('../images/profile.png')} alt="User Profile Image"/>
      <div className="p-4">
        <h2 className="text-2xl font-semibold">Rakesh Shah</h2>
        <p className="text-gray-600">UDI NO:SHU763GDY76</p>
        <p className="text-gray-800 mt-2">
        hi
        </p>
       
      </div>
    </div>
  );
};

export default ProfileCard;
