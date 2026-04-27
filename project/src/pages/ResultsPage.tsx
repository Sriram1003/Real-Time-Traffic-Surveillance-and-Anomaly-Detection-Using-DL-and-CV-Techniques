// import React, { useEffect, useState } from 'react';
// import { useAuth } from '../context/AuthContext';
// import { supabase } from '../lib/supabase';
// import { Trash2 } from 'lucide-react';

// interface DetectionResult {
//   id: string;
//   video_name: string;
//   total_vehicles: number;
//   detection_metrics: Record<string, number>;
//   created_at: string;
// }

// interface ResultsPageProps {
//   results?: DetectionResult[] | null;
// }

// export const ResultsPage: React.FC<ResultsPageProps> = ({ results: passedResults }) => {
//   const { user } = useAuth();
//   const [results, setResults] = useState<DetectionResult[]>(passedResults || []);
//   const [loading, setLoading] = useState(!passedResults);
//   const [error, setError] = useState('');

//   useEffect(() => {
//     // Only fetch if no results were passed as props
//     if (passedResults) return;

//     const fetchResults = async () => {
//       if (!user) return;

//       setLoading(true);
//       const { data, error: fetchError } = await supabase
//         .from('detection_results')
//         .select('*')
//         .eq('user_id', user.id)
//         .order('created_at', { ascending: false });

//       if (fetchError) {
//         setError('Failed to load results');
//       } else {
//         setResults((data as DetectionResult[]) || []);
//       }
//       setLoading(false);
//     };

//     fetchResults();
//   }, [user, passedResults]);

//   const deleteResult = async (id: string) => {
//     const { error } = await supabase
//       .from('detection_results')
//       .delete()
//       .eq('id', id);

//     if (!error) {
//       setResults((prev) => prev.filter((r) => r.id !== id));
//     }
//   };

//   if (loading) {
//     return (
//       <div className="min-h-screen bg-gray-50 flex items-center justify-center">
//         <div className="text-center">
//           <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
//           <p className="text-gray-600">Loading results...</p>
//         </div>
//       </div>
//     );
//   }

//   return (
//     <div className="min-h-screen bg-gradient-to-b from-gray-50 to-white">
//       <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
//         <h1 className="text-4xl font-bold text-gray-900 mb-8">Detection Results</h1>

//         {error && (
//           <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6 text-red-800">
//             {error}
//           </div>
//         )}

//         {results.length === 0 ? (
//           <div className="bg-white rounded-lg shadow-lg p-12 text-center">
//             <p className="text-gray-600 text-lg">No detection results yet. Upload a video to get started!</p>
//           </div>
//         ) : (
//           <div className="grid gap-6">
//             {results.map((result) => (
//               <div key={result.id} className="bg-white rounded-lg shadow-lg p-6 hover:shadow-xl transition">
//                 <div className="flex justify-between items-start mb-4">
//                   <div>
//                     <h3 className="text-2xl font-bold text-gray-900">{result.video_name}</h3>
//                     <p className="text-gray-600 text-sm">
//                       {new Date(result.created_at).toLocaleDateString()} at{' '}
//                       {new Date(result.created_at).toLocaleTimeString()}
//                     </p>
//                   </div>
//                   <button
//                     onClick={() => deleteResult(result.id)}
//                     className="text-red-600 hover:text-red-800 transition"
//                   >
//                     <Trash2 size={24} />
//                   </button>
//                 </div>

//                 <div className="grid md:grid-cols-5 gap-4 mt-6">
//                   <div className="bg-gradient-to-br from-blue-50 to-blue-100 rounded-lg p-4">
//                     <p className="text-gray-700 text-sm font-medium">Total Vehicles</p>
//                     <p className="text-3xl font-bold text-blue-600 mt-2">{result.total_vehicles}</p>
//                   </div>

//                   <div className="bg-gradient-to-br from-green-50 to-green-100 rounded-lg p-4">
//                     <p className="text-gray-700 text-sm font-medium">Cars</p>
//                     <p className="text-3xl font-bold text-green-600 mt-2">
//                       {result.detection_metrics?.cars ?? 0}
//                     </p>
//                   </div>

//                   <div className="bg-gradient-to-br from-yellow-50 to-yellow-100 rounded-lg p-4">
//                     <p className="text-gray-700 text-sm font-medium">Bikes</p>
//                     <p className="text-3xl font-bold text-yellow-600 mt-2">
//                       {result.detection_metrics?.bikes ?? 0}
//                     </p>
//                   </div>

//                   <div className="bg-gradient-to-br from-red-50 to-red-100 rounded-lg p-4">
//                     <p className="text-gray-700 text-sm font-medium">Trucks</p>
//                     <p className="text-3xl font-bold text-red-600 mt-2">
//                       {result.detection_metrics?.trucks ?? 0}
//                     </p>
//                   </div>

//                   <div className="bg-gradient-to-br from-purple-50 to-purple-100 rounded-lg p-4">
//                     <p className="text-gray-700 text-sm font-medium">Buses</p>
//                     <p className="text-3xl font-bold text-purple-600 mt-2">
//                       {result.detection_metrics?.buses ?? 0}
//                     </p>
//                   </div>
//                 </div>
//               </div>
//             ))}
//           </div>
//         )}
//       </div>
//     </div>
//   );
// };
//-------------------------------------------------------------------------------
import React from 'react';
import { LayoutDashboard, Car, ShieldAlert, ArrowLeft } from 'lucide-react';

interface ResultsPageProps {
  results: any;
}

export const ResultsPage: React.FC<ResultsPageProps> = ({ results }) => {
  // Safe Fallback: If no results exist (e.g., page reload), show a message instead of crashing
  if (!results) {
    return (
      <div className="min-h-[60vh] flex flex-col items-center justify-center text-center px-4 animate-fade-in-up">
        <LayoutDashboard className="w-20 h-20 text-slate-300 mb-6" />
        <h2 className="text-2xl font-bold text-slate-900 mb-2">No Analysis Data Found</h2>
        <p className="text-slate-500 max-w-md">
          It looks like you haven't processed a video yet, or the page was reloaded. Please go back and upload a video to see results.
        </p>
      </div>
    );
  }

  // Extract the specific data sent from Python 
  // Remember in ml_logic.py you returned: {"total_vehicles_detected": final_vehicle_count}
  const totalVehicles = results.total_vehicles_detected || 0;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 animate-fade-in-up">
      <div className="mb-10">
        <h1 className="text-3xl font-extrabold text-slate-900 tracking-tight flex items-center gap-3">
           <LayoutDashboard className="text-blue-600" /> Analysis Dashboard
        </h1>
        <p className="text-slate-500 mt-2">Summary of the processed offline footage.</p>
      </div>

      <div className="grid md:grid-cols-3 gap-6">
        
        {/* Primary Stat Card */}
        <div className="bg-white rounded-2xl p-8 border border-slate-200 shadow-sm relative overflow-hidden group hover:border-blue-300 transition-colors">
          <div className="absolute -right-6 -top-6 bg-blue-50 rounded-full w-32 h-32 flex items-center justify-center group-hover:scale-110 transition-transform">
             <Car className="text-blue-200 w-16 h-16 mr-4 mt-4" />
          </div>
          <div className="relative z-10">
            <h3 className="text-slate-500 font-semibold mb-1 uppercase tracking-wider text-sm">Total Vehicles</h3>
            <div className="text-5xl font-black text-slate-900">{totalVehicles}</div>
            <p className="text-sm text-emerald-600 font-medium mt-4 flex items-center gap-1">
               Successfully tracked through frame
            </p>
          </div>
        </div>

        {/* Placeholder Stat Card 1 */}
        <div className="bg-white rounded-2xl p-8 border border-slate-200 shadow-sm flex flex-col justify-center">
            <h3 className="text-slate-500 font-semibold mb-2 uppercase tracking-wider text-sm">Triple Riding Alerts</h3>
            <p className="text-slate-800 text-lg">Check video overlay for real-time flags. Aggregate counting coming soon.</p>
        </div>

        {/* Placeholder Stat Card 2 */}
        <div className="bg-white rounded-2xl p-8 border border-slate-200 shadow-sm flex flex-col justify-center">
            <h3 className="text-slate-500 font-semibold mb-2 uppercase tracking-wider text-sm">Helmet Violations</h3>
            <p className="text-slate-800 text-lg">Check video overlay for NO HELMET tags. Aggregate counting coming soon.</p>
        </div>

      </div>

      {/* Raw Data Output for Debugging */}
      <div className="mt-12 bg-slate-900 rounded-2xl p-6 shadow-xl overflow-hidden">
        <div className="flex items-center gap-2 text-slate-300 mb-4 font-mono text-sm border-b border-slate-700 pb-4">
          JSON Response Output
        </div>
        <pre className="text-emerald-400 font-mono text-sm overflow-x-auto">
          {JSON.stringify(results, null, 2)}
        </pre>
      </div>
    </div>
  );
};