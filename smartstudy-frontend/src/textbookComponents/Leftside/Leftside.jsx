import React, { useContext, useRef, useState, useEffect } from "react";
import AppContext from "../../textbookStore/app-context";
import Loader from "../Loader/Loader.jsx";
import "./Leftside.css";

const Leftside = (props) => {
  const inputRef = useRef(null);
  const [show, setShow] = useState(false);
  const [imageURL, setImageURL] = useState("");
  const [imageWidth, setImageWidth] = useState(null); // New state to store the image width
  const ctx = useContext(AppContext);

  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);

const formSubmitHandler = async (event) => {
  event.preventDefault();
  const file = inputRef.current.files[0];
  if (!file) {
    alert("Please select a PNG file.");
    return;
  }

  const reader = new FileReader();
  reader.onload = async () => {
    const url = reader.result;
    const img = new Image();
    img.src = url;
    img.onload = async () => {
      const maxWidth = window.innerWidth * 0.3; // Adjust this value as needed
      const scaleFactor = maxWidth / img.width;
      const resizedWidth = img.width * scaleFactor;
      setImageWidth(resizedWidth); // Store the resized width in state
      setImageURL(url);
      ctx.setBaseUrl(url);
      ctx.setUrl(url);
      ctx.setRetrievedData(true);

      const formData = new FormData();
      formData.append("image", file);

      try {
        ctx.setisLoading(true);
        const response = await fetch("http://172.20.10.13:8080/upload", {
          method: "POST",
          body: formData,
        });

        if (response.ok) {
          alert("Image uploaded successfully");
          const responseData = await response.json();
          // Process the response data as needed
            ctx.setloaded(true);
            ctx.setisLoading(false);
            ctx.setNotes(Math.floor(Math.random() * 5))
        } else {
          alert("Image upload failed");
        }
      } catch (error) {
        console.error("Error occurred during image upload:", error);
      }
    };
  };
  reader.readAsDataURL(file);

  // Additional logic if needed

  inputRef.current.value = null;
};

  useEffect(() => {
    const handleResize = () => {
      const maxWidth = window.innerWidth * 0.3; // Adjust this value as needed
      const scaleFactor = maxWidth / imageWidth;
      const resizedWidth = imageWidth * scaleFactor;
      setImageWidth(resizedWidth);
    };

    window.addEventListener("resize", handleResize);
    return () => {
      window.removeEventListener("resize", handleResize);
    };
  }, [imageWidth]);

  return (
    <>
      <div className="leftside right-align" style={{ marginLeft: "25vw", marginTop: "-10vw" }}>

        <form onSubmit={formSubmitHandler} className="HURR">
          <div style={{ display: "flex", alignItems: "center", flexDirection: "column" }}>
            <div style={{ display: "flex", width: "40vw", alignItems: "center", flexDirection: "column" }}>
              <input
                type="file"
                ref={inputRef}
                accept=".png"
                style={{ width: "20vw", height: "3vh", fontSize: "15px", padding: "0.5rem" }}
              />
            </div>
            <div>
              {imageURL !== "" ? (
                <img
                  src={imageURL}
                  alt="Uploaded PNG"
                  className="Leftside" // Apply the CSS class here
                  style={{ maxWidth: "100%", width: imageWidth }} // Set the image width with maxWidth and current width
                />
              ) : (
                <div>
                  {/* <Loader/> */}
                </div>
              )}
            </div>
            <div>
              <button type="submit" style={{ fontSize: "12px" }}>
                Upload PNG of a page of a textbook
              </button>
            </div>
          </div>
        </form>
      </div>
    </>
  );
};

export default Leftside;
