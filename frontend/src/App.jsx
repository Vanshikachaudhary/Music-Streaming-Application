import React, { useEffect, useState } from "react";
import { getHealth } from "./api";

function App() {
  const [status, setStatus] = useState("loading...");

  useEffect(() => {
    getHealth().then((res) => setStatus(res.status));
  }, []);

  return (
    <div style={{ padding: "2rem", fontFamily: "Arial" }}>
      <h1>Spotify Clone 🎵</h1>
      <p>Gateway Service Status: {status}</p>
    </div>
  );
}

export default App;
