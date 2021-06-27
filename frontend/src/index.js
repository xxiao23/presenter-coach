import React from 'react';
import ReactDOM from 'react-dom';
import Webcam from 'react-webcam';

const WebcamCapture = () => {
  const webcamRef = React.useRef(null);
  const [imgSrc, setImgSrc] = React.useState(null);

  const capture = React.useCallback(() => {
    const imgSrc = webcamRef.current.getScreenshot();
    setImgSrc(imgSrc);
  }, [webcamRef, setImgSrc]);

  return (
    <>
      <Webcam
        audio={false}
        ref={webcamRef}
        screenshotFormat='image/jpeg'
      />
      <button onClick={capture}>Capture photo</button>
      {imgSrc && (
        <img  src={imgSrc}/>
      )}
    </>
  )
}
// Mount the app to the mount point.
const root = document.getElementById('app');
ReactDOM.render(<WebcamCapture />, root);