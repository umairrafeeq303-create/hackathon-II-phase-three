import Link from "next/link";

export default function HomePage() {
  return (
    <div className="relative min-h-screen overflow-hidden bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950">
      {/* Animated Background Particles */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-20 left-10 w-72 h-72 bg-purple-500/10 rounded-full blur-3xl animate-float"></div>
        <div className="absolute top-40 right-20 w-96 h-96 bg-violet-500/10 rounded-full blur-3xl animate-float" style={{ animationDelay: '1s' }}></div>
        <div className="absolute bottom-20 left-1/3 w-80 h-80 bg-amber-500/5 rounded-full blur-3xl animate-float" style={{ animationDelay: '2s' }}></div>
      </div>

      {/* Grid Pattern Overlay */}
      <div className="absolute inset-0 bg-[linear-gradient(to_right,#1e293b_1px,transparent_1px),linear-gradient(to_bottom,#1e293b_1px,transparent_1px)] bg-[size:4rem_4rem] [mask-image:radial-gradient(ellipse_60%_50%_at_50%_0%,#000_70%,transparent_100%)] pointer-events-none"></div>

      {/* Content */}
      <div className="relative z-10 min-h-screen flex items-center justify-center px-4 sm:px-6 lg:px-8">
        <div className="max-w-6xl w-full">
          {/* Hero Section */}
          <div className="text-center space-y-8 mb-16 animate-fade-in-premium">
            {/* Animated Logo/Icon */}
            <div className="flex justify-center mb-8">
              <div className="icon-gradient-primary w-24 h-24 sm:w-28 sm:h-28 animate-float">
                <svg
                  className="w-12 h-12 sm:w-14 sm:h-14 text-white"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                  strokeWidth={2}
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
              </div>
            </div>

            {/* Hero Heading */}
            <div className="space-y-4">
              <h1 className="text-5xl sm:text-6xl lg:text-7xl font-extrabold">
                <span className="gradient-text-primary text-shadow-premium">
                  TaskFlow
                </span>
              </h1>
              <p className="text-xl sm:text-2xl lg:text-3xl font-bold text-slate-300">
                Elevate Your Productivity
              </p>
              <p className="text-base sm:text-lg text-slate-400 max-w-2xl mx-auto">
                Experience the future of task management with AI-powered assistance,
                intelligent automation, and premium design
              </p>
            </div>

            {/* Trust Indicators */}
            <div className="flex flex-wrap justify-center gap-4 pt-4">
              <div className="badge-primary">
                <svg className="w-4 h-4 mr-1.5" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M2.166 4.999A11.954 11.954 0 0010 1.944 11.954 11.954 0 0017.834 5c.11.65.166 1.32.166 2.001 0 5.225-3.34 9.67-8 11.317C5.34 16.67 2 12.225 2 7c0-.682.057-1.35.166-2.001zm11.541 3.708a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
                Enterprise Security
              </div>
              <div className="badge-success">
                <svg className="w-4 h-4 mr-1.5" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                </svg>
                AI-Powered
              </div>
              <div className="badge-info">
                <svg className="w-4 h-4 mr-1.5" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z" clipRule="evenodd" />
                </svg>
                Lightning Fast
              </div>
            </div>

            {/* CTA Buttons */}
            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center pt-8 max-w-md mx-auto">
              <Link
                href="/auth/signup"
                className="btn-premium-primary w-full sm:w-auto text-center"
              >
                Get Started Free
              </Link>

              <Link
                href="/auth/signin"
                className="btn-premium-secondary w-full sm:w-auto text-center"
              >
                Sign In
              </Link>
            </div>
          </div>

          {/* Features Section */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 lg:gap-8 max-w-5xl mx-auto animate-scale-in-premium">
            {/* Feature 1 */}
            <div className="glass-card-hover p-6 lg:p-8">
              <div className="icon-gradient-primary w-14 h-14 mb-4">
                <svg className="w-7 h-7 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                </svg>
              </div>
              <h3 className="text-xl font-bold gradient-text-primary mb-2">
                Military-Grade Security
              </h3>
              <p className="text-slate-400 text-sm leading-relaxed">
                Your data is protected with enterprise-level encryption, JWT authentication,
                and secure session management
              </p>
            </div>

            {/* Feature 2 */}
            <div className="glass-card-hover p-6 lg:p-8">
              <div className="icon-gradient-gold w-14 h-14 mb-4">
                <svg className="w-7 h-7 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09z" />
                </svg>
              </div>
              <h3 className="text-xl font-bold gradient-text-gold mb-2">
                AI Assistant
              </h3>
              <p className="text-slate-400 text-sm leading-relaxed">
                Let our intelligent AI assistant help you organize, prioritize, and complete
                tasks faster than ever before
              </p>
            </div>

            {/* Feature 3 */}
            <div className="glass-card-hover p-6 lg:p-8">
              <div className="icon-gradient-primary w-14 h-14 mb-4">
                <svg className="w-7 h-7 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 13.5l10.5-11.25L12 10.5h8.25L9.75 21.75 12 13.5H3.75z" />
                </svg>
              </div>
              <h3 className="text-xl font-bold gradient-text-primary mb-2">
                Blazing Performance
              </h3>
              <p className="text-slate-400 text-sm leading-relaxed">
                Built with Next.js 14+ and modern technologies for instant page loads
                and seamless interactions
              </p>
            </div>
          </div>

          {/* Footer Text */}
          <div className="text-center mt-16 animate-fade-in-premium">
            <p className="text-slate-500 text-sm">
              Join thousands of professionals who trust TaskFlow
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
