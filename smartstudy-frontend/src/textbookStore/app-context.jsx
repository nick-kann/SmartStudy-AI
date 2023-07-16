import React, { useState } from "react";

const AppContext = React.createContext({
  notes: "",
  url: "",
  timestamps: [""],
  wikipediaLinks: ["https://en.wikipedia.org/wiki/Thomas_Jefferson"],
  isLoading : false,
  loaded: false,
})

export const AppContextProvider = (props) => {
  const [notes, setNotes] = useState("");
  const [url, setUrl] = useState("");
  const [baseUrl, setBaseUrl] = useState("");
  const [wikipediaLinks, setWikipediaLinks] = useState(["https://en.wikipedia.org/wiki/Thomas_Jefferson"]);
  const [retrievedData, setRetrievedData] = useState(false);
  const [isLoading, setisLoading] = useState(false)
  const [loaded, setloaded] = useState(false)
  return (
    <AppContext.Provider value={{
      notes:notes,
      setNotes: setNotes,
      url:url,
      setUrl:setUrl,
      baseUrl:baseUrl,
      setBaseUrl: setBaseUrl,
      wikipediaLinks: wikipediaLinks,
      setWikipediaLinks: setWikipediaLinks,
      retrievedData: retrievedData,
      setRetrievedData: setRetrievedData,
      isLoading: isLoading,
      setisLoading: setisLoading,
      loaded: loaded,
      setloaded: setloaded,
    }}>
      {props.children}
    </AppContext.Provider>
  )
}

export default AppContext

