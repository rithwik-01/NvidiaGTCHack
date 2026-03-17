export const Nav = () => {
  return (
    <nav className="fixed top-0 left-0 right-0 h-14 bg-base/80 backdrop-blur-md border-b border-border z-50">
      <div className="max-w-7xl mx-auto px-6 h-full flex items-center justify-between">
        {/* Logo */}
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 bg-accent-blue rounded-lg flex items-center justify-center">
            <span className="text-white font-display font-bold text-lg">Z</span>
          </div>
          <span className="text-white font-display font-semibold">ZeroFail AI</span>
        </div>

        {/* Center subtitle */}
        <div className="hidden md:block">
          <span className="text-text-muted text-sm">
            Forward-Looking Academic Risk Engine
          </span>
        </div>

        {/* NVIDIA badge */}
        <div className="flex items-center gap-2">
          <div className="w-2 h-2 bg-accent-green rounded-full animate-pulse-slow"></div>
          <span className="text-text-muted text-sm font-medium">
            NVIDIA Nemotron
          </span>
        </div>
      </div>
    </nav>
  );
};
