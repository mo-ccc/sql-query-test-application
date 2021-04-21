import React from 'react'
import {useSelector} from 'react-redux'
import store from '../redux/store.js'
import Alert from 'react-bootstrap/Alert'

const NotificationAlert = () => {
  const success = useSelector(state => state.text)

  const style = {
    "position": "fixed",
    "bottom": "0px",
    "left": "10px",
    "right": "10px",
    "zIndex": "99999"
  }

  if (success) {
    setTimeout(() => {store.dispatch({type: "SET_ALERT", text: ""})}, 3000)
    return(
      <div style={style}>
        <Alert variant="danger" onClose={() => store.dispatch({type: "SET_ALERT", text: ""})} dismissible>
          <p>
            {success}
          </p>
        </Alert>
      </div>
    )}else {
    return(null)
  }
}
export default NotificationAlert