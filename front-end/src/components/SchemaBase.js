const SchemaBase = ({name, data}) => {
  console.log(data)
  if(!data) {
    return null
  }
  
  return (
    <div className="mb-5">
      <h5>{name}</h5>
      <table className="table table-bordered table-sm table-hover table-striped">
        <thead>
          <tr>
            <th>name</th>
            <th>type</th>
          </tr>
        </thead>
        <tbody>
          {data?.map((row) => (
            <tr key={`schema ${row[0]}`}>
              {row.map((col, colid) => (
                <td key={`schema i ${row[0]}#${colid}`}>{col}</td>
              ))
              }
            </tr>
          ))
          }
        </tbody>
      </table>
    </div>
  )
}
export default SchemaBase