import React from "react";

const Layout = ({ children }) => {
  return (
    <div className="app-bg">
      <div className="glass-card">
        {children}
      </div>
    </div>
  );
};

export default Layout;
