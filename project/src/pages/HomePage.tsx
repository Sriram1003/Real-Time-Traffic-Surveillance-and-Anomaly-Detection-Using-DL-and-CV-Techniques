// import React from 'react';
// import { useAuth } from '../context/AuthContext';
// import { Activity, BarChart3, Zap } from 'lucide-react';

// interface HomePageProps {
//   onPageChange: (page: string) => void;
// }

// export const HomePage: React.FC<HomePageProps> = ({ onPageChange }) => {
//   const { user } = useAuth();

//   return (
//     <div className="min-h-screen bg-gradient-to-b from-white to-gray-50">
//       <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
//         <div className="text-center mb-16">
//           <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6">
//             Real-Time Traffic Surveillance
//           </h1>
//           <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
//             Advanced AI-powered system for detecting, tracking, and analyzing vehicles in traffic streams. Get instant insights with deep learning and computer vision.
//           </p>
//           {user ? (
//             <button
//               onClick={() => onPageChange('upload')}
//               className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 rounded-lg font-semibold text-lg transition"
//             >
//               Start Surveillance
//             </button>
//           ) : (
//             <div className="flex gap-4 justify-center flex-wrap">
//               <button
//                 onClick={() => onPageChange('login')}
//                 className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 rounded-lg font-semibold text-lg transition"
//               >
//                 Login
//               </button>
//               <button
//                 onClick={() => onPageChange('signup')}
//                 className="bg-gray-800 hover:bg-gray-900 text-white px-8 py-3 rounded-lg font-semibold text-lg transition"
//               >
//                 Sign Up
//               </button>
//             </div>
//           )}
//         </div>

//         <div className="grid md:grid-cols-3 gap-8">
//           <div className="bg-white rounded-lg p-8 shadow-lg hover:shadow-xl transition">
//             <div className="text-blue-600 mb-4">
//               <Activity size={40} />
//             </div>
//             <h3 className="text-xl font-bold text-gray-900 mb-3">Real-Time Detection</h3>
//             <p className="text-gray-600">
//               Detect and classify vehicles in real-time using advanced YOLOv7 deep learning models.
//             </p>
//           </div>

//           <div className="bg-white rounded-lg p-8 shadow-lg hover:shadow-xl transition">
//             <div className="text-green-600 mb-4">
//               <BarChart3 size={40} />
//             </div>
//             <h3 className="text-xl font-bold text-gray-900 mb-3">Analytics & Stats</h3>
//             <p className="text-gray-600">
//               Get detailed statistics on vehicle counts, speeds, and helmet detection results.
//             </p>
//           </div>

//           <div className="bg-white rounded-lg p-8 shadow-lg hover:shadow-xl transition">
//             <div className="text-purple-600 mb-4">
//               <Zap size={40} />
//             </div>
//             <h3 className="text-xl font-bold text-gray-900 mb-3">Fast Processing</h3>
//             <p className="text-gray-600">
//               Process video streams with near real-time inference for instant results and insights.
//             </p>
//           </div>
//         </div>

//         <div className="mt-20 bg-gradient-to-r from-blue-600 to-blue-700 rounded-lg p-12 text-white">
//           <h2 className="text-3xl font-bold mb-4">Supported Features</h2>
//           <div className="grid md:grid-cols-2 gap-6">
//             <div>
//               <ul className="space-y-3">
//                 <li className="flex items-center gap-3">
//                   <span className="text-blue-300">✓</span> Vehicle Detection & Classification
//                 </li>
//                 <li className="flex items-center gap-3">
//                   <span className="text-blue-300">✓</span> Real-Time Vehicle Counting
//                 </li>
//                 <li className="flex items-center gap-3">
//                   <span className="text-blue-300">✓</span> Speed Estimation
//                 </li>
//               </ul>
//             </div>
//             <div>
//               <ul className="space-y-3">
//                 <li className="flex items-center gap-3">
//                   <span className="text-blue-300">✓</span> Helmet Detection
//                 </li>
//                 <li className="flex items-center gap-3">
//                   <span className="text-blue-300">✓</span> Video Upload & Processing
//                 </li>
//                 <li className="flex items-center gap-3">
//                   <span className="text-blue-300">✓</span> Historical Results Tracking
//                 </li>
//               </ul>
//             </div>
//           </div>
//         </div>
//       </section>
//     </div>
//   );
// };
//-----------------------------------------------------------------------------------------------------
import React from 'react';
import { Video, UploadCloud, ShieldAlert, Zap, Users, Camera } from 'lucide-react';

interface HomePageProps {
  onNavigate: (page: string) => void;
}

export const HomePage: React.FC<HomePageProps> = ({ onNavigate }) => {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      
      {/* Hero Section */}
      <div className="text-center max-w-3xl mx-auto mb-16 mt-8">
        <h1 className="text-5xl font-extrabold text-slate-900 tracking-tight mb-6 leading-tight">
          Next-Generation <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-indigo-600">Traffic Surveillance</span>
        </h1>
        <p className="text-xl text-slate-600 mb-10 leading-relaxed">
          Powered by state-of-the-art YOLOv8 AI. Automatically detect vehicle speeds, helmet violations, license plates, and triple-riding in real-time.
        </p>
        
        <div className="flex flex-col sm:flex-row justify-center gap-4">
          <button 
            onClick={() => onNavigate('live')}
            className="flex items-center justify-center gap-2 bg-red-500 hover:bg-red-600 text-white px-8 py-4 rounded-xl font-bold text-lg transition-transform hover:-translate-y-1 shadow-lg shadow-red-500/30"
          >
            <Video size={24} />
            Start Live Surveillance
          </button>
          
          <button 
            onClick={() => onNavigate('upload')}
            className="flex items-center justify-center gap-2 bg-white hover:bg-slate-50 text-slate-900 border-2 border-slate-200 px-8 py-4 rounded-xl font-bold text-lg transition-transform hover:-translate-y-1 shadow-sm"
          >
            <UploadCloud size={24} className="text-blue-600" />
            Analyze Recorded Video
          </button>
        </div>
      </div>

      {/* Features Grid */}
      <div className="mt-24 mb-12">
        <div className="flex items-center justify-between mb-8">
          <h2 className="text-2xl font-bold text-slate-900">System Capabilities</h2>
          <span className="text-sm font-semibold tracking-wider text-blue-600 uppercase bg-blue-50 px-3 py-1 rounded-full">Core Features</span>
        </div>
        
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          <FeatureCard 
            icon={<Users className="text-indigo-500" size={32} />}
            title="Triple Riding Alert"
            description="Utilizes spatial overlap logic to accurately detect when 3 or more individuals are riding a single motorcycle."
          />
          <FeatureCard 
            icon={<ShieldAlert className="text-red-500" size={32} />}
            title="Helmet Detection"
            description="Secondary custom YOLOv8 model isolates motorcycle riders to verify the presence of safety helmets."
          />
          <FeatureCard 
            icon={<Zap className="text-amber-500" size={32} />}
            title="Speed Estimation"
            description="Dynamic pixel-per-meter (PPM) scaling calculates vehicle speed across consecutive frames."
          />
          <FeatureCard 
            icon={<Camera className="text-emerald-500" size={32} />}
            title="ALPR (EasyOCR)"
            description="Automated License Plate Recognition kicks in for close-range vehicles to capture violator details."
          />
        </div>
      </div>

      {/* Tech Stack Banner */}
      <div className="mt-16 bg-slate-900 rounded-2xl p-8 sm:p-12 text-center text-white shadow-2xl relative overflow-hidden">
        <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-blue-500 via-indigo-500 to-purple-500"></div>
        <h3 className="text-2xl font-bold mb-4">Built for High Performance</h3>
        <p className="text-slate-300 max-w-2xl mx-auto">
          The backend runs on Django and OpenCV, utilizing YOLOv8 Nano for real-time 30FPS processing, and YOLOv8 Medium for high-fidelity offline video analysis.
        </p>
      </div>

    </div>
  );
};

// Reusable Feature Card Component
const FeatureCard = ({ icon, title, description }: { icon: React.ReactNode, title: string, description: string }) => (
  <div className="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm hover:shadow-xl transition-all duration-300 hover:-translate-y-1 group">
    <div className="bg-slate-50 w-16 h-16 rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
      {icon}
    </div>
    <h3 className="text-lg font-bold text-slate-900 mb-2">{title}</h3>
    <p className="text-slate-600 text-sm leading-relaxed">
      {description}
    </p>
  </div>
);