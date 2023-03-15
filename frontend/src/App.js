import lipsync from './lipsync.mov'
import jfk_img from './jfk.jpg'
import armstrong_img from './armstrong.jpeg'
import mandela_img from './mandela2.webp'
import roosevelt_img from './roosevelt.jpeg'
import feynman_img from "./feynman.jpeg"
import './App.css';
import React, { useEffect, useState} from 'react';
import axios from 'axios'
import { AudioRecorder } from 'react-audio-voice-recorder';
import { Alert } from '@mui/material';
import { Carousel } from 'react-responsive-carousel';
import "react-responsive-carousel/lib/styles/carousel.min.css"; // requires a loader


function App() {
  const [getMessage, setGetMessage] = useState({})
  const [audioText, setAudioText] = useState("");
  const [alert, setAlert] = useState(false);
  const [agent, setAgent] = useState("John F. Kennedy"); 

  useEffect(()=>{
    axios.get('http://localhost:5000/flask/hello').then(response => {
      console.log("SUCCESS", response)
      setGetMessage(response)
    }).catch(error => {
      console.log(error)
    })

  }, [])

  const addAudioElement = (blob) => {
    const url = URL.createObjectURL(blob);
    const audio = document.createElement('audio');
    audio.src = url;
    audio.controls = true;
    console.log(url);

    let formData = new FormData() 
    formData.append("audio_file", blob)


    axios.post('http://localhost:5000/transfer_audio', formData).then((response) => {
      console.log("Student Audio says " + response.data);
      setAudioText(response.data);
      setAlert(true);
      
      let formDataTwo = new FormData();
      formDataTwo.append("audioText", response.data)
      formDataTwo.append("agent", agent)
      axios.post('http://localhost:5000/call_gpt', formDataTwo).then((responseTwo) => {
        console.log("GPT says " + responseTwo.data)
        window.location.reload(false)
      })

    }).catch((error) => {
      console.log(error); 
    });
 
    // fetch('http://localhost:5000/flask/transfer_audio', {
    //   method: "POST",
    //   cache: "no-cache",
    //   body: formData}).then( resp => {
    //     console.log("Finished")
    //     }
    //   ); 
    
  };

  const switchAgent = (index) => {
    if (index === 0){
      setAgent("John F. Kennedy")
    }
    else if (index == 1){
      setAgent("Neil Armstrong")
    }
    else if (index == 2){
      setAgent("Nelson Mandela")
    }
    else if (index == 3){
      setAgent("Eleanor Roosevelt")
    }
    else{
      setAgent("Richard Feynman")
    }
  }

  return (
    <div className="App">
      <header className="App-header">
        <p>Lively: A Portal To The Beyond</p>
        <Carousel width="500px" onChange={switchAgent}>
          <div>
              <img src={jfk_img}/>
              <p className="legend">John F. Kennedy</p>
          </div>
          <div>
              <img src={armstrong_img}/>
              <p className="legend">Neil Armstrong</p>
          </div>
          <div>
              <img src={mandela_img}/>
              <p className="legend">Nelson Mandela</p>
          </div>
          <div>
              <img src={roosevelt_img}/>
              <p className="legend">Eleanor Roosevelt</p>
          </div>
          <div>
              <img src={feynman_img}/>
              <p className="legend">Richard Feynman</p>
          </div>

        </Carousel>
        <AudioRecorder onRecordingComplete={addAudioElement} />
        
        <div className="alert-div">
           
        </div>
        {alert ? <Alert severity='info'>{agent} is thinking of a response!</Alert> : <></> }  
        
        <video width="750" height="500" controls >
          <source src={lipsync} type="video/mp4"/>
        </video>      
      </header>
        
    </div>
  );
}

export default App;


// import logo from './logo.svg';
// import './App.css';
// import React, { useEffect, useState } from 'react';
// import axios from 'axios'

// function App() {
//   const [getMessage, setGetMessage] = useState({})

//   useEffect(()=>{
//     axios.get('http://localhost:5000/flask/hello').then(response => {
//       console.log("SUCCESS", response)
//       setGetMessage(response)
//     }).catch(error => {
//       console.log(error)
//     })

//   }, [])
//   return (
//     <div className="App">
//       <header className="App-header">
//         <img src={logo} className="App-logo" alt="logo" />
//         <p>React + Flask Tutorial</p>
//         <div>{getMessage.status === 200 ? 
//           <h3>{getMessage.data.message}</h3>
//           :
//           <h3>LOADING</h3>}</div>
//       </header>
//     </div>
//   );
// }

// export default App;