import { useContext, useRef, useState } from "react";
import ReactMarkdown from 'react-markdown';
import AppContext from "../../youtubeStore/app-context"
import { Circles } from 'react-loader-spinner'
import Lottie from "lottie-react";
import loaderAnimation from "../../../animations/96187-gears.json"
import "./Rightside.css";


const Rightside = props => {
	let inputRef = useRef("");
  const [ notes, setNotes ] = useState("");
  const ctx = useContext(AppContext);

  const timestamps = ctx.timestamps;

  let wikipediaLinks = ctx.wikipediaLinks;

  const [showNotePad, setShowNotePad ] = useState(false) ;

	const retrieveMeow = async (event) => {
    
	}

  const toggleNotePad = () => {
    console.log("meow")
    setShowNotePad(!showNotePad);
  }
  
  const timestampFunct = (seconds) => {
    ctx.setUrl(ctx.baseUrl+"?start="+seconds)
  }

  const validateUrl = (url) => {
    const regex = /^(https?:\/\/)?(www\.)?youtube\.com\/watch\?v=([a-zA-Z0-9_-]+)$/;
    return regex.test(url);
  }

	return (
    ctx.retrievedData ? (
    <div className="rightside">
      <div className="sitsOnTop">
      <div className="notePad">
        <h1 style={{display: "block",  zIndex: "-1", textAlign: "center"}}>{ctx.subject} Notes</h1>
        {/* <button style={{display : "block", margin: "auto", position: "relative"}} onClick={()=>toggleNotePad()}> X </button> */} 
        <ReactMarkdown style={{display: false}}className="notesMarkdown" children={ctx.notes}/>
        
      </div>
      <div className="timestamplist">
        <h1>Important Timestamps</h1>
        {timestamps.map((seconds)=>{
              let singleDigit = false;
              if((seconds%60).toString().length==1){
                singleDigit = true
              }
          return(
            <p onClick={() => timestampFunct(seconds)} key={seconds} className="timestampLink">{Math.floor( seconds/60 )}:{singleDigit? "0": ""}{seconds%60}</p>
          )
        })}
    </div>
    </div>
      <div className="wikipediaLinks">
        <h1>Wikipedia links that you may be interested in:</h1>
        {wikipediaLinks.map((link)=>{
          const parts = link.split("/").filter(Boolean);
          // The title is the last part of the split array
          const title = parts[parts.length - 1];
          
          // Decode the URI component
          const decodedTitle = decodeURIComponent(title);
           const formattedTitle = decodedTitle.replace(/_/g, " ");
          return(
            <a style={{textDecoration: "none", color: "cyan", fontSize : "40px"}}href={link} key={link} target="_blank" rel="noopener noreferrer" >{formattedTitle}</a>
          )
        })}
      </div>
    </div>
    ) : (
      (
          ctx.fetchingData?(
            <Lottie animationData={loaderAnimation}/>
          ): (
            <div>
              temp
            </div>
          )
        )
    )
  )
}

export default Rightside

