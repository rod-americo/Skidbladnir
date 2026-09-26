use serde::Deserialize;
use std::error::Error;
use std::io::Write;
use std::path::Path;
use std::time::{SystemTime, UNIX_EPOCH};

#[derive(Debug, Deserialize, Default)]
#[serde(default, deny_unknown_fields)]
pub struct Settings {
    pub app: AppSettings,
}

#[derive(Debug, Deserialize)]
#[serde(default, deny_unknown_fields)]
pub struct AppSettings {
    pub name: String,
    pub env: String,
    pub log_level: String,
}

impl Default for AppSettings {
    fn default() -> Self {
        Self {
            name: {{PROJECT_NAME_LITERAL}}.to_owned(),
            env: "dev".to_owned(),
            log_level: "INFO".to_owned(),
        }
    }
}

pub fn parse_settings(json: &str) -> Result<Settings, Box<dyn Error>> {
    let settings: Settings = serde_json::from_str(json)?;
    if settings.app.name.trim().is_empty()
        || settings.app.env.trim().is_empty()
        || settings.app.log_level.trim().is_empty()
    {
        return Err("app fields must be non-empty strings".into());
    }
    Ok(settings)
}

pub fn run(config: Option<&Path>, output: &mut impl Write) -> Result<(), Box<dyn Error>> {
    let json = match config {
        Some(path) => std::fs::read_to_string(path)?,
        None => "{}".to_owned(),
    };
    let settings = parse_settings(&json)?;
    let event = serde_json::json!({
        "ts": SystemTime::now().duration_since(UNIX_EPOCH)?.as_secs(),
        "lvl": settings.app.log_level,
        "svc": settings.app.name,
        "mod": "main",
        "evt": "startup",
        "msg": "service initialized"
    });
    serde_json::to_writer(&mut *output, &event)?;
    writeln!(output)?;
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn configuration_is_typed_and_validated() {
        let settings =
            parse_settings(r#"{"app":{"name":"service-é","log_level":"DEBUG"}}"#).unwrap();
        assert_eq!(settings.app.name, "service-é");
        assert_eq!(settings.app.log_level, "DEBUG");
        assert!(parse_settings(r#"{"app":{"name":42}}"#).is_err());
        assert!(parse_settings(r#"{"app":{"name":""}}"#).is_err());
        assert!(parse_settings("invalid json").is_err());
    }

    #[test]
    fn startup_produces_a_parseable_event() {
        let mut output = Vec::new();
        run(None, &mut output).unwrap();
        let event: serde_json::Value = serde_json::from_slice(&output).unwrap();
        assert_eq!(event["evt"], "startup");
        assert!(event["ts"].as_u64().unwrap() > 0);
        assert_eq!(output.last(), Some(&b'\n'));
    }

    #[test]
    fn missing_explicit_configuration_is_an_error() {
        assert!(run(Some(Path::new("missing-settings.json")), &mut Vec::new()).is_err());
    }
}
