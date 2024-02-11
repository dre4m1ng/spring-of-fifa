import "./App.css";
import indexVideoSrc from "./youtube.mp4";
import indexFCOnlineLogo from "./fc_online_logo.png";
import { Input } from "@/components/ui/input";
import * as React from "react";
import CarouselOrientation from "CarouselOrientation";
import MenubarDemo from "MenubarDemo";

function App() {
  return (
    <div className="App">
      <div className="App-top-nav-bar">
        <MenubarDemo></MenubarDemo>
      </div>
      <video
        className="App-video"
        src={indexVideoSrc}
        autoPlay
        loop
        muted
      ></video>
      <div className="App-vertical-line"></div>
      <img className="App-logo" src={indexFCOnlineLogo} alt="logo" />
      <Input
        className="App-input"
        type="email"
        placeholder="구단주 이름 / 선수 정보 / 전적 검색..."
      />
      <div className="App-carousel-wrapper">
        <CarouselOrientation />
      </div>
    </div>
  );
}

export default App;
