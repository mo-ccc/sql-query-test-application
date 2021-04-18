import {useState} from 'react'
import Button from 'react-bootstrap/Button'
import Modal from 'react-bootstrap/Modal'

const ModalConfirm = ({handleSubmit}) => {
  const [show, setShow] = useState(false);

  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);

  return (
    <>
      <Button variant="outline-danger" onClick={handleShow}>
        Submit
      </Button>

      <Modal show={show} onHide={handleClose}>
        <Modal.Header closeButton>
          <Modal.Title>Are you sure you want to submit?</Modal.Title>
        </Modal.Header>
        <Modal.Body>Once submitted answer will be graded and cannot be edited.</Modal.Body>
        <Modal.Footer>
          <Button variant="outline-dark" onClick={handleClose}>
            No
          </Button>
          <Button variant="outline-danger" onClick={handleSubmit}>
            Yes
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  )
}
export default ModalConfirm