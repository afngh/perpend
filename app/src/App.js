import React from 'react';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';

import NotFound from './components/NotFound';
import Main from './components/Main';
import Login from './components/Login';
import Home from './components/Home';

const router = createBrowserRouter([
  {
    path: '/',
    element: <Main />,
  },
  {
    path: '/login',
    element: <Login />,
  },
  {
    path: '/home',
    element: <Home />,
  },
  {
    path: '*',
    element: <NotFound />,
  }
]);

function App() {
  return (
    <RouterProvider router={router} />
  );
}

export default App;