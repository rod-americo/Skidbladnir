package {{JAVA_PACKAGE}};

import com.google.gson.Gson;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import java.io.IOException;
import java.io.PrintStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.time.Instant;

public final class App {
    private App() {}

    public record Settings(String name, String env, String logLevel) {}
    public record LogEvent(String ts, String lvl, String svc, String mod, String evt, String msg) {}

    private static String field(JsonObject app, String key, String fallback) {
        if (!app.has(key)) return fallback;
        var value = app.get(key);
        if (!value.isJsonPrimitive() || !value.getAsJsonPrimitive().isString() || value.getAsString().isBlank()) {
            throw new IllegalArgumentException("app." + key + " must be a non-empty string");
        }
        return value.getAsString();
    }

    public static Settings parseSettings(String json) {
        JsonObject root = JsonParser.parseString(json).getAsJsonObject();
        JsonObject app = root.has("app") ? root.getAsJsonObject("app") : new JsonObject();
        return new Settings(field(app, "name", {{PROJECT_NAME_LITERAL}}), field(app, "env", "dev"), field(app, "log_level", "INFO"));
    }

    public static int run(Path config, PrintStream output, PrintStream errors) {
        try {
            Settings settings = parseSettings(config == null ? "{}" : Files.readString(config));
            output.println(new Gson().toJson(new LogEvent(Instant.now().toString(), settings.logLevel(), settings.name(), "main", "startup", "service initialized")));
            return 0;
        } catch (IOException | RuntimeException error) {
            errors.println("configuration error: " + error.getMessage());
            return 2;
        }
    }

    public static void main(String[] args) {
        if (args.length == 1 && args[0].equals("--help")) {
            System.out.println("Usage: java -jar {{DIST_NAME}}-0.1.0.jar [config.json]");
            return;
        }
        if (args.length > 1) {
            System.err.println("expected at most one configuration file");
            System.exit(2);
        }
        String explicit = args.length == 1 ? args[0] : System.getenv("{{ENV_PREFIX}}_CONFIG_FILE");
        Path config = explicit == null ? null : Path.of(explicit);
        if (config == null) {
            for (String candidate : new String[] {"config/settings.local.json", "config/settings.example.json"}) {
                if (Files.exists(Path.of(candidate))) { config = Path.of(candidate); break; }
            }
        }
        System.exit(run(config, System.out, System.err));
    }
}
