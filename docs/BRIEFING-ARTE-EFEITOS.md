# Aluguito — briefing de arte: efeitos dos golpes e estados

30/10/2026. Lista do que o jogo ainda desenha em código (linhas, arcos, retângulos e brilhos) e para o qual não existe arte nos assets atuais para montar. Cada item traz o tamanho, os quadros e as referências. Quando os PNGs chegarem, eles são recortados, montados em atlas e ligados no `index.html`.

Já resolvidos com arte e fora deste briefing: projéteis dos chefes (`projeteis-chefes.png`), porta das arenas (`porta-chefe.png`) e ilhas do mapa (`mapa-regioes.png`).

## 1. Regras para todas as peças

**Estilo.** O mesmo dos personagens e atlas atuais: pixel art 16-bit densa, contorno quase preto, luz vindo de cima à esquerda, sombras em 2 ou 3 tons, sem degradê suave e sem antisserrilhado. Paleta da marca: dourado/laranja, creme e aço escuro. Cada chefe tem uma cor de destaque, que já aparece nos golpes atuais:

| Chefe | Destaque | Já usado em |
|---|---|---|
| Ruído | dourado claro e branco quente | ondas e grito |
| Pressa | ciano (tempo lento) | relógio e zona lenta |
| Barão Silo | aço e ciano (escudo) | cadeado, cabo e escudo |
| Dona Complexa | vermelho/rosa | peças, garra e nó |
| Ideia Torta | amarelo elétrico | raio e colunas |
| Apagão | dourado sobre preto (vazio) | esferas e piso apagado |

**Referências para anexar ao pedido de arte** (todas em `assets/`):
- `atlas/projeteis-extra.png`: o melhor modelo de efeito, com voo, impacto e dissipação em células de 64×64.
- `atlas/tiro-forte.png` e `atlas/tiro-simples.png`: densidade e acabamento dos tiros.
- `atlas/projeteis-chefes.png`: os projéteis de cada chefe que estes efeitos acompanham.
- `personagens/<chefe>.png`: a folha do chefe dono do efeito.

**Densidade.** 1 pixel da arte vale meio pixel do jogo, como em todos os atlas (o jogo desenha com escala 0,5). Abaixo, **"px do jogo"** é o tamanho na tela e **"px da arte"** é o tamanho do PNG (o dobro).

**Entrega.**
- PNG com fundo transparente. Um arquivo por efeito, com os quadros lado a lado da esquerda para a direita, todos do mesmo tamanho.
- Nome do arquivo: `chefe-efeito.png` (por exemplo, `ruido-sonar.png`).
- O corpo que causa dano deve ser opaco e legível. Brilho e aura podem ser semitransparentes, mas nunca podem ser a única coisa visível.
- Se o gerador não respeitar a grade exata, pode mandar assim mesmo, desde que cada quadro esteja separado e o fundo seja liso. O recorte e o alinhamento ficam na integração.

**Ciclo de um golpe.** Sempre que fizer sentido, separe em **preparação → ativo → impacto → dissipação**. A preparação é o aviso: o jogador precisa ver onde o golpe vai cair antes de ele ficar perigoso.

## 2. Efeitos por chefe

Tamanhos em px da arte. A coluna "Hitbox" é a área de dano no jogo, em px do jogo; o corpo desenhado deve ocupar mais ou menos esse tamanho.

### Ruído
| Arquivo | Célula | Quadros | Hitbox | Descrição |
|---|---|---|---|---|
| `ruido-onda.png` | 64×64 | 4 em loop + 2 de dissipação | 12×12 | Onda baixa que corre pelo chão depois do salto. Arco de som dourado rente ao piso. Vira para a esquerda por espelhamento. |
| `ruido-grito.png` | 64×64 | 4 em loop + 2 de dissipação | 14×26 | Rajada sonora horizontal: 3 arcos concêntricos, o da frente creme e os de trás dourados. |
| `ruido-sonar.png` | 256×256 | 8 | — | Anel de sonar crescendo a partir do chefe, de 8 a 120 px do jogo de raio, cada vez mais apagado. Vermelho claro. |
| `ruido-mira.png` | 64×64 | 2 de travamento + 2 em loop | — | Retícula sobre o Aluguito quando ele está marcado: os cantos fecham e depois ela pisca. Vermelho. |
| `ruido-estatica.png` | 128×128 | 3 de entrada + 3 de saída | — | Nuvem de estática do teleporte: chuviscos, faixas de TV e faíscas, do tamanho do chefe (42×38 px do jogo). |

### Pressa
| Arquivo | Célula | Quadros | Hitbox | Descrição |
|---|---|---|---|---|
| `pressa-rastro.png` | 96×64 | 3 | — | Rastro da investida: linhas de velocidade e poeira atrás do relógio. |
| `pressa-impacto.png` | 128×64 | 4 | — | Impacto da queda do salto: anel de poeira e engrenagens soltas no chão. |
| `pressa-zona.png` | 96×32 | 4 em loop + 3 de expiração | 40×6 | Poça de tempo lento no chão: ponteiros e números flutuando em ciano. Precisa ficar claro que é uma área, não um projétil. |
| `pressa-lento.png` | 128×128 | 4 em loop | — | Aura em volta do chefe quando ele está lento pela ferramenta Ritmo: relógios pequenos girando devagar, em ciano. |
| `pressa-atordoado.png` | 64×32 | 4 em loop | — | Estrelas e engrenagens girando sobre a cabeça depois de bater na parede. |

### Barão Silo
| Arquivo | Célula | Quadros | Hitbox | Descrição |
|---|---|---|---|---|
| `silo-gancho.png` | 48×48 + segmento de 16×16 | cabeça: 2; segmento: 2 | 10×8 | Ponta do cabo-gancho (conector com garras) e um pedaço de cabo que repete. O cabo estica entre o chefe e a ponta. |
| `silo-soco.png` | 64×48 + segmento de 16×16 | punho: 3 (estica, acerta, recolhe); segmento: 1 | 18×10 | Punho de aço com braço segmentado, saindo do corpo. |
| `silo-escudo.png` | 160×144 | 3 de abertura + 2 em loop + 3 de quebra | — | Bolha/escudo em volta do chefe (52×42 px do jogo), em ciano com placas. A quebra marca a janela de vulnerabilidade. |
| `silo-queda-aviso.png` | 32×32 | 2 em loop | — | Marca no chão onde o bloco vai cair. Hoje é uma faixa vermelha piscando. O bloco em si sai dos tiles da Fortaleza. |

### Dona Complexa
| Arquivo | Célula | Quadros | Hitbox | Descrição |
|---|---|---|---|---|
| `dona-garra.png` | 48×48 + segmento de 16×16 | garra: 3 (aberta, fechando, fechada); segmento: 1 | — | Garra articulada vermelha, com o braço segmentado que liga ao chefe. |
| `dona-no-dissipa.png` | 64×64 | 4 | 12×12 | O nó (já existe em `projeteis-chefes.png`) se desfazendo ao bater ou expirar. |
| `dona-teto-aviso.png` | 64×32 | 2 em loop | — | Aviso no teto antes da queda. |

### Ideia Torta
| Arquivo | Célula | Quadros | Hitbox | Descrição |
|---|---|---|---|---|
| `torta-coluna.png` | topo de 64×32 + meio de 64×64 + base de 96×48 | meio: 3 em loop; topo e base: 2 | 8 de largura | Coluna de descarga do teto ao chão (cerca de 160 px do jogo). O meio repete na vertical. |
| `torta-coluna-aviso.png` | 32×16 | 2 em loop | — | Marca no chão onde a coluna vai cair. |
| `torta-linha.png` | segmento de 64×32 + pontas de 32×32 | segmento: 3 em loop | altura 6 | Linha elétrica horizontal entre o chefe e o ponto de chegada. O segmento repete na horizontal. |
| `torta-clone-quebra.png` | 128×128 | 4 | — | Clone desfazendo em rabiscos de rascunho ao ser atingido. |
| `torta-escuro.png` | 128×128 | 3 de entrada + 3 de saída | — | Aura de escuridão em volta do chefe e o retorno da clareza. |

### Apagão
| Arquivo | Célula | Quadros | Hitbox | Descrição |
|---|---|---|---|---|
| `apagao-braco.png` | 64×48 + segmento de 16×16 | mão: 2; segmento: 1 | 18×10 | Braço/cabo baixo do Arquivista varrendo o chão. |
| `apagao-gaveta.png` | 96×96 | 3 (abrindo, aberta com brilho, fechando) | — | Gaveta aberta de verdade, com o núcleo vulnerável dentro. É o sinal de "pode atacar". |
| `apagao-piso.png` | 128×32 | aviso: 2 em loop; apagando: 4; restaurando: 4 | 4 tiles | Marca do piso que vai sumir, os blocos se desfazendo e voltando. **Antes:** decidir se o ataque abre um buraco ou um rebaixo de 16 px (pendente na revisão). |
| `apagao-transicao.png` | 192×192 | 6 | — | Passagem do Arquivista para o Núcleo. |

## 3. Estados do Aluguito

Hoje os estados são só uma cor ou um brilho em volta do personagem. Cada um precisa de duas peças: um **sobreposto no personagem** (64×64, em loop) e um **ícone para o HUD** (32×32, no estilo de `atlas/hud-estados.png`). A duração continua sendo mostrada pela barra que já existe.

| Estado | Causa | Sobreposto | Ícone |
|---|---|---|---|
| `estado-lento` | zona do Pressa | relógios pequenos girando devagar, ciano | ampulheta/relógio |
| `estado-preso` | cabo do Silo | cabo/corrente em volta da cintura | cadeado com cabo |
| `estado-mira` | sonar do Ruído | retícula seguindo o personagem | retícula |
| `estado-invertido` | nó da Dona | nó sobre a cabeça e setas trocadas | setas cruzadas |

Não use só a cor para diferenciar os estados: cada um precisa de um desenho reconhecível.

## 4. Ordem sugerida

1. Os avisos de preparação (`silo-queda-aviso`, `torta-coluna-aviso`, `dona-teto-aviso`, `apagao-piso`) e os estados do Aluguito. São o que mais afeta a leitura do jogo.
2. Os efeitos ativos: escudo do Silo, garra e gancho, colunas e linha elétrica, zona lenta, sonar.
3. Impactos, dissipações e transições.

## 5. O que não entra aqui

- **Kit de fachada e interiores do Silo:** pode ser montado a partir de `fundos/fortaleza-desconectada.png` e `tiles/fortaleza-desconectada.png`.
- **Textos de estado no chefe** ("ABERTO", "ATORDOADA"): continuam com a fonte do jogo.
- **Bloco que cai na arena do Silo:** sai dos tiles da Fortaleza.
