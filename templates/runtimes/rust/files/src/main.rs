use std::path::{Path, PathBuf};
use std::process::ExitCode;

fn main() -> ExitCode {
    let args: Vec<String> = std::env::args().skip(1).collect();
    if args == ["--help"] {
        println!("Usage: lock-sample [config.json]");
        return ExitCode::SUCCESS;
    }
    if args.len() > 1 {
        eprintln!("expected at most one configuration file");
        return ExitCode::from(2);
    }
    let explicit = args
        .first()
        .cloned()
        .or_else(|| std::env::var("{{ENV_PREFIX}}_CONFIG_FILE").ok());
    let config = explicit.map(PathBuf::from).or_else(|| {
        ["config/settings.local.json", "config/settings.example.json"]
            .iter()
            .map(Path::new)
            .find(|path| path.exists())
            .map(Path::to_path_buf)
    });
    match {{RUST_CRATE}}::run(config.as_deref(), &mut std::io::stdout().lock()) {
        Ok(()) => ExitCode::SUCCESS,
        Err(error) => {
            eprintln!("configuration error: {error}");
            ExitCode::from(2)
        }
    }
}
