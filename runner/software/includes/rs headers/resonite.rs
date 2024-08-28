/*
File_name: resonite.rs
Project: <project_name>
Description: This file contains helper functions.
*/
use std::*;
use std::io::*;
use std::fs::*;
use std::path::*;
use std::collections::*;
use std::sync::*;
use std::thread::*;
use std::time::*;
use std::net::*;
use std::os::*;
use std::ffi::*;
use std::mem::*;
use std::ptr::*;
use std::str::*;
use std::fmt::*;
use std::error::*;


// debug(<string>) -> [DEBUG] <string>
pub fn debug(s: &str) {
    println!("[DEBUG] {}", s);
}

// error(<string>) -> [ERROR] <string>
pub fn error(s: &str) {
    println!("[ERROR] {}", s);
}

// info(<string>) -> [INFO] <string>
pub fn info(s: &str) {
    println!("[INFO] {}", s);
}

// warn(<string>) -> [WARN] <string>
pub fn warn(s: &str) {
    println!("[WARN] {}", s);
}

// get_file_name(<string>) -> <string>
pub fn get_file_name(s: &str) -> String {
    let path = Path::new(s);
    let file_name = path.file_name().unwrap();
    let file_name = file_name.to_str().unwrap();
    file_name.to_string()
}

//get_random_str_num_symbol_uppercase(length)
pub fn get_random_str_num_symbol_uppercase(length: usize) -> String {
    let mut rng = rand::thread_rng();
    let mut s = String::new();
    for _ in 0..length {
        let c = rng.gen_range(0, 3);
        match c {
            0 => {
                s.push(rng.gen_range(48, 58) as u8 as char);
            }
            1 => {
                s.push(rng.gen_range(65, 91) as u8 as char);
            }
            2 => {
                s.push(rng.gen_range(33, 48) as u8 as char);
            }
            _ => {}
        }
    }
    s
}

//get_random_str_num_symbol_lowercase(length)
pub fn get_random_str_num_symbol_lowercase(length: usize) -> String {
    let mut rng = rand::thread_rng();
    let mut s = String::new();
    for _ in 0..length {
        let c = rng.gen_range(0, 3);
        match c {
            0 => {
                s.push(rng.gen_range(48, 58) as u8 as char);
            }
            1 => {
                s.push(rng.gen_range(97, 123) as u8 as char);
            }
            2 => {
                s.push(rng.gen_range(33, 48) as u8 as char);
            }
            _ => {}
        }
    }
    s
}

// write_and_run_file(code,name,command,command2)
pub fn write_and_run_file(code: &str, name: &str, command: &str, command2: &str) -> Result<(), Box<dyn Error>> {
    let path = Path::new(name);
    let mut file = File::create(path)?;
    file.write_all(code.as_bytes())?;
    drop(file);
    let output = Command::new(command).arg(name).output()?;
    let output = Command::new(command2).output()?;
    let output = String::from_utf8(output.stdout).unwrap();
    println!("{}", output);
    Ok(())
}

// write_file(code,name)
pub fn write_file(code: &str, name: &str) -> Result<(), Box<dyn Error>> {
    let path = Path::new(name);
    let mut file = File::create(path)?;
    file.write_all(code.as_bytes())?;
    drop(file);
    Ok(())
}

// run_file(name,command)
pub fn run_file(name: &str, command: &str) -> Result<(), Box<dyn Error>> {
    let output = Command::new(command).arg(name).output()?;
    let output = String::from_utf8(output.stdout).unwrap();
    println!("{}", output);
    Ok(())
}

// run_command(command)
pub fn run_command(command: &str) -> Result<(), Box<dyn Error>> {
    let output = Command::new(command).output()?;
    let output = String::from_utf8(output.stdout).unwrap();
    println!("{}", output);
    Ok(())
}

// get_file_content(name) -> <string>
pub fn get_file_content(name: &str) -> Result<String, Box<dyn Error>> {
    let path = Path::new(name);
    let mut file = File::open(path)?;
    let mut content = String::new();
    file.read_to_string(&mut content)?;
    Ok(content)
}

// get_file_content(name) -> <string>
pub fn get_file_content_bytes(name: &str) -> Result<Vec<u8>, Box<dyn Error>> {
    let path = Path::new(name);
    let mut file = File::open(path)?;
    let mut content = Vec::new();
    file.read_to_end(&mut content)?;
    Ok(content)
}
