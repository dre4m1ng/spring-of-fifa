import "./App.css";
import indexVideoSrc from "./youtube.mp4";
import indexFCOnlineLogo from "./fc_online_logo.png";

function App() {
  return (
    <div className="App">
      <video
        className="App-video"
        src={indexVideoSrc}
        autoPlay
        loop
        muted
      ></video>
      <div className="App-vertical-line"></div>
      <img className="App-logo" src={indexFCOnlineLogo} alt="logo" />
    </div>
  );
}

export default App;
