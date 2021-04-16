import { useLocation } from 'react-router-dom'
import { useEffect, useState } from 'react'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'
import Button from 'react-bootstrap/Button'
import axios from 'axios'
import TableBase from '../components/TableBase.js'
import SchemaBase from '../components/SchemaBase.js'
import Alert from 'react-bootstrap/Alert'

const TestPage = () => {
  let externalState = useLocation().state
  let [state, setState] = useState()
  let [textareaState, setTextareaState] = useState()
  let [responseState, setResponseState] = useState()


  useEffect(() =>{
    axios.get(`${process.env.REACT_APP_HOST}/test/${externalState?.testId}`)
    .then(response => {setState(response.data); console.log(response.data)})
    .catch(error => console.log(error.response))
  }, [])

  const handleAreaChange = (event) => {
    setTextareaState(event.target.value)
  }

  const handleExecute = () => {
    axios.post(`${process.env.REACT_APP_HOST}/test/${externalState?.testId}/execute`, {query: textareaState})
    .then(response => {setResponseState(response.data); console.log(response)})
    .catch(error => {setResponseState(error.response.data); console.log(error)})
  }

  return(
    <div className="container">
      <h1>Question 1.</h1>
      <hr/>
      <Row>
        <Col xs={12} md={8}>
          <h5>{state?.question?.prompt}</h5>
          <textarea style={{height: 100}} className="w-100 form-control" value={textareaState} onChange={handleAreaChange} />
          <Button className="m-1" onClick={handleExecute}>Execute</Button>
          {responseState?.error && 
            <Alert variant="danger">
              {responseState?.error}
            </Alert>
          }
          <TableBase data={responseState?.result_set} />
          <h5>{responseState?.matches ? "query is correct" : "query is incorrect"}</h5>
        </Col>
        <Col className="p-4" xs={12} md={4} style={{overflowY: "scroll", height: 400}}>
          <h3>Schema's</h3>
          <hr/>
          {state && Object.keys(state?.question?.tables).map(tableName => (
            <SchemaBase key={tableName} name={tableName} data={state.question.tables[tableName]} />
          ))}
        </Col>
      </Row>
      
    </div>
  )
}

export default TestPage