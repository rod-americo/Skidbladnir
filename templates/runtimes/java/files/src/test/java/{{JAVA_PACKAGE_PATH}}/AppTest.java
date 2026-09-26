package {{JAVA_PACKAGE}};

import static org.junit.jupiter.api.Assertions.*;
import com.google.gson.JsonParser;
import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.nio.file.Files;
import java.nio.file.Path;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

class AppTest {
    @TempDir Path directory;

    @Test void configurationControlsStructuredOutput() throws Exception {
        Path config = directory.resolve("settings.json");
        Files.writeString(config, "{\"app\":{\"name\":\"service-é\",\"log_level\":\"DEBUG\"}}");
        var output = new ByteArrayOutputStream();
        assertEquals(0, App.run(config, new PrintStream(output), System.err));
        var event = JsonParser.parseString(output.toString(java.nio.charset.StandardCharsets.UTF_8)).getAsJsonObject();
        assertEquals("service-é", event.get("svc").getAsString());
        assertEquals("DEBUG", event.get("lvl").getAsString());
        assertEquals("startup", event.get("evt").getAsString());
        assertDoesNotThrow(() -> java.time.Instant.parse(event.get("ts").getAsString()));
    }

    @Test void invalidConfigurationFailsInsteadOfFallingBack() throws Exception {
        Path config = directory.resolve("bad.json");
        Files.writeString(config, "{\"app\":{\"name\":42}}");
        var errors = new ByteArrayOutputStream();
        assertEquals(2, App.run(config, System.out, new PrintStream(errors)));
        assertTrue(errors.toString().contains("app.name"));
        assertEquals(2, App.run(directory.resolve("missing.json"), System.out, new PrintStream(errors)));
    }
}
