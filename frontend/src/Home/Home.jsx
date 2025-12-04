import "./Home.css";
import { useState } from "react";
import Button from "../Button/Button";
import { shortenUrl, API_BASE } from "../main";

export default function Home() {
  const [query, setQuery] = useState("");
  const [slug, setSlug] = useState(null);

  async function handleShort() {
    const result = await shortenUrl(query);
    setSlug(result.data);
  }

  return (
    <div className="container">
      <h1 className="title">URL Shortener</h1>

      <div className="input-row">
        <input
          type="text"
          className="input"
          placeholder="Long URL"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <Button className="btn" onClick={handleShort}> Shorten </Button>
      </div>

      {slug && (
        <div className="result-box">
          <div className="short-link-wrapper">
            <span className="link-icon">🔗</span>
            <a
              className="short-link"
              href={`${API_BASE}${slug}`}
              target="_blank"
            >
              {API_BASE}
              {slug}
            </a>
          </div>

          <Button
            className="copy-btn"
            onClick={() => navigator.clipboard.writeText(`${API_BASE}${slug}`)}
          >
            Copy Ctrl+C
          </Button>
        </div>
      )}
    </div>
  );
}