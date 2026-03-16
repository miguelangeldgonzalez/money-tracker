import { useAuth0 } from '@auth0/auth0-react';
import axios, { type AxiosRequestConfig } from 'axios';

export const useApiService = () => {
  const { getAccessTokenSilently } = useAuth0();
  const callApi = async (endpoint: string, config: AxiosRequestConfig = {}) => {
    const token = await getAccessTokenSilently();
    
    const headers = {
      ...(config.headers || {}),
      Authorization: `Bearer ${token}`,
    };
    const axiosConfig: AxiosRequestConfig = {
      ...config,
      headers,
      url: endpoint,
    };
    
    const response = await axios(axiosConfig);
    return response.data;
  };


  return { callApi };
};
