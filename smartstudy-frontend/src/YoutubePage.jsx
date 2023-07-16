import React, { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import NavBar from "./youtubeComponents/Navbar/NavBar"
import Leftside from "./youtubeComponents/Leftside/Leftside"
import Rightside from "./youtubeComponents/Rightside/Rightside"
import { AppContextProvider } from './youtubeStore/app-context'

function YoutubePage() {

  return (
  <AppContextProvider>
    <div>
      <NavBar/>
      <div className="body">
          <Leftside/>
          <Rightside/>
      </div>
    </div>
  </AppContextProvider>
)
}

export default YoutubePage
