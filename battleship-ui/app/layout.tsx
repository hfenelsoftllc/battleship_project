import "../app/styles/globals.css";

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="bg-gray-100 min-h-screen">
        <main className="container mx-auto p-6">{children}</main>
      </body>
    </html>
  );
}
