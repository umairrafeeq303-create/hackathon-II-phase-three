'use client';

/**
 * Premium Header component with luxury dark theme navigation
 */
import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';
import { getCurrentUser, removeAuthToken } from '@/lib/auth';
import { api } from '@/lib/api';
import { Button } from '@/components/ui/Button';

export function Header() {
  const router = useRouter();
  const pathname = usePathname();
  const user = getCurrentUser();

  const handleLogout = async () => {
    await api.logout();
    removeAuthToken();
    router.push('/auth/signin');
  };

  const isActive = (path: string) => pathname === path;

  return (
    <header className="glass-card sticky top-0 z-40 border-b border-slate-700/50 animate-slide-down-premium">
      <div className="container-premium">
        <div className="flex justify-between items-center h-20">
          {/* Logo & Brand */}
          <div className="flex items-center gap-8">
            <Link href="/dashboard" className="flex items-center gap-3 group">
              <div className="icon-gradient-primary w-11 h-11 transition-transform duration-300 group-hover:scale-110">
                <svg className="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <div>
                <h1 className="text-2xl font-bold gradient-text-primary text-shadow-premium">
                  TaskFlow
                </h1>
                <p className="text-xs text-slate-500 font-medium">Premium Task Management</p>
              </div>
            </Link>

            {/* Navigation Links */}
            <nav className="hidden md:flex gap-2">
              <Link
                href="/dashboard"
                className={`
                  px-5 py-2.5 text-sm font-semibold rounded-xl transition-all duration-300
                  ${
                    isActive('/dashboard')
                      ? 'bg-gradient-to-r from-purple-600 to-violet-700 text-white shadow-lg shadow-purple-500/30'
                      : 'text-slate-400 hover:text-purple-400 hover:bg-slate-700/30'
                  }
                `}
              >
                <div className="flex items-center gap-2">
                  <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
                  </svg>
                  <span>Dashboard</span>
                </div>
              </Link>
            </nav>
          </div>

          {/* User Profile & Actions */}
          <div className="flex items-center gap-4">
            {user && (
              <div className="flex items-center gap-3 px-4 py-2 glass-card border-slate-600/50">
                {/* User Avatar */}
                <div className="relative">
                  <div className="w-10 h-10 icon-gradient-primary text-white font-bold text-sm flex items-center justify-center">
                    {user.name.charAt(0).toUpperCase()}
                  </div>
                  <div className="absolute -bottom-0.5 -right-0.5 w-3.5 h-3.5 bg-emerald-500 rounded-full border-2 border-slate-800 animate-pulse"></div>
                </div>

                {/* User Info */}
                <div className="hidden sm:flex flex-col">
                  <span className="text-sm font-semibold text-slate-200">{user.name}</span>
                  <span className="text-xs text-slate-500">{user.email}</span>
                </div>
              </div>
            )}

            {/* Logout Button */}
            <Button
              variant="secondary"
              onClick={handleLogout}
              className="shadow-md hover:shadow-lg"
            >
              <svg className="w-5 h-5 mr-1.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
              </svg>
              <span className="hidden sm:inline">Logout</span>
            </Button>
          </div>
        </div>
      </div>
    </header>
  );
}
