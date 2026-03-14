import axios from "axios";
import { toast } from "react-toastify";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000/api/",
});

// REQUEST INTERCEPTOR
api.interceptors.request.use((config) => {
  const access = localStorage.getItem("access");

  if (access) {
    config.headers.Authorization = `Bearer ${access}`;
  }
  return config;
});

// RESPONSE INTERCEPTOR
api.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error) => {
    const originalRequest = error.config;

    if (error.response) {
      const status = error.response.status;

      // 401 Unauthorized
      if (status === 401) {
        toast.error("Session expired. Please login again.");
      }

      // 403 Forbidden
      if (status === 403) {
        toast.error("You do not have permission.");
      }

      // 500 Server Error
      if (status === 500) {
        toast.error("Server error. Please try again later.");
      }

      if (error.response && error.response.status === 401) {
        const refresh = localStorage.getItem("refresh");

        if (refresh) {
          try {
            const res = await axios.post(
              "http://127.0.0.1:8000/api/token/refresh/",
              { refresh: refresh },
            );

            const newAccess = res.data.access;
            localStorage.setItem("access", newAccess);

            originalRequest.headers.Authorization = `Bearer ${newAccess}`;

            return api(originalRequest);
          } catch (err) {
            localStorage.removeItem("access");
            localStorage.removeItem("refresh");
            window.location.href = "/token";
          }
        }
      }
    }
    return Promise.reject(error);
  },
);

export default api;
