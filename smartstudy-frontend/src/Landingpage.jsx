import React, { useState } from 'react'
import Button from 'react-bootstrap/Button';
import { Outlet, Link } from "react-router-dom";


function Landingpage() {

  return (
  <div>
      <h1 style={{ fontSize: '130px', color : "#3de5ff" }}>Welcome to VizED AI</h1>  
      <div className="rightSide">
       <Link style={{textDecoration: "none", fontSize: "100px", display: "inline-block" , color:"cyan"}} to ={`/youtube`}> Youtube </Link>
        <p style={{fontSize: "50px"}}>
          Enter a youtube link to get your summary and notes !
        </p>
      </div>
      <div className="leftSide">
       <Link style={{textDecoration: "none", fontSize: "100px", display: "inline-block", color:"cyan"}} to ={`/textbook`}> Textbook </Link>
        <p style={{fontSize: "50px"}}>
          Upload a picture of a textbook to get a slideshow, that summarizes the content, along with an AI audio narraration that expands on the topic!
        </p>
      </div>
  </div>
  )
}

export default Landingpage 
