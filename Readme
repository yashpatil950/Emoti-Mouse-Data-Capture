# Mouse + EmotiBit Capture (End-to-End Guide)

This project supports a combined workflow that records data from:

- Mionix mouse (WebSocket API)
- EmotiBit wristband (UDP stream)

The main goal is to produce one Excel file where both streams are time-aligned for comparison.

## 1) Scripts in this project

- `mionix_capture.html`
  - Frontend dashboard for live visualization and recording.
  - Now supports both Mionix and EmotiBit live display.
  - Can directly download a combined Excel file.

- `emotibit_ws_bridge.py`
  - Local bridge from EmotiBit UDP to browser WebSocket.
  - Needed for EmotiBit values to appear in the dashboard.

- `synced_emotibit_mouse_to_excel.py`
  - Python-only capture path (no dashboard required).
  - Captures both streams and writes one synced Excel file.

## 2) One-time setup

Install required Python packages:

```bash
pip install pandas openpyxl websocket-client websockets
```

## 3) Device/software prerequisites

### EmotiBit

- EmotiBit powered on and connected to Wi-Fi.
- Computer and EmotiBit on the same network.
- EmotiBit Oscilloscope open with UDP output enabled.
- UDP target should be `localhost` (or `127.0.0.1`) and port `12346`.

### Mionix

- Mionix Device Hub running.
- WebSocket endpoint available at `ws://localhost:7681` with protocol `mionix-beta`.

## 4) Recommended workflow: dashboard + direct Excel download

1. Start the EmotiBit bridge:

   ```bash
   python3 emotibit_ws_bridge.py
   ```

2. Open `mionix_capture.html` in your browser.

3. Confirm connections on the page:
   - `Mionix: Connected`
   - `EmotiBit bridge: Connected`

4. Click `Start Capture`.

5. Run your study/trial.

6. Click `Stop Capture`.

7. Click `Download Excel (Combined)`.

This downloads one workbook with combined study data and a companion metadata file:

- `combined_capture_<timestamp>.xlsx`
- `combined_capture_<timestamp>_info.json`

## 5) Alternative workflow: Python-only capture

If you do not need the frontend dashboard:

```bash
python3 synced_emotibit_mouse_to_excel.py
```

Stop with `Ctrl+C` to save output.

Example with fixed duration:

```bash
python3 synced_emotibit_mouse_to_excel.py --duration 120 --output study_run.xlsx
```

## 6) Excel output format

Combined workbook includes:

- `Mouse_HR_GSR`
  - Mouse rows for `bioMetrics` / `bioRaw`.
  - Focus fields for study use: heart rate and GSR.

- `EmotiBit_Raw`
  - EmotiBit packets with stream tag, value, reliability, and timestamps.

- `Synced_Comparison`
  - Time-synced comparison rows (nearest timestamp match).
  - Useful for mouse-vs-EmotiBit analysis.
  - EmotiBit EDA-related streams are kept in separate columns:
    - `emotibit_EA` = overall EDA signal
    - `emotibit_EL` = tonic component (electrodermal level)
    - `emotibit_ER` = phasic component (electrodermal response)
  - EmotiBit heart rate is exported as `emotibit_heartRate`.

- `*_info.json` (companion metadata export)
  - Per-stream metadata derived from captured EmotiBit packets.
  - Includes stream tags, sample counts, estimated nominal sample rate, and packet/value handling notes.

## 7) Timestamp and sync behavior

- Timestamps are recorded in local time with timezone offset where available.
- Syncing is nearest-neighbor by timestamp.
- For EmotiBit, nearest-neighbor matching is done independently by stream/tag (for example, `EA`, `EL`, and `ER` are matched separately).
- In the Python script, sync tolerance is configurable with:
  - `--sync-tolerance-ms` (default: `500`)

## 8) Notes on values and interpretation

- Mouse `heartRate` from `bioMetrics` is BPM.
- Mouse `bioRaw.heartRate` is a raw optical sensor value (not BPM).
- GSR values are treated as raw.
- EmotiBit packets can include multiple samples in one payload (comma-separated values).
  - In exports, these are normalized to a single scalar using the last sample in the packet payload.
- `EA`, `EL`, and `ER` are not interchangeable and are not merged into one EDA field.
- Empty cells are expected when a field is not present in that message type.

## 9) Troubleshooting

- EmotiBit not showing in dashboard:
  - Verify `emotibit_ws_bridge.py` is running.
  - Verify Oscilloscope UDP output is enabled to port `12346`.

- Mionix not connected:
  - Verify Mionix Device Hub is running.
  - Check endpoint `ws://localhost:7681`.

- No data in Excel:
  - Make sure capture was started before trial.
  - Confirm both connection labels show connected status.
