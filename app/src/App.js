import React from "react";
import { createBrowserRouter, Router, RouterProvider } from 'react-router-dom'
import Login from "./components/Login";
import Home from "./components/Home";
import NotFound from "./components/NotFound";

router = createBrowserRouter([
  { path: "/", element: <Login /> },
  { path: "/login", element: <Login /> },
  { path: "/home", element: <Home /> },
  { path: "*", element: <NotFound /> }
])

function App() {
  return (
    <RouterProvider router={router} />
  );
}

export default App;
