import { useLocation, useHistory } from 'react-router-dom'
import { useEffect, useState } from 'react'
import axios from 'axios'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'
import Button from 'react-bootstrap/Button'
import Alert from 'react-bootstrap/Alert'

import TableBase from '../components/TableBase.js'
import SchemaBase from '../components/SchemaBase.js'
import FeedBackText from '../components/FeedBackText.js'
import ModalConfirm from '../components/ModalConfirm.js'

const TestPage = () => {
  let externalState = useLocation().state
  let history = useHistory()
  let [state, setState] = useState()
  let [textareaState, setTextareaState] = useState()
  let [responseState, setResponseState] = useState()

  // Question data is retrieved
  useEffect(() =>{
    if (!externalState) {
      history.push('/') // return to homepage if there is no question
    }
    axios.get(`${process.env.REACT_APP_HOST}/test/${externalState?.testId}`)
      .then(response => {setState(response?.data)})
        .catch(error => console.log(error?.response))
  }, [])

  // Keeping track of textarea state
  const handleAreaChange = (event) => {
    setTextareaState(event.target.value)
  }

  // Execute data is retrieved
  const handleExecute = () => {
    axios.post(`${process.env.REACT_APP_HOST}/test/${externalState?.testId}/execute`, {query: textareaState})
      .then(response => {setResponseState(response?.data)})
        .catch(error => {setResponseState(error.response?.data)})
  }

  const handleSubmit = () => {
    console.log(textareaState)
  }

  if (!externalState) {
    return null
  }
  return(
    <div className="container">
      <h1>Question</h1>
      <hr/>
      <Row>
        <Col xs={12} md={8}>
          <h5>{state?.question?.prompt}</h5>
          <textarea style={{height: 100}} className="w-100 form-control" value={textareaState} onChange={handleAreaChange} />
          <Button variant="outline-dark" className="m-1" onClick={handleExecute}>Execute</Button>
          <ModalConfirm handleSubmit={handleSubmit}/>
          {responseState?.error && 
            <Alert variant="danger">
              {responseState?.error}
            </Alert>
          }
          <TableBase className="mt-3 mb-3 border-bottom" data={responseState} />
          <FeedBackText data={responseState} />
          
        </Col>
        <Col className="p-4" xs={12} md={4} style={{overflowY: "scroll", maxHeight: 600}}>
          <div>
            <h3>Schema's</h3>
            <hr/>
            {state && Object.keys(state?.question?.tables).map(tableName => (
              <SchemaBase key={tableName} name={tableName} data={state.question.tables[tableName]} />
            ))}
          </div>
        </Col>
      </Row>
      
    </div>
  )
}

export default TestPage