use pyo3::prelude::*;
use pyo3::wrap_pymodule;


mod sql;
mod cl;

/// A Python module implemented in Rust.
#[pymodule]
fn protectionstnd(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_wrapped(wrap_pymodule!(sql::sql))?;
    m.add_wrapped(wrap_pymodule!(cl::cl))?;
    Ok(())
}
