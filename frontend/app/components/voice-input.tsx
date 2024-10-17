"use client";

import { useState, useEffect, useRef } from 'react';
import PatientHistory from './patient-history';
import { surgeonQuery } from '@/actions/surgeon-query';
import { FaMicrophone, FaStop } from "react-icons/fa";
import { SpeechRecognitionErrorEvent, SpeechRecognitionEvent } from '@/types/global';

/**
 * VoiceInput Component
 * Captures user speech, sends it to the AI, and plays the AI's response as audio.
 */
const VoiceInput = () => {
  const recognitionRef = useRef<SpeechRecognition>();

  const [isActive, setIsActive] = useState<boolean>(false);
  const [text, setText] = useState<string>('');
  const [patientHistory, setPatientHistory] = useState<string>('');
  const [voices, setVoices] = useState<Array<SpeechSynthesisVoice>>();
  const [aiResponse, setAIResponse] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [audioUrl, setAudioUrl] = useState<string | null>(null);

  // Pre-selected Sound Model
  const SELECTED_SOUND_MODEL = {
    name: "Speechbrain - Ljspeech",
    url: "https://api-inference.huggingface.co/models/speechbrain/tts-tacotron2-ljspeech",
  };

  useEffect(() => {
    const availableVoices = window.speechSynthesis.getVoices();
    if (Array.isArray(availableVoices) && availableVoices.length > 0) {
      setVoices(availableVoices);
      return;
    }
    if ('onvoiceschanged' in window.speechSynthesis) {
      window.speechSynthesis.onvoiceschanged = () => {
        const updatedVoices = window.speechSynthesis.getVoices();
        setVoices(updatedVoices);
      };
    }
  }, []);

  /**
   * Handles starting and stopping the speech recognition.
   */
  function handleOnRecord() {
    if (isActive) {
      recognitionRef.current?.stop();
      setIsActive(false);
      return;
    }

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognitionRef.current = new SpeechRecognition();

    recognitionRef.current.onstart = () => {
      setIsActive(true);
    };

    recognitionRef.current.onend = () => {
      setIsActive(false);
    };

    recognitionRef.current.onresult = async (event: SpeechRecognitionEvent) => {
      const transcript = event.results[0][0].transcript;
      setText(transcript);
      setIsLoading(true);

      try {
        const response = await surgeonQuery(transcript, patientHistory);
        setAIResponse(response.data);
      } catch (error) {
        console.error("Error fetching AI response:", error);
        setAIResponse("Sorry, there was an error processing your request.");
      } finally {
        setIsLoading(false);
      }
    };

    recognitionRef.current.onerror = (event: SpeechRecognitionErrorEvent) => {
      console.error("Speech Recognition Error:", event.error);
      setIsActive(false);
    };

    recognitionRef.current.start();
  }

  /**
   * Generates audio from the AI response using the selected sound model.
   */
  const generateAndPlayAudio = async (text: string) => {
    try {
      const response = await fetch("/api/generate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          input: text,
          modelUrl: SELECTED_SOUND_MODEL.url,
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to fetch audio data.");
      }

      const data = await response.arrayBuffer();
      const blob = new Blob([data], { type: "audio/mpeg" });
      const generatedAudioUrl = URL.createObjectURL(blob);
      setAudioUrl(generatedAudioUrl);

      // Automatically play the audio
      const audio = new Audio(generatedAudioUrl);
      audio.play();
    } catch (error) {
      console.error("Error generating audio:", error);
    }
  };

  /**
   * useEffect to watch for changes in aiResponse and trigger audio generation.
   */
  useEffect(() => {
    if (aiResponse.trim() !== "") {
      generateAndPlayAudio(aiResponse);
    }
    // Cleanup the audio URL when component unmounts or audioUrl changes
    return () => {
      if (audioUrl) {
        URL.revokeObjectURL(audioUrl);
      }
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [aiResponse]);

  return (
    <section className="max-w-md w-full flex flex-col gap-y-5 rounded-xl overflow-hidden mx-auto">
      <div className="bg-zinc-200 p-4">
        <div className="bg-blue-200 rounded-lg p-2 border-2 border-blue-300">
          <ul className="font-mono text-center font-bold text-blue-900 uppercase px-4 py-2 border border-blue-800 rounded">
            <li>&gt; SurgiAI</li>
          </ul>
        </div>
      </div>

      <PatientHistory setPatientHistory={setPatientHistory} />

      {isActive && (
        <div className="w-full h-12 rounded-lg mb-8 flex items-center justify-center space-x-2">
          {/* Simulated waveform animation */}
          <div className="w-2 h-6 bg-blue-500 animate-pulse rounded-sm"></div>
          <div className="w-2 h-8 bg-blue-500 animate-pulse rounded-sm"></div>
          <div className="w-2 h-4 bg-blue-500 animate-pulse rounded-sm"></div>
          <div className="w-2 h-6 bg-blue-500 animate-pulse rounded-sm"></div>
          <div className="w-2 h-8 bg-blue-500 animate-pulse rounded-sm"></div>
          <div className="w-2 h-6 bg-blue-500 animate-pulse rounded-sm"></div>
          <div className="w-2 h-8 bg-blue-500 animate-pulse rounded-sm"></div>
          <div className="w-2 h-4 bg-blue-500 animate-pulse rounded-sm"></div>
          <div className="w-2 h-6 bg-blue-500 animate-pulse rounded-sm"></div>
          <div className="w-2 h-8 bg-blue-500 animate-pulse rounded-sm"></div>
        </div>
      )}

      {patientHistory.length > 0 && (
        <>
          <button
            className={`w-full h-full flex items-center gap-x-2 justify-center uppercase font-semibold text-sm ${
              isActive
                ? 'text-white bg-red-500'
                : 'text-zinc-200 bg-zinc-900'
            } color-white py-3 rounded-sm`}
            onClick={handleOnRecord}
          >
            {isActive ? (
              <FaStop className="animate-pulse w-4 h-4" />
            ) : (
              <FaMicrophone className="w-4 h-4" />
            )}
            {isActive ? 'Stop' : 'Ask AI'}
          </button>
          <p>
            <strong>Surgeon Query:</strong> {text}
          </p>
          {isLoading ? (
            <p className="mb-4 animate-pulse text-sm text-gray-500">AI Response: Loading...</p>
          ) : (
            <p className="mb-4">
              <strong>AI Response:</strong> {aiResponse}
            </p>
          )}
        </>
      )}

      {/* Audio Player (optional, can be removed if auto-playing) */}
      {audioUrl && (
        <audio controls className="mt-4">
          <source type="audio/mpeg" src={audioUrl} />
          Your browser does not support the audio element.
        </audio>
      )}
    </section>
  );
};

export default VoiceInput;
