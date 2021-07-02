import React from 'react';
import ReactDOM from 'react-dom';

class AudioVideoStream extends React.Component {
  constructor(props) {
    super(props);
    console.log('AudioVideoStream constructor');
  }

  componentDidMount() {
    console.log('componentDidMount');
    const constraints = {
      video: { width: { exact: 640 }, height: { exact: 480 } },
      audio: true,
    };

    const videoElement = document.querySelector('video');
    if (videoElement) {
      console.log('Find video element');
      navigator.mediaDevices.getUserMedia(constraints)
        .then((stream) => {
          console.log('stream');
          console.log(stream);


          console.log('set window stream');
          window.stream = stream;

          console.log('set video element stream');
          console.log(videoElement);
          videoElement.srcObject = stream;

          const track = stream.getVideoTracks()[0];
          const imageCapture = new ImageCapture(track);

          setInterval(() => {
            imageCapture.takePhoto()
              .then(blob => {
                console.log('take snapshot')
                console.log(blob);
              })
              .catch(error => console.log(error));
          }, 5000);
        })
        .catch(error => console.error(error));
    } else {
      console.error('Can\'t find video elemeent');
    }

  }

  render() {
    return (
      <div>
        <video 
          autoPlay 
          muted
          playsInline />
      </div>
    );
  }
}

// Mount the app to the mount point.
const root = document.getElementById('app');
ReactDOM.render(<AudioVideoStream />, root);