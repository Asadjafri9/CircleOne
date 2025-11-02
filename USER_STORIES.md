# User Stories & Epics - CircleOne Professional Network

## Project Overview
CircleOne is a professional networking platform where users can create profiles, manage business listings, and connect with others. The platform features secure authentication, a clean dashboard UI, and modern architecture.

---

## EPICS

### Epic 1: User Authentication & Account Management
**Goal**: Provide secure and flexible authentication options for users to access the platform

**Priority**: Critical  
**Status**: ✅ Complete

### Epic 2: User Profile Management
**Goal**: Allow users to create and manage their professional profiles with rich information

**Priority**: Critical  
**Status**: ✅ Complete

### Epic 3: Business Directory
**Goal**: Enable users to create, manage, and discover business listings

**Priority**: Critical  
**Status**: ✅ Complete

### Epic 4: Professional Directory
**Goal**: Allow professionals to showcase their skills and connect with others in the network

**Priority**: Critical  
**Status**: ✅ Complete

### Epic 5: User Dashboard & Analytics
**Goal**: Provide users with a centralized dashboard to view their activity and statistics

**Priority**: High  
**Status**: ✅ Complete

### Epic 6: Search & Discovery
**Goal**: Enable users to find businesses and professionals through search and filtering

**Priority**: High  
**Status**: ✅ Complete

### Epic 7: UI/UX & Theme Customization
**Goal**: Provide a modern, responsive interface with theme customization options

**Priority**: Medium  
**Status**: ✅ Complete

### Epic 8: Image & Media Management
**Goal**: Support image uploads for business logos and profile photos

**Priority**: Medium  
**Status**: ✅ Complete

### Epic 9: User Connections & Networking ⚠️ FUTURE
**Goal**: Enable users to connect with each other, build networks, and manage connections

**Priority**: Critical  
**Status**: ❌ Not Implemented

### Epic 10: Messaging & Communication ⚠️ FUTURE
**Goal**: Allow users to communicate with each other through the platform

**Priority**: High  
**Status**: ❌ Not Implemented

---

## USER STORIES

### Epic 1: User Authentication & Account Management

#### US-1.1: User Registration
**As a** new user  
**I want to** create an account with username, name, email, and password  
**So that** I can access the platform and create my profile

**Acceptance Criteria:**
- ✅ User can register with username, name, email, and password
- ✅ Password must be at least 6 characters
- ✅ Email and username must be unique
- ✅ User is automatically logged in after registration
- ✅ Success message is displayed upon registration

**Technical Notes:**
- Route: `/signup`
- Handles password hashing with Werkzeug
- Supports email validation

---

#### US-1.2: Local Username/Password Login
**As a** registered user  
**I want to** log in with my username/email and password  
**So that** I can access my account

**Acceptance Criteria:**
- ✅ User can log in with username or email
- ✅ Password is validated securely
- ✅ Failed login attempts show error messages
- ✅ Successful login redirects to dashboard
- ✅ User session is maintained

**Technical Notes:**
- Route: `/login`
- Uses Flask-Login for session management
- Supports both username and email login

---

#### US-1.3: Google OAuth Login
**As a** user  
**I want to** log in with my Google account  
**So that** I can access the platform without creating a separate password

**Acceptance Criteria:**
- ✅ User can initiate Google OAuth login
- ✅ Google account information is retrieved
- ✅ New users are automatically created from Google account
- ✅ Existing users are logged in if email matches
- ✅ Profile photo from Google is imported

**Technical Notes:**
- Routes: `/auth/google`, `/auth/google/callback`
- Uses Authlib for OAuth 2.0 integration
- Stores OAuth provider information

---

#### US-1.4: User Logout
**As a** logged-in user  
**I want to** log out of my account  
**So that** I can secure my session when done

**Acceptance Criteria:**
- ✅ Logout button is accessible
- ✅ User session is cleared on logout
- ✅ User is redirected to home page
- ✅ Protected routes require re-authentication after logout

**Technical Notes:**
- Route: `/logout`
- Uses Flask-Login logout_user()

---

#### US-1.5: Protected Routes
**As a** user  
**I want to** have certain pages protected from unauthorized access  
**So that** only authenticated users can access sensitive features

**Acceptance Criteria:**
- ✅ Unauthenticated users are redirected to login
- ✅ Login redirects back to intended page after authentication
- ✅ Dashboard, profile editing, and business management require authentication

**Technical Notes:**
- Uses `@login_required` decorator
- Flask-Login handles redirects

---

### Epic 2: User Profile Management

#### US-2.1: View User Profile
**As a** user  
**I want to** view my profile information  
**So that** I can see my account details

**Acceptance Criteria:**
- ✅ Profile page displays user information
- ✅ Shows email, name, profile photo
- ✅ Displays login provider information
- ✅ Shows theme preference

**Technical Notes:**
- Route: `/profile`
- Requires authentication

---

#### US-2.2: Create Professional Profile
**As a** professional  
**I want to** create a professional profile with job title, summary, skills, and LinkedIn  
**So that** others can discover my expertise

**Acceptance Criteria:**
- ✅ User can create a professional profile
- ✅ Profile includes job title, summary, how I help section
- ✅ Skills can be added as comma-separated list
- ✅ LinkedIn URL can be added
- ✅ Privacy controls for visibility and contact information

**Technical Notes:**
- Route: `/dashboard/profile/edit`
- Stores skills as JSON array
- Consent required for public visibility

---

#### US-2.3: Edit Professional Profile
**As a** professional  
**I want to** edit my professional profile  
**So that** I can keep my information up to date

**Acceptance Criteria:**
- ✅ User can edit all profile fields
- ✅ Changes are saved to database
- ✅ Success message is displayed
- ✅ Profile is updated immediately

**Technical Notes:**
- Same route as creation
- Checks for existing profile

---

#### US-2.4: Delete Professional Profile
**As a** professional  
**I want to** delete my professional profile  
**So that** I can remove my public information if needed

**Acceptance Criteria:**
- ✅ Delete button with confirmation
- ✅ Profile is removed from directory
- ✅ Success message is displayed
- ✅ User can create a new profile later

**Technical Notes:**
- Route: `/dashboard/profile/delete`
- POST method with CSRF protection

---

#### US-2.5: Profile Visibility Control
**As a** professional  
**I want to** control whether my profile is publicly visible  
**So that** I can maintain privacy if needed

**Acceptance Criteria:**
- ✅ Consent checkbox when creating/editing profile
- ✅ Profiles without consent are not shown in directory
- ✅ Owner can always view their own profile
- ✅ Public/private status is clearly displayed

**Technical Notes:**
- `consent_given` boolean field in ProfessionalProfile model
- Filtered in directory queries

---

### Epic 3: Business Directory

#### US-3.1: Create Business Listing
**As a** business owner  
**I want to** create a business listing with details, contact info, and logo  
**So that** potential customers can find my business

**Acceptance Criteria:**
- ✅ User can create business listing from dashboard
- ✅ Required fields: business name, category, description
- ✅ Optional fields: contact email, phone, website, location, hours
- ✅ Logo can be uploaded or URL provided
- ✅ Social media links can be added (Facebook, Twitter, Instagram, LinkedIn)
- ✅ Listing is immediately visible in directory

**Technical Notes:**
- Route: `/dashboard/business/new`
- Image upload via Cloudinary
- Social links stored as JSON

---

#### US-3.2: Edit Business Listing
**As a** business owner  
**I want to** edit my business listing  
**So that** I can update information as needed

**Acceptance Criteria:**
- ✅ Only owner can edit listing
- ✅ All fields can be updated
- ✅ Logo can be replaced
- ✅ Changes are saved immediately
- ✅ Success message is displayed

**Technical Notes:**
- Route: `/dashboard/business/edit/<id>`
- Ownership verification required

---

#### US-3.3: Delete Business Listing
**As a** business owner  
**I want to** delete my business listing  
**So that** I can remove it if no longer relevant

**Acceptance Criteria:**
- ✅ Only owner can delete listing
- ✅ Confirmation dialog before deletion
- ✅ Listing is permanently removed
- ✅ Success message is displayed

**Technical Notes:**
- Route: `/dashboard/business/delete/<id>`
- POST method with CSRF protection

---

#### US-3.4: View Business Details
**As a** visitor  
**I want to** view detailed information about a business  
**So that** I can contact them or learn more

**Acceptance Criteria:**
- ✅ Business detail page shows all information
- ✅ Contact information is displayed
- ✅ Social media links are clickable
- ✅ View counter increments on each visit
- ✅ Owner can see edit/delete options

**Technical Notes:**
- Route: `/business/<id>`
- View counter auto-increments

---

#### US-3.5: Browse Business Directory
**As a** visitor  
**I want to** browse all business listings  
**So that** I can discover businesses in the network

**Acceptance Criteria:**
- ✅ All public business listings are displayed
- ✅ Businesses can be filtered by category
- ✅ Search functionality for business name and description
- ✅ Location-based filtering
- ✅ Results sorted by view count and date

**Technical Notes:**
- Route: `/businesses`
- Supports search, category, and location filters

---

### Epic 4: Professional Directory

#### US-4.1: Browse Professional Directory
**As a** user  
**I want to** browse professional profiles  
**So that** I can find professionals with specific skills

**Acceptance Criteria:**
- ✅ Only profiles with consent are displayed
- ✅ Search by name, job title, or summary
- ✅ Filter by skills
- ✅ Results sorted by view count and date
- ✅ Profile cards show key information

**Technical Notes:**
- Route: `/professionals`
- Filters by `consent_given=True`
- Skill search in JSON array

---

#### US-4.2: View Professional Profile Details
**As a** user  
**I want to** view detailed professional profile information  
**So that** I can learn about their expertise and contact them

**Acceptance Criteria:**
- ✅ Full profile information displayed
- ✅ Skills list shown as tags
- ✅ Contact information shown based on privacy settings
- ✅ View counter increments
- ✅ Owner can see edit options

**Technical Notes:**
- Route: `/profile/<id>`
- Privacy controls for email visibility

---

### Epic 5: User Dashboard & Analytics

#### US-5.1: View Dashboard
**As a** logged-in user  
**I want to** access a dashboard with my account overview  
**So that** I can see my activity and statistics

**Acceptance Criteria:**
- ✅ Dashboard displays welcome message with user name
- ✅ Shows statistics: business count, total views, profile views
- ✅ Displays account information
- ✅ Lists all user's business listings
- ✅ Shows professional profile status
- ✅ Quick action buttons for common tasks

**Technical Notes:**
- Route: `/dashboard`
- Requires authentication
- Aggregates data from user's businesses and profile

---

#### US-5.2: View Business Statistics
**As a** business owner  
**I want to** see view statistics for my business listings  
**So that** I can track engagement

**Acceptance Criteria:**
- ✅ Total views shown for each business
- ✅ Aggregate view count on dashboard
- ✅ View counts update automatically

**Technical Notes:**
- View count tracked in BusinessListing model
- Incremented on detail page view

---

#### US-5.3: View Profile Statistics
**As a** professional  
**I want to** see view statistics for my professional profile  
**So that** I can track visibility

**Acceptance Criteria:**
- ✅ Profile view count displayed on dashboard
- ✅ View count updates when profile is viewed
- ✅ Owner views don't count

**Technical Notes:**
- View count tracked in ProfessionalProfile model
- Logic to exclude owner views

---

### Epic 6: Search & Discovery

#### US-6.1: Search Businesses
**As a** visitor  
**I want to** search for businesses by name or description  
**So that** I can find relevant businesses quickly

**Acceptance Criteria:**
- ✅ Search box on business directory page
- ✅ Case-insensitive search
- ✅ Searches business name and description
- ✅ Results update dynamically
- ✅ Search term is preserved in URL

**Technical Notes:**
- Uses SQLAlchemy `ilike` for case-insensitive search
- Query parameters in URL

---

#### US-6.2: Filter Businesses by Category
**As a** visitor  
**I want to** filter businesses by category  
**So that** I can find businesses in specific industries

**Acceptance Criteria:**
- ✅ Category filter dropdown
- ✅ Shows all available categories
- ✅ Filters results immediately
- ✅ Can combine with search

**Technical Notes:**
- Categories extracted from existing businesses
- Filter applied via query parameter

---

#### US-6.3: Filter Businesses by Location
**As a** visitor  
**I want to** filter businesses by location  
**So that** I can find local businesses

**Acceptance Criteria:**
- ✅ Location search input
- ✅ Searches location field
- ✅ Works with other filters

**Technical Notes:**
- Location filter uses partial matching

---

#### US-6.4: Search Professionals
**As a** user  
**I want to** search for professionals by name, title, or skills  
**So that** I can find relevant professionals

**Acceptance Criteria:**
- ✅ Search functionality on professionals page
- ✅ Searches name, job title, and summary
- ✅ Results filtered to public profiles only

**Technical Notes:**
- Joins User table for name search

---

#### US-6.5: Filter Professionals by Skills
**As a** user  
**I want to** filter professionals by skills  
**So that** I can find experts in specific areas

**Acceptance Criteria:**
- ✅ Skill filter dropdown
- ✅ Shows all available skills
- ✅ Filters results immediately

**Technical Notes:**
- Extracts unique skills from all profiles
- Searches in JSON skills array

---

### Epic 7: UI/UX & Theme Customization

#### US-7.1: Dark/Light Theme Toggle
**As a** user  
**I want to** toggle between dark and light themes  
**So that** I can use the interface comfortably in different lighting

**Acceptance Criteria:**
- ✅ Theme toggle button in navigation
- ✅ Toggles between light and dark modes
- ✅ Theme preference saved for authenticated users
- ✅ Theme persists across sessions
- ✅ Smooth transition between themes

**Technical Notes:**
- Uses CSS custom properties
- API endpoint: `/api/update-theme`
- Saves to user's database record

---

#### US-7.2: Responsive Design
**As a** user  
**I want to** access the platform on any device  
**So that** I can use it on desktop, tablet, or mobile

**Acceptance Criteria:**
- ✅ Interface adapts to screen size
- ✅ Navigation is mobile-friendly
- ✅ Forms are usable on small screens
- ✅ Cards and grids resize appropriately

**Technical Notes:**
- CSS media queries
- Flexbox and Grid layouts

---

#### US-7.3: Modern UI with Animations
**As a** user  
**I want to** experience a modern, animated interface  
**So that** the platform feels polished and professional

**Acceptance Criteria:**
- ✅ Smooth transitions and animations
- ✅ Hover effects on interactive elements
- ✅ Loading states for actions
- ✅ Visual feedback on interactions

**Technical Notes:**
- JavaScript animations in `static/js/main.js`
- CSS transitions and transforms

---

### Epic 8: Image & Media Management

#### US-8.1: Upload Business Logo
**As a** business owner  
**I want to** upload a logo image for my business  
**So that** my business is easily recognizable

**Acceptance Criteria:**
- ✅ File upload input for logo
- ✅ Supports common image formats (PNG, JPG, JPEG, GIF, WEBP)
- ✅ Image uploaded to Cloudinary
- ✅ Logo URL stored in database
- ✅ Image validation before upload

**Technical Notes:**
- Uses Cloudinary SDK
- File validation in `utils.py`
- Max file size: 5MB

---

#### US-8.2: Use Logo URL
**As a** business owner  
**I want to** provide a logo URL instead of uploading  
**So that** I can use existing hosted images

**Acceptance Criteria:**
- ✅ Option to provide logo URL
- ✅ URL validated
- ✅ Logo displays correctly

**Technical Notes:**
- Alternative to file upload
- Both options available in form

---

#### US-8.3: Profile Photo from OAuth
**As a** user  
**I want to** use my Google profile photo automatically  
**So that** I don't need to upload one separately

**Acceptance Criteria:**
- ✅ Google profile photo imported on OAuth login
- ✅ Photo URL stored in user record
- ✅ Photo displays in profile and dashboard

**Technical Notes:**
- OAuth provider supplies profile picture URL
- Stored in User model

---

### Epic 9: User Connections & Networking ⚠️ FUTURE

#### US-9.1: Send Connection Request
**As a** user  
**I want to** send connection requests to other users  
**So that** I can build my professional network

**Status**: ❌ Not Implemented  
**Priority**: Critical

---

#### US-9.2: Accept/Reject Connection Requests
**As a** user  
**I want to** accept or reject connection requests  
**So that** I can control who is in my network

**Status**: ❌ Not Implemented  
**Priority**: Critical

---

#### US-9.3: View My Connections
**As a** user  
**I want to** see a list of my connections  
**So that** I can manage my network

**Status**: ❌ Not Implemented  
**Priority**: High

---

#### US-9.4: View Mutual Connections
**As a** user  
**I want to** see mutual connections with other users  
**So that** I can discover common connections

**Status**: ❌ Not Implemented  
**Priority**: Medium

---

### Epic 10: Messaging & Communication ⚠️ FUTURE

#### US-10.1: Send Messages to Connections
**As a** user  
**I want to** send messages to my connections  
**So that** I can communicate within the platform

**Status**: ❌ Not Implemented  
**Priority**: High

---

#### US-10.2: View Message Inbox
**As a** user  
**I want to** view and manage my messages  
**So that** I can keep track of conversations

**Status**: ❌ Not Implemented  
**Priority**: High

---

## Story Points Summary

### Completed Features
- **Epic 1**: User Authentication - 21 points
- **Epic 2**: User Profile Management - 13 points
- **Epic 3**: Business Directory - 21 points
- **Epic 4**: Professional Directory - 13 points
- **Epic 5**: User Dashboard - 8 points
- **Epic 6**: Search & Discovery - 13 points
- **Epic 7**: UI/UX & Theme - 8 points
- **Epic 8**: Image & Media - 8 points

**Total Completed**: 105 story points

### Future Features
- **Epic 9**: User Connections - Estimated 34 points
- **Epic 10**: Messaging - Estimated 21 points

**Total Future**: 55 story points

---

## Priority Matrix

| Priority | Epic | Status |
|----------|------|--------|
| Critical | Authentication | ✅ Complete |
| Critical | Profile Management | ✅ Complete |
| Critical | Business Directory | ✅ Complete |
| Critical | Professional Directory | ✅ Complete |
| Critical | **User Connections** | ❌ **Not Implemented** |
| High | Dashboard & Analytics | ✅ Complete |
| High | Search & Discovery | ✅ Complete |
| High | **Messaging** | ❌ **Not Implemented** |
| Medium | UI/UX Customization | ✅ Complete |
| Medium | Image Management | ✅ Complete |

---

## Technical Debt & Improvements

1. **Missing Core Feature**: User connections/networking functionality
2. **Missing Feature**: In-app messaging system
3. **Enhancement**: Add email notifications for connection requests
4. **Enhancement**: Add activity feed for user actions
5. **Enhancement**: Add recommendations based on connections
6. **Enhancement**: Add profile completion percentage indicator
7. **Enhancement**: Add analytics dashboard with graphs
8. **Enhancement**: Add export functionality for business listings

---

*Last Updated: 2024*

