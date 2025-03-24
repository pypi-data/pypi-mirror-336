import './App.css';
import { useState, useEffect } from 'react';

function App() {
  const [joke, setJoke] = useState('');
  const [showPunchline, setShowPunchline] = useState(false);
  const [emoji, setEmoji] = useState('🤔');
  const [dadJokeMode, setDadJokeMode] = useState(false);
  const [showConfetti, setShowConfetti] = useState(false);
  
  const regularJokes = [
    { setup: "Why don't scientists trust atoms?", punchline: "Because they make up everything!" },
    { setup: "Why did the scarecrow win an award?", punchline: "Because he was outstanding in his field!" },
    { setup: "Why don't eggs tell jokes?", punchline: "They'd crack each other up!" },
    { setup: "What do you call a fake noodle?", punchline: "An impasta!" },
    { setup: "How do you organize a space party?", punchline: "You planet!" },
    { setup: "Why did the bicycle fall over?", punchline: "It was two-tired!" },
    { setup: "What's the best thing about Switzerland?", punchline: "I don't know, but the flag is a big plus!" }
  ];
  
  const dadJokes = [
    { setup: "I'm reading a book about anti-gravity.", punchline: "It's impossible to put down!" },
    { setup: "Did you hear about the guy who invented the knock-knock joke?", punchline: "He won the 'no-bell' prize!" },
    { setup: "I used to be a baker, but I couldn't make enough dough.", punchline: "So I got a job at the local gym. Now I'm making tons of cake!" },
    { setup: "Why don't skeletons fight each other?", punchline: "They don't have the guts!" },
    { setup: "I was going to tell a time-traveling joke,", punchline: "but you didn't like it." },
    { setup: "What's Forrest Gump's password?", punchline: "1Forrest1" },
    { setup: "Why did the invisible man turn down a job offer?", punchline: "He couldn't see himself doing it." },
  ];
  
  const getRandomJoke = () => {
    const jokesList = dadJokeMode ? dadJokes : regularJokes;
    const randomIndex = Math.floor(Math.random() * jokesList.length);
    setJoke(jokesList[randomIndex]);
    setShowPunchline(false);
    setEmoji('🤔');
  };
  
  useEffect(() => {
    if (!joke) {
      setEmoji('🤔');
    } else if (showPunchline) {
      const laughEmojis = dadJokeMode ? ['👨', '👴', '😐', '🤦‍♂️', '👍'] : ['😂', '🤣', '😆', '😹', '🥲'];
      const randomEmoji = laughEmojis[Math.floor(Math.random() * laughEmojis.length)];
      setEmoji(randomEmoji);
      
      // Show confetti when punchline is revealed
      setShowConfetti(true);
      setTimeout(() => {
        setShowConfetti(false);
      }, 2000);
    } else {
      setEmoji('🤔');
    }
  }, [joke, showPunchline, dadJokeMode]);
  
  const toggleDadJokeMode = () => {
    setDadJokeMode(!dadJokeMode);
    setJoke('');  // Clear current joke
  };
  
  // Creates multiple confetti pieces with random properties
  const renderConfetti = () => {
    const confettiCount = 50;
    const colors = ['#f8e16c', '#ff9800', '#61dafb', '#ff6b6b', '#4facfe'];
    
    return Array.from({ length: confettiCount }).map((_, index) => {
      const size = Math.floor(Math.random() * 10) + 5;
      const color = colors[Math.floor(Math.random() * colors.length)];
      const left = Math.random() * 100;
      const animationDuration = Math.random() * 3 + 1;
      const animationDelay = Math.random() * 0.5;
      
      return (
        <div
          key={index}
          className="confetti-piece"
          style={{
            left: `${left}%`,
            width: `${size}px`,
            height: `${size}px`,
            backgroundColor: color,
            animationDuration: `${animationDuration}s`,
            animationDelay: `${animationDelay}s`
          }}
        />
      );
    });
  };
  
  return (
    <div className="App">
      <div className="background-shapes">
        <div className="shape shape1"></div>
        <div className="shape shape2"></div>
        <div className="shape shape3"></div>
        <div className="shape shape4"></div>
        <div className="shape shape5"></div>
      </div>
      
      {showConfetti && (
        <div className="confetti-container">
          {renderConfetti()}
        </div>
      )}
      
      <header className="App-header">
        <h1 className="app-title">Hello, World!</h1>
        <p className="app-subtitle">Welcome to my first React app</p>
        
        <div className={`emoji-container ${joke ? 'emoji-animated' : ''}`}>
          <span className="emoji">{emoji}</span>
        </div>
        
        <div className="joke-container">
          <div className="mode-toggle">
            <label className="switch">
              <input type="checkbox" checked={dadJokeMode} onChange={toggleDadJokeMode} />
              <span className="slider round"></span>
            </label>
            <span className="mode-label">{dadJokeMode ? "Dad Joke Mode 👨" : "Regular Joke Mode 😆"}</span>
          </div>
          
          <button onClick={getRandomJoke} className="joke-button">
            Tell me a joke!
          </button>
          
          {joke && (
            <div className="joke">
              <p>{joke.setup}</p>
              
              {!showPunchline ? (
                <button onClick={() => setShowPunchline(true)} className="punchline-button">
                  Reveal punchline
                </button>
              ) : (
                <p className="punchline">{joke.punchline}</p>
              )}
            </div>
          )}
        </div>
      </header>
    </div>
  );
}

export default App;
