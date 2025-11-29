// frontend/app/layout.tsx
import "./globals.css"
import type { Metadata } from "next"
import { Inter } from "next/font/google"

const inter = Inter({ 
  subsets: ["latin"],
  variable: "--font-inter"
})

export const metadata: Metadata = {
  title: "GenZweeK",
  description: "Text-first ephemeral social • 7-day posts • Gen Z vibes",
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="dark">
      <body className={`${inter.variable} font-sans antialiased`}>
        <div className="min-h-screen bg-gradient-to-br from-slate-950 via-purple-950/20 to-slate-950 text-white`}>
          {/* Header */}
          <header className="border-b border-white/5 backdrop-blur-md sticky top-0 z-50">
            <div className="max-w-xl mx-auto px-4 py-3 flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-2xl bg-gradient-to-br from-blue-500 via-purple-500 to-pink-500 shadow-xl flex items-center justify-center">
                  <span className="text-sm font-black">GZ</span>
                </div>
                <div>
                  <h1 className="text-xl font-bold bg-gradient-to-r from-white to-slate-200 bg-clip-text text-transparent">
                    GenZweeK
                  </h1>
                  <p className="text-xs text-slate-400">text disappears in 7 days</p>
                </div>
              </div>
            </div>
          </header>

          {/* Main content */}
          <main className="max-w-xl mx-auto px-4 pb-20">
            {children}
          </main>
        </div>
      </body>
    </html>
  )
}
