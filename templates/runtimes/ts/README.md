# TypeScript

Use `src/`, TypeScript estrito, `package-lock.json` e `npm ci`. `npm test` compila e executa testes; `npm start` é o entrypoint. A versão do runtime no manifesto é a versão Node; TypeScript é fixado nas dependências.

Versões e comandos exatos estão no [catálogo](../catalog.json) e na [documentação gerada](../../../docs/runtime-catalog.md). A existência deste scaffold não favorece a escolha da linguagem. O baseline usa `deploy.target: none`, salvo preset com operação HTTP local explícita.
