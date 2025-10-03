# Deployment Guide for Testing SaaS Platform

This guide will walk you through deploying your Testing SaaS Platform to Vercel (frontend) and Render.com (backend) using their free tiers.

## Prerequisites

- GitHub account with repository: https://github.com/harsha3008-commits/testing-saas-platform.git
- Code has been successfully pushed to GitHub
- Production build completed without errors

---

## Part 1: Setting Up Vercel Account and Deploying Frontend

### Step 1: Create Vercel Account

1. Go to [https://vercel.com/signup](https://vercel.com/signup)
2. Click "Continue with GitHub" to sign up using your GitHub account
3. Authorize Vercel to access your GitHub repositories
4. Complete the account setup

### Step 2: Import Your Frontend Repository

1. Once logged in, click "Add New..." → "Project"
2. Click "Import" next to your `testing-saas-platform` repository
3. Vercel will detect it's a Next.js project automatically

### Step 3: Configure Frontend Build Settings

**Root Directory:**
- Set root directory to: `frontend`

**Build & Development Settings:**
- Framework Preset: `Next.js`
- Build Command: `npm run build`
- Output Directory: `.next`
- Install Command: `npm install`

**Environment Variables:**
Add the following environment variable (we'll update the backend URL after deploying backend):
```
NEXT_PUBLIC_API_URL=https://your-backend-url.onrender.com/api
```

For now, you can leave this blank and update it later.

### Step 4: Deploy Frontend

1. Click "Deploy"
2. Wait 2-3 minutes for the build to complete
3. Once deployed, you'll get a URL like: `https://your-project-name.vercel.app`
4. **Save this URL** - you'll need it for backend CORS configuration

---

## Part 2: Setting Up Render.com Account and Deploying Backend

### Step 1: Create Render.com Account

1. Go to [https://render.com/register](https://render.com/register)
2. Click "Sign up with GitHub"
3. Authorize Render to access your GitHub repositories
4. Complete the account setup

### Step 2: Create PostgreSQL Database

1. From Render Dashboard, click "New +" → "PostgreSQL"
2. Fill in the details:
   - **Name**: `testing-saas-db`
   - **Database**: `testing_saas`
   - **User**: (auto-generated)
   - **Region**: Choose closest to you
   - **PostgreSQL Version**: 15
   - **Plan**: `Free`
3. Click "Create Database"
4. Wait for database to be created (1-2 minutes)
5. **Important**: Once created, go to the database's "Info" tab and copy:
   - **Internal Database URL** (for backend connection)
   - Keep this tab open - you'll need these details

### Step 3: Deploy Backend Web Service

1. From Render Dashboard, click "New +" → "Web Service"
2. Connect your GitHub repository: `testing-saas-platform`
3. Configure the service:

**Basic Settings:**
- **Name**: `testing-saas-backend`
- **Region**: Same as your database
- **Branch**: `main` (or `master`)
- **Root Directory**: `backend`
- **Runtime**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

**Environment Variables:**
Click "Advanced" and add these environment variables:

```
DATABASE_URL=<paste-internal-database-url-from-step-2>
SECRET_KEY=<generate-a-random-secret-key>
ALLOWED_ORIGINS=https://your-project-name.vercel.app
ENVIRONMENT=production
```

To generate a SECRET_KEY, run this in your terminal:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

4. **Plan**: Select `Free`
5. Click "Create Web Service"
6. Wait 5-10 minutes for the first deployment
7. Once deployed, you'll get a URL like: `https://testing-saas-backend.onrender.com`

---

## Part 3: Update Environment Variables

### Update Frontend Environment Variable

1. Go to your Vercel dashboard
2. Select your frontend project
3. Go to "Settings" → "Environment Variables"
4. Update or add `NEXT_PUBLIC_API_URL`:
   ```
   NEXT_PUBLIC_API_URL=https://testing-saas-backend.onrender.com/api
   ```
5. Click "Save"
6. Go to "Deployments" tab
7. Click the three dots on the latest deployment → "Redeploy"

### Update Backend CORS Configuration

1. Go to your Render dashboard
2. Select your backend service
3. Go to "Environment" tab
4. Update `ALLOWED_ORIGINS` with your actual Vercel URL:
   ```
   ALLOWED_ORIGINS=https://your-actual-project-name.vercel.app
   ```
5. Save - the service will automatically redeploy

---

## Part 4: Initialize Database

After backend is deployed, you need to initialize the database:

### Option 1: Using Render Shell

1. Go to your backend service in Render
2. Click "Shell" tab in the top menu
3. Run these commands:
   ```bash
   python
   >>> from database import init_db
   >>> init_db()
   >>> exit()
   ```

### Option 2: Using API Endpoint

If you created an initialization endpoint in your backend:
1. Visit: `https://testing-saas-backend.onrender.com/api/init-db`
2. Or use curl:
   ```bash
   curl -X POST https://testing-saas-backend.onrender.com/api/init-db
   ```

---

## Part 5: Testing Your Deployment

### Test Backend

1. Visit: `https://testing-saas-backend.onrender.com/docs`
2. You should see the FastAPI interactive documentation
3. Test an endpoint to ensure it's working

### Test Frontend

1. Visit your Vercel URL: `https://your-project-name.vercel.app`
2. Try logging in or creating an account
3. Test the main features:
   - Dashboard
   - Organizations page
   - Settings/Notifications page

---

## Important Notes

### Free Tier Limitations

**Vercel Free Tier:**
- 100 GB bandwidth/month
- Automatic HTTPS
- Instant global CDN
- Automatic deployments from GitHub

**Render.com Free Tier:**
- Web services spin down after 15 minutes of inactivity
- First request after spin-down may take 30-50 seconds
- 750 hours/month (enough for one service to run continuously)
- PostgreSQL database limited to 90 days, then deleted (backup your data!)

### Custom Domain (Optional)

**For Vercel:**
1. Go to Project Settings → Domains
2. Add your custom domain
3. Follow DNS configuration instructions

**For Render:**
1. Go to your service Settings → Custom Domain
2. Add your custom domain
3. Follow DNS configuration instructions

---

## Troubleshooting

### Frontend Issues

**Build Fails:**
- Check build logs in Vercel dashboard
- Verify `package.json` and `package-lock.json` are committed
- Ensure root directory is set to `frontend`

**Can't Connect to Backend:**
- Verify `NEXT_PUBLIC_API_URL` is correct
- Check browser console for CORS errors
- Ensure backend `ALLOWED_ORIGINS` includes your Vercel URL

### Backend Issues

**Service Won't Start:**
- Check logs in Render dashboard
- Verify `requirements.txt` is present in backend directory
- Check start command is correct

**Database Connection Failed:**
- Verify `DATABASE_URL` is correctly set
- Ensure you're using the Internal Database URL, not External
- Check database is active in Render dashboard

**CORS Errors:**
- Update `ALLOWED_ORIGINS` to include your exact Vercel URL
- Include both `http://` and `https://` if testing locally

---

## Monitoring and Logs

### Vercel Logs
- Go to Project → Deployments → Click on deployment → View Function Logs
- Use for debugging frontend issues

### Render Logs
- Go to Service → Logs tab
- Real-time logs for backend requests and errors
- Filter by time range or search keywords

---

## Automatic Deployments

Both Vercel and Render are configured for automatic deployments:

- **Frontend**: Any push to the main branch will trigger a new Vercel deployment
- **Backend**: Any push to the main branch will trigger a new Render deployment

To disable automatic deployments, go to Settings in respective platforms.

---

## Next Steps After Deployment

1. **Set up monitoring**: Consider using Sentry or similar for error tracking
2. **Configure backups**: Render free tier PostgreSQL expires after 90 days
3. **Add analytics**: Google Analytics, Mixpanel, etc.
4. **Set up CI/CD**: Add automated tests before deployment
5. **Custom domain**: Add your own domain for professional appearance

---

## Support Resources

- **Vercel Docs**: https://vercel.com/docs
- **Render Docs**: https://render.com/docs
- **Next.js Docs**: https://nextjs.org/docs
- **FastAPI Docs**: https://fastapi.tiangolo.com

---

## Summary Checklist

- [ ] Vercel account created
- [ ] Frontend deployed to Vercel
- [ ] Frontend URL saved
- [ ] Render.com account created
- [ ] PostgreSQL database created on Render
- [ ] Database credentials saved
- [ ] Backend deployed to Render
- [ ] Backend URL saved
- [ ] Frontend environment variable updated with backend URL
- [ ] Backend CORS configured with frontend URL
- [ ] Database initialized
- [ ] Both frontend and backend tested and working
- [ ] Automatic deployments verified

**Congratulations!** Your Testing SaaS Platform is now live on the internet! 🎉