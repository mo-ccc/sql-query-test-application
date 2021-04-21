import {createStore} from 'redux'

const initialState = {
    text: ""
}

const alertReducer = (state = initialState, action) => {
    if (action.type == SET_NOTIFICATION){
         return {
            text: action.text
        }
    }
    return state
}

const store = createStore(alertReducer)
export default store