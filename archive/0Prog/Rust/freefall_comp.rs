use std::fs::File;
use std::io::prelude::*;

fn main() -> std::io::Result<()> {
    let mut file = File::create("/storage/emulated/0/0Prog/Rust/foo.txt")?;
    file.write_all(b"Hello, world!")?;
    println!("na mi van");
    Ok(())    
}
