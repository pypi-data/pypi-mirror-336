use pyo3::prelude::*;
use rand::Rng;


/// A Python module implemented in Rust. The name of this function must match
/// the `lib.name` setting in the `Cargo.toml`, else Python will not be able to
/// import the module.
#[pymodule]
fn _core(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(pi64, m)?)?;
    m.add_function(wrap_pyfunction!(mc, m)?)?;
    m.add_function(wrap_pyfunction!(arctan, m)?)?;
    Ok(())
}


/// Builtin f64 value
#[pyfunction]
fn pi64() -> String {
    return std::f64::consts::PI.to_string();
}


/// Naive Monte Carlo
#[pyfunction]
fn mc() -> String {
    let mut rng = rand::rng();

    let mut count: i64 = 0;
    let mut n: i64 = 0;

    while n <10000000 {
        n += 1;
        let x:f64 = rng.random();
        let y:f64 = rng.random();
        if x*x + y*y <= 1.0 {
            count += 1;
        }
    }

    let result: f64 = 4.0 * (count as f64)/(n as f64);
    return result.to_string()
}

/// Taylor series for arctan(x)
/// π = 4 * (1-1/3+1/5-1/7+1/9-1/11+...)
#[pyfunction]
fn arctan() -> String {
    let mut n: i64 = 0;
    let mut positive: f64 = 0.0;
    let mut negative: f64 = 0.0;

    while n<1000000000 {
        if n % 2 == 0 {
            positive += 4.0/((2 * n + 1) as f64);
        } else {
            negative += 4.0/((2 * n + 1) as f64);
        }
        n += 1;
    }
    let sum: f64 = positive - negative;
    return sum.to_string();
}
