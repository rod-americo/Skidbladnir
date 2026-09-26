# Swift

Siga Swift Package Manager com entrypoint, núcleo e testes separados. Execute `swift package resolve`, `swift test` e `swift build`. A CI provisiona imagem oficial com versão e digest fixos; o baseline não exige dependências externas.

Versões e comandos exatos estão no [catálogo](../catalog.json) e na [documentação gerada](../../../docs/runtime-catalog.md). A existência deste scaffold não favorece a escolha da linguagem. O baseline usa `deploy.target: none`, salvo preset com operação HTTP local explícita.
