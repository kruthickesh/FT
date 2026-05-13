export default function NotFoundPage() {
  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="text-center">
        <h1 className="text-6xl font-bold text-primary">404</h1>
        <p className="text-xl text-gray-600 mt-4">Page not found</p>
        <a href="/" className="mt-6 inline-block px-6 py-2 bg-primary text-white rounded-lg">Go Home</a>
      </div>
    </div>
  );
}