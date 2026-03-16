
import Header from "./components/Header/Header";
import Dashboard from "./pages/Dashboard/Dashboard";
import { useAuth0 } from '@auth0/auth0-react';

function App() {
  const { isAuthenticated } = useAuth0();
  return (
    <>
      <Header />
      {isAuthenticated && <Dashboard />}
    </>
  );
}

export default App;
