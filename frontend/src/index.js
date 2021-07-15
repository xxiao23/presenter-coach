import React from 'react';
import ReactDOM from 'react-dom';
import axios from 'axios';

class AudioVideoStream extends React.Component {
  constructor(props) {
    super(props);
    console.log('AudioVideoStream constructor');
    this.audioCtx = null;
    this.canvas = null;
    this.canvasCtx = null;
    this.mediaRecorder = null;
    this.requestDataId = null;
    this.chunks = [];
    this.mediaBlob = null;

    this.draw = this.draw.bind(this);
    this.visualize = this.visualize.bind(this);
    this.startRecord = this.startRecord.bind(this);
    this.stopRecord = this.stopRecord.bind(this);
  }

  draw(canvas, canvasCtx, analyser, dataArray, bufferLength) {
    const WIDTH = canvas.width
    const HEIGHT = canvas.height;

    requestAnimationFrame(() => {
      this.draw(canvas, canvasCtx, analyser, dataArray, bufferLength);
    });

    analyser.getByteTimeDomainData(dataArray);

    canvasCtx.fillStyle = 'rgb(200, 200, 200)';
    canvasCtx.fillRect(0, 0, WIDTH, HEIGHT);

    canvasCtx.lineWidth = 2;
    canvasCtx.strokeStyle = 'rgb(0, 0, 0)';

    canvasCtx.beginPath();

    let sliceWidth = WIDTH * 1.0 / bufferLength;
    let x = 0;


    for(let i = 0; i < bufferLength; i++) {

      let v = dataArray[i] / 128.0;
      let y = v * HEIGHT/2;

      if(i === 0) {
        canvasCtx.moveTo(x, y);
      } else {
        canvasCtx.lineTo(x, y);
      }

      x += sliceWidth;
    }

    canvasCtx.lineTo(canvas.width, canvas.height/2);
    canvasCtx.stroke();
  }

  visualize(stream) {
    if (!this.audioCtx) {
      this.audioCtx = new AudioContext();
    }

    const source = this.audioCtx.createMediaStreamSource(stream);

    const analyser = this.audioCtx.createAnalyser();
    analyser.fftSize = 2048;
    const bufferLength = analyser.frequencyBinCount;
    const dataArray = new Uint8Array(bufferLength);

    source.connect(analyser);

    this.draw(this.canvas, this.canvasCtx, analyser, dataArray, bufferLength);
  }

  componentDidMount() {
    console.log('componentDidMount');
    this.canvas = document.getElementById('visualizer');
    this.canvasCtx = this.canvas.getContext('2d');

    const videoElement = document.querySelector('video');
    if (videoElement) {
      console.log('Find video element');
      const vidoeConstraints = {
        video: { width: { exact: 640 }, height: { exact: 480 } },
        audio: true,
      };
      navigator.mediaDevices.getUserMedia(vidoeConstraints)
        .then((stream) => {
          console.log('stream');
          console.log(stream);

          console.log('set window stream');
          window.stream = stream;

          console.log('set video element stream');
          console.log(videoElement);
          videoElement.srcObject = stream;

          console.log('create media recorder');
          this.mediaRecorder = new MediaRecorder(stream);

          this.visualize(stream);

          this.mediaRecorder.ondataavailable = (event) => {
            console.log('media recorder data available');
            if (event.data.size > 0) {
              console.log('media recorder blob:');
              console.log(event.data);
              event.data.text().then(text => {
                axios({
                  auth: {
                    username: 'admin',
                    password: '123456',
                  },
                  method: 'post',
                  url: 'http://127.0.0.1:8000/mediablobs/',
                  data: {
                    title: 'presenter media data',
                    data: text,
                  }
                })
                  .then(res => console.log('send media data to server'));
              });
              this.chunks.push(event.data);
              console.log(this.chunks);
            } else {
              console.log('empty media recorder data');
            }
          }
          console.log(this.mediaRecorder.state);

          this.mediaRecorder.onstop = (event) => {
            this.mediaBlob = new Blob(this.chunks, {'type' : 'video/webm'});
            this.chunks = [];
            const player = document.getElementById('playback');
            player.src = window.URL.createObjectURL(this.mediaBlob);
            console.log('load playback');
          }
        })
        .catch(error => console.error(error));
    } else {
      console.error('Can\'t find video element');
    }
  }

  startRecord() {
    this.mediaRecorder.start();
    this.requestDataId = setInterval(() => {
      this.mediaRecorder.requestData();
    }, 5000);
    console.log(this.mediaRecorder.state);
    console.log('recorder started');
  }

  stopRecord() {
    clearInterval(this.requestDataId);
    this.mediaRecorder.stop();
    console.log(this.mediaRecorder.state);
    console.log('recorder stopped');
  }

  render() {
    return (
      <section>
        <video 
          autoPlay 
          muted
          playsInline />
        <canvas id='visualizer' height='60px' />
        <div id="buttons">
          <button id='record' onClick={this.startRecord}>Record</button>
          <button id='stop' onClick={this.stopRecord}>Stop</button>
        </div>
        <video id='playback' controls />
      </section>
    );
  }
}

// Mount the app to the mount point.
const root = document.getElementById('app');
ReactDOM.render(<AudioVideoStream />, root);