

use pyo3::prelude::*;
use pyo3::types::{PyString};


fn digit_calculation(total: i32) -> String {
    let remainder = total % 11;
    let calculated_digit = (11 - remainder).to_string();

    if calculated_digit == "11" {
        return "0".to_string();
    }
    else if calculated_digit == "10" {
        return "K".to_string();
    }

    return calculated_digit;
}

/// function rut_run_checker
///
/// checks a rut/run number
///Args:
///     rut_run: str. 
/// Return
///     bool: Validation of rut/run
///
#[pyfunction]
pub fn rut_run_checker(rut_run: &Bound<'_, PyString>) -> bool {

    let binding = rut_run.to_string();
    let element: Vec<&str> = binding.split("-").collect();

    if element[0].len() < 2 {
        return false;
    }

    let mut total: i32 = 0;
    let mut factor: i32 = 2;

    for rut_run_char in element[0].chars().rev() {
        total = total + rut_run_char.to_string().parse::<i32>().unwrap() * factor;
        if factor == 7 {
            factor = 2;
        }
        else {
            factor = factor + 1;
        }
    }

    let calculated_digit = digit_calculation(total);

    if calculated_digit == element[1] {
        return true
    }
    false
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn rut_run_test() {
        pyo3::prepare_freethreaded_python();
        Python::with_gil(|py| {
            let valid_rutrun = PyString::new(py, "17945265-0");
            let result = rut_run_checker(&valid_rutrun);
            assert_eq!(result, true);
        });
    }

    #[test]
    fn rut_run_second_test() {
        pyo3::prepare_freethreaded_python();
        Python::with_gil(|py| {
            let key = PyString::new(py, "");
            let result = rut_run_checker(&key);
            assert_eq!(result, false);
        });
    }
}