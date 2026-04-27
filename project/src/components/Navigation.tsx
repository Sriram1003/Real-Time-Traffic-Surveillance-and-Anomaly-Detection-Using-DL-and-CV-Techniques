import React from 'react';
import { useAuth } from '../context/AuthContext';
import { LogOut, Menu, X } from 'lucide-react';
import { useState } from 'react';

interface NavigationProps {
  currentPage: string;
  onPageChange: (page: string) => void;
}

export const Navigation: React.FC<NavigationProps> = ({ currentPage, onPageChange }) => {
  const { user, signOut } = useAuth();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const handleSignOut = async () => {
    await signOut();
    onPageChange('home');
  };

  return (
    <nav className="bg-gradient-to-r from-slate-800 to-slate-900 shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center cursor-pointer" onClick={() => onPageChange('home')}>
            <div className="text-2xl font-bold text-white">🚗 TrafficAI</div>
          </div>

          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="md:hidden text-white"
          >
            {mobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
          </button>

          <div className={`${mobileMenuOpen ? 'block' : 'hidden'} md:flex gap-6 absolute md:static top-16 left-0 right-0 md:top-auto bg-slate-800 md:bg-transparent p-4 md:p-0 flex-col md:flex-row`}>
            {user ? (
              <>
                <button
                  onClick={() => {
                    onPageChange('upload');
                    setMobileMenuOpen(false);
                  }}
                  className={`px-4 py-2 rounded transition ${
                    currentPage === 'upload'
                      ? 'bg-blue-600 text-white'
                      : 'text-gray-300 hover:text-white'
                  }`}
                >
                  Upload Video
                </button>
                <button
                  onClick={() => {
                    onPageChange('results');
                    setMobileMenuOpen(false);
                  }}
                  className={`px-4 py-2 rounded transition ${
                    currentPage === 'results'
                      ? 'bg-blue-600 text-white'
                      : 'text-gray-300 hover:text-white'
                  }`}
                >
                  Results
                </button>
                <div className="flex items-center gap-4 text-gray-300 text-sm">
                  <span>{user.email}</span>
                  <button
                    onClick={handleSignOut}
                    className="flex items-center gap-2 bg-red-600 hover:bg-red-700 text-white px-3 py-2 rounded transition"
                  >
                    <LogOut size={18} />
                    Logout
                  </button>
                </div>
              </>
            ) : (
              <>
                <button
                  onClick={() => {
                    onPageChange('login');
                    setMobileMenuOpen(false);
                  }}
                  className={`px-4 py-2 rounded transition ${
                    currentPage === 'login'
                      ? 'bg-blue-600 text-white'
                      : 'text-gray-300 hover:text-white'
                  }`}
                >
                  Login
                </button>
                <button
                  onClick={() => {
                    onPageChange('signup');
                    setMobileMenuOpen(false);
                  }}
                  className={`px-4 py-2 rounded transition ${
                    currentPage === 'signup'
                      ? 'bg-blue-600 text-white'
                      : 'text-gray-300 hover:text-white'
                  }`}
                >
                  Sign Up
                </button>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};
