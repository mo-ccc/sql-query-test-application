import React from 'react'

import {render, fireEvent, cleanup, waitForElement, waitForDomChange} from "@testing-library/react"

import LandingPage from './LandingPage'

afterEach(cleanup)

test("test form validation", async () => {
    const {getByPlaceholderText} = render(
        <LandingPage />
    )
    debug()
    const emailField = getByPlaceholderText('login email')
    fireEvent.change(emailField, {target: {value: "use"}})
    await waitForDomChange()
    debug()
}

)