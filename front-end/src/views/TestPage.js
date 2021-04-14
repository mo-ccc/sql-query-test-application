import { useLocation } from 'react-router-dom'
import { useEffect, useState } from 'react'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'
import Button from 'react-bootstrap/Button'
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

  const handleExecute = () => {
    axios.post(`${process.env.REACT_APP_HOST}/test/${externalState?.testId}/execute`, {query: textareaState})
    .then(response => console.log(response))
    .catch(error => console.log(error))
  }

  return(
    <div className="container">
      <h1>Question 1.</h1>
      <hr/>
      <Row>
        <Col xs={12} md={6}>
          <h5>{state?.question?.prompt}</h5>
          <textarea style={{height: 200}} className="w-100 form-control" value={textareaState} onChange={handleAreaChange} />
          <Button className="m-1" onClick={handleExecute}>Execute</Button>
        </Col>
        <Col xs={12} md={6}>
          <img src="https://vtb-league.com/app/plugins/photonic/include/images/placeholder.png" width="100%"/>
        </Col>
      </Row>
      
    </div>
  )
}

export default TestPage