next

```markdown
# README.md
```
<details><summary>Click to Copy</summary>

```markdown
# GenZweeK 🚀

**Text-first ephemeral social media for Gen Z.** Posts auto-delete after 7 days, stories after 24h. Strict media limits: **10MB photos, 50MB videos**.

## ✨ Features
- ✅ Text-first posts (priority in algorithm)
- ✅ 7-day ephemeral posts + 24h stories
- ✅ Like/view/comment counters
- ✅ Follow system
- ✅ File size validation (10MB image/50MB video)
- ✅ Production security (CSRF, HSTS, CORS)
- ✅ Mobile-first Gen Z UI (blue-purple gradients)
- ✅ Feed algorithm (recency + engagement)

## 🛠 Tech Stack
```
Backend: Django 5 + DRF + SQLite/Postgres
Frontend: Next.js 14 + TypeScript + Tailwind
Deployment: Vercel (frontend) + Railway/Render (backend)
```

## 🚀 Quick Start

### Backend
```
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Frontend
```
cd frontend
npm install
npm run dev
```

**Backend runs on `http://localhost:8000` | Frontend on `http://localhost:3000`**

## 📱 Environment Variables

**backend/.env**
```
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=True
FRONTEND_ORIGIN=http://localhost:3000
```

**frontend/.env.local**
```
NEXT_PUBLIC_API_BASE=http://localhost:8000/api
```

## 🧪 Test It
1. Create post with text ✅
2. Add image (<10MB) or video (<50MB) ✅
3. See it in feed with counters ✅
4. Large files get rejected ✅

## 🚀 Production Deploy
1. **Frontend**: `npm run build` → Vercel
2. **Backend**: Railway/Render/Heroku with Postgres
3. Set production env vars + HTTPS

## 🔒 Security Features
- File size limits enforced server-side
- CSRF protection
- Auth required for writes
- CORS locked to frontend domain
- HSTS + secure headers (prod)

## 📈 Feed Algorithm
```
score = 1.5×recency + 0.5×comments + 0.3×likes + 0.1×log(views)
+1.1×boost for text-only posts
```

## 🤝 Contributing
```
git clone https://github.com/YOUR_USERNAME/genzweek
cd backend && pip install -r requirements.txt
cd frontend && npm install
```

**Made with ❤️ for Gen Z developers**
```
"Your week, your words, your way ✨"
```
```
</details>

***
