import { Inter, Playfair_Display } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"], variable: "--font-inter" });
const playfair = Playfair_Display({ subsets: ["latin"], variable: "--font-playfair" });

export const metadata = { title: "Clínica Mais | Private", description: "Gestão de Leads de Alto Padrão" };

export default function RootLayout({ children }) {
  return (
    <html lang="pt-BR" className={`${inter.variable} ${playfair.variable}`}>
      <body className="min-h-screen bg-obsidian-900 text-platinum-100 antialiased selection:bg-gold-500 selection:text-white">
        {children}
      </body>
    </html>
  );
}
