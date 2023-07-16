import React, { useState } from "react";

const AppContext = React.createContext({
  notes: "",
  url: "",
  timestamps: [""],
  wikipediaLinks: [""],
  fetchingData : false,
  subject: "",
  quizData: [],
})

export const AppContextProvider = (props) => {
  const [notes, setNotes] = useState("");
  const [url, setUrl] = useState("");
  const [baseUrl, setBaseUrl] = useState("");
  const [timestamps, setTimestamps] = useState([])
  const [wikipediaLinks, setWikipediaLinks] = useState([""]);
  const [retrievedData, setRetrievedData] = useState(false);
  const [fetchingData, setFetchingData] = useState(false);
  const [subject, setSubject] = useState("");
  const [quizData, setQuizData] = useState([]);
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
      fetchingData: fetchingData,
      setFetchingData: setFetchingData,
      timestamps: timestamps,
      setTimestamps: setTimestamps,
      subject: subject,
      setSubject: setSubject,
    }}>
      {props.children}
    </AppContext.Provider>
  )
}

export default AppContext

