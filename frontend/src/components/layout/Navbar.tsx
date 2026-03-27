import { Link, useLocation } from 'react-router-dom';
import { Shield, LayoutDashboard, Camera, Search, Database } from 'lucide-react';

const Navbar = () => {
  const location = useLocation();

  const navLinks = [
    { name: 'Dashboard', path: '/', icon: LayoutDashboard },
    { name: 'Register', path: '/register', icon: Camera },
    { name: 'Verify', path: '/verify', icon: Search },
    { name: 'Explorer', path: '/explorer', icon: Database },
  ];

  return (
    <nav className="border-b border-white/10 bg-black/20 backdrop-blur-md sticky top-0 z-50">
      <div className="container mx-auto px-6 h-20 flex items-center justify-between">
        <Link to="/" className="flex items-center gap-3">
          <div className="w-10 h-10 bg-[#0066A1] rounded-xl flex items-center justify-center shadow-lg shadow-blue-500/20">
            <Shield className="text-white w-6 h-6" />
          </div>
          <span className="text-xl font-bold tracking-tight">MediProof</span>
        </Link>

        <div className="flex items-center gap-8">
          <div className="hidden md:flex items-center gap-6">
            {navLinks.map((link) => {
              const Icon = link.icon;
              const isActive = location.pathname === link.path;
              return (
                <Link
                  key={link.path}
                  to={link.path}
                  className={`flex items-center gap-2 text-sm font-medium transition-colors ${
                    isActive ? 'text-[#4A90E2]' : 'text-gray-400 hover:text-white'
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  {link.name}
                </Link>
              );
            })}
          </div>
          <div className="w-[1px] h-6 bg-white/10 mx-2 hidden md:block"></div>
          <button className="px-5 py-2 bg-[#0066A1] hover:bg-[#4A90E2] transition-colors rounded-lg text-sm font-semibold shadow-lg shadow-blue-600/20">
            Dr. Smith
          </button>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
