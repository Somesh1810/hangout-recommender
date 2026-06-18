import axios from "axios";

const API = axios.create({
  baseURL:
    "https://hangout-recommender.onrender.com"
});

export default API;