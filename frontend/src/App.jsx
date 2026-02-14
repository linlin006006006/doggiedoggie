import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [prompt, setPrompt] = useState('')
  const [duration, setDuration] = useState(30)
  const [forceInstrumental, setForceInstrumental] = useState(true)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [audioUrl, setAudioUrl] = useState(null)
  const [presets, setPresets] = useState({})
  const [selectedPreset, setSelectedPreset] = useState('')

  useEffect(() => {
    // Fetch available presets
    fetch('/api/presets')
      .then(res => res.json())
      .then(data => setPresets(data.presets || {}))
      .catch(err => console.error('Failed to load presets:', err))
  }, [])

  const handleGenerate = async () => {
    if (!prompt.trim() && !selectedPreset) {
      setError('Please enter a prompt or select a preset')
      return
    }

    setLoading(true)
    setError(null)
    setAudioUrl(null)

    try {
      let response

      if (selectedPreset) {
        // Generate from preset
        const url = `/api/generate-from-preset?preset=${encodeURIComponent(selectedPreset)}&duration_seconds=${duration}`
        response = await fetch(url, { method: 'POST' })
      } else {
        // Generate from custom prompt
        response = await fetch('/api/generate-music', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            prompt,
            duration_seconds: duration,
            force_instrumental: forceInstrumental,
          }),
        })
      }

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'Unknown error' }))
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`)
      }

      // Create blob URL from audio response
      const blob = await response.blob()
      const audioUrl = URL.createObjectURL(blob)
      setAudioUrl(audioUrl)
    } catch (err) {
      setError(err.message)
      console.error('Error generating music:', err)
    } finally {
      setLoading(false)
    }
  }

  const handlePresetChange = (preset) => {
    setSelectedPreset(preset)
    setPrompt('') // Clear custom prompt when preset is selected
  }

  const handleCustomPrompt = () => {
    setSelectedPreset('') // Clear preset when custom prompt is entered
  }

  return (
    <div className="app">
      <div className="container">
        <header className="header">
          <h1>🎵 AI Music Generator</h1>
          <p className="subtitle">Generate music using ElevenLabs AI</p>
        </header>

        <div className="card">
          <div className="form-section">
            <h2>Generate Custom Music</h2>
            <div className="form-group">
              <label htmlFor="prompt">Music Description</label>
              <textarea
                id="prompt"
                value={prompt}
                onChange={(e) => {
                  setPrompt(e.target.value)
                  handleCustomPrompt()
                }}
                placeholder="e.g., peaceful ambient piano with soft synthesizer pads, slow tempo"
                rows={3}
                disabled={loading || !!selectedPreset}
              />
              <small className="hint">
                Describe the music you want: genre, mood, instruments, tempo
              </small>
            </div>

            <div className="form-group">
              <label htmlFor="duration">Duration (seconds)</label>
              <input
                id="duration"
                type="number"
                min="1"
                max="300"
                value={duration}
                onChange={(e) => setDuration(parseFloat(e.target.value))}
                disabled={loading}
              />
              <small className="hint">Maximum 300 seconds (5 minutes)</small>
            </div>

            <div className="form-group checkbox-group">
              <label>
                <input
                  type="checkbox"
                  checked={forceInstrumental}
                  onChange={(e) => setForceInstrumental(e.target.checked)}
                  disabled={loading || !!selectedPreset}
                />
                Force instrumental (no vocals)
              </label>
            </div>
          </div>

          <div className="divider">
            <span>OR</span>
          </div>

          <div className="form-section">
            <h2>Use Preset</h2>
            <div className="form-group">
              <label htmlFor="preset">Select Preset</label>
              <select
                id="preset"
                value={selectedPreset}
                onChange={(e) => handlePresetChange(e.target.value)}
                disabled={loading}
              >
                <option value="">-- Select a preset --</option>
                {Object.entries(presets).map(([key, description]) => (
                  <option key={key} value={key}>
                    {description}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <button
            className="generate-button"
            onClick={handleGenerate}
            disabled={loading || (!prompt.trim() && !selectedPreset)}
          >
            {loading ? 'Generating...' : 'Generate Music'}
          </button>

          {error && (
            <div className="error-message">
              <strong>Error:</strong> {error}
            </div>
          )}

          {audioUrl && (
            <div className="audio-player">
              <h3>Generated Music</h3>
              <audio controls src={audioUrl} className="audio-element">
                Your browser does not support the audio element.
              </audio>
              <a
                href={audioUrl}
                download="generated_music.mp3"
                className="download-button"
              >
                Download MP3
              </a>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default App

