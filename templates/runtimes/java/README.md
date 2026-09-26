# Java

Preset `base`: Temurin 25 LTS, Maven Wrapper 3.9.16, layout Maven convencional, configuração JSON e logs estruturados em stdout. JUnit Jupiter testa configuração, falhas de leitura e evento de inicialização. `./mvnw -B verify` produz JAR executável; use o nome exato publicado no README gerado.

As versões concretas estão no catálogo e no `pom.xml`. Scripts `mvnw` e `mvnw.cmd` foram gerados pelo [Maven Wrapper Plugin 3.3.4](https://maven.apache.org/wrapper/), distribuição `only-script`, e conservam o cabeçalho Apache-2.0. O download de Maven usa checksum SHA-256. Não há download durante a geração.

O baseline não configura implantação, HTTP ou framework. A escolha de Java depende dos requisitos do projeto e não da disponibilidade deste scaffold.
