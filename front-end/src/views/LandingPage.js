import FormBase from '../components/FormBase'
import axios from 'axios'
import { useHistory } from 'react-router-dom'

const LandingPage = () => {
  let history = useHistory()

  const onSubmit = (data) => {
    axios.post(`${process.env.REACT_APP_HOST}/user`, data)
    .then(response => {
      history.push({pathname: '/test', state: {testId: response.data.tests[0].id}})
    })
    .catch(error => console.log(error.response))
  }

  const loginFields = [
    {name: "email", label: "Email:", placeholder: "login email", inputType: "email"},
  ]

  return (
  <div className="container">
    <div className="d-flex justify-content-center align-items-center mt-5">
      <div style={{maxWidth: 800}}>
        <FormBase fields={loginFields} onSubmit={onSubmit}/>
      </div>
    </div>
  </div>
  )
}
export default LandingPage