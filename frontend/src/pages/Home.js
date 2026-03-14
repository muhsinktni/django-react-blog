import { Link } from "react-router-dom";
import { useEffect, useState } from "react";
import "../styles/home.css";
import api from "../api/axios";
import Sidebar from "../components/Sidebar";
import { toast } from "react-toastify";

function Home() {
  const [posts, setPosts] = useState([]);
  const [title, setTitle] = useState("");
  const [editingId, setEditingId] = useState(null);
  const [content, setContent] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    api
      .get("posts/")
      .then((res) => {
        setPosts(res.data.results);
        setLoading(false);
      })
      .catch((err) => {
        setError("Failed to load posts");
        setLoading(false);
      });
  }, []);

  // submit function
  function handleSubmit(e) {
    e.preventDefault();
    if (!title || !content) {
      alert("Please fill all fields");
      return;
    }
    const request = editingId
      ? api.patch(`posts/${editingId}/`, { title, content })
      : api.post("posts/", { title, content });
    request
      .then((res) => {
        const data = res.data;
        if (editingId) {
          setPosts(posts.map((p) => (p.id === editingId ? data : p)));
          toast.success("Post Updated successfully!");
        } else {
          setPosts([data, ...posts]);
          toast.success("Post created succefully!");
        }

        setTitle("");
        setContent("");
        setEditingId(null);
      })
      .catch((err) => {
        toast.error("failed to create post");
      });
  }

  // delete operation
  function handleDelete(id) {
    api
      .delete(`posts/${id}/`)
      .then(() => {
        setPosts(posts.filter((post) => post.id !== id));
        toast.success("Post deleted");
      })
      .catch((err) => console.error(err));
  }

  // edit operation
  function startEdit(post) {
    setEditingId(post.id);
    setTitle(post.title);
    setContent(post.content);
  }

  return (
    // greeting

    <div className="home-wrapper">
      <div className="sidebar">
        <Sidebar />
      </div>
      <div className="home-content">
        <div className="home-welcometext">
          <h2>Welcome to my Blog</h2>
          <h3>Do you have an account yet?</h3>
          <h3>
            <Link to="/token">Click here</Link> to create an account
          </h3>
        </div>
        {/* create post */}

        <h3 style={{ textAlign: "center" }}>Create Post</h3>
        <div className="post-form">
          <form onSubmit={handleSubmit}>
            <input
              className="postTitle"
              type="text"
              placeholder="Enter title here"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
            />
            <br />

            <textarea
              className="postContent"
              placeholder="Type your content here"
              value={content}
              onChange={(e) => setContent(e.target.value)}
            />

            <br />
            <button>{editingId ? "Update" : "Create"}</button>
          </form>
        </div>

        {/* show posts on home */}
        <div className="posts">
          <h2 style={{ textAlign: "center", color: "white" }}>Posts</h2>

          {loading && (
            <p>Loading posts...Please Wait..Thank you for your patience..!</p>
          )}
          {error && <p style={{ color: "red" }}>{error}</p>}

          {!loading &&
            !error &&
            (posts.length === 0 ? (
              <p>No posts yet</p>
            ) : (
              posts.map((post) => (
                <div
                  key={post.id}
                  style={{
                    border: "1px solid #ccc",
                    margin: "10px",
                    padding: "10px",
                    background: "white",
                  }}
                >
                  <h3>{post.title}</h3>
                  <h4>{post.author}</h4>
                  <p>{post.content}</p>
                  <button onClick={() => handleDelete(post.id)}>Delete</button>
                  <button onClick={() => startEdit(post)}>Edit</button>
                </div>
              ))
            ))}
        </div>
      </div>
    </div>
  );
}

export default Home;
