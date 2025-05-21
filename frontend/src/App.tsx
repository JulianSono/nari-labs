import { useState } from 'react'
import { Button } from './components/ui/button'
import { Input } from './components/ui/input'
import { Label } from './components/ui/label'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './components/ui/select'
import { Slider } from './components/ui/slider'
import { Loader2 } from 'lucide-react'

const emotions = ['happy', 'sad', 'angry', 'neutral', 'excited']
const tones = ['formal', 'casual', 'professional', 'friendly']

// Get the current hostname for the API URL
const API_BASE = window.location.origin

function App() {
  const [text, setText] = useState('')
  const [emotion, setEmotion] = useState('neutral')
  const [tone, setTone] = useState('casual')
  const [pace, setPace] = useState(1)
  const [loading, setLoading] = useState(false)
  const [audioUrl, setAudioUrl] = useState<string | null>(null)

  const handleGenerate = async () => {
    if (!text) return

    setLoading(true)
    setAudioUrl(null)
    try {
      const response = await fetch(`${API_BASE}/generate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text,
          emotion,
          tone,
          pace,
        }),
      })

      if (!response.ok) {
        throw new Error('Failed to generate audio')
      }

      const data = await response.json()
      setAudioUrl(`${API_BASE}/${data.audio_path}`)
    } catch (error) {
      console.error('Error generating audio:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-background p-8">
      <div className="mx-auto max-w-2xl space-y-8">
        <div className="space-y-2">
          <h1 className="text-3xl font-bold">Voice Generation</h1>
          <p className="text-muted-foreground">
            Generate natural-sounding voice from text with customizable parameters.
          </p>
        </div>

        <div className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="text">Text</Label>
            <Input
              id="text"
              placeholder="Enter text to convert to speech..."
              value={text}
              onChange={(e) => setText(e.target.value)}
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="emotion">Emotion</Label>
              <Select value={emotion} onValueChange={setEmotion}>
                <SelectTrigger id="emotion">
                  <SelectValue placeholder="Select emotion" />
                </SelectTrigger>
                <SelectContent>
                  {emotions.map((e) => (
                    <SelectItem key={e} value={e}>
                      {e.charAt(0).toUpperCase() + e.slice(1)}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label htmlFor="tone">Tone</Label>
              <Select value={tone} onValueChange={setTone}>
                <SelectTrigger id="tone">
                  <SelectValue placeholder="Select tone" />
                </SelectTrigger>
                <SelectContent>
                  {tones.map((t) => (
                    <SelectItem key={t} value={t}>
                      {t.charAt(0).toUpperCase() + t.slice(1)}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="pace">Pace: {pace.toFixed(1)}x</Label>
            <Slider
              id="pace"
              min={0.5}
              max={2}
              step={0.1}
              value={[pace]}
              onValueChange={([value]) => setPace(value)}
            />
          </div>

          <Button
            className="w-full"
            onClick={handleGenerate}
            disabled={loading || !text}
          >
            {loading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Generating...
              </>
            ) : (
              'Generate Voice'
            )}
          </Button>
        </div>

        {audioUrl && (
          <div className="space-y-2">
            <Label>Generated Audio</Label>
            <audio controls className="w-full">
              <source src={audioUrl} type="audio/wav" />
              Your browser does not support the audio element.
            </audio>
          </div>
        )}
      </div>
    </div>
  )
}

export default App 