
use pyo3::prelude::*;
use pyo3::types::{PyDict, PyList, PyString, PyModule};

mod definitions;



#[warn(unused_must_use)]
fn analysis_sql(py: Python, input_dict: &Bound<'_, PyDict>) -> PyResult<PyObject> {
    let my_dict = PyDict::new(py);
    let my_list = PyList::empty(py);
    let mut is_injected = false;

    let my_regex = definitions::SqlRegexStruct::new();
    // iterate over the dictionary
    for (_, value) in input_dict.iter() {
        if let Ok(val_str) = value.downcast::<PyString>() {
            if my_regex.test_patterns(val_str.to_string_lossy().into()) {
                let _ = my_list.append(val_str.to_string());
                is_injected = true;
            }
        }
        else if let Ok(val_list) = value.downcast::<PyList>() {
            for val_element in val_list.iter() {
                if let Ok(val_item) = val_element.downcast::<PyString>() {
                    if my_regex.test_patterns(val_item.to_string_lossy().into()) {
                       let _ =my_list.append(val_item.to_string());
                       is_injected = true;
                    }
                }
            }
        }
        else if let Ok(val_dict) = value.downcast::<PyDict>() {
            return analysis_sql(py, val_dict);
        }

    }
    my_dict.set_item("is_injected", is_injected).unwrap();
    my_dict.set_item("found_injection", my_list.clone()).unwrap();
    Ok(my_dict.into())
}

/// function sql_analizer
///
/// analize a dictionary for sql injections providing information about what has been found if 
/// there is suspicion of an sql injection
///Args:
///     input_dict: dict. 
/// Return
///     dict: sql injection analysis
///
#[pyfunction]
fn sql_analizer(py: Python, input_dict: &Bound<'_, PyDict>) -> PyResult<PyObject> {
    analysis_sql(py, input_dict)
}

fn sql_check_injection(input_dict: &Bound<'_, PyDict>) -> bool {

    let my_regex = definitions::SqlRegexStruct::new();
    // iterate over the dictionary
    for (_, value) in input_dict.iter() {
        //let key_str: String = key.to_string();
        if let Ok(val_str) = value.downcast::<PyString>() {
            if my_regex.test_patterns(val_str.to_string_lossy().into()) {
                return true;
            }
        }
        else if let Ok(val_list) = value.downcast::<PyList>() {
            for val_element in val_list.iter() {
                if let Ok(val_item) = val_element.downcast::<PyString>() {
                    if my_regex.test_patterns(val_item.to_string_lossy().into()) {
                        return true;
                    }
                }
            }
        }
        else if let Ok(val_dict) = value.downcast::<PyDict>() {
            return sql_check_injection(val_dict);
        }

    }
    return false
}

/// function sql_check
///
/// checks the validity of a dictionary
///Args:
///     input_dict: dict. 
/// Return
///     bool: Result if in any place a possible sql injection is detected
///
#[pyfunction]
fn sql_check(input_dict: &Bound<'_, PyDict>) -> bool {
    /*
    Function checks validity of a json Data
    */
    return sql_check_injection(input_dict);

}

/// SQL Module for sql injection protection
///
/// 
/// functions :py:func:`sql_check`, :py:func:`sql_analyzer`.
///
#[pymodule]
pub fn sql(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(sql_check, m)?)?;
    m.add_function(wrap_pyfunction!(sql_analizer, m)?)?;
    Ok(())
}


#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn sql_check_injection_true_test() {
        pyo3::prepare_freethreaded_python();
        Python::with_gil(|py| {
            let  my_dict = PyDict::new(py);
            let  my_sub_dict = PyDict::new(py);
            let _ = my_sub_dict.set_item("second", "select from");
            let _ = my_dict.set_item("first", my_sub_dict);
            let result = sql_check(&my_dict);
            assert_eq!(result, true);
        });
    }

    #[test]
    fn sql_check_injection_false_test() {
        pyo3::prepare_freethreaded_python();
        Python::with_gil(|py| {
            let  my_dict = PyDict::new(py);
            let  my_sub_dict = PyDict::new(py);
            let _ = my_sub_dict.set_item("second", "a test");
            let _ = my_dict.set_item("first", my_sub_dict);
            let result = sql_check(&my_dict);
            assert_eq!(result, false);
        });
    }
}