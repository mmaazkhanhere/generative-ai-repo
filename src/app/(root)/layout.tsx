import React from 'react'
import { MicrophoneContextProvider } from './context/microphone-context-provider'
import { DeepgramContextProvider } from './context/deepgram-context-provider'

type Props = {
    children: React.ReactNode
}

const RootLayout = ({children}: Props) => {
  return (
    <main>
      <MicrophoneContextProvider>
        <DeepgramContextProvider>
          {children}
        </DeepgramContextProvider>
      </MicrophoneContextProvider>
        
    </main>
  )
}

export default RootLayout