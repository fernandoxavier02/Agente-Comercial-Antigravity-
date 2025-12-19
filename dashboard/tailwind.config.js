/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        "./app/**/*.{js,ts,jsx,tsx,mdx}",
    ],
    theme: {
        extend: {
            colors: {
                obsidian: {
                    900: "#050505", // Fundo principal (quase preto puro)
                    800: "#0a0a0b", // Cards / Paineis
                    700: "#121214", // Bordas sutis
                },
                gold: {
                    300: "#F2D088", // Texto destaque claro
                    400: "#D4AF37", // Dourado clássico metálico
                    500: "#AA8C2C", // Dourado escuro para bordas/sombras
                },
                platinum: {
                    50: "#F8F9FA",
                    100: "#E9ECEF",
                    400: "#CED4DA",
                }
            },
            fontFamily: {
                sans: ['var(--font-inter)', 'sans-serif'],
                serif: ['var(--font-playfair)', 'serif'], // Para títulos de luxo
            },
            backgroundImage: {
                'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
                'luxury-glow': 'conic-gradient(from 180deg at 50% 50%, #0a0a0b 0deg, #121214 180deg, #0a0a0b 360deg)',
            }
        },
    },
    plugins: [],
};
