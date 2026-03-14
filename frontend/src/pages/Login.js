import { Link, useNavigate } from "react-router-dom";
import "../styles/Login.css";
import { useContext, useState } from "react";
import { AuthContext } from "../context/AuthContext";
import { toast } from "react-toastify";

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const { setUser } = useContext(AuthContext);
  const navigate = useNavigate();

  function handleSubmit(e) {
    e.preventDefault();

    fetch("http://127.0.0.1:8000/api/token/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        username: username,
        password: password,
      }),
    })
      .then((res) => res.json())
      .then((data) => {
        console.log("Backend response:", data);

        if (data.access) {
          localStorage.setItem("access", data.access);
          localStorage.setItem("refresh", data.refresh);
          localStorage.setItem("username", username);

          setUser(username);

          toast.success("Login Successful!");
          navigate("/");
        } else {
          toast.error("Login failed. Invalid Username or Password");
        }
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  }
  return (
    <div className="login-container">
      <div className="login-card">
        <h2 className="login-title">Login Form</h2>
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="Enter Your name here"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className="login-input"
          />

          <input
            type="password"
            placeholder="Enter Your password here"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="login-input"
          />

          <button className="login-button">Click here to Login</button>
          <Link to="/">Back to Home </Link>
        </form>
      </div>
    </div>
  );
}

export default Login;
