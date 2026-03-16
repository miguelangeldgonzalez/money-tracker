import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { Auth0Provider } from "@auth0/auth0-react";
import App from "./App";
import "./global.css";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <Auth0Provider
      domain="dev-p2iro3psonbr3wtf.us.auth0.com"
      clientId="pPBTHcUqiFoin0hpbfP5XM6uv9j50fBk"
      authorizationParams={{ 
        redirect_uri: window.location.origin,
        audience: "https://dev-p2iro3psonbr3wtf.us.auth0.com/api/v2/"
      }}
    >
      <App />
    </Auth0Provider>
  </StrictMode>,
);
