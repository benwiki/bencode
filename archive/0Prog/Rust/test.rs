/*
use std::env;

fn main() -> std::io::Result<()> {
    let res = env::set_current_dir("../home/storage/emulated/0/0Prog/Rust");
    let path = env::current_dir()?;
    println!("The current directory is {}, {:?}", path.display(), res);
    Ok(())
}*/

use std::fs;

fn main() {
    let paths = fs::read_dir("../root").unwrap();

    for path in paths {
        println!("Name: {}", path.unwrap().path().display())
    }
}
