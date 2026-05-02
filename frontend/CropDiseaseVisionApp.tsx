/**
 * Enhanced Frontend for Crop Disease Vision with Multilingual Support
 * React + TypeScript + Tailwind CSS
 * Supports: Speech Recognition, Translation, Text-to-Speech, Chat Assistant
 */

import React, { useState, useEffect, useRef } from 'react';

// ============ Types & Interfaces ============

interface PredictionResult {
  disease: string;
  confidence: number;
  status: string;
  description: string;
  treatment: string;
  raw_class?: string;
}

interface TranslatedResult extends PredictionResult {
  target_language: string;
}

interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  language: string;
  timestamp: Date;
}

// ============ Main App Component ============

const CropDiseaseVisionApp: React.FC = () => {
  // State Management
  const [selectedLanguage, setSelectedLanguage] = useState<string>('English');
  const [isRecording, setIsRecording] = useState<boolean>(false);
  const [transcript, setTranscript] = useState<string>('');
  const [uploadedImage, setUploadedImage] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string>('');
  const [prediction, setPrediction] = useState<PredictionResult | null>(null);
  const [translatedResult, setTranslatedResult] = useState<TranslatedResult | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>('');
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([]);
  const [chatInput, setChatInput] = useState<string>('');
  const [showChat, setShowChat] = useState<boolean>(false);
  const [activeTab, setActiveTab] = useState<'image' | 'voice' | 'chat'>('image');

  // Refs
  const recognitionRef = useRef<SpeechRecognition | null>(null);
  const speechSynthesisRef = useRef<SpeechSynthesisUtterance | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // API Base URL
  const API_BASE = 'http://localhost:5000';
  const MULTILINGUAL_API = `${API_BASE}/api/multilingual`;

  // ============ Speech Recognition Setup ============

  useEffect(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
      recognitionRef.current = new SpeechRecognition();
      recognitionRef.current.continuous = false;
      recognitionRef.current.interimResults = false;

      recognitionRef.current.onstart = () => {
        setIsRecording(true);
        setError('');
      };

      recognitionRef.current.onresult = async (event: SpeechRecognitionEvent) => {
        const text = Array.from(event.results)
          .map((result: SpeechRecognitionResult) => result[0].transcript)
          .join('');
        
        setTranscript(text);
        
        // Process transcription
        try {
          const response = await fetch(`${MULTILINGUAL_API}/speech-to-text`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              transcribed_text: text,
              language_code: getLanguageCode(selectedLanguage),
              confidence: 0.95
            })
          });
          
          if (response.ok) {
            const data = await response.json();
            console.log('Transcription processed:', data);
          }
        } catch (err) {
          console.error('Error processing transcription:', err);
        }
      };

      recognitionRef.current.onerror = (event: SpeechRecognitionEvent) => {
        setError(`Speech recognition error: ${event.error}`);
        setIsRecording(false);
      };

      recognitionRef.current.onend = () => {
        setIsRecording(false);
      };
    }
  }, [selectedLanguage]);

  // ============ Helper Functions ============

  const getLanguageCode = (language: string): string => {
    const codes: { [key: string]: string } = {
      'English': 'en-US',
      'Gujarati': 'gu-IN',
      'Hindi': 'hi-IN',
      'Marathi': 'mr-IN',
      'Tamil': 'ta-IN',
      'Telugu': 'te-IN'
    };
    return codes[language] || 'en-US';
  };

  const startRecording = () => {
    if (recognitionRef.current) {
      recognitionRef.current.lang = getLanguageCode(selectedLanguage);
      recognitionRef.current.start();
    }
  };

  const stopRecording = () => {
    if (recognitionRef.current) {
        recognitionRef.current.stop();
    }
  };

  // ============ Image Upload Handler ============

  const handleImageUpload = (file: File) => {
    if (!file.type.startsWith('image/')) {
      setError('Please upload a valid image file');
      return;
    }

    setUploadedImage(file);
    const reader = new FileReader();
    reader.onload = (e) => {
      setPreviewUrl(e.target?.result as string);
    };
    reader.readAsDataURL(file);
    setError('');
  };

  // ============ Prediction Handler ============

  const handlePredict = async () => {
    if (!uploadedImage) {
      setError('Please select an image first');
      return;
    }

    setLoading(true);
    setError('');

    try {
      // Upload image
      const formData = new FormData();
      formData.append('file', uploadedImage);

      const response = await fetch(`${API_BASE}/predict`, {
        method: 'POST',
        body: formData
      });

      if (!response.ok) {
        throw new Error('Prediction failed');
      }

      const result = await response.json();
      setPrediction(result);

      // Translate result if needed
      if (selectedLanguage !== 'English') {
        await translateResult(result);
      } else {
        setTranslatedResult(result as TranslatedResult);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Prediction failed');
    } finally {
      setLoading(false);
    }
  };

  // ============ Translation Handler ============

  const translateResult = async (result: PredictionResult) => {
    try {
      const response = await fetch(`${MULTILINGUAL_API}/translate-disease`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          disease: result.disease,
          status: result.status,
          description: result.description,
          treatment: result.treatment,
          confidence: result.confidence,
          target_language: selectedLanguage
        })
      });

      if (response.ok) {
        const data = await response.json();
        setTranslatedResult(data.translated);
        
        // Speak translated result
        if (selectedLanguage !== 'English') {
          speakText(data.translated.treatment, selectedLanguage);
        }
      }
    } catch (err) {
      console.error('Translation error:', err);
    }
  };

  // ============ Text-to-Speech Handler ============

  const speakText = async (text: string, language: string) => {
    try {
      const response = await fetch(`${MULTILINGUAL_API}/text-to-speech`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          text: text,
          language_code: getLanguageCode(language)
        })
      });

      if (response.ok) {
        const config = await response.json();
        
        // Use Web Speech API
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = getLanguageCode(language);
        utterance.rate = 0.9;
        
        speechSynthesis.speak(utterance);
      }
    } catch (err) {
      console.error('TTS error:', err);
    }
  };

  // ============ Chat Handler ============

  const handleChat = async () => {
    if (!chatInput.trim()) return;

    const userMessage: ChatMessage = {
      role: 'user',
      content: chatInput,
      language: selectedLanguage,
      timestamp: new Date()
    };

    setChatMessages([...chatMessages, userMessage]);
    setChatInput('');
    setLoading(true);

    try {
      const response = await fetch(`${MULTILINGUAL_API}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          question: chatInput,
          language: selectedLanguage,
          context: prediction ? { disease: prediction.raw_class } : undefined
        })
      });

      if (response.ok) {
        const data = await response.json();
        
        const assistantMessage: ChatMessage = {
          role: 'assistant',
          content: data.response,
          language: selectedLanguage,
          timestamp: new Date()
        };

        setChatMessages(prev => [...prev, assistantMessage]);
        
        // Speak response
        speakText(data.response, selectedLanguage);
      }
    } catch (err) {
      setError('Chat error: ' + (err instanceof Error ? err.message : 'Unknown error'));
    } finally {
      setLoading(false);
    }
  };

  // ============ Render Components ============

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-50 p-4">
      {/* Header */}
      <div className="max-w-6xl mx-auto">
        <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-4xl font-bold text-green-700 flex items-center gap-2">
                <span>🌾</span> Crop Disease Vision
              </h1>
              <p className="text-gray-600 mt-2">AI-Powered Crop Health Assistant</p>
            </div>
            
            {/* Language Selector */}
            <div className="flex flex-col items-end gap-2">
              <label className="text-sm font-semibold text-gray-700">Select Language</label>
              <select
                value={selectedLanguage}
                onChange={(e) => setSelectedLanguage(e.target.value)}
                className="px-4 py-2 border-2 border-green-500 rounded-lg focus:outline-none focus:border-green-700"
              >
                <option>English</option>
                <option>Gujarati</option>
                <option>Hindi</option>
                <option>Marathi</option>
                <option>Tamil</option>
                <option>Telugu</option>
              </select>
            </div>
          </div>
        </div>

        {/* Tab Navigation */}
        <div className="flex gap-2 mb-6">
          <TabButton
            active={activeTab === 'image'}
            onClick={() => setActiveTab('image')}
            icon="📷"
            label="Image Upload"
          />
          <TabButton
            active={activeTab === 'voice'}
            onClick={() => setActiveTab('voice')}
            icon="🎤"
            label="Voice Input"
          />
          <TabButton
            active={activeTab === 'chat'}
            onClick={() => setActiveTab('chat')}
            icon="💬"
            label="Ask Assistant"
          />
        </div>

        {/* Error Display */}
        {error && (
          <div className="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mb-6 rounded">
            <p className="font-semibold">Error</p>
            <p>{error}</p>
          </div>
        )}

        {/* Image Upload Tab */}
        {activeTab === 'image' && <ImageUploadSection {...{ handleImageUpload, previewUrl, loading, handlePredict, translatedResult, speakText, selectedLanguage }} />}

        {/* Voice Input Tab */}
        {activeTab === 'voice' && <VoiceInputSection {...{ transcript, isRecording, startRecording, stopRecording, loading, selectedLanguage }} />}

        {/* Chat Tab */}
        {activeTab === 'chat' && <ChatSection {...{ chatMessages, chatInput, setChatInput, handleChat, loading, selectedLanguage }} />}
      </div>
    </div>
  );
};

// ============ Sub-Components ============

const TabButton: React.FC<{
  active: boolean;
  onClick: () => void;
  icon: string;
  label: string;
}> = ({ active, onClick, icon, label }) => (
  <button
    onClick={onClick}
    className={`px-6 py-3 rounded-lg font-semibold transition-all ${
      active
        ? 'bg-green-600 text-white shadow-lg'
        : 'bg-white text-gray-700 border-2 border-gray-300 hover:border-green-500'
    }`}
  >
    {icon} {label}
  </button>
);

const ImageUploadSection: React.FC<any> = ({
  handleImageUpload,
  previewUrl,
  loading,
  handlePredict,
  translatedResult,
  speakText,
  selectedLanguage
}) => {
  const fileInputRef = useRef<HTMLInputElement>(null);

  return (
    <div className="grid md:grid-cols-2 gap-6">
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h2 className="text-2xl font-bold text-gray-800 mb-4">📷 Upload Crop Image</h2>
        
        <div
          onClick={() => fileInputRef.current?.click()}
          className="border-4 border-dashed border-green-500 rounded-lg p-8 text-center cursor-pointer hover:bg-green-50 transition"
        >
          <p className="text-gray-600 font-semibold">Click to upload or drag and drop</p>
          <p className="text-gray-400 text-sm mt-2">PNG, JPG, GIF up to 10MB</p>
        </div>

        <input
          ref={fileInputRef}
          type="file"
          accept="image/*"
          className="hidden"
          onChange={(e) => e.target.files && handleImageUpload(e.target.files[0])}
        />

        {previewUrl && (
          <div className="mt-4">
            <img src={previewUrl} alt="Preview" className="w-full rounded-lg" />
          </div>
        )}

        <button
          onClick={handlePredict}
          disabled={!previewUrl || loading}
          className="w-full mt-4 px-6 py-3 bg-green-600 text-white font-bold rounded-lg hover:bg-green-700 disabled:bg-gray-400 transition"
        >
          {loading ? '🔄 Analyzing...' : '🔍 Analyze Image'}
        </button>
      </div>

      {translatedResult && (
        <ResultCard result={translatedResult} speakText={speakText} selectedLanguage={selectedLanguage} />
      )}
    </div>
  );
};

const VoiceInputSection: React.FC<any> = ({
  transcript,
  isRecording,
  startRecording,
  stopRecording,
  loading,
  selectedLanguage
}) => (
  <div className="bg-white rounded-lg shadow-lg p-6 max-w-2xl mx-auto">
    <h2 className="text-2xl font-bold text-gray-800 mb-4">🎤 Voice Input</h2>
    
    <button
      onClick={isRecording ? stopRecording : startRecording}
      className={`w-full py-4 px-6 rounded-lg font-bold text-white text-xl transition mb-4 ${
        isRecording
          ? 'bg-red-600 hover:bg-red-700 animate-pulse'
          : 'bg-green-600 hover:bg-green-700'
      }`}
    >
      {isRecording ? '⏹️ Stop Recording' : '🎤 Start Recording'}
    </button>

    {transcript && (
      <div className="bg-blue-50 border-l-4 border-blue-500 p-4 rounded">
        <p className="font-semibold text-gray-700">Transcribed Text:</p>
        <p className="text-gray-800 mt-2">{transcript}</p>
      </div>
    )}
  </div>
);

const ChatSection: React.FC<any> = ({
  chatMessages,
  chatInput,
  setChatInput,
  handleChat,
  loading,
  selectedLanguage
}) => (
  <div className="bg-white rounded-lg shadow-lg p-6 max-w-2xl mx-auto">
    <h2 className="text-2xl font-bold text-gray-800 mb-4">💬 Ask Assistant</h2>
    
    <div className="h-96 overflow-y-auto border rounded-lg p-4 mb-4 bg-gray-50">
      {chatMessages.length === 0 ? (
        <p className="text-gray-500 text-center">Start a conversation...</p>
      ) : (
        chatMessages.map((msg, idx) => (
          <div key={idx} className={`mb-3 ${msg.role === 'user' ? 'text-right' : 'text-left'}`}>
            <div
              className={`inline-block px-4 py-2 rounded-lg max-w-xs ${
                msg.role === 'user'
                  ? 'bg-green-600 text-white'
                  : 'bg-gray-300 text-gray-900'
              }`}
            >
              <p>{msg.content}</p>
            </div>
          </div>
        ))
      )}
    </div>

    <div className="flex gap-2">
      <input
        type="text"
        value={chatInput}
        onChange={(e) => setChatInput(e.target.value)}
        onKeyPress={(e) => e.key === 'Enter' && handleChat()}
        placeholder="Ask your question..."
        className="flex-1 px-4 py-2 border rounded-lg focus:outline-none focus:border-green-600"
      />
      <button
        onClick={handleChat}
        disabled={loading || !chatInput.trim()}
        className="px-6 py-2 bg-green-600 text-white font-bold rounded-lg hover:bg-green-700 disabled:bg-gray-400"
      >
        Send
      </button>
    </div>
  </div>
);

const ResultCard: React.FC<{
  result: any;
  speakText: (text: string, lang: string) => void;
  selectedLanguage: string;
}> = ({ result, speakText, selectedLanguage }) => (
  <div className="bg-white rounded-lg shadow-lg p-6">
    <h2 className="text-2xl font-bold text-gray-800 mb-4">✅ Analysis Result</h2>
    
    <div className="space-y-4">
      <div className="bg-yellow-50 border-l-4 border-yellow-500 p-4 rounded">
        <p className="font-semibold text-gray-700">Disease</p>
        <p className="text-xl font-bold text-gray-900">{result.disease}</p>
      </div>

      <div className="bg-blue-50 border-l-4 border-blue-500 p-4 rounded">
        <p className="font-semibold text-gray-700">Status</p>
        <p className="text-lg font-bold text-gray-900">{result.status}</p>
      </div>

      <div className="bg-purple-50 border-l-4 border-purple-500 p-4 rounded">
        <p className="font-semibold text-gray-700">Confidence</p>
        <div className="w-full bg-gray-300 rounded-full h-2 mt-2">
          <div
            className="bg-green-600 h-2 rounded-full"
            style={{ width: `${result.confidence * 100}%` }}
          />
        </div>
        <p className="text-sm text-gray-600 mt-2">{(result.confidence * 100).toFixed(1)}%</p>
      </div>

      <div className="bg-green-50 border-l-4 border-green-500 p-4 rounded">
        <p className="font-semibold text-gray-700">Description</p>
        <p className="text-gray-800 mt-2">{result.description}</p>
      </div>

      <div className="bg-red-50 border-l-4 border-red-500 p-4 rounded">
        <p className="font-semibold text-gray-700">Treatment</p>
        <p className="text-gray-800 mt-2">{result.treatment}</p>
      </div>

      <button
        onClick={() => speakText(result.treatment, selectedLanguage)}
        className="w-full px-4 py-2 bg-blue-600 text-white font-bold rounded-lg hover:bg-blue-700"
      >
        🔊 Speak Result
      </button>
    </div>
  </div>
);

// ============ Exports ============

export default CropDiseaseVisionApp;
