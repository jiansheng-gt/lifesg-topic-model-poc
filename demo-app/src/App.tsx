import React from "react";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import { Home } from "./pages/Home";
import { Top5 } from "./pages/Top5";

const router = createBrowserRouter([
  {
    path: "/",
    element: <Home />,
  },
  {
    path: "/top-5",
    element: <Top5 />,
  },
]);

const App = () => {
  return <RouterProvider router={router} />;
};

export default App;
