#!/usr/bin/env bash
# Instalacja darmowych narzędzi do grafik, animacji, napisów i montażu „Szkoła kłamała”.
# Kontener sesji jest ulotny – uruchom na początku sesji, w której pracujesz z wideo.
set -euo pipefail
cd "$(dirname "$0")/.."

pip install -q -r requirements.txt

# ffmpeg z libass (napisy) i loudnorm (−14 LUFS)
command -v ffmpeg >/dev/null || { apt-get update -qq && apt-get install -y -qq ffmpeg; }
ffmpeg -hide_banner -filters 2>/dev/null | grep " ass " >/dev/null || echo "⚠ ffmpeg bez libass – napisy nie zadziałają"

# czcionka marki
fc-list | grep -i "Inter Display" >/dev/null || echo "⚠ brak czcionki Inter Display – zainstaluj z github.com/rsms/inter do ~/.fonts i uruchom fc-cache -f"

# model rozpoznawania mowy (ok. 1,5 GB, pobierany raz na sesję)
python3 -c "from faster_whisper import WhisperModel; WhisperModel('${WHISPER_MODEL:-medium}', device='cpu', compute_type='int8')" 2>&1 | grep -v Warning || true

# polski głos lektora (Piper, mc_speech)
python3 - <<'PY' 2>&1 | grep -v Warning || true
from huggingface_hub import hf_hub_download
rel = "pl/pl_PL/mc_speech/medium/pl_PL-mc_speech-medium.onnx"
for ext in ("", ".json"):
    hf_hub_download("rhasspy/piper-voices", rel + ext, local_dir="/root/piper")
PY

echo "ffmpeg: $(ffmpeg -version | head -1 | cut -d' ' -f3)"
python3 -c "import faster_whisper, playwright; print('faster-whisper', faster_whisper.__version__)"
auto-editor --version
echo "Gotowe."
