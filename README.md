# GreenGrid India - Clean India, Gamified

A gamified waste management platform that encourages citizens to clean up India through an interactive map, AI verification, and social competition.

## 🚀 Quick Start

### Prerequisites
- Node.js 16+ and npm

### Installation & Running

1. **Install dependencies:**
```bash
   npm install
```

2. **Run development server:**
```bash
   npm run dev
```
   Open browser to `http://localhost:5173`

3. **Build for production:**
```bash
   npm run build
```

4. **Preview production build:**
```bash
   npm run preview
```

## 🔑 Admin Access

- **Email:** `admin@greengrid.com`
- **Password:** `admin123`

## 🎮 Features

### For Users
- **Interactive Map:** Click anywhere in India to claim cleanup spots
- **AI Verification:** Upload before/after photos for AI-powered approval
- **Gamification:** Earn points, build streaks, climb leaderboards
- **Premium Membership:** Upgrade to Green Guardian for 2x points and gold badges
- **Dark/Light Theme:** Auto-detects system preference, toggle with button or `T` key
- **Social Sharing:** Share progress to WhatsApp (copies invite to clipboard)

### For Admins
- **Dashboard:** View statistics and user growth charts
- **User Management:** Ban/unban users
- **Map Oversight:** Reset all map data with action logging

## 🛠️ Developer Tools

Press `Ctrl+Shift+D` to open dev panel:

- **Seed Fake Data:** Add test users and spots
- **Adjust AI Approval Rate:** Control verification success rate (default 70%)
- **Simulate Time:** Fast-forward days to test decay logic (spots >7 days revert to dirty)
- **Reset All Data:** Clear entire database

## 📁 Project Structure
```
greengrid-india/
├── index.html              # Main HTML with README comment
├── styles.css              # Tailwind + custom CSS with variables
├── tailwind.config.cjs     # Tailwind config (darkMode: 'class')
├── postcss.config.cjs      # PostCSS config
├── vite.config.js          # Vite build config
├── package.json            # Dependencies and scripts
├── src/
│   ├── main.js            # App logic and UI
│   └── db.js              # Mock backend with localStorage
└── README.md              # This file
```

## 🎨 Theme System

- **Auto Theme Detection:** Reads system preference on first load
- **Manual Toggle:** Click theme button in header or press `T` key
- **Persistent:** Saves preference to localStorage
- **Comprehensive:** Changes UI colors, map tiles, markers, and charts instantly

## 🔒 Security Notice

**This is a client-only prototype.** Production requires:

- Server-side password hashing (not browser bcrypt)
- JWT tokens with HTTP-only cookies
- Rate limiting and CSRF protection
- Server-side image storage (not localStorage base64)
- Input validation and sanitization
- Proper session management

## 🧪 Testing

1. **Signup/Login:** Create account or use admin credentials
2. **Claim Spot:** Click map to add cleanup location
3. **Upload Cleanup:** Select spot, upload before/after images
4. **AI Verification:** Watch scanning animation, get instant feedback
5. **Premium Upgrade:** Test payment flow (always succeeds)
6. **Admin Panel:** Login as admin, view stats, manage users
7. **Theme Toggle:** Switch between light/dark, verify map/charts update
8. **Dev Tools:** Press Ctrl+Shift+D, seed data, adjust AI rate, simulate time

## 📊 Data Persistence

All data stored in localStorage:
- Users (with hashed passwords via bcryptjs)
- Spots (lat/lng, status, images)
- Transactions (cleanups, upgrades, admin actions)
- Settings (theme, AI rate, simulated date)
- Session (current user)

## 🎯 Advanced Features (Scaffolded)

The following features have TODO markers in code:
- Waste Exchange (barter system)
- Sponsor-a-Bin (IoT simulation)
- Corporate Clash (company leaderboards)
- Time-Lapse Gallery (repeated cleanup tracking)
- PWA manifest + service worker

## 🐛 Known Limitations

- localStorage has ~5-10MB limit; large image uploads may fail
- No server-side validation
- AI verification is simulated (random probability)
- No real payment processing
- Map performance may degrade with 1000+ markers

## 📝 License

MIT License - Educational prototype for GreenGrid India concept demonstration.
```

---filename: .gitignore---
```
node_modules/
dist/
.DS_Store
*.log
.vite/