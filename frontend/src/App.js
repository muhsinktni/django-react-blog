import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Login from "./pages/Login";
import Layout from "./components/Layout";
import ProtectedRoute from "./components/ProtectedRoute";
import { useState } from "react";
import { ToastContainer } from "react-toastify";
import "react-toastify/ReactToastify.css";
// import Navbar from "./components/Navbar";

function App() {
  const [user, setUser] = useState(localStorage.getItem("username"));

  return (
    <BrowserRouter>
      <ToastContainer
        position="top-right"
        autoClose={3000}
        hideProgressBar={false}
        newestOnTop={true}
        closeOnClick
        pauseOnHover
      />
      <Routes>
        <Route element={<Layout user={user} setUser={setUser} />}>
          <Route
            path="/"
            element={
              <ProtectedRoute>
                <Home />
              </ProtectedRoute>
            }
          />

          <Route path="/token" element={<Login setUser={setUser} />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
