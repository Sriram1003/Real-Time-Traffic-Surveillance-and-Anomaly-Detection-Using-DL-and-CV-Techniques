// import React, { useRef, useState } from 'react';
// import { Upload, Play, RefreshCw, Check, AlertCircle } from 'lucide-react';
// // REMOVED: import { useAuth } ...
// // REMOVED: import { supabase } ... (Skipping DB save for anonymous usage)

// interface UploadPageProps {
//   onPageChange: (page: string) => void;
//   setAnalysisResults?: (results: any) => void; 
// }

// export const UploadPage: React.FC<UploadPageProps> = ({ onPageChange, setAnalysisResults }) => {
//   // REMOVED: const { user } = useAuth(); 
//   const fileInputRef = useRef<HTMLInputElement>(null);

//   const [videoFile, setVideoFile] = useState<File | null>(null);
//   const [videoPreview, setVideoPreview] = useState<string | null>(null);
  
//   const [isUploading, setIsUploading] = useState(false);
//   const [analysisStatus, setAnalysisStatus] = useState<'idle' | 'running' | 'completed' | 'error'>('idle');
//   const [statusMessage, setStatusMessage] = useState('');

//   const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
//     const file = e.target.files?.[0];
//     if (file) {
//       setVideoFile(file);
//       setVideoPreview(URL.createObjectURL(file));
//       setAnalysisStatus('idle');
//       setStatusMessage('');
//     }
//   };

//   const startServerAnalysis = async () => {
//     if (!videoFile) return;

//     setIsUploading(true);
//     setAnalysisStatus('running');
//     setStatusMessage('Uploading video to Python backend...');

//     const formData = new FormData();
//     formData.append('video', videoFile);

//     try {
//       setStatusMessage('Analysis running! Check the "Traffic Surveillance Output" popup window on your taskbar.');
      
//       const response = await fetch('http://127.0.0.1:8000/api/upload/', {
//         method: 'POST',
//         body: formData,
//       });

//       const data = await response.json();

//       if (response.ok) {
//         setAnalysisStatus('completed');
//         setStatusMessage('Analysis finished successfully.');
        
//         // --- 1. Pass Results to App State ---
//         if (data.results && setAnalysisResults) {
//             console.log("Received Results:", data.results);
//             setAnalysisResults(data.results);
//         }

//         // --- 2. Redirect to Results Page ---
//         setTimeout(() => {
//              onPageChange('results');
//         }, 1500);

//       } else {
//         throw new Error(data.message || 'Server error');
//       }
//     } catch (error) {
//       console.error('Analysis Error:', error);
//       setAnalysisStatus('error');
//       setStatusMessage(`Error: ${error instanceof Error ? error.message : 'Failed to connect'}. Is Django running?`);
//     } finally {
//       setIsUploading(false);
//     }
//   };

//   const resetUpload = () => {
//     setVideoFile(null);
//     setVideoPreview(null);
//     setAnalysisStatus('idle');
//     setStatusMessage('');
//     if (fileInputRef.current) fileInputRef.current.value = '';
//   };

//   return (
//     <div className="min-h-screen bg-gradient-to-b from-gray-50 to-white">
//       <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
//         <h1 className="text-4xl font-bold text-gray-900 mb-8">Video Upload & Detection</h1>

//         <div className="grid md:grid-cols-3 gap-8">
//           {/* Left Column: Video Preview */}
//           <div className="md:col-span-2">
//             <div className="bg-white rounded-lg shadow-lg overflow-hidden">
//               {videoFile && videoPreview ? (
//                 <div className="space-y-4 p-6">
//                   <div className="bg-black rounded-lg overflow-hidden relative">
//                     <video
//                       src={videoPreview}
//                       className="w-full h-auto max-h-96 opacity-80"
//                       controls
//                     />
//                     {analysisStatus === 'running' && (
//                       <div className="absolute inset-0 flex items-center justify-center bg-black/60 text-white">
//                         <div className="text-center p-4">
//                           <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-white mx-auto mb-4"></div>
//                           <p className="font-bold text-lg">Running AI Model...</p>
//                           <p className="text-sm text-gray-300">Check the popup window!</p>
//                         </div>
//                       </div>
//                     )}
//                   </div>

//                   <div className="flex gap-4">
//                     <button
//                       onClick={startServerAnalysis}
//                       disabled={isUploading || analysisStatus === 'running'}
//                       className={`flex items-center gap-2 px-6 py-2 rounded-lg font-semibold transition text-white
//                         ${isUploading ? 'bg-blue-400 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-700'}
//                       `}
//                     >
//                       <Play size={20} />
//                       {isUploading ? 'Processing...' : 'Start Python Analysis'}
//                     </button>

//                     <button
//                       onClick={resetUpload}
//                       disabled={isUploading}
//                       className="flex items-center gap-2 bg-gray-600 hover:bg-gray-700 text-white px-6 py-2 rounded-lg font-semibold transition"
//                     >
//                       <RefreshCw size={20} />
//                       Reset
//                     </button>
//                   </div>

//                   {statusMessage && (
//                     <div className={`border rounded-lg p-4 mt-4 
//                       ${analysisStatus === 'error' ? 'bg-red-50 border-red-200 text-red-800' : 
//                         analysisStatus === 'completed' ? 'bg-green-50 border-green-200 text-green-800' : 
//                         'bg-blue-50 border-blue-200 text-blue-800'}`}>
//                       <div className="flex items-start gap-3">
//                         {analysisStatus === 'error' ? <AlertCircle size={20} /> : <Check size={20} />}
//                         <p>{statusMessage}</p>
//                       </div>
//                     </div>
//                   )}
//                 </div>
//               ) : (
//                 <div
//                   onClick={() => fileInputRef.current?.click()}
//                   className="p-12 text-center cursor-pointer hover:bg-gray-50 transition min-h-[400px] flex flex-col justify-center"
//                 >
//                   <Upload className="mx-auto mb-4 text-gray-400" size={48} />
//                   <p className="text-xl font-semibold text-gray-900 mb-2">Upload Traffic Video</p>
//                   <p className="text-gray-600">Click to select MP4/WebM file</p>
//                 </div>
//               )}
//               <input ref={fileInputRef} type="file" accept="video/*" onChange={handleFileUpload} className="hidden" />
//             </div>
//           </div>
          
//           {/* Instructions Column */}
//           <div className="md:col-span-1">
//             <div className="bg-white rounded-lg shadow-lg p-6 sticky top-8">
//               <h2 className="text-2xl font-bold text-gray-900 mb-6">How it Works</h2>
//               <div className="space-y-6 text-gray-600">
//                 <p>1. Upload Video</p>
//                 <p>2. Start Python Analysis</p>
//                 <p>3. View Results</p>
//               </div>
//             </div>
//           </div>
//         </div>
//       </div>
//     </div>
//   );
// };
//-------------------------------------------------------------------------------------------------------------------
// import React, { useRef, useState } from 'react';
// import { Upload, Play, RefreshCw, Check, AlertCircle } from 'lucide-react';

// interface UploadPageProps {
//   onPageChange: (page: string) => void;
//   setAnalysisResults?: (results: any) => void; 
// }

// export const UploadPage: React.FC<UploadPageProps> = ({ onPageChange, setAnalysisResults }) => {
//   const fileInputRef = useRef<HTMLInputElement>(null);

//   const [videoFile, setVideoFile] = useState<File | null>(null);
//   const [videoPreview, setVideoPreview] = useState<string | null>(null);
  
//   const [isUploading, setIsUploading] = useState(false);
//   const [analysisStatus, setAnalysisStatus] = useState<'idle' | 'running' | 'completed' | 'error'>('idle');
//   const [statusMessage, setStatusMessage] = useState('');

//   const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
//     const file = e.target.files?.[0];
//     if (file) {
//       setVideoFile(file);
//       setVideoPreview(URL.createObjectURL(file));
//       setAnalysisStatus('idle');
//       setStatusMessage('');
//     }
//   };

//   const startServerAnalysis = async () => {
//     if (!videoFile) return;

//     setIsUploading(true);
//     setAnalysisStatus('running');
//     setStatusMessage('Uploading video to Python backend...');

//     const formData = new FormData();
//     formData.append('video', videoFile);

//     try {
//       setStatusMessage('Processing... Check the Python window on your taskbar.');
      
//       const response = await fetch('http://127.0.0.1:8000/api/upload/', {
//         method: 'POST',
//         body: formData,
//       });

//       const data = await response.json();

//       if (response.ok) {
//         setAnalysisStatus('completed');
//         setStatusMessage('Analysis finished successfully.');
        
//         // Pass results to App.tsx
//         if (data.results && setAnalysisResults) {
//             console.log("Received Results:", data.results);
//             setAnalysisResults(data.results);
//         }

//         // Redirect to results page
//         setTimeout(() => {
//              onPageChange('results');
//         }, 1500);

//       } else {
//         throw new Error(data.message || 'Server error');
//       }
//     } catch (error) {
//       console.error('Analysis Error:', error);
//       setAnalysisStatus('error');
//       setStatusMessage(`Error: ${error instanceof Error ? error.message : 'Failed to connect'}. Is Django running?`);
//     } finally {
//       setIsUploading(false);
//     }
//   };

//   const resetUpload = () => {
//     setVideoFile(null);
//     setVideoPreview(null);
//     setAnalysisStatus('idle');
//     setStatusMessage('');
//     if (fileInputRef.current) fileInputRef.current.value = '';
//   };

//   return (
//     <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
//       <h1 className="text-3xl font-bold text-gray-900 mb-8">Video Upload Detection</h1>

//       <div className="grid md:grid-cols-3 gap-8">
//         <div className="md:col-span-2">
//           <div className="bg-white rounded-lg shadow-lg overflow-hidden">
//             {videoFile && videoPreview ? (
//               <div className="space-y-4 p-6">
//                 <div className="bg-black rounded-lg overflow-hidden relative">
//                   <video
//                     src={videoPreview}
//                     className="w-full h-auto max-h-96 opacity-80"
//                     controls
//                   />
//                   {analysisStatus === 'running' && (
//                     <div className="absolute inset-0 flex items-center justify-center bg-black/60 text-white">
//                       <div className="text-center p-4">
//                         <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-white mx-auto mb-4"></div>
//                         <p className="font-bold text-lg">Running AI Model...</p>
//                       </div>
//                     </div>
//                   )}
//                 </div>

//                 <div className="flex gap-4">
//                   <button
//                     onClick={startServerAnalysis}
//                     disabled={isUploading || analysisStatus === 'running'}
//                     className={`flex items-center gap-2 px-6 py-2 rounded-lg font-semibold transition text-white
//                       ${isUploading ? 'bg-blue-400 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-700'}
//                     `}
//                   >
//                     <Play size={20} />
//                     {isUploading ? 'Processing...' : 'Start Python Analysis'}
//                   </button>

//                   <button
//                     onClick={resetUpload}
//                     disabled={isUploading}
//                     className="flex items-center gap-2 bg-gray-600 hover:bg-gray-700 text-white px-6 py-2 rounded-lg font-semibold transition"
//                   >
//                     <RefreshCw size={20} />
//                     Reset
//                   </button>
//                 </div>

//                 {statusMessage && (
//                   <div className={`border rounded-lg p-4 mt-4 
//                     ${analysisStatus === 'error' ? 'bg-red-50 border-red-200 text-red-800' : 
//                       analysisStatus === 'completed' ? 'bg-green-50 border-green-200 text-green-800' : 
//                       'bg-blue-50 border-blue-200 text-blue-800'}`}>
//                     <div className="flex items-start gap-3">
//                       {analysisStatus === 'error' ? <AlertCircle size={20} /> : <Check size={20} />}
//                       <p>{statusMessage}</p>
//                     </div>
//                   </div>
//                 )}
//               </div>
//             ) : (
//               <div
//                 onClick={() => fileInputRef.current?.click()}
//                 className="p-12 text-center cursor-pointer hover:bg-gray-50 transition min-h-[400px] flex flex-col justify-center"
//               >
//                 <Upload className="mx-auto mb-4 text-gray-400" size={48} />
//                 <p className="text-xl font-semibold text-gray-900 mb-2">Upload Traffic Video</p>
//                 <p className="text-gray-600">Click to select MP4/WebM file</p>
//               </div>
//             )}
//             <input ref={fileInputRef} type="file" accept="video/*" onChange={handleFileUpload} className="hidden" />
//           </div>
//         </div>
        
//         <div className="md:col-span-1">
//           <div className="bg-white rounded-lg shadow-lg p-6 sticky top-24">
//             <h2 className="text-2xl font-bold text-gray-900 mb-6">How it Works</h2>
//             <div className="space-y-4 text-gray-600">
//               <p>1. Upload Video or Select Live Camera.</p>
//               <p>2. Wait for Python to process the frames.</p>
//               <p>3. View detailed analytics in the Results tab.</p>
//             </div>
//           </div>
//         </div>
//       </div>
//     </div>
//   );
// };
//-----------------------------------------------------------------------------------------------------
import React, { useRef, useState } from 'react';
import { UploadCloud, Play, RefreshCw, CheckCircle, AlertCircle, Film, ArrowRight } from 'lucide-react';

interface UploadPageProps {
  onPageChange: (page: string) => void;
  setAnalysisResults: (results: any) => void; 
}

export const UploadPage: React.FC<UploadPageProps> = ({ onPageChange, setAnalysisResults }) => {
  const fileInputRef = useRef<HTMLInputElement>(null);

  const [videoFile, setVideoFile] = useState<File | null>(null);
  const [videoPreview, setVideoPreview] = useState<string | null>(null);
  
  const [isUploading, setIsUploading] = useState(false);
  const [analysisStatus, setAnalysisStatus] = useState<'idle' | 'running' | 'completed' | 'error'>('idle');
  const [statusMessage, setStatusMessage] = useState('');

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setVideoFile(file);
      setVideoPreview(URL.createObjectURL(file));
      setAnalysisStatus('idle');
      setStatusMessage('');
    }
  };

  const startServerAnalysis = async () => {
    if (!videoFile) return;

    setIsUploading(true);
    setAnalysisStatus('running');
    setStatusMessage('Uploading and processing... This may take a few minutes depending on video length.');

    const formData = new FormData();
    formData.append('video', videoFile);

    try {
      const response = await fetch('http://127.0.0.1:8000/api/upload/', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (response.ok) {
        setAnalysisStatus('completed');
        setStatusMessage('Analysis finished successfully!');
        
        // Pass results safely to App.tsx
        if (data.results) {
            setAnalysisResults(data.results);
        } else {
            setAnalysisResults({ total_vehicles_detected: 'Unknown (No data returned)' });
        }

        // Redirect to results page after a brief delay
        setTimeout(() => {
             onPageChange('results');
        }, 1500);

      } else {
        throw new Error(data.message || 'Server error occurred');
      }
    } catch (error) {
      console.error('Analysis Error:', error);
      setAnalysisStatus('error');
      setStatusMessage(`Error: ${error instanceof Error ? error.message : 'Failed to connect'}. Ensure Django is running.`);
    } finally {
      setIsUploading(false);
    }
  };

  const resetUpload = () => {
    setVideoFile(null);
    setVideoPreview(null);
    setAnalysisStatus('idle');
    setStatusMessage('');
    if (fileInputRef.current) fileInputRef.current.value = '';
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="mb-8">
        <h1 className="text-3xl font-extrabold text-slate-900 tracking-tight">Offline Video Analysis</h1>
        <p className="text-slate-500 mt-2">Upload pre-recorded CCTV footage for high-fidelity YOLOv8 Medium processing.</p>
      </div>

      <div className="grid lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 space-y-6">
          <div className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden transition-all">
            {videoFile && videoPreview ? (
              <div className="p-6">
                <div className="bg-slate-900 rounded-xl overflow-hidden relative shadow-inner">
                  <video src={videoPreview} className="w-full h-auto max-h-[450px] opacity-90" controls />
                  
                  {analysisStatus === 'running' && (
                    <div className="absolute inset-0 flex items-center justify-center bg-slate-900/80 backdrop-blur-sm text-white">
                      <div className="text-center p-6 bg-slate-800/50 rounded-2xl border border-slate-700 shadow-2xl">
                        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
                        <p className="font-bold text-lg tracking-wide">Analyzing Frames...</p>
                        <p className="text-sm text-slate-300 mt-2 max-w-xs">Our AI is scanning for vehicles, helmets, speeds, and license plates.</p>
                      </div>
                    </div>
                  )}
                </div>

                <div className="flex flex-wrap gap-4 mt-6">
                  <button
                    onClick={startServerAnalysis}
                    disabled={isUploading || analysisStatus === 'running'}
                    className={`flex-1 flex justify-center items-center gap-2 px-6 py-3 rounded-xl font-bold transition-all shadow-sm text-white
                      ${isUploading ? 'bg-blue-400 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-700 hover:shadow-md'}
                    `}
                  >
                    <Play size={20} fill="currentColor" />
                    {isUploading ? 'Processing...' : 'Start AI Analysis'}
                  </button>

                  <button
                    onClick={resetUpload}
                    disabled={isUploading}
                    className="flex items-center gap-2 bg-slate-100 hover:bg-slate-200 text-slate-700 px-6 py-3 rounded-xl font-bold transition-all"
                  >
                    <RefreshCw size={20} /> Reset
                  </button>
                </div>
              </div>
            ) : (
              <div
                onClick={() => fileInputRef.current?.click()}
                className="p-16 text-center cursor-pointer hover:bg-blue-50/50 transition-colors border-2 border-dashed border-slate-200 hover:border-blue-400 m-6 rounded-2xl flex flex-col items-center justify-center min-h-[400px]"
              >
                <div className="bg-blue-100 text-blue-600 p-4 rounded-full mb-4">
                  <UploadCloud size={40} />
                </div>
                <h3 className="text-xl font-bold text-slate-900 mb-2">Select a Video File</h3>
                <p className="text-slate-500 max-w-sm">Drag and drop or click to upload MP4, WebM, or AVI files from your local storage.</p>
              </div>
            )}
            <input ref={fileInputRef} type="file" accept="video/*" onChange={handleFileUpload} className="hidden" />
          </div>

          {/* Status Message */}
          {statusMessage && (
            <div className={`p-4 rounded-xl border flex items-start gap-3 animate-fade-in-up
              ${analysisStatus === 'error' ? 'bg-red-50 border-red-200 text-red-800' : 
                analysisStatus === 'completed' ? 'bg-emerald-50 border-emerald-200 text-emerald-800' : 
                'bg-blue-50 border-blue-200 text-blue-800'}`}>
              {analysisStatus === 'error' ? <AlertCircle className="shrink-0" /> : 
               analysisStatus === 'completed' ? <CheckCircle className="shrink-0" /> : 
               <RefreshCw className="shrink-0 animate-spin" />}
              <p className="font-medium">{statusMessage}</p>
            </div>
          )}
        </div>
        
        {/* Info Sidebar */}
        <div className="lg:col-span-1">
          <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-6 sticky top-24">
            <h2 className="text-xl font-bold text-slate-900 mb-6 flex items-center gap-2">
              <Film className="text-blue-500" /> Instructions
            </h2>
            <ul className="space-y-6">
              <li className="flex gap-4">
                <div className="bg-blue-100 text-blue-700 font-bold w-8 h-8 rounded-full flex items-center justify-center shrink-0">1</div>
                <div>
                  <p className="font-semibold text-slate-900">Upload Footage</p>
                  <p className="text-sm text-slate-500 mt-1">Select a clear CCTV or drone footage file from your computer.</p>
                </div>
              </li>
              <li className="flex gap-4">
                <div className="bg-blue-100 text-blue-700 font-bold w-8 h-8 rounded-full flex items-center justify-center shrink-0">2</div>
                <div>
                  <p className="font-semibold text-slate-900">Run Analysis</p>
                  <p className="text-sm text-slate-500 mt-1">The server will process the video frame-by-frame. A popup window may appear.</p>
                </div>
              </li>
              <li className="flex gap-4">
                <div className="bg-blue-100 text-blue-700 font-bold w-8 h-8 rounded-full flex items-center justify-center shrink-0">3</div>
                <div>
                  <p className="font-semibold text-slate-900">Review Results</p>
                  <p className="text-sm text-slate-500 mt-1">Automatically redirect to the dashboard to view the generated statistics.</p>
                </div>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};