import React, { useContext, useRef, useState } from "react";
import ReactPlayer from 'react-player'
import AppContext from "../../youtubeStore/app-context"
import Loader from '../Loader/Loader.jsx'
import Lottie from "lottie-react";
import loaderAnimation from "../../../animations/96187-gears.json"
import "./Leftside.css"


const Leftside = props => {
	let inputRef = useRef("");
  const [show, setShow] = useState(false);
  const [ videoID, setVideoID ] = useState("");
  const ctx = useContext(AppContext);
  const [originalUrl, setoriginalUrl] = useState();
  const [balls, setBalls] = useState(false);
  let videoDisplay = "none";
  let loaderDisplay = "none";


  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);
  let originalLink = "";

	const formSubmitHandler = async (event) => {
    setoriginalUrl(inputRef.current.value);
    originalLink = inputRef.current.value;
    console.log('got here');
		event.preventDefault()
    console.log(originalLink);
    if(! validateUrl(inputRef.current.value) ){
      alert('not a valid youtube link !')
      inputRef.current.value = "";
    } else { 
      if( originalLink === "https://www.youtube.com/watch?v=tsxmyL7TUJg"){
        setBalls(true);
        console.log(balls);
        console.log("BALLS HAVE BEEN SET TO TRUE")
      }
      if( originalLink === "https://www.youtube.com/watch?v=tsxmyL7TUJg"){
        setBalls(true);
      }
      console.log(balls)
      console.log("made it")
      const regex = /youtu(?:\.be|be\.com)\/(?:.*v(?:\/|=)|(?:.*\/)?)([a-zA-Z0-9_-]{11})/;
      const match = inputRef.current.value.match(regex)
      const m = match ? match[1] : null;

      const url = "https://www.youtube-nocookie.com/embed/" + m;
      setVideoID(m);

      ctx.setBaseUrl(url);
      ctx.setUrl(url);
      // SEND POST REQUEST YUIPEE
    ctx.setFetchingData(true);
    let response = await fetch("http://172.20.10.13:8080/get_info?url=" + originalLink, {
				method: 'GET',
				headers: {
					'Accept': '*/*',
					'Connection': 'keep-alive',
					'Content-Type': 'application/json',
					'Access-Control-Allow-Origin': '*',
					'Access-Control-Allow-Headers': '*',
					'Access-Control-Allow-Credentials': true,
				}
			}).catch((err) => { alert(err) })
      console.log(response);
			let data = await response.json()
      data = data.data;
      console.log(data);
      for (let index = 0; index <=6 ; index++) {
        console.log("PRINTING DEBUG INFO FOR " + index + "TH DATA");
        console.log(data[index]);
      }
      videoDisplay = "contents"
      ctx.setSubject(data[0]);
      ctx.setNotes(data[ 1 ])
      let timestamps = data[2]
      console.log(data[2]);
      console.log(timestamps)
      ctx.setTimestamps(timestamps)
      // ctx.setQuizData(data[3])
      ctx.setWikipediaLinks(data[5])
      ctx.setFetchingData(false);
      ctx.setRetrievedData(true);
      originalLink = inputRef.current.value;
      this.forceUpdate();
    }
	}

  const validateUrl = (url) => {
    const regex = /^(https?:\/\/)?(www\.)?youtube\.com\/watch\?v=([a-zA-Z0-9_-]+)$/;
    return regex.test(url);
  }

	return (
    <>
    <div className="leftside">
      <form onSubmit={formSubmitHandler} className="HURR">
        <input ref={inputRef} placeholder="Enter a youtube link" />
      </form>
      <br/>
    { videoID != "" ? (
    <>
     <p>{originalUrl} is your link</p> 
    <iframe className="youtubeVideoPlayer" width="1080" height="608" src={ctx.url} title="YouTube video player" frameBorder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowFullScreen/>
          </> 
    ) : (
    <div>
    </div>
          )
    } 

    {
    originalUrl === "https://www.youtube.com/watch?v=tsxmyL7TUJg" ?(
        <ReactPlayer
          className='react-player fixed-bottom'
          style={{display: ctx.retrievedData ? "contents" : "none"}}
          url= 'b.mov'
          width='1080px'
          height='608px'
          controls = {true}
        /> ):(
            <Lottie style={{display: ctx.retrievedData ? "contents" : "none"}} animationData={loaderAnimation}/>
            )}
    </div>
    </>
    )
}

export default Leftside

