import React from "react";
import { Link, useLocation } from "react-router-dom";

const Navbar = () => {
  const location = useLocation();

  const navLinks = [
    { path: "/", label: "Home", icon: "🏠" },
    { path: "/job", label: "Job Description", icon: "📝" },
    { path: "/history", label: "History", icon: "📋" },
  ];

  const isActive = (path) => {
    if (path === "/") return location.pathname === "/";
    return location.pathname.startsWith(path);
  };

  return (
    <nav className="bg-gradient-to-r from-blue-600 to-blue-800 shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <div className="flex items-center">
            <Link to="/" className="flex items-center space-x-2">
              <div className="text-3xl">🎯</div>
              <span className="text-white font-bold text-xl hidden sm:block">
                AI Resume Screening
              </span>
            </Link>
          </div>

          {/* Navigation Links */}
          <div className="flex space-x-1 sm:space-x-4">
            {navLinks.map((link) => (
              <Link
                key={link.path}
                to={link.path}
                className={`px-3 py-2 rounded-md text-sm font-medium transition-all duration-200 flex items-center space-x-2 ${
                  isActive(link.path)
                    ? "bg-blue-900 text-white shadow-md"
                    : "text-blue-100 hover:bg-blue-700 hover:text-white"
                }`}
              >
                <span className="text-lg">{link.icon}</span>
                <span className="hidden sm:inline">{link.label}</span>
              </Link>
            ))}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
