import { Outlet } from "react-router-dom";
import Navbar from "./Navbar";
import "./Layout.css";

function Layout({ user, setUser }) {
  return (
    <div className="container">
      <h2 id="mainHead"> My Blog </h2>
      <Navbar user={user} setUser={setUser} />
      <div className="layoutbody">
        <div className="content">
          <Outlet />
        </div>
      </div>

      <p id="mainFoot">Footer</p>
    </div>
  );
}

export default Layout;
