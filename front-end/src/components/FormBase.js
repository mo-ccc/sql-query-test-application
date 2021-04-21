import {useEffect} from 'react'
import _ from 'lodash';
import { useForm } from 'react-hook-form'

const FormBase = ({defaultData, onSubmit, formMeta, fields, submitLabel}) => {
  const {register, handleSubmit, errors, setError} = useForm(formMeta)
  useEffect(() => {
    setError(fields?.[0]?.name, "fill me") // this makes submit disabled by default
  }, [])

  // if no values are given for an option. values will default to i
  // if no labels are given for an option. labels will default to values
  // either labels or values are required
  const renderInput = {
    "select": (item) => (
      <>
        <select className="form-control" name={item.name} ref={register(item.validation)} defaultValue={defaultData?.[item.name]}>
          {item.options.map((option, i) => <option key={option.value ?? option.label} value={option.value ?? i}>{option.label ?? option.value}</option>)} 
        </select>
      </>
    ),
    "bool": (item) => (
      <>
        <select className="form-control" name={item.name} ref={register(item.validation)} defaultValue={defaultData?.[item.name]}>
          <option key="true" value="true">true</option>
          <option key="false" value="false">false</option>
        </select>
      </>
    ),
    "flex": (item) => (
      <div className="row">
        {item.fields.map((nestedItem, i) => (
          <div className="col-6 col-md-4">
            {renderer(nestedItem, i, true)}
          </div>
        ))}
      </div>
    )
  }
  // this render will use renderInput to render a form group with surrounding error messages
  const renderer = (item, i, noBot) => (
    <div className="form-group" key={item.name} style={noBot && {marginBottom: 0}}>
      {item.label && <label>{item.label}</label>}
      {_.has(errors, item.name) &&
        <small className="form-text text-muted">{_.get(errors, item.name).message}</small>
      }
      {item.inputType in renderInput ?
        renderInput[item.inputType](item)
          :
        <input className="form-control" name={item.name} placeholder={item.placeholder} type={item.inputType} defaultValue={defaultData?.[item.name]} ref={register(item.validation)} />
      }
    </div>
  )

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="w-100">
      {fields.map((item, i) => {
        return renderer(item, i)
      })}
      <input disabled={Object.keys(errors).length} type="submit" className="btn btn-primary" value={submitLabel}/>
    </form>
  )
}
export default FormBase