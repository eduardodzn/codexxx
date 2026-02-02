# Sistema automático de cortes e edição para vídeos de influência

Este projeto fornece um **pipeline simples e extensível** para que uma IA gere cortes automáticos de um vídeo de influência e prepare os trechos para edição. A ideia é usar a transcrição (ex.: Whisper) como base para identificar momentos fortes e criar clipes curtos automaticamente.

## Visão geral

O fluxo básico é:

1. **Transcrever** o vídeo com Whisper (ou outro ASR) e salvar o JSON.
2. **Pontuar** trechos do texto com palavras-chave e heurísticas simples.
3. **Selecionar clipes** não sobrepostos com melhor pontuação.
4. **Cortar** o vídeo em arquivos separados via `ffmpeg`.

> O pipeline foi desenhado para você evoluir: substitua o módulo de pontuação por um modelo de LLM, adicione detecção de cenas, B-roll, legendas, etc.

## Pré-requisitos

- Python 3.10+
- `ffmpeg` instalado e disponível no PATH

## Uso rápido

1. Instale dependências (não há libs obrigatórias além do Python padrão):

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Gere o JSON de transcrição (exemplo com Whisper):

```bash
whisper meu_video.mp4 --model medium --language pt --output_format json
```

3. Ajuste o arquivo de configuração:

```bash
cp configs/sample.json configs/local.json
```

4. Execute o pipeline:

```bash
python -m src.main --config configs/local.json
```

Os clipes serão gerados na pasta configurada (`output_dir`).

## Arquitetura

- `src/transcript.py`: carrega a transcrição.
- `src/segmenter.py`: cria candidatos e escolhe os melhores trechos.
- `src/editor.py`: recorta o vídeo com `ffmpeg`.
- `src/pipeline.py`: orquestra o fluxo.

## Próximos passos sugeridos

- Integrar um modelo LLM para pontuação semântica.
- Usar detecção de cenas para cortes mais naturais.
- Adicionar legendas automáticas.
- Inserir vinhetas e padronização de formato (ex.: 9:16).

## Estrutura esperada do Whisper JSON

Este projeto usa o formato padrão do Whisper:

```json
{
  "segments": [
    {
      "start": 0.0,
      "end": 3.4,
      "text": "Olá, pessoal..."
    }
  ]
}
```

## Licença

Uso livre para protótipos internos.
