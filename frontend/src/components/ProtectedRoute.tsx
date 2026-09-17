import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import Layout from '../components/Layout';
import LoadingSpinner from '../components/LoadingSpinner';

export function ProtectedRoute() {
  const { isAuthenticated, loading } = useAuth();

  if (loading) return <LoadingSpinner>Loading...</LoadingSpinner>;
  if (!isAuthenticated) return <Navigate to="/login" replace />;

  return (
    <Layout>
      <Outlet />
    </Layout>
  );
}

export function PublicRoute() {
  const { isAuthenticated, loading } = useAuth();

  if (loading) return <LoadingSpinner>Loading...</LoadingSpinner>;
  if (isAuthenticated) return <Navigate to="/" replace />;

  return <Outlet />;
}
