import React from "react";
import "./NavBar.css"
import { useNavigate } from 'react-router-dom'

const NavBar = props => {
  const history = useNavigate();
  const home = () => {
    history('/');
  }
	return (
		<header className="header">
			<h1 onClick={()=>home()}> SmartSudy AI </h1>
		</header>
	)
}
export default NavBar

