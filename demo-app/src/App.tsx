import React from "react";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import { Home } from "./pages/Home";

const router = createBrowserRouter([
  {
    path: "/",
    element: <Home />,
  },
  {
    path: "/top-5",
    element: <Home />,
  },
]);

const App = () => {
  return <RouterProvider router={router} />;
};

export default App;
