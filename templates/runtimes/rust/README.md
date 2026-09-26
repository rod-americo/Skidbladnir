# Rust

Preset `base`: edição 2024, toolchain 1.98.1, binário e biblioteca testável, configuração tipada com Serde, logs JSON em stdout e `Cargo.lock` versionado. O campo `ts` do baseline é Unix time em segundos.

Execute `cargo fmt --all -- --check`, `cargo clippy --locked --all-targets -- -D warnings`, `cargo test --locked` e `cargo build --locked --release`. O código próprio proíbe `unsafe`; dependências exigem revisão própria. Não há download durante a geração.

O baseline não configura implantação, HTTP ou runtime assíncrono. Rust é uma alternativa quando manutenção, recursos e contratos justificarem seu custo; não é uma preferência automática por desempenho presumido.
