import { useLocation } from 'react-router-dom'
import { useEffect, useState } from 'react'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'
import axios from 'axios'

const TestPage = () => {
  let externalState = useLocation().state
  let [state, setState] = useState()
  let [textareaState, setTextareaState] = useState()


  useEffect(() =>{
    axios.get(`${process.env.REACT_APP_HOST}/test/${externalState?.testId}`)
    .then(response => {setState(response.data); console.log(response.data)})
    .catch(error => console.log(error))
  }, [])

  const handleAreaChange = (event) => {
    setTextareaState(event.target.value)
  }

  return(
    <div className="container">
      <h1>Test page {externalState?.testId}</h1>
      <Row>
        <Col md={6}>
          <h4>{state?.question?.prompt}</h4>
          <textarea value={textareaState} onChange={handleAreaChange} />
        </Col>
        <Col md={6}>
          <img src="https://vtb-league.com/app/plugins/photonic/include/images/placeholder.png" width="400px"/>
        </Col>
      </Row>
      
    </div>
  )
}

export default TestPage