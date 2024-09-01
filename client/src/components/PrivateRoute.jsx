import React from 'react';
import { Navigate } from 'react-router-dom';

const PrivateRoute = ({ element: Element, ...rest }) => {
  // Check if the user is authenticated
  const isAuthenticated = !!localStorage.getItem('token'); // Replace with your auth logic

  // Render the element if authenticated, otherwise redirect to login
  return isAuthenticated ? <Element {...rest} /> : <Navigate to="/" />;
};

export default PrivateRoute;
