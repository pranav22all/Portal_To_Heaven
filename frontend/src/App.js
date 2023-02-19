import logo from './logo.svg';
import './App.css';
import React, { useEffect, useState } from 'react';
import axios from 'axios'
import { AudioRecorder } from 'react-audio-voice-recorder';

function App() {
  const [getMessage, setGetMessage] = useState({})
  const [audioText, setAudioText] = useState("");

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
      console.log("Student Audio says " + response.data)
      setAudioText(response.data)

      let formDataTwo = new FormData() 
      formDataTwo.append("audioText", response.data)
      axios.post('http://localhost:5000/call_gpt', formDataTwo).then((responseTwo) => {
        console.log("GPT says " + responseTwo.data)
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

  return (
    <div className="App">
      <header className="App-header">
        <p>Portal To Heaven</p>
        <AudioRecorder onRecordingComplete={addAudioElement} />
      </header>
        <video controls width="250">
          <source src="../public/lipsync.mov" type="video/mov" />
        </video>
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