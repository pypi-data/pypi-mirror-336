use std::env;
use std::path::PathBuf;

fn main() {
    let manifest_dir = env::var("CARGO_MANIFEST_DIR").unwrap();
    let out_dir = PathBuf::from(env::var("OUT_DIR").unwrap());
    let target_dir = out_dir.join("target");

    // Create target directory if it doesn't exist
    std::fs::create_dir_all(&target_dir).unwrap_or_else(|e| {
        println!("cargo:warning=Failed to create target directory: {}", e);
    });

    // Determine library extension based on platform
    let lib_extension = if cfg!(target_os = "windows") {
        "dll"
    } else if cfg!(target_os = "macos") {
        "dylib"
    } else {
        "so"
    };

    let core_lib_name = format!("finatic_core.{}", lib_extension);
    let core_lib_path = PathBuf::from(&manifest_dir)
        .join("..")
        .join("core")
        .join("target")
        .join("release")
        .join(&core_lib_name);

    // Print debug information
    println!("cargo:warning=Looking for core library at: {:?}", core_lib_path);

    if core_lib_path.exists() {
        std::fs::copy(&core_lib_path, target_dir.join(&core_lib_name))
            .unwrap_or_else(|e| {
                println!("cargo:warning=Failed to copy core library: {}", e);
                0
            });
    } else {
        println!("cargo:warning=Core library not found at {:?}", core_lib_path);
    }

    // Tell cargo to rerun this script if the core library changes
    println!("cargo:rerun-if-changed=../core/src");
} 