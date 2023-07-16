import React, { useState, useContext } from 'react';
import './Rightside.css';
import AppContext from "../../textbookStore/app-context";
import Lottie from "lottie-react"
import loaderAnimation from "../../../animations/96187-gears.json"

const Rightside = (props) => {
  const ctx = useContext(AppContext);
  const [currentSlide, setCurrentSlide] = useState(0); // State to keep track of the current slide

  const nextSlide = () => {
    setCurrentSlide((prevSlide) => (prevSlide + 1) % 3); // Increment current slide index cyclically
  };

  const renderAudioPlayer = () => {
    switch (currentSlide) {
      case 0:
        return <audio src="public/mp3/output1.mp3" controls />;
      case 1:
        return <audio src="public/mp3/output2.mp3" controls />;
      case 2:
        return <audio src="public/mp3/output3.mp3" controls />;
      default:
        return null;
    }
  };

  return ( 
    ctx.loaded ? (
    <div className="Rightside" style={{ marginTop: '20vh' }}>
      {/* Apply the CSS class here */}
        <div style={{ position: 'relative', left:'10vh'}}>
        <img
          src={`public/slides/${currentSlide}.png`}
          alt=""
            style={{ width: '32vw' , height: '25vw'}} // Increase the width of the slide
        />
        <button
          onClick={nextSlide}
          style={{
            position: 'absolute',
            bottom: '50%',
            transform: 'translateY(50%)',
          }}
        >
          Next
        </button>
         <p>{ctx.notes}</p> 
      </div>
      {renderAudioPlayer()} {/* Render the audio player based on the current slide */}
    </div>
    ) : (
        ctx.isLoading ? (
            <Lottie animationData={loaderAnimation}/>
        ) :(
    <div>
    </div>
          )
    )
  );
};

export default Rightside;
