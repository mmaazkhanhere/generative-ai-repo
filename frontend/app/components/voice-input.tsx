"use client";

import { useState, useEffect, useRef } from 'react';

import PatientHistory from './patient-history';

import { surgeonQuery } from '@/actions/surgeon-query';

import { FaMicrophone, FaStop } from "react-icons/fa";

import { SpeechRecognitionErrorEvent, SpeechRecognitionEvent } from '@/types/global';


const VoiceInput = () => {
  const recognitionRef = useRef<SpeechRecognition>();

  const [isActive, setIsActive] = useState<boolean>(false);
  const [text, setText] = useState<string>('');
  const [patientHistory, setPatientHistory] = useState<string>('')
  const [voices, setVoices] = useState<Array<SpeechSynthesisVoice>>();
  const [aiResponse, setAIResponse] = useState<string>('')
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const isSpeechDetected = false;

  useEffect(() => {
    const voices = window.speechSynthesis.getVoices();
    if (Array.isArray(voices) && voices.length > 0) {
      setVoices(voices);
      return;
    }
    if ('onvoiceschanged' in window.speechSynthesis) {
      window.speechSynthesis.onvoiceschanged = function () {
        const voices = window.speechSynthesis.getVoices();
        setVoices(voices);
      };
    }
  }, []);

  function handleOnRecord() {
    if (isActive) {
      recognitionRef.current?.stop();
      setIsActive(false);
      return;
    }

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognitionRef.current = new SpeechRecognition();

    recognitionRef.current.onstart = function () {
      setIsActive(true);
    };

    recognitionRef.current.onend = function () {
      setIsActive(false);
    };

    recognitionRef.current.onresult = async function (event: SpeechRecognitionEvent) {
      const transcript = event.results[0][0].transcript;
      setText(transcript);
      setIsLoading(true);

      const response = await surgeonQuery(transcript, patientHistory)
      setAIResponse(response.data)
      setIsLoading(false)
    };

    recognitionRef.current.onerror = (event: SpeechRecognitionErrorEvent) => {
      console.error("Speech Recognition Error:", event.error);
      setIsActive(false);
    };

    recognitionRef.current.start();
  }

  console.log(patientHistory)

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

      {
        patientHistory.length > 0 && (
          <>
            <button
                className={`w-full h-full flex items-center gap-x-2 justify-center uppercase font-semibold text-sm  ${isActive ? 'text-white bg-red-500' : 'text-zinc-200 bg-zinc-900'} color-white py-3 rounded-sm`}
                onClick={handleOnRecord}
            >
                {
                  isActive ? <FaStop className='animate-pulse w-4 h-4' /> : <FaMicrophone className='w-4 h-4' />
                }
                {isActive ? 'Stop' : 'Ask AI'}
            </button>
            <p>
                Surgeon Query: {text}
            </p>
            {
              isLoading ? (
                <p className="mb-4 animate-pulse text-sm text-gray-500">AI Response: Loading...</p> // Loading state
              ) : (
                <p className="mb-4">AI Response: {aiResponse}</p> // Show AI response
              )
            }
          </>
      
        )
      }
      

        
      </section>
  );
};

export default VoiceInput;
