// import React, { useState } from 'react';
// import { Youtube, StopCircle, Play, AlertTriangle } from 'lucide-react';

// export const LivePage: React.FC = () => {
//   const [isStreaming, setIsStreaming] = useState(false);
  
//   // This points to your Django Backend Live Feed
//   const STREAM_URL = "http://127.0.0.1:8000/api/live_feed/"; 

//   return (
//     <div className="max-w-7xl mx-auto px-4 py-8">
//       <h1 className="text-3xl font-bold text-gray-900 mb-6 flex items-center gap-2">
//         <Youtube className="text-red-600" size={32} /> Live Traffic Surveillance
//       </h1>

//       <div className="grid md:grid-cols-3 gap-8">
//         {/* Main Video Feed Area */}
//         <div className="md:col-span-2">
//           <div className="bg-black rounded-xl shadow-2xl overflow-hidden aspect-video relative flex items-center justify-center border-4 border-gray-900">
//             {isStreaming ? (
//               <img 
//                 src={STREAM_URL} 
//                 alt="Live Processing Feed" 
//                 className="w-full h-full object-contain"
//               />
//             ) : (
//               <div className="text-center p-8">
//                 <Youtube className="mx-auto h-20 w-20 text-gray-600 mb-4" />
//                 <h3 className="text-xl font-bold text-gray-300">Feed Offline</h3>
//                 <p className="text-gray-500">Click connect to start the YouTube Live Stream</p>
//               </div>
//             )}
//           </div>

//           <div className="mt-6 flex justify-center">
//             {!isStreaming ? (
//               <button 
//                 onClick={() => setIsStreaming(true)}
//                 className="flex items-center gap-3 bg-red-600 hover:bg-red-700 text-white px-8 py-3 rounded-full font-bold text-lg shadow-lg transition transform hover:scale-105"
//               >
//                 <Play fill="currentColor" /> Connect Live Feed
//               </button>
//             ) : (
//               <button 
//                 onClick={() => setIsStreaming(false)}
//                 className="flex items-center gap-3 bg-gray-700 hover:bg-gray-800 text-white px-8 py-3 rounded-full font-bold text-lg shadow-lg transition"
//               >
//                 <StopCircle /> Stop Processing
//               </button>
//             )}
//           </div>
//         </div>

//         {/* Info Panel */}
//         <div className="md:col-span-1 space-y-4">
//           <div className="bg-white p-6 rounded-xl shadow-lg border border-gray-100">
//             <h2 className="font-bold text-xl mb-4 text-gray-800">Stream Info</h2>
//             <div className="space-y-3 text-sm">
//               <div className="flex justify-between border-b pb-2">
//                 <span className="text-gray-500">Source</span>
//                 <span className="font-semibold text-red-600">YouTube Live</span>
//               </div>
//               <div className="flex justify-between border-b pb-2">
//                 <span className="text-gray-500">Status</span>
//                 <span className={`font-semibold ${isStreaming ? 'text-green-600' : 'text-gray-400'}`}>
//                   {isStreaming ? 'Online • Processing' : 'Offline'}
//                 </span>
//               </div>
//             </div>
            
//             <div className="mt-6 bg-yellow-50 p-4 rounded-lg border border-yellow-200">
//                 <div className="flex items-center gap-2 text-yellow-800 font-bold mb-1">
//                     <AlertTriangle size={16} /> Note:
//                 </div>
//                 <p className="text-xs text-yellow-700">
//                     There is a 5-10 second delay while the server downloads and processes the YouTube stream.
//                 </p>
//             </div>
//           </div>
//         </div>
//       </div>
//     </div>
//   );
// };
//--------------------------------------------------------------------------------------------------------
import React, { useState } from 'react';
import { Activity, Wifi, WifiOff, Camera, AlertTriangle, ShieldCheck, CheckCircle } from 'lucide-react'; // <-- FIX: Added CheckCircle here

export const LivePage: React.FC = () => {
  const [isStreaming, setIsStreaming] = useState(false);
  
  // Django Backend Live Feed Endpoint
  const STREAM_URL = "http://127.0.0.1:8000/api/live_feed/"; 

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 animate-fade-in-up">
      <div className="flex justify-between items-end mb-8">
        <div>
          <h1 className="text-3xl font-extrabold text-slate-900 tracking-tight flex items-center gap-3">
            <span className="relative flex h-4 w-4">
              <span className={`animate-ping absolute inline-flex h-full w-full rounded-full opacity-75 ${isStreaming ? 'bg-red-500' : 'bg-slate-400'}`}></span>
              <span className={`relative inline-flex rounded-full h-4 w-4 ${isStreaming ? 'bg-red-600' : 'bg-slate-500'}`}></span>
            </span>
            Live Operations Center
          </h1>
          <p className="text-slate-500 mt-2">Real-time object detection and tracking via high-speed YOLOv8 Nano.</p>
        </div>
      </div>

      <div className="grid lg:grid-cols-4 gap-8">
        {/* Main Feed */}
        <div className="lg:col-span-3">
          <div className="bg-slate-900 rounded-2xl shadow-xl overflow-hidden border border-slate-800 relative">
            
            {/* Top Bar of the Camera View */}
            <div className="absolute top-0 left-0 w-full p-4 flex justify-between items-center z-10 bg-gradient-to-b from-black/60 to-transparent">
              <div className="flex items-center gap-2 text-white/90 text-sm font-mono tracking-wider">
                <Camera size={16} /> CAM-01 (YOUTUBE-STREAM)
              </div>
              <div className="text-white/90 text-sm font-mono tracking-wider">
                {new Date().toLocaleTimeString()}
              </div>
            </div>

            <div className="aspect-video bg-black flex items-center justify-center">
              {isStreaming ? (
                <img 
                  src={STREAM_URL} 
                  alt="Live Processing Feed" 
                  className="w-full h-full object-contain"
                  onError={(e) => {
                    // Fallback if the connection drops
                    (e.target as HTMLImageElement).style.display = 'none';
                    setIsStreaming(false);
                    alert("Stream disconnected. Please ensure Django is running.");
                  }}
                />
              ) : (
                <div className="text-center p-8">
                  <WifiOff className="mx-auto h-16 w-16 text-slate-600 mb-4" />
                  <h3 className="text-2xl font-bold text-slate-400">Stream Inactive</h3>
                  <p className="text-slate-500 mt-2">Connect to the live feed to begin processing.</p>
                </div>
              )}
            </div>
          </div>

          <div className="mt-8 flex justify-center">
            {!isStreaming ? (
              <button 
                onClick={() => setIsStreaming(true)}
                className="flex items-center justify-center gap-2 bg-red-500 hover:bg-red-600 text-white px-10 py-4 rounded-full font-bold text-lg shadow-lg shadow-red-500/30 transition-transform hover:-translate-y-1 w-full max-w-md"
              >
                <Wifi size={24} /> Initialize Live Connection
              </button>
            ) : (
              <button 
                onClick={() => setIsStreaming(false)}
                className="flex items-center justify-center gap-2 bg-slate-800 hover:bg-slate-900 text-white px-10 py-4 rounded-full font-bold text-lg shadow-lg transition-transform hover:-translate-y-1 w-full max-w-md"
              >
                <WifiOff size={24} /> Terminate Connection
              </button>
            )}
          </div>
        </div>

        {/* Side Panel Stats */}
        <div className="lg:col-span-1 space-y-6">
          <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-6">
            <h2 className="font-bold text-lg text-slate-900 mb-4 flex items-center gap-2">
              <Activity className="text-blue-500" size={20} /> System Status
            </h2>
            <div className="space-y-4 text-sm">
              <div className="flex justify-between items-center border-b border-slate-100 pb-3">
                <span className="text-slate-500">Core Model</span>
                <span className="font-semibold text-slate-900 bg-slate-100 px-2 py-1 rounded">YOLOv8 Nano</span>
              </div>
              <div className="flex justify-between items-center border-b border-slate-100 pb-3">
                <span className="text-slate-500">Sub Model</span>
                <span className="font-semibold text-slate-900 bg-slate-100 px-2 py-1 rounded">Helmet-PT</span>
              </div>
              <div className="flex justify-between items-center pt-1">
                <span className="text-slate-500">Network State</span>
                <span className={`font-bold flex items-center gap-1 ${isStreaming ? 'text-emerald-500' : 'text-slate-400'}`}>
                  {isStreaming ? <><div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></div> Receiving</> : 'Disconnected'}
                </span>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-6">
            <h2 className="font-bold text-lg text-slate-900 mb-4 flex items-center gap-2">
              <ShieldCheck className="text-indigo-500" size={20} /> Active Modules
            </h2>
            <ul className="space-y-3 text-sm text-slate-600 font-medium">
              <li className="flex items-center gap-2"><CheckCircle size={16} className="text-emerald-500"/> Vehicle Tracking</li>
              <li className="flex items-center gap-2"><CheckCircle size={16} className="text-emerald-500"/> Speed Estimation</li>
              <li className="flex items-center gap-2"><CheckCircle size={16} className="text-emerald-500"/> Triple Riding Check</li>
              <li className="flex items-center gap-2"><CheckCircle size={16} className="text-emerald-500"/> Helmet Detection</li>
              <li className="flex items-center gap-2"><CheckCircle size={16} className="text-emerald-500"/> License Plate OCR</li>
            </ul>
          </div>

          {/* Warning Note */}
          <div className="bg-amber-50 rounded-2xl p-5 border border-amber-200">
            <div className="flex items-center gap-2 text-amber-800 font-bold mb-2">
              <AlertTriangle size={18} /> Latency Warning
            </div>
            <p className="text-sm text-amber-700 leading-relaxed">
              Initial connection takes 5-10 seconds to buffer. The feed runs at ~30 FPS depending on your CPU capabilities.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};