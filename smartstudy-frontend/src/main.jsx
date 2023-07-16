import React from 'react'
import ReactDOM from 'react-dom/client'
import YoutubePage from './YoutubePage'
import TextbookPage from './TextbookPage'
import Landingpage from './Landingpage'
import './index.css'
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";

const router = createBrowserRouter([
  {
    path: "/",
    element: <Landingpage/>,
  },
  {
    path: "/youtube",
    element: <YoutubePage/>
  },
  {
    path: "/textbook",
    element: <TextbookPage/>
  }
]);

ReactDOM.createRoot(document.getElementById('root')).render(
	<React.StrictMode>
      <RouterProvider router={router} />
	</React.StrictMode>,
)


