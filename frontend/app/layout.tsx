// frontend/app/layout.tsx
import "./globals.css"
import type { Metadata } from "next"

export const metadata: Metadata = {
  title: "GenZweeK",
  description: "Text-first ephemeral social",
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="bg-slate-950 text-white antialiased">
        <div className="min-h-screen max-w-xl mx-auto px-4 py-8">
          {children}
        </div>
      </body>
    </html>
  )
}
