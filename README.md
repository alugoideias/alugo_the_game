# Aluguito e os Fragmentos da Ideia

Plataforma 16-bit inspirado em Mega Man, feito para a Alugo Ideias.

Aluguito é um Realizador que viaja ao mundo **Digitus** para descobrir o que está atrapalhando a criação de novas ideias. No fim da Fase 1-1 o **Apagão** rouba suas cinco ferramentas e cria cinco chefes; o jogador escolhe a ordem no mapa do mundo e recupera uma ferramenta a cada vitória.

## Como jogar

Abra `index.html` em qualquer navegador moderno (ou publique no GitHub Pages). Não há build nem dependências: o código está em `index.html` e todas as imagens ficam em `assets/` (só as fontes vêm do Google Fonts).

| Ação | Teclado | Toque |
|---|---|---|
| Andar | ← → | ◀ ▶ |
| Pular (segure = mais alto) | Espaço / Z | A |
| Pulso / segure para pulso forte | X | PULSO |
| Usar ferramenta | C | USA |
| Trocar ferramenta | Q / E ou 1–5 | ◁ ▷ |
| Pausa / guia / som | P / H / M | II / ? |

Funciona na horizontal (tela cheia) e na vertical (layout Game Boy). O progresso fica salvo no `localStorage` do navegador.

## Estrutura

```
index.html                 jogo (HTML + CSS + JS)
assets/
  capa/                    arte da tela inicial
  personagens/             Aluguito, inimigos, chefes e Apagão (folhas de 8 poses)
  atlas/                   kits de cenário, HUD, mecanismos, tiros, voo e água
  tiles/                   blocos de chão de cada mundo
  fundos/                  fundos de cada mundo, céu da Oficina e água do Distrito
```

Os atlas seguem os retângulos e âncoras definidos no próprio `index.html` (constantes `ATD` e `ATL`). Para trocar uma arte, substitua o PNG mantendo o mesmo tamanho de célula.

## Publicar no GitHub Pages

1. Suba esta pasta para um repositório.
2. Em **Settings → Pages**, escolha a branch `main` e a pasta raiz.
3. O jogo fica disponível em `https://<usuario>.github.io/<repositorio>/`.

## Conteúdo

- Fase 1-1 (Vale das Ideias Perdidas) com tutorial das ferramentas
- Mapa do mundo estilo Super Mario Bros. 3
- 5 fases de chefe + Arquivo do Apagão
- Fortaleza do Barão Silo com escalada vertical
- Abertura aérea na Oficina dos Rascunhos e canal com nado no Distrito dos Prazos
