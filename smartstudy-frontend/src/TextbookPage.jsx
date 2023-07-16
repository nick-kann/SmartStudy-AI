import React, { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import NavBar from "./textbookComponents/Navbar/NavBar"
import Leftside from "./textbookComponents/Leftside/Leftside"
import Rightside from "./textbookComponents/Rightside/Rightside"
import { AppContextProvider } from './textbookStore/app-context'

function TextbookPage() {

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

export default TextbookPage 
