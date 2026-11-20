import React, { useRef, useState } from 'react';
import { getTtsAudioUrl } from '../api/client';

interface AudioWaveformPlayerProps {
  text: string;
  lang: 'hi' | 'en';
  isHi: boolean;
}

export const AudioWaveformPlayer: React.FC<AudioWaveformPlayerProps> = ({ text, lang, isHi }) => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const audioRef = useRef<HTMLAudioElement | null>(null);

  const handleToggle = () => {
    if (!text || text.trim().length === 0) return;

    if (!audioRef.current) {
      audioRef.current = new Audio(getTtsAudioUrl(text, lang));
      audioRef.current.onplay = () => {
        setIsPlaying(true);
        setIsLoading(false);
      };
      audioRef.current.onpause = () => setIsPlaying(false);
      audioRef.current.onended = () => setIsPlaying(false);
      audioRef.current.onerror = () => {
        setIsPlaying(false);
        setIsLoading(false);
        alert(isHi ? 'ऑडियो प्लेबैक में समस्या आई।' : 'Audio playback error.');
      };
      setIsLoading(true);
      audioRef.current.play();
    } else {
      if (isPlaying) {
        audioRef.current.pause();
      } else {
        audioRef.current.play();
      }
    }
  };

  return (
    <div className="flex items-center gap-3 p-3 rounded-2xl bg-emerald-950 text-white border border-emerald-800 shadow-sm">
      <button
        type="button"
        onClick={handleToggle}
        className="w-10 h-10 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 flex items-center justify-center font-bold text-lg transition shrink-0 cursor-pointer"
        aria-label={isPlaying ? 'Pause advisory audio' : 'Play advisory audio'}
      >
        {isLoading ? '⏳' : isPlaying ? '⏸️' : '🔊'}
      </button>

      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-2">
          <span className="text-xs font-bold text-white truncate">
            {isHi ? 'किसान वाणी (न्यूरल वॉयस सारांश)' : 'Kisan Vani (Neural Audio Summary)'}
          </span>
          {isPlaying && (
            <div className="inline-flex items-center gap-1 text-emerald-400" aria-label="Audio playing">
              <span className="sound-wave-bar" style={{ animationDelay: '0.1s' }} />
              <span className="sound-wave-bar" style={{ animationDelay: '0.3s' }} />
              <span className="sound-wave-bar" style={{ animationDelay: '0.2s' }} />
              <span className="sound-wave-bar" style={{ animationDelay: '0.5s' }} />
              <span className="sound-wave-bar" style={{ animationDelay: '0.4s' }} />
            </div>
          )}
        </div>
        <p className="text-[11px] text-emerald-300 truncate">
          {isPlaying
            ? isHi ? 'सलाह सुनाई जा रही है...' : 'Playing advisory audio...'
            : isHi ? 'पूरी योजना अपनी भाषा में सुनें' : 'Listen to full plan in your language'}
        </p>
      </div>

      <a
        href={getTtsAudioUrl(text, lang)}
        download="khetsathi-advisory.mp3"
        className="text-[11px] font-bold px-2.5 py-1.5 rounded-lg bg-emerald-800/80 hover:bg-emerald-700 text-emerald-200 transition shrink-0"
      >
        📥 MP3
      </a>
    </div>
  );
};
