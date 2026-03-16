import React from 'react';
import { useAuth0 } from '@auth0/auth0-react';
import './Header.css';

const Header: React.FC = () => {
  const {
    isAuthenticated,
    isLoading,
    user,
    loginWithRedirect,
    logout,
    error
  } = useAuth0();
  
  if (isLoading) return <header className="header">Loading...</header>;

  return (
    <header className="header">
      <div className="header-title">Money Tracker</div>
      <div className="header-actions">
        {isAuthenticated ? (
          <>
            <span className="header-user">Welcome, {user?.name || user?.email}</span>
            <button className="header-btn" onClick={() => logout({ logoutParams: { returnTo: window.location.origin } })}>Logout</button>
          </>
        ) : (
          <button className="header-btn" onClick={() => loginWithRedirect()}>Login</button>
        )}
        {error && <span className="header-error">Error: {error.message}</span>}
      </div>
    </header>
  );
};

export default Header;
