import { useRef, useState } from "react";
import axios from "axios";
import YouTube from "react-youtube";
import "./App.css";

function App() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState([]);
  const [loading, setLoading] = useState(false);

  const playerRef = useRef(null);

  const videoId = "ygXn5nV5qFc";

  const askQuestion = async () => {
    if (!question.trim()) return;

    setLoading(true);
    setAnswer("");
    setSources([]);

    try {
      const response = await axios.post("http://127.0.0.1:8000/ask", {
        question: question,
      });

      setAnswer(response.data.answer);
      setSources(response.data.sources);
    } catch (error) {
      console.error(error);
      setAnswer("Something went wrong. Please try again.");
    }

    setLoading(false);
  };

  const handlePlayerReady = (event) => {
    playerRef.current = event.target;
  };

  const jumpToTimestamp = (seconds) => {
    if (playerRef.current) {
      playerRef.current.seekTo(seconds, true);
      playerRef.current.playVideo();
    }
  };

  const formatTime = (seconds) => {
    const totalSeconds = Math.floor(seconds);

    const hours = Math.floor(totalSeconds / 3600);
    const minutes = Math.floor((totalSeconds % 3600) / 60);
    const remainingSeconds = totalSeconds % 60;

    if (hours > 0) {
      return `${hours}:${String(minutes).padStart(2, "0")}:${String(
        remainingSeconds,
      ).padStart(2, "0")}`;
    }

    return `${minutes}:${String(remainingSeconds).padStart(2, "0")}`;
  };

  return (
    <div className="app">
      {/* HEADER */}
      <header className="header">
        <div className="logo">
          🎓 <span>LectureAI</span>
        </div>

        {/* <div className="course-name">Python for AI</div> */}
      </header>

      {/* MAIN */}
      <main className="main">
        {/* LEFT PANEL */}
        <section className="left-panel">
          <div className="hero">
            <h1>Ask your lecture.</h1>

            <p>
              Ask questions about the lecture and get answers grounded in the
              course content.
            </p>
          </div>

          {/* QUESTION INPUT */}
          <div className="question-box">
            <textarea
              placeholder="What do you want to learn?"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                  e.preventDefault();
                  askQuestion();
                }
              }}
            />

            <button onClick={askQuestion} disabled={loading}>
              {loading ? "Thinking..." : "Ask Question →"}
            </button>
          </div>

          {/* ANSWER */}
          {answer && (
            <div className="answer-section">
              <h2>AI Explanation</h2>

              <div className="answer-card">{answer}</div>
            </div>
          )}

          {/* SOURCES */}
          {sources.length > 0 && (
            <div className="sources-section">
              <h2>Lecture Sources</h2>

              <div className="sources">
                {sources.map((source, index) => (
                  <div
                    className="source-card"
                    key={index}
                    onClick={() => jumpToTimestamp(source.start_time)}
                  >
                    <div className="source-number">{index + 1}</div>

                    <div className="source-info">
                      <strong>{source.video_title}</strong>

                      <span>{formatTime(source.start_time)}</span>

                      <button className="jump-button">
                        ▶ Jump to this section
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </section>

        {/* RIGHT PANEL */}
        <section className="right-panel">
          <div className="video-container">
            <YouTube
              videoId={videoId}
              onReady={handlePlayerReady}
              opts={{
                width: "100%",
                height: "100%",
                playerVars: {
                  autoplay: 0,
                  rel: 0,
                },
              }}
              className="youtube-player"
            />

            <div className="video-title">
              Python for AI - Full Beginner Course
            </div>

            <p className="video-description">
              Click a lecture source to jump directly to that section of the
              video.
            </p>
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;
