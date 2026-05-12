import { Suspense, lazy } from 'react'
import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'

import { AppShell } from './components/layout/AppShell'
import { AuthProvider, useAuth } from './context/AuthContext'
import { ThemeProvider } from './context/ThemeProvider'
import { ToastProvider } from './hooks/useToast'

const AdminDashboardPage = lazy(() => import('./pages/AdminDashboardPage').then((module) => ({ default: module.AdminDashboardPage })))
const AdminLoginPage = lazy(() => import('./pages/AdminLoginPage').then((module) => ({ default: module.AdminLoginPage })))
const AuthPage = lazy(() => import('./pages/AuthPage').then((module) => ({ default: module.AuthPage })))
const BookingPage = lazy(() => import('./pages/BookingPage').then((module) => ({ default: module.BookingPage })))
const BrowsePage = lazy(() => import('./pages/BrowsePage').then((module) => ({ default: module.BrowsePage })))
const CinemasPage = lazy(() => import('./pages/CinemasPage').then((module) => ({ default: module.CinemasPage })))
const ConfirmationPage = lazy(() => import('./pages/ConfirmationPage').then((module) => ({ default: module.ConfirmationPage })))
const HomePage = lazy(() => import('./pages/HomePage').then((module) => ({ default: module.HomePage })))
const MovieDetailsPage = lazy(() => import('./pages/MovieDetailsPage').then((module) => ({ default: module.MovieDetailsPage })))
const NotFoundPage = lazy(() => import('./pages/NotFoundPage').then((module) => ({ default: module.NotFoundPage })))
const ProfilePage = lazy(() => import('./pages/ProfilePage').then((module) => ({ default: module.ProfilePage })))
const TicketsPage = lazy(() => import('./pages/TicketsPage').then((module) => ({ default: module.TicketsPage })))
const UserLoginPage = lazy(() => import('./pages/UserLoginPage').then((module) => ({ default: module.UserLoginPage })))
const UserSignupPage = lazy(() => import('./pages/UserSignupPage').then((module) => ({ default: module.UserSignupPage })))

function RequireUserRoute({ children }) {
  const { user } = useAuth()
  if (!user) return <Navigate to="/login" replace />
  if (user.role === 'admin') return <Navigate to="/admin/dashboard" replace />
  return children
}

function RequireAdminRoute({ children }) {
  const { user } = useAuth()
  if (!user) return <Navigate to="/login" replace />
  if (user.role !== 'admin') return <Navigate to="/home" replace />
  return children
}

function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/home" replace />} />
      <Route path="/auth" element={<AuthPage />} />
      <Route path="/login" element={<AppShell />}>
        <Route index element={<UserLoginPage />} />
      </Route>
      <Route path="/signup" element={<AppShell />}>
        <Route index element={<UserSignupPage />} />
      </Route>
      <Route path="/admin/login" element={<AdminLoginPage />} />

      <Route element={<AppShell />}>
        <Route path="/home" element={<HomePage />} />
        <Route path="/browse" element={<BrowsePage />} />
        <Route path="/movies" element={<BrowsePage />} />
        <Route path="/movie/:movieId" element={<MovieDetailsPage />} />
        <Route path="/movies/:movieId" element={<MovieDetailsPage />} />
        <Route path="/cinemas" element={<CinemasPage />} />
        <Route path="/watchlist" element={<BrowsePage />} />
        <Route
          path="/booking/:showId"
          element={
            <RequireUserRoute>
              <BookingPage />
            </RequireUserRoute>
          }
        />
        <Route
          path="/confirmation/:bookingId"
          element={
            <RequireUserRoute>
              <ConfirmationPage />
            </RequireUserRoute>
          }
        />
        <Route
          path="/tickets"
          element={
            <RequireUserRoute>
              <TicketsPage />
            </RequireUserRoute>
          }
        />
        <Route
          path="/profile"
          element={
            <RequireUserRoute>
              <ProfilePage />
            </RequireUserRoute>
          }
        />
      </Route>

      <Route
        path="/admin/dashboard"
        element={
          <RequireAdminRoute>
            <AdminDashboardPage />
          </RequireAdminRoute>
        }
      />
      <Route path="/admin" element={<Navigate to="/admin/dashboard" replace />} />
      <Route path="*" element={<NotFoundPage />} />
    </Routes>
  )
}

function App() {
  return (
    <AuthProvider>
      <ThemeProvider>
        <BrowserRouter>
          <ToastProvider>
            <Suspense fallback={<div className="section-shell py-20 text-muted">Loading cinematic experience...</div>}>
              <AppRoutes />
            </Suspense>
          </ToastProvider>
        </BrowserRouter>
      </ThemeProvider>
    </AuthProvider>
  )
}

export default App
