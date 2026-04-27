import { useState, useEffect } from 'react';
import { ShieldCheck, Video, UploadCloud, Activity, LayoutDashboard, Moon, Sun } from 'lucide-react';
import { HomePage } from './pages/HomePage';
import { UploadPage } from './pages/UploadPage';
import { LivePage } from './pages/LivePage';
import { ResultsPage } from './pages/ResultsPage';

function App() {
  // Navigation State: 'home', 'upload', 'live', 'results'
  const [currentPage, setCurrentPage] = useState('home');
  const [analysisResults, setAnalysisResults] = useState(null);
  const [darkMode, setDarkMode] = useState(false);

  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [darkMode]);

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-950 font-sans text-slate-900 dark:text-slate-100 transition-colors duration-200">
      {/* Premium Sticky Navigation Bar */}
      <nav className="bg-white/80 dark:bg-slate-900/80 backdrop-blur-md border-b border-slate-200 dark:border-slate-800 sticky top-0 z-50 transition-all duration-300">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16 items-center">
            
            {/* Brand Logo */}
            <div 
              onClick={() => setCurrentPage('home')} 
              className="flex items-center gap-2 cursor-pointer group"
            >
              <div className="bg-blue-600 p-2 rounded-lg text-white group-hover:bg-blue-700 transition">
                <ShieldCheck size={24} />
              </div>
              <span className="text-2xl font-extrabold tracking-tight text-slate-900 dark:text-white">
                Traffic<span className="text-blue-600 dark:text-blue-500">AI</span>
              </span>
            </div>

            {/* Desktop Navigation */}
            <div className="hidden md:flex items-center gap-2">
              <NavButton 
                active={currentPage === 'home'} 
                onClick={() => setCurrentPage('home')} 
                icon={<Activity size={18} />} 
                label="Home" 
              />
              <NavButton 
                active={currentPage === 'upload'} 
                onClick={() => setCurrentPage('upload')} 
                icon={<UploadCloud size={18} />} 
                label="Upload Video" 
              />
              <NavButton 
                active={currentPage === 'results'} 
                onClick={() => setCurrentPage('results')} 
                icon={<LayoutDashboard size={18} />} 
                label="Dashboard" 
              />
              
              {/* Special Live Button */}
              <button 
                onClick={() => setCurrentPage('live')}
                className={`ml-2 flex items-center gap-2 px-5 py-2 rounded-full font-semibold transition-all shadow-sm ${
                  currentPage === 'live' 
                  ? 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400 ring-2 ring-red-500 ring-offset-1 dark:ring-offset-slate-900' 
                  : 'bg-red-500 hover:bg-red-600 text-white shadow-red-500/30'
                }`}
              >
                <Video size={18} className={currentPage === 'live' ? 'animate-pulse' : ''} />
                Live Camera
              </button>

              <button
                onClick={() => setDarkMode(!darkMode)}
                className="ml-4 p-2 text-slate-500 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-full transition-colors"
                aria-label="Toggle Dark Mode"
              >
                {darkMode ? <Sun size={20} /> : <Moon size={20} />}
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content Area */}
      <main className="animate-fade-in-up">
        {currentPage === 'home' && (
          <HomePage onNavigate={setCurrentPage} />
        )}
        
        {currentPage === 'upload' && (
          <UploadPage 
            onPageChange={setCurrentPage} 
            setAnalysisResults={setAnalysisResults} 
          />
        )}
        
        {currentPage === 'results' && (
          <ResultsPage results={analysisResults} />
        )}

        {currentPage === 'live' && (
           <LivePage />
        )}
      </main>

      {/* Simple Footer */}
      <footer className="border-t border-slate-200 dark:border-slate-800 mt-20 py-8 bg-white dark:bg-slate-900 text-center text-slate-500 dark:text-slate-400 text-sm transition-colors duration-200">
        <p>© {new Date().getFullYear()} TrafficAI. Powered by YOLOv8 & EasyOCR.</p>
      </footer>
    </div>
  );
}

// Reusable Navigation Button Component
const NavButton = ({ active, onClick, icon, label }: { active: boolean, onClick: () => void, icon: React.ReactNode, label: string }) => (
  <button
    onClick={onClick}
    className={`flex items-center gap-2 px-4 py-2 rounded-md font-medium transition-all duration-200 ${
      active 
      ? 'bg-blue-50 dark:bg-blue-900/40 text-blue-700 dark:text-blue-400' 
      : 'text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 hover:text-slate-900 dark:hover:text-white'
    }`}
  >
    {icon} {label}
  </button>
);

export default App;
