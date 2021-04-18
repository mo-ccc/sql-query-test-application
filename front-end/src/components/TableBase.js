const TableBase = ({data, className}) => {
  if (!data) {
    return null
  }
  return(
    <div className={className} style={{"maxHeight": "200px", "overflowY": "auto", fontSize: 13}}>
      <table className="table table-bordered table-sm table-hover table-striped">
        <thead className="thead-dark">
          <tr>
            {data?.keys?.map(key => (
              <th key={key} style={{"position": "sticky", "top": 0}} >{key}</th>
            )
            )}
          </tr>
        </thead>
        <tbody>
          {data?.rows?.map((row, rowid) => (
            <tr key={`row#${rowid}`}>
              {row.map((col, colid) => (
                <td key={`${row}.col#${colid}`}>{col?.toString() ?? "null"}</td>
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

export default TableBase