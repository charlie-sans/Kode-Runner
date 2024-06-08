// Coderunner tools 
// 2024 OpenStudio, all rights reserved

use std::env;
use std::fs;
use std::path::Path;
use std::process::Command;
use std::process::Stdio;
use std::io::*;
use std::io::prelude::*;

// args
// 0: the language of the code
// 1: the code file/files
// 2: the output name
fn main() {
    let args: Vec<String> = env::args().collect();
    let lang = &args[1];
    let code = &args[2];
    let output = &args[3];

    match lang.as_str() {
        "cpp" => {
            let mut cmd = Command::new("g++")
                .arg(code)
                .arg("-o")
                .arg(output)
                .stdout(Stdio::piped())
                .stderr(Stdio::piped())
                .spawn()
                .expect("Failed to compile the code");

            let output = cmd.wait_with_output().expect("Failed to wait on child");

            if output.status.success() {
                println!("Compilation succeeded");
            } else {
                println!("Compilation failed");
                println!("Error: {}", String::from_utf8_lossy(&output.stderr));
            }
        }
        "c" => {
            let mut cmd = Command::new("gcc")
                .arg(code)
                .arg("-o")
                .arg(output)
                .stdout(Stdio::piped())
                .stderr(Stdio::piped())
                .spawn()
                .expect("Failed to compile the code");

            let output = cmd.wait_with_output().expect("Failed to wait on child");

            if output.status.success() {
                println!("Compilation succeeded");
            } else {
                println!("Compilation failed");
                println!("Error: {}", String::from_utf8_lossy(&output.stderr));
            }
        }
        "java" => {
            let mut cmd = Command::new("javac")
                .arg(code)
                .stdout(Stdio::piped())
                .stderr(Stdio::piped())
                .spawn()
                .expect("Failed to compile the code");

            let output = cmd.wait_with_output().expect("Failed to wait on child");

            if output.status.success() {
                println!("Compilation succeeded");
            } else {
                println!("Compilation failed");
                println!("Error: {}", String::from_utf8_lossy(&output.stderr));
            }
        }
        "rust" => {
            let mut cmd = Command::new("rustc")
                .arg(code)
                .arg("-o")
                .arg(output)
                .stdout(Stdio::piped())
                .stderr(Stdio::piped())
                .spawn()
                .expect("Failed to compile the code");

            let output = cmd.wait_with_output().expect("Failed to wait on child");

            if output.status.success() {
                println!("Compilation succeeded");
            } else {
                println!("Compilation failed");
                println!("Error: {}", String::from_utf8_lossy(&output.stderr));
            }
        }
        "mono" => {
            let mut cmd = Command::new("mcs")
                .arg(code)
                .arg("-out")
                .arg(output)
                .stdout(Stdio::piped())
                .stderr(Stdio::piped())
                .spawn()
                .expect("Failed to compile the code");

            // run the code 
            let output = cmd.wait_with_output().expect("Failed to wait on child");

            if output.status.success() {
                println!("Compilation succeeded");
            } else {
                println!("Compilation failed");
                println!("Error: {}", String::from_utf8_lossy(&output.stderr));
            }
        }
        _ => {
            println!("Unsupported language");
        }
    }
}