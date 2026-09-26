# Go

Use `cmd/<slug>/` e pacote interno testável. A toolchain é fixada; execute `go vet ./...` e `go test -race ./...`. Não há dependências externas no baseline; versione `go.sum` se adicioná-las.

Versões e comandos exatos estão no [catálogo](../catalog.json) e na [documentação gerada](../../../docs/runtime-catalog.md). A existência deste scaffold não favorece a escolha da linguagem. O baseline usa `deploy.target: none`, salvo preset com operação HTTP local explícita.
