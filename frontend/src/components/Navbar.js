import { Link, useNavigate } from "react-router-dom";
import "./Navbar.css";
import { useContext } from "react";
import { AuthContext } from "../context/AuthContext";
import Lottie from "lottie-react";
import HiRobot from "../assets/animations/HiRobot.json";

function Navbar() {
  const { user, setUser } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    localStorage.removeItem("username");
    setUser(null);
    navigate("/token");
  };

  return (
    <nav className="navbar">
      <SayHi />
      <Link to="/">Home</Link>
      {user ? (
        <>
          <span
            style={{ marginLeft: "10px", color: "white", fontWeight: "bold" }}
          >
            | Hello, {user}
          </span>
          <button onClick={handleLogout} style={{ marginLeft: "10px" }}>
            Logout
          </button>
        </>
      ) : (
        <Link to="/token">not logged in yet, click here to login</Link>
      )}
    </nav>
  );
}

const SayHi = () => {
  return (
    <Lottie
      animationData={HiRobot}
      loop={true}
      autoplay={true}
      style={{ height: 100, width: 100 }}
    />
  );
};
export default Navbar;
